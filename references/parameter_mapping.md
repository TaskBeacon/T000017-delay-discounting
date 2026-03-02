# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task_name | `task.task_name` | `delay_discounting` | W2032105672 | Delay-discounting intertemporal-choice task framing | exact | Runtime task identifier |
| magnitude_conditions | `task.conditions` | `[small, medium, large]` | W2509303870 | MCQ item-bank grouped by magnitude tiers | exact | Used for block/condition scheduling |
| trial_count_human | `task.total_trials` | `27` (human) | W2509303870 | Standard MCQ-27 item count | exact | Full protocol run |
| trial_count_smoke | `task.total_trials` | `9` (qa/sim) | W2509303870 | Reduced subset for operational smoke runs | inferred | Maintains phase completeness for gates |
| response_keys | `task.key_list` | `['f','j']` | W2032105672 | Binary intertemporal choice requires two-option response | inferred | Key labels are implementation-specific |
| item_pool | `controller.item_pool` | `MCQ27_ITEMS` table | W2509303870 | 27 SS/LL options with implied discounting structure | exact | Implemented in `src/utils.py` |
| randomize_order | `controller.randomize_order` | `true` | W2509303870 | Typical MCQ administration randomizes order | exact | Per-run shuffle |
| side_counterbalance | `controller.counterbalance_sides` | `true` | W2032105672 | Counterbalancing controls response-side bias | inferred | Left/right option swapping |
| cue_duration | `timing.cue_duration` | `0.6` human / `0.4` qa/sim | W2032105672 | Pre-choice cue phase is implementation-level timing | inferred | Keeps fast smoke runtime |
| decision_window | `timing.decision_duration` | `6.0` human / `1.5-2.0` qa/sim | W2032105672 | Intertemporal choice response window | inferred | Shortened in smoke profiles |
| feedback_duration | `timing.feedback_duration` | `0.5` human / `0.3` qa/sim | W2032105672 | Post-choice response acknowledgement stage | inferred | No objective correctness feedback |
| iti_duration | `timing.iti_duration` | `0.5` human / `0.2` qa/sim | W2032105672 | Inter-trial interval for trial segmentation | inferred | Operational timing parameter |
| scripted_responder | `sim.responder.type` | `scripted` | W2032105672 | Simulation responder is runtime infrastructure | inferred | For deterministic scripted test |
| sampler_responder | `sim.responder.type` | `responders.task_sampler:TaskSamplerResponder` | W2032105672 | Sampler responder emulates probabilistic choice behavior | inferred | For stochastic simulation |
| sampler_discount_rate | `sim.responder.kwargs.discount_k` | `0.015` | W2509303870 | Discount-rate based choice tendency parameterization | inferred | Adjustable synthetic-participant parameter |
