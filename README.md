# Delay Discounting Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field                | Value                                        |
|----------------------|----------------------------------------------|
| Name                 | Delay Discounting Task                       |
| Version              | v0.2.0-dev                                   |
| URL / Repository     | https://github.com/TaskBeacon/T000017-delay-discounting |
| Short Description    | MCQ-27 style intertemporal choice task (smaller-sooner vs larger-later) |
| Created By           | TaskBeacon                                   |
| Date Updated         | 2026-02-17                                   |
| PsyFlow Version      | 0.1.9                                        |
| PsychoPy Version     | 2025.1.1                                     |
| Modality             | Behavior                                     |
| Language             | Chinese                                      |
| Voice Name           | zh-CN-YunyangNeural                          |

## 1. Task Overview

This task implements an MCQ-27 style delay discounting paradigm where participants repeatedly choose between a smaller-sooner (SS) and larger-later (LL) monetary option. Trial offers are generated from a fixed 27-item item pool, with configurable randomization and side counterbalancing. The implementation supports `human`, `qa`, and `sim` modes, records choice and RT outcomes at trial level, and emits structured triggers for each phase.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|------|-------------|
| 1. Parse mode and config | `main.py` resolves `human/qa/sim` and loads the requested YAML profile. |
| 2. Build participant context | Human mode uses full subject form; QA and sim use synthetic IDs from runtime context. |
| 3. Initialize runtime | Construct `TaskSettings`, initialize trigger runtime, window, keyboard, and preload all configured stimuli. |
| 4. Initialize controller | `DelayDiscountingController.from_dict(...)` loads controller options and MCQ item pool behavior. |
| 5. Start experiment | Emit `exp_onset`; show instruction screen and wait for continue key. |
| 6. Prepare block plan | For each block (`total_blocks=1`), controller generates trial plan and side assignments via `prepare_block(...)`. |
| 7. Run trials | `BlockUnit` emits `block_onset`, executes `run_trial(...)` for each planned condition, then emits `block_end`. |
| 8. Compute block summary | After block, compute response rate, LL choice rate, and mean RT from collected trial records. |
| 9. Show block break | Present block summary screen (`block_break`) with formatted metrics. |
| 10. Finalize | Show final summary screen (`good_bye`), emit `exp_end`, save CSV, close trigger runtime, and quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|------|-------------|
| 1. Fetch planned offer | `next_trial(...)` provides one preplanned item with magnitude, SS/LL amounts, delay, side assignment, and item ID. |
| 2. Cue phase | Show neutral fixation for `cue_duration=0.6 s` and emit `cue_onset`. Condition labels are intentionally not shown before choice. |
| 3. Anticipation phase | Show fixation for `anticipation_duration=0.2 s` and emit `anticipation_onset`. |
| 4. Choice phase | Draw left/right option text and choice prompt; collect `f/j` response within `decision_duration=6.0 s`; emit `choice_onset`, response trigger (`31/32`), or timeout trigger (`39`). |
| 5. Choice state derivation | Compute chosen side, chosen option (`ss`/`ll`), chosen amount, chosen delay, and LL indicator (`chose_ll`). |
| 6. Choice confirm phase (if responded) | Present both options plus a highlight rectangle on selected side for `choice_confirm_duration=0.3 s`; emit `choice_confirm_onset`. |
| 7. Feedback phase | If responded, show `feedback_choice` (`feedback_choice_onset=40`); if timeout, show `feedback_timeout` (`feedback_timeout_onset=41`) for `feedback_duration=0.5 s`. |
| 8. ITI phase | Show fixation for `iti_duration=0.5 s` and emit `iti_onset`. |

### Controller Logic

| Component | Description |
|-----------|-------------|
| Item pool | Uses embedded 27-item MCQ table (`MCQ27_ITEMS`) with fields: item ID, magnitude tier, SS amount, LL amount, delay days, and reference discount factor (`k_ref`). |
| Block plan generation | `prepare_block(...)` builds trial list of length `trial_per_block`, optionally randomizes order, and stores queue by block index. |
| Side assignment | With `counterbalance_sides=true`, LL side is balanced across trials (half left, half right when possible) and shuffled by seed. |
| Option rendering fields | For each trial, controller computes `left_amount/right_amount`, `left_delay_days/right_delay_days`, `ll_side`, and `ss_side`. |
| Trial serving | `next_trial(...)` pops next planned trial, increments `global_trial_id`, and warns on expected-condition mismatch. |

### Other Logic

| Component | Description |
|-----------|-------------|
| Neutral pre-choice design | Although `cue_text` is defined in config, current trial logic intentionally presents fixation in cue phase to avoid exposing condition labels before choice. |
| Derived behavioral outputs | Trial data includes response presence, response key, RT, chosen side, chosen option, LL choice flag, and chosen value/delay fields. |
| Block-level metrics | Main loop computes response rate, LL rate among valid responses, and mean RT for block feedback text. |
| Trial context plumbing | Each stage (`cue`, `anticipation`, `target`, `choice_confirm`, `feedback`, `iti`) calls `set_trial_context(...)` for responder compatibility and simulation auditability. |

