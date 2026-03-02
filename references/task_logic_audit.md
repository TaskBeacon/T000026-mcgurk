# Task Logic Audit: McGurk Effect Task

## 1. Paradigm Intent

- Task: `mcgurk`.
- Construct: audiovisual speech integration with explicit measurement of fused `/da/` percept in incongruent trials.
- Manipulated factor: condition (`congruent`, `incongruent`, `audio_only`).
- Primary dependent measures: reported syllable, response latency, fusion rate in incongruent condition.

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `3` blocks x `30` trials.
- QA/sim profiles: `1` block x `12` trials.
- Condition scheduling: block-level condition list from `BlockUnit.generate_conditions()`.
- Within-condition stimulus composition: `Controller.build_trial(condition)`.

### Trial State Machine

1. `fixation`
- Central fixation (`+`) with jittered duration.
- Trigger: `fixation_onset`.

2. `av_stimulus`
- Face primitives, condition-appropriate mouth shape, and syllable audio are presented simultaneously.
- Trigger: `{condition}_av_onset`.

3. `decision`
- Participant reports perceived syllable (`/ba/`, `/da/`, `/ga/`).
- Trigger: `{condition}_decision_onset`.
- Timeout trigger: `{condition}_no_response`.

4. `feedback`
- Recorded-response feedback or timeout feedback.
- Trigger: `response_recorded_fb_onset` or `timeout_fb_onset`.

5. `inter_trial_interval`
- Fixation with jittered ITI.
- Trigger: `iti_onset`.

## 3. Condition Semantics

- `congruent`:
- Audio and visual syllables match (`ba+ba`, `da+da`, `ga+ga`).

- `incongruent`:
- Canonical mismatched pairings (`ba+ga`, `ga+ba`) to evoke fusion reports.

- `audio_only`:
- Auditory syllable with neutral `mouth_none` visual cue.

## 4. Response and Scoring Rules

- Key mapping:
- `f -> ba`
- `j -> da`
- `k -> ga`

- Timeout policy:
- No valid response within deadline sets `decision_timed_out = true` and feedback switches to timeout message.

- Derived trial metrics:
- `reported_syllable` from response key mapping.
- `matches_expected` for congruent/audio_only expected percept alignment.
- `fusion_da = true` when `condition == incongruent` and reported syllable is `da`.

## 5. Stimulus Layout Plan

- AV screen uses explicit face geometry with fixed positions:
- face center `(0, 40)`, eyes at `(-58, 95)` and `(58, 95)`, nose at `(0, 52)`, mouth at `(0, -8)`.
- `speech_prompt` appears below the face at `(0, -220)`.
- Decision screen shows question at `(0, 120)` and key hint at `(0, 40)`.
- All Chinese participant-facing text uses `font: SimHei`.

## 6. Trigger Plan

| Trigger | Code | Meaning |
|---|---:|---|
| `exp_onset` | 1 | Experiment start |
| `exp_end` | 2 | Experiment end |
| `block_onset` | 10 | Block start |
| `block_end` | 11 | Block end |
| `fixation_onset` | 20 | Fixation onset |
| `congruent_av_onset` | 30 | Congruent AV onset |
| `incongruent_av_onset` | 31 | Incongruent AV onset |
| `audio_only_av_onset` | 32 | Audio-only AV onset |
| `congruent_decision_onset` | 40 | Congruent decision onset |
| `incongruent_decision_onset` | 41 | Incongruent decision onset |
| `audio_only_decision_onset` | 42 | Audio-only decision onset |
| `response_ba` | 50 | `/ba/` response |
| `response_da` | 51 | `/da/` response |
| `response_ga` | 52 | `/ga/` response |
| `congruent_no_response` | 60 | Congruent timeout |
| `incongruent_no_response` | 61 | Incongruent timeout |
| `audio_only_no_response` | 62 | Audio-only timeout |
| `response_recorded_fb_onset` | 70 | Recorded feedback onset |
| `timeout_fb_onset` | 71 | Timeout feedback onset |
| `iti_onset` | 80 | ITI onset |

## 7. Architecture Decisions (Auditability)

- `main.py` uses one mode-aware execution path (`human|qa|sim`) with shared initialization order.
- `src/run_trial.py` is aligned to McGurk-specific states; legacy MID sequence labels are removed.
- Participant-facing text is sourced from config stimuli via `StimBank`, not hardcoded in runtime logic.
- Trial context contains condition/audio/visual/expected-percept factors for reproducible simulation and audit.

## 8. Inference Log

- Exact fixation and ITI jitter ranges are inferred implementation parameters; selected papers constrain temporal sensitivity but do not prescribe these exact values.
- The chosen incongruent pair set (`ba+ga`, `ga+ba`) is inferred from canonical McGurk protocols.
- The auditory-only condition with neutral mouth cue is an inferred control implementation to isolate unimodal perception effects.