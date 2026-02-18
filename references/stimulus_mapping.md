# Stimulus Mapping

Task: `McGurk Effect Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `congruent` | `congruent_cue`, `congruent_target`, `congruent_hit_feedback`, `congruent_miss_feedback`, `fixation` | `W2061698928` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `incongruent` | `incongruent_cue`, `incongruent_target`, `incongruent_hit_feedback`, `incongruent_miss_feedback`, `fixation` | `W2061698928` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `audio_only` | `audio_only_cue`, `audio_only_target`, `audio_only_hit_feedback`, `audio_only_miss_feedback`, `fixation` | `W2061698928` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye`, `fixation` | `W2061698928` | Shared instruction, transition, and fixation assets support the common task envelope across all conditions. | `psychopy_builtin` | Shared assets are condition-agnostic and used in every run mode. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
