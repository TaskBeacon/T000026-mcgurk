# CHANGELOG

## [v0.2.0-dev] - 2026-02-19

### Changed
- Repaired `T000026-mcgurk` from MID-template trial flow to a literature-aligned McGurk paradigm.
- Replaced trial state machine with `fixation -> av_stimulus -> decision -> feedback -> iti`.
- Added concrete audiovisual syllable stimuli (`assets/audio/ba.wav`, `da.wav`, `ga.wav`) and articulatory viseme rendering (`mouth_ba/mouth_da/mouth_ga/mouth_none`).
- Replaced MID-style adaptive-duration controller with condition-specific McGurk trial planner.
- Rewrote `responders/task_sampler.py` to model perceptual reports, including fusion tendency in incongruent trials.
- Rewrote all configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`) with clean UTF-8 Chinese participant text and McGurk-specific trigger map.
- Rebuilt references artifacts and documentation (`task_logic_audit.md`, `stimulus_mapping.md`, `parameter_mapping.md`, `references.yaml/.md`, `selected_papers.json`, `README.md`) to be literature-first and paradigm-consistent.
- Removed irrelevant reference contamination from task evidence list.

### Fixed
- Removed legacy MID cue/anticipation/target semantics from runtime, trigger map, and audit artifacts.

## [v0.1.1-dev] - 2026-02-19

### Changed
- Rebuilt literature bundle with task-relevant curated papers and regenerated reference artifacts.
- Replaced corrupted `references/task_logic_audit.md` with a full state-machine audit.
- Updated `references/stimulus_mapping.md` to concrete implemented stimulus IDs per condition.
- Synced metadata (`README.md`, `taskbeacon.yaml`) with current configuration and evidence.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for McGurk Effect Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
