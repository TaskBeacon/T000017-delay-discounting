# Task Plot Audit

- generated_at: 2026-03-25T20:58:17
- mode: existing
- task_path: E:\xhmhc\TaskBeacon\T000017-delay-discounting

## 1. Inputs and provenance

- E:\xhmhc\TaskBeacon\T000017-delay-discounting\README.md
- E:\xhmhc\TaskBeacon\T000017-delay-discounting\config\config.yaml
- E:\xhmhc\TaskBeacon\T000017-delay-discounting\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |------|-------------|
- | 1. Resolve planned offer | `run_trial.py` derives block-trial index, reconstructs the deterministic block plan, and fetches the matching MCQ item spec (magnitude, amounts, delay, side assignment, item ID). |
- | 2. Cue phase | Show neutral fixation for `cue_duration=0.6 s` and emit `cue_onset`. Condition labels are intentionally not shown before choice. |
- | 3. Anticipation phase | Show fixation for `anticipation_duration=0.2 s` and emit `anticipation_onset`. |
- | 4. Choice phase | Draw left/right option text and choice prompt; collect `f/j` response within `decision_duration=6.0 s`; emit `choice_onset`, response trigger (`31/32`), or timeout trigger (`39`). |
- | 5. Choice state derivation | Compute chosen side, chosen option (`ss`/`ll`), chosen amount, chosen delay, and LL indicator (`chose_ll`). |
- | 6. Choice confirm phase (if responded) | Present both options plus a highlight rectangle on selected side for `choice_confirm_duration=0.3 s`; emit `choice_confirm_onset`. |
- | 7. Feedback phase | If responded, show `feedback_choice` (`feedback_choice_onset=40`); if timeout, show `feedback_timeout` (`feedback_timeout_onset=41`) for `feedback_duration=0.5 s`. |
- | 8. ITI phase | Show fixation for `iti_duration=0.5 s` and emit `iti_onset`. |

## 3. Evidence extracted from config/source

- small: phase=pre choice fixation, deadline_expr=float(settings.cue_duration), response_expr=n/a, stim_expr='fixation'
- small: phase=offer onset jitter, deadline_expr=anticipation_duration, response_expr=n/a, stim_expr='fixation'
- small: phase=intertemporal choice, deadline_expr=float(settings.decision_duration), response_expr=float(settings.decision_duration), stim_expr=f"mcq27_item_{int(spec['item_id'])}"
- small: phase=choice confirmation, deadline_expr=confirm_duration, response_expr=n/a, stim_expr=f'highlight_{chosen_side}'
- small: phase=outcome feedback, deadline_expr=float(settings.feedback_duration), response_expr=n/a, stim_expr='feedback_choice' if choice_made else 'feedback_timeout'
- small: phase=inter trial interval, deadline_expr=float(settings.iti_duration), response_expr=n/a, stim_expr='fixation'
- medium: phase=pre choice fixation, deadline_expr=float(settings.cue_duration), response_expr=n/a, stim_expr='fixation'
- medium: phase=offer onset jitter, deadline_expr=anticipation_duration, response_expr=n/a, stim_expr='fixation'
- medium: phase=intertemporal choice, deadline_expr=float(settings.decision_duration), response_expr=float(settings.decision_duration), stim_expr=f"mcq27_item_{int(spec['item_id'])}"
- medium: phase=choice confirmation, deadline_expr=confirm_duration, response_expr=n/a, stim_expr=f'highlight_{chosen_side}'
- medium: phase=outcome feedback, deadline_expr=float(settings.feedback_duration), response_expr=n/a, stim_expr='feedback_choice' if choice_made else 'feedback_timeout'
- medium: phase=inter trial interval, deadline_expr=float(settings.iti_duration), response_expr=n/a, stim_expr='fixation'
- large: phase=pre choice fixation, deadline_expr=float(settings.cue_duration), response_expr=n/a, stim_expr='fixation'
- large: phase=offer onset jitter, deadline_expr=anticipation_duration, response_expr=n/a, stim_expr='fixation'
- large: phase=intertemporal choice, deadline_expr=float(settings.decision_duration), response_expr=float(settings.decision_duration), stim_expr=f"mcq27_item_{int(spec['item_id'])}"
- large: phase=choice confirmation, deadline_expr=confirm_duration, response_expr=n/a, stim_expr=f'highlight_{chosen_side}'
- large: phase=outcome feedback, deadline_expr=float(settings.feedback_duration), response_expr=n/a, stim_expr='feedback_choice' if choice_made else 'feedback_timeout'
- large: phase=inter trial interval, deadline_expr=float(settings.iti_duration), response_expr=n/a, stim_expr='fixation'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.029, right=0.032, blank=0.115
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0291, 'right_ratio': 0.032, 'blank_ratio': 0.1149}
- validator_warnings:
  - timelines[0].phases[0] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[2] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[4] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[5] missing duration_ms; renderer will annotate as n/a.

