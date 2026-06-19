# Task Plot Review

## Evidence Match

- Pass: title and construct match the delay discounting paradigm.
- Pass: Small, Medium, and Large magnitude rows match the configured condition labels.
- Pass: phase order matches README and `src/run_trial.py`: Cue -> Anticipation -> Choice -> Confirm -> Feedback -> ITI.
- Pass: timing labels match config: 600 ms cue, 200 ms anticipation, up to 6000 ms choice, 300 ms confirmation, 500 ms feedback, 500 ms ITI.
- Pass: choice screen shows smaller-sooner and larger-later monetary options.
- Pass: key mapping shows F for left and J for right, with LL side counterbalanced.
- Pass: feedback distinguishes valid choice feedback from timeout feedback.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
