# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `small` | `cue` | `cue_text_small` | Cue indicating small-magnitude decision set before choice | W2509303870 | MCQ magnitude-tier organization | psychopy_builtin | config text stimuli | Internal condition tier shown as cue |
| `medium` | `cue` | `cue_text_medium` | Cue indicating medium-magnitude decision set before choice | W2509303870 | MCQ magnitude-tier organization | psychopy_builtin | config text stimuli | Internal condition tier shown as cue |
| `large` | `cue` | `cue_text_large` | Cue indicating large-magnitude decision set before choice | W2509303870 | MCQ magnitude-tier organization | psychopy_builtin | config text stimuli | Internal condition tier shown as cue |
| `small` | `decision` | `option_left`, `option_right`, `choice_prompt` | Two-option SS vs LL monetary offer text with delay | W2032105672 | Intertemporal choice requires explicit option-pair selection | psychopy_builtin | runtime formatted text | Left/right side counterbalanced |
| `medium` | `decision` | `option_left`, `option_right`, `choice_prompt` | Two-option SS vs LL monetary offer text with delay | W2032105672 | Intertemporal choice requires explicit option-pair selection | psychopy_builtin | runtime formatted text | Left/right side counterbalanced |
| `large` | `decision` | `option_left`, `option_right`, `choice_prompt` | Two-option SS vs LL monetary offer text with delay | W2032105672 | Intertemporal choice requires explicit option-pair selection | psychopy_builtin | runtime formatted text | Left/right side counterbalanced |
| `all` | `feedback` | `feedback_choice`, `feedback_timeout` | Response confirmation or timeout message | W2032105672 | RT-based choice task requires response-state handling | psychopy_builtin | config text stimuli | No objective right/wrong correctness |
| `all` | `iti` | `fixation` | Inter-trial fixation cross | W2032105672 | ITI separation between trial events | psychopy_builtin | config text stimulus | Shared across all conditions |
