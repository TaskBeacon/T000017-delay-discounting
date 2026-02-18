# Stimulus Mapping

Task: `Delay Discounting Task` (`T000017`)

| Component | Implemented Stimulus IDs | Source Paper ID | Evidence | Implementation Mode | Notes |
|---|---|---|---|---|---|
| MCQ-27 offer amounts and delays (27 items) | runtime trial table in `src/utils.py` (`MCQ27_ITEMS`) | `W2509303870` | Kaplan et al. (2016) report the standard 27-item Monetary Choice Questionnaire values (amount, delay, implied k). | `psychopy_builtin` | The task uses these 27 values as the canonical human-run offer set. |
| Trial decision screen (SS vs LL two-option choice) | `option_left`, `option_right`, `choice_prompt` | `W2032105672` | Methodological work describes delay discounting as explicit option-pair choices requiring participant selection. | `psychopy_builtin` | Left/right sides are counterbalanced per trial (inferred implementation detail). |
| Cue before decision | `cue_text` | `W2032105672` | Choice tasks typically separate preparatory and response stages. | `psychopy_builtin` | Displays magnitude set (small/medium/large) for structured logging and auditability. |
| Post-choice status | `feedback_choice`, `feedback_timeout` | `W2032105672` | Response and non-response handling is required in RT-based implementations. | `psychopy_builtin` | Used for status feedback only; no objective correctness is defined. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives/text.
- `generated_reference_asset`: synthetic assets generated from reference-described rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
