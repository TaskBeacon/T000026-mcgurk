# Assets for McGurk Effect Task

This task ships concrete audiovisual stimuli required by the McGurk paradigm.

## Included assets

- `assets/audio/ba.wav`
- `assets/audio/da.wav`
- `assets/audio/ga.wav`

These audio files are local syllable tokens used by `audio_ba`, `audio_da`, and `audio_ga` in all run modes.

Visual articulatory cues are rendered by PsychoPy primitives (`mouth_ba`, `mouth_da`, `mouth_ga`, `mouth_none`) defined in `config/*.yaml`. `src/run_trial.py` rebuilds those primitives into short mouth-frame sequences during the AV phase so visible syllables animate across the audio window.

If assets are updated, keep `references/stimulus_mapping.md` synchronized with exact stimulus IDs and evidence rationale.
