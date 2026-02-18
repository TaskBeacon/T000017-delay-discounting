# CHANGELOG

All notable development changes for `T000017-delay-discounting` are documented here.

## [0.2.0] - 2026-02-17

### Changed
- Replaced MID-style scaffold with a delay-discounting specific implementation based on MCQ-27 style offer pairs.
- Refactored `src/utils.py` into `DelayDiscountingController` with deterministic trial planning, order randomization, and left/right side counterbalancing.
- Refactored `src/run_trial.py` to execute explicit SS vs LL decision trials, including trial-context fields for responder/sim plumbing.
- Updated `main.py` block flow to consume controller-planned trials and report choice metrics (response rate, LL choice ratio, RT).

### Updated
- Rebuilt all configs in human-friendly format with strict mode separation:
  - `config/config.yaml` (human only)
  - `config/config_qa.yaml` (qa only)
  - `config/config_scripted_sim.yaml` (scripted sim only)
  - `config/config_sampler_sim.yaml` (sampler sim only)
- Replaced generic sampler with task-specific delay-discounting responder (`responders/task_sampler.py`) using hyperbolic SV + logistic choice.
- Updated `README.md`, `assets/README.md`, `references/stimulus_mapping.md`, and `references/parameter_mapping.md` to reflect reference-aligned task logic.

### Fixed
- Fixed sampler sim instruction-stage timeout by adding continue-key handling for non-choice phases.

### Verified
- `python -m psyflow.validate e:\Taskbeacon\T000017-delay-discounting`
- `python main.py qa --config config/config_qa.yaml`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Delay Discounting Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
