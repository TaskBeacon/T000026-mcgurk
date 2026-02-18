# Stimulus Mapping

Task: `McGurk Effect Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `congruent` | `congruent_cue`, `congruent_target` | `W2104396257` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for CONGRUENT; target token for condition-specific response context. |
| `incongruent` | `incongruent_cue`, `incongruent_target` | `W2104396257` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for INCONGRUENT; target token for condition-specific response context. |
| `audio_only` | `audio_only_cue`, `audio_only_target` | `W2104396257` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for AUDIO ONLY; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
