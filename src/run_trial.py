from __future__ import annotations

from functools import partial

from psyflow import StimUnit, set_trial_context, next_trial_id


def _delay_label(days: int) -> str:
    return "ä»Šå¤©åˆ°è´¦" if int(days) <= 0 else f"{int(days)}å¤©åŽåˆ°è´¦"


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one delay-discounting choice trial (smaller-sooner vs larger-later)."""
    keys = list(getattr(settings, "key_list", ["f", "j"]))
    if len(keys) < 2:
        raise ValueError("Delay Discounting task requires at least two response keys.")

    left_key, right_key = str(keys[0]), str(keys[1])

    spec = controller.next_trial(block_idx=int(block_idx or 0), expected_condition=str(condition))
    trial_id = next_trial_id()
    magnitude = str(spec["magnitude"])

    ll_side = str(spec["ll_side"])
    ss_side = str(spec["ss_side"])
    ll_key = left_key if ll_side == "left" else right_key
    ss_key = right_key if ll_side == "left" else left_key

    left_text = f"{float(spec['left_amount']):.0f}å…ƒï¼Œ{_delay_label(int(spec['left_delay_days']))}"
    right_text = f"{float(spec['right_amount']):.0f}å…ƒï¼Œ{_delay_label(int(spec['right_delay_days']))}"

    trial_data = {
        "condition": magnitude,
        "offer_id": int(spec["item_id"]),
        "magnitude": magnitude,
        "ss_amount": float(spec["ss_amount"]),
        "ll_amount": float(spec["ll_amount"]),
        "delay_days": int(spec["delay_days"]),
        "k_ref": float(spec["k_ref"]),
        "ll_side": ll_side,
        "ss_side": ss_side,
        "left_option_text": left_text,
        "right_option_text": right_text,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # Keep pre-choice stage neutral: fixation only, no condition text shown.
    cue = make_unit(unit_label="cue").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="pre_choice_fixation",
        deadline_s=float(settings.cue_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=magnitude,
        task_factors={
            "magnitude": magnitude,
            "offer_id": int(spec["item_id"]),
            "stage": "pre_choice_fixation",
            "block_idx": block_idx,
        },
        stim_id="fixation",
    )
    cue.show(
        duration=settings.cue_duration,
        onset_trigger=settings.triggers.get("cue_onset"),
    ).to_dict(trial_data)

    anticipation_duration = float(getattr(settings, "anticipation_duration", 0.2))
    anticipation = make_unit(unit_label="anticipation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        anticipation,
        trial_id=trial_id,
        phase="offer_onset_jitter",
        deadline_s=anticipation_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=magnitude,
        task_factors={
            "magnitude": magnitude,
            "offer_id": int(spec["item_id"]),
            "stage": "offer_onset_jitter",
            "block_idx": block_idx,
        },
        stim_id="fixation",
    )
    anticipation.show(
        duration=anticipation_duration,
        onset_trigger=settings.triggers.get("anticipation_onset"),
    ).to_dict(trial_data)

    choice = (
        make_unit(unit_label="choice")
        .add_stim(stim_bank.rebuild("option_left", text=left_text))
        .add_stim(stim_bank.rebuild("option_right", text=right_text))
        .add_stim(stim_bank.get("choice_prompt"))
    )

    set_trial_context(
        choice,
        trial_id=trial_id,
        phase="intertemporal_choice",
        deadline_s=float(settings.decision_duration),
        valid_keys=keys,
        block_id=block_id,
        condition_id=magnitude,
        task_factors={
            "magnitude": magnitude,
            "offer_id": int(spec["item_id"]),
            "ss_amount": float(spec["ss_amount"]),
            "ll_amount": float(spec["ll_amount"]),
            "delay_days": int(spec["delay_days"]),
            "k_ref": float(spec["k_ref"]),
            "ll_side": ll_side,
            "ss_side": ss_side,
            "ss_key": ss_key,
            "ll_key": ll_key,
            "left_key": left_key,
            "right_key": right_key,
            "block_idx": block_idx,
            "stage": "intertemporal_choice",
        },
        stim_id=f"mcq27_item_{int(spec['item_id'])}",
    )

    choice.capture_response(
        keys=keys,
        correct_keys=keys,
        duration=settings.decision_duration,
        onset_trigger=settings.triggers.get("choice_onset"),
        response_trigger={
            left_key: settings.triggers.get("choice_response_left"),
            right_key: settings.triggers.get("choice_response_right"),
        },
        timeout_trigger=settings.triggers.get("choice_no_response"),
    )

    response = choice.get_state("response", None)
    rt = choice.get_state("rt", None)
    choice_made = response in keys

    chosen_side = None
    chosen_option = None
    chosen_amount = None
    chosen_delay_days = None
    chose_ll = False

    if choice_made:
        chosen_side = "left" if response == left_key else "right"
        chose_ll = chosen_side == ll_side
        chosen_option = "ll" if chose_ll else "ss"
        if chose_ll:
            chosen_amount = float(spec["ll_amount"])
            chosen_delay_days = int(spec["delay_days"])
        else:
            chosen_amount = float(spec["ss_amount"])
            chosen_delay_days = 0

    trial_data.update(
        choice_made=bool(choice_made),
        choice_key=response,
        choice_rt=rt,
        chosen_side=chosen_side,
        chosen_option=chosen_option,
        chose_ll=bool(chose_ll),
        chosen_amount=chosen_amount,
        chosen_delay_days=chosen_delay_days,
        ss_key=ss_key,
        ll_key=ll_key,
    )

    choice.set_state(
        choice_made=bool(choice_made),
        choice_key=response,
        choice_rt=rt,
        chosen_side=chosen_side,
        chosen_option=chosen_option,
        chose_ll=bool(chose_ll),
        chosen_amount=chosen_amount,
        chosen_delay_days=chosen_delay_days,
        ss_key=ss_key,
        ll_key=ll_key,
    ).to_dict(trial_data)

    if choice_made:
        confirm_duration = float(getattr(settings, "choice_confirm_duration", 0.25))
        highlight = stim_bank.get("highlight_left") if response == left_key else stim_bank.get("highlight_right")
        confirm = (
            make_unit(unit_label="choice_confirm")
            .add_stim(stim_bank.rebuild("option_left", text=left_text))
            .add_stim(stim_bank.rebuild("option_right", text=right_text))
            .add_stim(highlight)
        )
        set_trial_context(
            confirm,
            trial_id=trial_id,
            phase="choice_confirmation",
            deadline_s=confirm_duration,
            valid_keys=[],
            block_id=block_id,
            condition_id=magnitude,
            task_factors={
                "magnitude": magnitude,
                "choice_made": True,
                "chosen_side": chosen_side,
                "stage": "choice_confirmation",
                "block_idx": block_idx,
            },
            stim_id=f"highlight_{chosen_side}",
        )
        confirm.show(
            duration=confirm_duration,
            onset_trigger=settings.triggers.get("choice_confirm_onset"),
        ).to_dict(trial_data)

    if choice_made:
        fb_stim = stim_bank.get("feedback_choice")
        fb_trigger = settings.triggers.get("feedback_choice_onset")
    else:
        fb_stim = stim_bank.get("feedback_timeout")
        fb_trigger = settings.triggers.get("feedback_timeout_onset")

    feedback = make_unit(unit_label="feedback").add_stim(fb_stim)
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="outcome_feedback",
        deadline_s=float(settings.feedback_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=magnitude,
        task_factors={
            "magnitude": magnitude,
            "choice_made": bool(choice_made),
            "chosen_option": chosen_option,
            "chose_ll": bool(chose_ll),
            "stage": "outcome_feedback",
            "block_idx": block_idx,
        },
        stim_id="feedback_choice" if choice_made else "feedback_timeout",
    )
    feedback.show(duration=settings.feedback_duration, onset_trigger=fb_trigger).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=float(settings.iti_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=magnitude,
        task_factors={"magnitude": magnitude, "stage": "inter_trial_interval", "block_idx": block_idx},
        stim_id="fixation",
    )
    iti.show(duration=settings.iti_duration, onset_trigger=settings.triggers.get("iti_onset")).to_dict(trial_data)

    return trial_data

