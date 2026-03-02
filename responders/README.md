# Responders

Task-specific responders for `T000026-mcgurk`.

- Scripted simulation uses `config/config_scripted_sim.yaml`.
- Sampler simulation uses `responders.task_sampler:TaskSamplerResponder` with condition-dependent percept sampling:
  - high match rate for `congruent`
  - elevated `/da/` fusion probability for `incongruent`
  - auditory-match tendency for `audio_only`
