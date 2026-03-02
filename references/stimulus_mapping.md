# Stimulus Mapping

Task: `McGurk Effect Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `congruent` | `audio_ba + mouth_ba`, `audio_da + mouth_da`, `audio_ga + mouth_ga`, plus shared face scaffold (`avatar_face`, `eye_left`, `eye_right`, `nose`) | `W2061698928` | Congruent audiovisual syllable pairings provide baseline speech-identification performance. | `psychopy_builtin` + `generated_reference_asset` | Audio files are local task assets (`assets/audio/*.wav`), visemes are PsychoPy primitives. |
| `incongruent` | `audio_ba + mouth_ga`, `audio_ga + mouth_ba`, plus shared face scaffold | `W2061698928` | Incongruent audiovisual pairings are expected to increase fused `/da/` percepts (McGurk effect). | `psychopy_builtin` + `generated_reference_asset` | Pairings are sampled by `Controller.build_trial()` from configured `incongruent_pairs`. |
| `audio_only` | `audio_ba|audio_da|audio_ga + mouth_none`, plus shared face scaffold | `W2104396257` | Auditory-only style control supports dissociating audiovisual integration from unimodal speech perception. | `psychopy_builtin` + `generated_reference_asset` | `mouth_none` removes informative articulatory visual cue. |
| `all_conditions` | `instruction_text`, `fixation`, `speech_prompt`, `decision_prompt`, `key_hint`, `feedback_recorded`, `feedback_timeout`, `block_break`, `good_bye` | `W1976571557` | Shared instruction/report envelope for syllable identification and trial transitions. | `psychopy_builtin` | Participant-facing text is Chinese and uses `font: SimHei`. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives configured in YAML.
- `generated_reference_asset`: non-placeholder task assets generated to match reference-described stimuli.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