### Runtime Context Phases
| Phase Label | Meaning |
|---|---|
| `pre_choice_fixation` | pre choice fixation stage in `src/run_trial.py` responder context. |
| `offer_onset_jitter` | offer onset jitter stage in `src/run_trial.py` responder context. |
| `intertemporal_choice` | intertemporal choice stage in `src/run_trial.py` responder context. |
| `choice_confirmation` | choice confirmation stage in `src/run_trial.py` responder context. |
| `outcome_feedback` | outcome feedback stage in `src/run_trial.py` responder context. |
| `inter_trial_interval` | inter trial interval stage in `src/run_trial.py` responder context. |

## 3. Configuration Summary

All settings are defined in `config/config.yaml`.

### a. Subject Info

| Field | Meaning |
|-------|---------|
| subject_id | Required participant ID, integer, 3 digits, constrained to 101-999. |
| subname | Participant name string (pinyin label in mapping). |
| age | Integer age constrained to 5-60. |
| gender | Choice field with `Male` and `Female`. |

### b. Window Settings

| Parameter | Value |
|-----------|-------|
| size | `[1280, 720]` |
| units | `pix` |
| screen | `0` |
| bg_color | `black` |
| fullscreen | `false` |
| monitor_width_cm | `35.5` |
| monitor_distance_cm | `60` |

### c. Stimuli

| Name | Type | Description |
|------|------|-------------|
| fixation | text | Center fixation `+` used in cue/anticipation/ITI. |
| instruction_text | text | Chinese instruction describing SS/LL choices and key mapping. |
| cue_text | text | Condition label text template (`金额等级...`) defined in config; currently not shown in trial runtime. |
| option_left | text | Left offer text stimulus, rebuilt each trial with concrete amount and delay. |
| option_right | text | Right offer text stimulus, rebuilt each trial with concrete amount and delay. |
| highlight_left | rect | Left-side selection highlight rectangle shown after response. |
| highlight_right | rect | Right-side selection highlight rectangle shown after response. |
| choice_prompt | text | Neutral choice prompt shown during decision window. |
| feedback_choice | text | Feedback text for valid choices. |
| feedback_timeout | text | Feedback text for missed responses. |
| block_break | text | Block summary text with response rate, LL rate, and mean RT. |
| good_bye | text | Final summary with total trials, valid trials, and LL rate. |

### d. Timing

| Phase | Duration |
|-------|----------|
| cue | `0.6 s` |
| anticipation | `0.2 s` |
| choice response window | `6.0 s` |
| choice confirm | `0.3 s` |
| feedback | `0.5 s` |
| iti | `0.5 s` |

### e. Triggers

| Event | Code |
|-------|------|
| exp_onset | 1 |
| exp_end | 2 |
| block_onset | 10 |
| block_end | 11 |
| cue_onset | 20 |
| anticipation_onset | 25 |
| choice_onset | 30 |
| choice_response_left | 31 |
| choice_response_right | 32 |
| choice_confirm_onset | 33 |
| choice_no_response | 39 |
| feedback_choice_onset | 40 |
| feedback_timeout_onset | 41 |
| iti_onset | 50 |

### f. Adaptive Controller

| Parameter | Value |
|-----------|-------|
| randomize_order | `true` |
| counterbalance_sides | `true` |
| ll_left_prob | `0.5` (used when side counterbalancing is disabled) |
| enable_logging | `true` |
| item pool size | `27` MCQ items |
| seed behavior | Block seed passed via `settings.block_seed[block_i]`; produces deterministic block plan for fixed seed |
| adaptation style | Non-staircase offer sampling with preplanned item/side schedule |

## 4. Methods (for academic publication)

Participants performed a delay discounting task based on the 27-item Monetary Choice Questionnaire framework. On each trial, they selected between two monetary options: a smaller immediate reward (SS) and a larger delayed reward (LL). The task used one block of 27 trials, with item content spanning small, medium, and large magnitude tiers. Responses were made with two keys (`F`/`J`) mapped to left/right options.

Each trial started with a neutral fixation cue (0.6 s) and a brief anticipation interval (0.2 s), followed by the decision screen (maximum 6.0 s). The decision screen displayed two option texts containing amount and delay information. If a choice was made, a short confirmation stage (0.3 s) highlighted the selected side without revealing internal condition labels; then feedback was shown for 0.5 s. Missed trials produced timeout feedback. A 0.5 s inter-trial interval separated trials.

Offer generation was controlled by a deterministic planner initialized from the configured seed, with optional order randomization and side counterbalancing to distribute LL placement across left and right positions. Behavioral outputs included response rate, reaction time, choice side, and LL choice proportion at both trial and block level. Event markers were emitted for all principal phases to support synchronized behavioral and neurophysiological analyses.
