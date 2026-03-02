# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['congruent', 'incongruent', 'audio_only']` | `W2061698928` | `inferred` | Core contrast between matched, mismatched, and control audiovisual speech conditions. |
| `task.key_list` | `['f', 'j', 'k', 'space']` | `W1976571557` | `inferred` | Three-alternative forced report for `/ba/`, `/da/`, `/ga/` plus continue key. |
| `task.ba_key`, `task.da_key`, `task.ga_key` | `f`, `j`, `k` | `W1976571557` | `inferred` | Explicit key mapping required for deterministic implementation of reported percept categories. |
| `timing.av_duration` | `1.1 s` | `W2061698928` | `inferred` | Short audiovisual presentation window consistent with temporal-constraint paradigms. |
| `timing.decision_deadline` | `1.8 s` | `W2061698928` | `inferred` | Bounded response window to standardize RT and timeout handling. |
| `controller.incongruent_pairs` | `[['ba','ga'], ['ga','ba']]` | `W2061698928` | `inferred` | Canonical McGurk incongruent pairings used to elicit fused `/da/` reports. |
| `stimuli.audio_*` | `assets/audio/ba.wav`, `da.wav`, `ga.wav` | `W1976571557` | `inferred` | Concrete auditory syllables required for audiovisual speech integration task. |
| `stimuli.mouth_*` | `mouth_ba`, `mouth_da`, `mouth_ga`, `mouth_none` | `W2104396257` | `inferred` | Visual articulatory cues implemented with PsychoPy primitives; neutral mouth for control trials. |
| `triggers.map.*_av_onset` | `30/31/32` | `W2015198688` | `inferred` | Condition-specific audiovisual onset markers support synchrony and downstream analyses. |
| `triggers.map.response_ba/da/ga` | `50/51/52` | `W2015198688` | `inferred` | Distinct response triggers for report-category-level event coding. |
| `triggers.map.*_no_response` | `60/61/62` | `W2015198688` | `inferred` | Timeout classification by condition for QA and synchronization checks. |
