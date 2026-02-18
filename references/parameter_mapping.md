# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.task_name` | `delay_discounting` | `W2032105672` | `exact` | Delay discounting intertemporal-choice paradigm label. |
| `task.conditions` | `[small, medium, large]` | `W2509303870` | `exact` | MCQ-27 is organized by small/medium/large magnitude sets. |
| `task.total_trials` | `27` (human), `9` (qa/sim) | `W2509303870` | `exact` / `inferred` | Human run uses full MCQ-27; QA/sim use a short mechanism-complete subset. |
| `task.key_list` | `["f", "j"]` | `W2032105672` | `inferred` | Two-key forced choice is required; concrete key labels are implementation-specific. |
| `controller.item_pool` | MCQ-27 amount/delay table | `W2509303870` | `exact` | Uses the 27 standard SS/LL choice items and implied k values. |
| `controller.randomize_order` | `true` | `W2509303870` | `exact` | MCQ items are typically presented in randomized order. |
| `controller.counterbalance_sides` | `true` | `W2032105672` | `inferred` | Side balancing reduces left/right motor bias during binary choice tasks. |
| `timing.cue_duration` | `0.6 s` (human), `0.4 s` (qa/sim) | `W2032105672` | `inferred` | Cue timing is an implementation parameter; decision stage remains primary. |
| `timing.decision_duration` | `6.0 s` (human), `1.5-2.0 s` (qa/sim) | `W2032105672` | `inferred` | Human run keeps realistic choice window; QA/sim are shortened for quick gating. |
| `timing.feedback_duration` | `0.5 s` (human), `0.3 s` (qa/sim) | `W2032105672` | `inferred` | Feedback timing is operational and does not alter core choice variables. |
| `timing.iti_duration` | `0.5 s` (human), `0.2 s` (qa/sim) | `W2032105672` | `inferred` | ITI is implementation-level for clear trial boundaries. |
| `sim.responder.type` | `scripted` / `responders.task_sampler:TaskSamplerResponder` | `W2032105672` | `inferred` | Simulation responder type is a PsyFlow runtime extension, not in source protocol. |
| `sampler.discount_k` | `0.015` (default) | `W2509303870` | `inferred` | Example simulated participant discount rate; user-adjustable at runtime. |
