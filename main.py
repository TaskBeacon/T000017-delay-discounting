from contextlib import nullcontext
from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    count_down,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import build_block_conditions, run_trial


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def run(options: TaskRunOptions) -> None:
    """Run Delay Discounting task in human/qa/sim mode with one auditable flow."""
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path), extra_keys=["condition_generation"])

    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        if options.mode == "human":
            subject_data = SubInfo(cfg["subform_config"]).collect()
        elif options.mode == "qa":
            subject_data = {"subject_id": "qa"}
        else:
            participant_id = "sim"
            if runtime_ctx is not None and runtime_ctx.session is not None:
                participant_id = str(runtime_ctx.session.participant_id or "sim")
            subject_data = {"subject_id": participant_id}

        settings = TaskSettings.from_dict(cfg["task_config"])
        if options.mode in ("qa", "sim") and output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)

        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.triggers = cfg["trigger_config"]
        trigger_runtime = initialize_triggers(mock=True) if options.mode in ("qa", "sim") else initialize_triggers(cfg)

        win, kb = initialize_exp(settings)

        if bool(getattr(settings, "voice_enabled", False)) and options.mode not in ("qa", "sim"):
            stim_bank = (
                StimBank(win, cfg["stim_config"])
                .convert_to_voice("instruction_text", voice=settings.voice_name)
                .preload_all()
            )
        else:
            stim_bank = StimBank(win, cfg["stim_config"]).preload_all()

        condition_generation_cfg = dict(cfg.get("condition_generation_config", {}))

        settings.save_to_json()
        trigger_runtime.send(settings.triggers.get("exp_onset"))

        instruction = StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get("instruction_text")
        )
        if bool(getattr(settings, "voice_enabled", False)) and options.mode not in ("qa", "sim"):
            instruction.add_stim(stim_bank.get("instruction_text_voice"))
        instruction.wait_and_continue()

        all_data: list[dict] = []
        for block_i in range(int(settings.total_blocks)):
            block_id = f"block_{block_i}"

            if options.mode not in ("qa", "sim"):
                count_down(win, 3, color="white")

            block = (
                BlockUnit(
                    block_id=block_id,
                    block_idx=block_i,
                    settings=settings,
                    window=win,
                    keyboard=kb,
                )
                .generate_conditions(
                    func=build_block_conditions,
                    n_trials=int(settings.trials_per_block),
                    condition_labels=list(getattr(settings, "conditions", [])),
                    **condition_generation_cfg,
                )
                .on_start(lambda _b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda _b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(
                        run_trial,
                        stim_bank=stim_bank,
                        trigger_runtime=trigger_runtime,
                        condition_generation_config=condition_generation_cfg,
                        block_id=block_id,
                        block_idx=block_i,
                    )
                )
                .to_dict(all_data)
            )

            block_trials = block.get_all_data()
            # Normalize condition column to readable magnitude labels if BlockUnit wrote planned labels differently.
            for trial in block_trials:
                if trial.get("magnitude") is not None:
                    trial["condition"] = str(trial["magnitude"])

            responded = [t for t in block_trials if bool(t.get("choice_made", False))]
            response_rate = len(responded) / max(1, len(block_trials))
            ll_rate = sum(1 for t in responded if bool(t.get("chose_ll", False))) / max(1, len(responded))
            rt_values = [float(t["choice_rt"]) for t in responded if t.get("choice_rt") is not None]
            mean_rt = (sum(rt_values) / len(rt_values)) if rt_values else None

            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=settings.total_blocks,
                    response_rate=response_rate,
                    ll_rate=ll_rate,
                    mean_rt=(f"{mean_rt:.3f} s" if mean_rt is not None else "NA"),
                )
            ).wait_and_continue()

        valid_trials = [t for t in all_data if bool(t.get("choice_made", False))]
        overall_ll_rate = sum(1 for t in valid_trials if bool(t.get("chose_ll", False))) / max(1, len(valid_trials))

        StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get_and_format(
                "good_bye",
                total_trials=len(all_data),
                valid_trials=len(valid_trials),
                ll_rate=overall_ll_rate,
            )
        ).wait_and_continue(terminate=True)

        trigger_runtime.send(settings.triggers.get("exp_end"))
        pd.DataFrame(all_data).to_csv(settings.res_file, index=False)

        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run Delay Discounting task in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