## 7. Output files and checksums

- E:\xhmhc\TaskBeacon\T000017-delay-discounting\references\task_plot_spec.yaml: sha256=ecabddddfec4c756ffa0f0538781683b5677fbb83381dc0d111ba6e5844b6ec4
- E:\xhmhc\TaskBeacon\T000017-delay-discounting\references\task_plot_spec.json: sha256=7732ed4332821b12dd686efdc95f7cedaed26cfb85a0fd889a4a7922faccedc6
- E:\xhmhc\TaskBeacon\T000017-delay-discounting\references\task_plot_source_excerpt.md: sha256=b58833c5b0e67b0c025d48d7d47a9193d33cce911defe7a29ebc41468fa1f1e1
- E:\xhmhc\TaskBeacon\T000017-delay-discounting\task_flow.png: sha256=0a57611c2114ff707c5592b6b5f8c68be7279e177e78d980b71ee7c184236569

## 8. Inferred/uncertain items

- small:pre choice fixation:unable to resolve duration from 'float(settings.cue_duration)'
- small:offer onset jitter:heuristic numeric parse from 'float(getattr(settings, 'anticipation_duration', 0.2))'
- small:intertemporal choice:unable to resolve duration from 'float(settings.decision_duration)'
- small:choice confirmation:heuristic numeric parse from 'float(getattr(settings, 'choice_confirm_duration', 0.25))'
- small:outcome feedback:unable to resolve duration from 'float(settings.feedback_duration)'
- small:inter trial interval:unable to resolve duration from 'float(settings.iti_duration)'
- medium:pre choice fixation:unable to resolve duration from 'float(settings.cue_duration)'
- medium:offer onset jitter:heuristic numeric parse from 'float(getattr(settings, 'anticipation_duration', 0.2))'
- medium:intertemporal choice:unable to resolve duration from 'float(settings.decision_duration)'
- medium:choice confirmation:heuristic numeric parse from 'float(getattr(settings, 'choice_confirm_duration', 0.25))'
- medium:outcome feedback:unable to resolve duration from 'float(settings.feedback_duration)'
- medium:inter trial interval:unable to resolve duration from 'float(settings.iti_duration)'
- large:pre choice fixation:unable to resolve duration from 'float(settings.cue_duration)'
- large:offer onset jitter:heuristic numeric parse from 'float(getattr(settings, 'anticipation_duration', 0.2))'
- large:intertemporal choice:unable to resolve duration from 'float(settings.decision_duration)'
- large:choice confirmation:heuristic numeric parse from 'float(getattr(settings, 'choice_confirm_duration', 0.25))'
- large:outcome feedback:unable to resolve duration from 'float(settings.feedback_duration)'
- large:inter trial interval:unable to resolve duration from 'float(settings.iti_duration)'
- collapsed equivalent condition logic into representative timeline: small, medium, large
- unparsed if-tests defaulted to condition-agnostic applicability: block_idx is None; choice_made; chose_ll; len(keys) < 2
