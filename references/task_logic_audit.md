# Task Logic Audit: Delay Discounting Task (MCQ-27 style)

## 1. Paradigm Intent

- Task: Delay Discounting (intertemporal choice; MCQ-27 style)
- Primary construct: preference for smaller-sooner (SS) vs larger-later (LL) rewards
- Manipulated factors: offer magnitude tier (`small`, `medium`, `large`) and item-specific amount/delay combinations
- Dependent measures: choice key, choice side, LL choice indicator, RT, response rate
- Key references: Kirby-style MCQ item set and downstream implementations summarized in project references

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: configurable (`task.total_blocks`; default 1)
- Trials per block: configurable (`task.trial_per_block`; default 27)
- Randomization/counterbalancing:
  - block item order can be randomized (`condition_generation.randomize_order`)
  - LL side can be balanced (`condition_generation.counterbalance_sides`) or sampled probabilistically (`condition_generation.ll_left_prob`)
- Condition generation method:
  - `BlockUnit.generate_conditions(func=build_block_conditions, ...)`
  - custom generation is required because simple condition labels alone cannot encode MCQ item identity + left/right side assignment
  - generated block conditions remain readable magnitude labels (`small|medium|large`) for logging/auditability
- Runtime-generated trial values (deterministic):
  - `run_trial.py` reconstructs the exact planned item spec for the current block/trial position using block seed + block trial index
  - reproducibility fields logged in trial data include `plan_seed`, `block_trial_index`, `condition_id`, and item parameters

### Trial State Machine

1. `pre_choice_fixation`
   - Onset trigger: `cue_onset`
   - Stimuli shown: fixation (`+`)
   - Valid keys: none
   - Timeout behavior: auto-advance after `cue_duration`
   - Next state: `offer_onset_jitter`

2. `offer_onset_jitter`
   - Onset trigger: `anticipation_onset`
   - Stimuli shown: fixation (`+`)
   - Valid keys: none
   - Timeout behavior: auto-advance after `anticipation_duration`
   - Next state: `intertemporal_choice`

3. `intertemporal_choice`
   - Onset trigger: `choice_onset`
   - Stimuli shown: left option text, right option text, neutral prompt
   - Valid keys: `task.key_list` (default `f`, `j`)
   - Timeout behavior: emit `choice_no_response`, continue to feedback
   - Next state: `choice_confirmation` (if responded) else `outcome_feedback`

4. `choice_confirmation` (conditional)
   - Onset trigger: `choice_confirm_onset`
   - Stimuli shown: option texts + selected-side highlight rectangle
   - Valid keys: none
   - Timeout behavior: auto-advance after `choice_confirm_duration`
   - Next state: `outcome_feedback`

5. `outcome_feedback`
   - Onset trigger: `feedback_choice_onset` or `feedback_timeout_onset`
   - Stimuli shown: choice-recorded feedback or timeout feedback
   - Valid keys: none
   - Timeout behavior: auto-advance after `feedback_duration`
   - Next state: `inter_trial_interval`

6. `inter_trial_interval`
   - Onset trigger: `iti_onset`
   - Stimuli shown: fixation (`+`)
   - Valid keys: none
   - Timeout behavior: auto-advance after `iti_duration`
   - Next state: next trial / block end

## 3. Condition Semantics

For each condition token in `task.conditions`:

- `small`
  - Participant-facing meaning: magnitude tier for MCQ items (not explicitly shown during trials in current implementation)
  - Concrete stimulus realization: one MCQ item with SS/LL amounts/delay rendered as left/right option texts
  - Outcome rules: no correctness; participant preference choice is recorded

- `medium`
  - Participant-facing meaning: same as above (medium magnitude tier)
  - Concrete stimulus realization: item-specific amount/delay text pair from configured/default item pool
  - Outcome rules: no correctness; participant preference choice is recorded

- `large`
  - Participant-facing meaning: same as above (large magnitude tier)
  - Concrete stimulus realization: item-specific amount/delay text pair from configured/default item pool
  - Outcome rules: no correctness; participant preference choice is recorded

Participant-facing text source:
- Static prompts/feedback/layout stimuli are config-defined in `config/*.yaml` (`stimuli` section)
- Trial option texts are formatted in `run_trial.py` from deterministic item spec fields
- This split is appropriate because option text is trial-specific and depends on generated amount/delay values

## 4. Response and Scoring Rules

- Response mapping: left/right choice mapped from `task.key_list` (default `f`=`left`, `j`=`right`)
- Response key source: config (`task.key_list`)
- Missing-response policy: mark `choice_made=False`, record timeout feedback, continue trial flow
- Correctness logic: not applicable (preference task; no objectively correct answer)
- Reward/penalty updates: none (descriptive behavioral logging only)
- Running metrics: response rate, LL-choice proportion, mean RT among valid responses

## 5. Stimulus Layout Plan

- `intertemporal_choice`
  - Stimulus IDs shown together: `option_left`, `option_right`, `choice_prompt`
  - Layout anchors: left/right symmetric text positions and centered lower prompt
  - Size/spacing: option text height 40, prompt height 24, explicit `wrapWidth`
  - Readability/overlap checks: verified in QA/sim traces with concrete amount/delay strings
  - Rationale: clear left/right mapping for binary intertemporal choice

- `choice_confirmation`
  - Stimulus IDs shown together: `option_left`, `option_right`, `highlight_left|highlight_right`
  - Layout anchors: highlight rect matches option text regions
  - Rationale: confirm selected side without exposing hidden condition tokens

## 6. Trigger Plan

- Experiment: `exp_onset`, `exp_end`
- Block: `block_onset`, `block_end`
- Pre-choice fixation: `cue_onset`
- Offer jitter: `anticipation_onset`
- Choice phase: `choice_onset`, `choice_response_left`, `choice_response_right`, `choice_no_response`
- Choice confirmation: `choice_confirm_onset`
- Feedback: `feedback_choice_onset`, `feedback_timeout_onset`
- ITI: `iti_onset`

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: simple mode-aware single-flow (`human|qa|sim`) without controller setup
- `utils.py` used?: yes
- Exact purpose: MCQ item-pool normalization, deterministic block planning, and custom block condition generation helper
- Custom controller used?: no
- Why PsyFlow-native path alone is insufficient: built-in condition labels cannot encode item identity and side counterbalancing requirements
- Legacy/backward-compatibility fallback logic required?: no

## 8. Inference Log

- Decision: neutral fixation used pre-choice instead of showing magnitude label cue text
- Why inference was required: many delay-discounting implementations emphasize direct choice display; no correctness-learning cue is required
- Citation-supported rationale: preserves unbiased pre-choice stage and avoids leaking internal condition tokens before response
