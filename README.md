# McGurk Effect Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | McGurk Effect Task |
| Version | v0.1.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000026-mcgurk |
| Short Description | Audiovisual speech integration with congruent/incongruent and audio-only conditions. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-18 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | English |
| Voice Name |  |

## 1. Task Overview

This task implements a McGurk-style perceptual integration paradigm with three conditions: `congruent`, `incongruent`, and `audio_only`. Each trial presents a cue, an anticipation interval, a target display, and then feedback.

Participants respond with `space` when they detect the target content during the response window. Trial logs record response timing, hit/miss outcomes, and condition-specific trigger streams for downstream QA and synchronization checks.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Trial scheduling | `BlockUnit(...).add_condition(...)` loads the configured condition sequence per block. |
| 2. Trial execution | `run_trial(...)` presents cue, anticipation, target, and feedback phases. |
| 3. Block summary | Block-level accuracy and cumulative score are displayed. |
| 4. Final summary | Final cumulative score is displayed at task end. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Cue | Condition-specific cue text is shown. |
| Anticipation | Fixation is shown while early responses are tracked. |
| Target | Condition-specific target is shown with response capture. |
| Pre-feedback fixation | A short fixation interval separates target and feedback. |
| Feedback | Hit/miss feedback is shown with score delta. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive duration | `Controller.get_duration(condition)` returns condition-specific target duration. |
| Condition history | `Controller.update(hit, condition)` tracks performance by condition. |
| Scoring | Trial delta is computed from response outcome and condition class. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `anticipation` | Pre-target response window with fixation. |
| `target` | Condition-specific target-response window. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `*_cue` | text | Condition cue text (`congruent`, `incongruent`, `audio_only`). |
| `fixation` | text | Central fixation marker used in anticipation/prefeedback. |
| `*_target` | text | Condition target token used for response capture. |
| `*_hit_feedback`, `*_miss_feedback` | text | Condition-specific feedback text. |
| `block_break`, `good_bye` | text | Block transition and task-end summary. |

### d. Timing

| Phase | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 1.0 s |
| prefeedback | 0.4 s |
| feedback | 0.8 s |
| target | adaptive via controller (`0.08`-`0.40` s bounds) |

## 4. Methods (for academic publication)

Participants completed a perceptual integration task with congruent, incongruent, and audio-only speech-like conditions. Each trial included a cue, anticipation period, target response window, and explicit feedback, allowing condition-resolved analysis of hit rate and response timing.

The implementation tracks trial-wise responses, early responses, adaptive target durations, and condition-specific performance history. Trigger events are emitted at cue, anticipation, target, and feedback onsets to support synchronized acquisition workflows.

Runtime profiles include human, QA, scripted simulation, and sampler simulation modes using dedicated configuration files.
