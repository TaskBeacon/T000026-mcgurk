# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['congruent','incongruent','audio_only']` | W2061698928 | McGurk paradigms contrast matched vs mismatched audiovisual pairings; control conditions are common in follow-up designs. | inferred | `audio_only` isolates unimodal auditory report behavior. |
| task.keys | `task.key_list`, `task.ba_key`, `task.da_key`, `task.ga_key` | `f -> /ba/`, `j -> /da/`, `k -> /ga/` | W1976571557 | Syllable-level categorical report (`/ba/`, `/da/`, `/ga/`) is central to McGurk percept measurement. | inferred | `space` is reserved for continue screens. |
| timing.fixation | `timing.fixation_duration` | `[0.5, 0.8]` s | W2061698928 | Temporal alignment constraints motivate controlled pre-stimulus pacing; exact jitter values are implementation-level. | inferred | Sampled per trial by controller. |
| timing.av_window | `timing.av_duration` | `1.1` s | W2061698928 | Audiovisual presentation window constrained to short speech segment timing. | inferred | Same across conditions for comparability. |
| timing.decision_deadline | `timing.decision_deadline` | `1.8` s | W2061698928 | Bounded report window keeps RT and timeout metrics comparable. | inferred | Condition-specific timeout triggers are emitted. |
| timing.feedback | `timing.feedback_duration` | `0.7` s | W2015198688 | Event-aligned analyses require explicit post-response feedback epoch markers. | inferred | Separate recorded/timeout feedback onset codes. |
| timing.iti | `timing.iti_duration` | `[0.5, 0.9]` s | W2015198688 | Event separation supports downstream epoching and contamination control. | inferred | Sampled per trial by controller. |
| controller.incongruent_pairs | `controller.incongruent_pairs` | `[['ba','ga'], ['ga','ba']]` | W2061698928 | Canonical incongruent pairings reliably evoke fused `/da/` reports. | inferred | Implemented via `Controller.build_trial(...)`. |
| controller.syllables | `controller.syllables` | `['ba','da','ga']` | W1976571557 | Report space uses three stop-consonant syllable categories. | inferred | Shared for congruent and audio-only sampling. |
| trigger.av_onsets | `triggers.map.*_av_onset` | `30/31/32` by condition | W2015198688 | Condition-specific event tagging required for analysis of multisensory integration. | inferred | Congruent, incongruent, and audio-only are separable in logs. |
| trigger.decision_onsets | `triggers.map.*_decision_onset` | `40/41/42` by condition | W2015198688 | Distinct decision-window onsets facilitate response-epoch alignment. | inferred | Emitted at decision screen onset. |
| trigger.response_codes | `triggers.map.response_ba/da/ga` | `50/51/52` | W1976571557 | Report categories are the primary dependent variable and need category-specific event markers. | inferred | Sent after response key is mapped to syllable. |
| trigger.timeout_codes | `triggers.map.*_no_response` | `60/61/62` by condition | W2015198688 | Non-response must be explicitly tagged to separate omissions from percept reports. | inferred | Emitted via decision timeout policy. |