# Task Plot Review

## Evidence Match

- Pass: title and construct match the McGurk Effect Task.
- Pass: rows match configured congruent, incongruent, and audio_only conditions.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> AV stimulus -> Decision -> Feedback -> ITI.
- Pass: timing labels match config: 500-800 ms fixation, 1100 ms AV stimulus, 1800 ms decision, 700 ms feedback, 500-900 ms ITI.
- Pass: key mapping shows F=/ba/, J=/da/, and K=/ga/.
- Pass: incongruent row preserves canonical mismatch examples and the /da/ fusion report is treated as a decision option.
- Pass: feedback is shown as response-recorded or timeout status, not correctness feedback.

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
