from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for McGurk perceptual report trials."""

    miss_rate: float = 0.05
    p_match_congruent: float = 0.92
    p_match_audio_only: float = 0.90
    p_fusion_incongruent: float = 0.58
    p_auditory_incongruent: float = 0.27
    rt_congruent_mean_s: float = 0.56
    rt_incongruent_mean_s: float = 0.68
    rt_audio_only_mean_s: float = 0.60
    rt_sd_s: float = 0.10
    rt_min_s: float = 0.20

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.miss_rate = max(0.0, min(1.0, float(self.miss_rate)))
        self.p_match_congruent = max(0.0, min(1.0, float(self.p_match_congruent)))
        self.p_match_audio_only = max(0.0, min(1.0, float(self.p_match_audio_only)))
        self.p_fusion_incongruent = max(0.0, min(1.0, float(self.p_fusion_incongruent)))
        self.p_auditory_incongruent = max(0.0, min(1.0, float(self.p_auditory_incongruent)))
        self.rt_congruent_mean_s = float(self.rt_congruent_mean_s)
        self.rt_incongruent_mean_s = float(self.rt_incongruent_mean_s)
        self.rt_audio_only_mean_s = float(self.rt_audio_only_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _sample_rt(self, mean: float) -> float:
        return max(self.rt_min_s, self._sample_normal(mean, self.rt_sd_s))

    def _continue_action(self, valid_keys: list[str], phase: str) -> Action:
        key = "space" if "space" in valid_keys else valid_keys[0]
        rt = self._sample_rt(self.rt_congruent_mean_s)
        return Action(
            key=key,
            rt_s=rt,
            meta={"source": "task_sampler", "phase": phase, "outcome": "continue"},
        )

    def _pick_other_syllable(self, preferred: str) -> str:
        pool = ["ba", "da", "ga"]
        pool = [s for s in pool if s != preferred]
        if not pool:
            return preferred
        idx = int(self._sample_random() * len(pool)) % len(pool)
        return pool[idx]

    def act(self, obs: Observation) -> Action:
        valid_keys = [str(k).strip().lower() for k in list(obs.valid_keys or []) if str(k).strip()]
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        if self._rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        phase = str(obs.phase or "")
        if phase != "decision":
            return self._continue_action(valid_keys, phase)

        if self._sample_random() < self.miss_rate:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "outcome": "timeout"})

        factors = dict(obs.task_factors or {})
        condition = str(factors.get("condition", "")).strip().lower()
        audio_syllable = str(factors.get("audio_syllable", "ba")).strip().lower()
        visual_syllable = str(factors.get("visual_syllable", "none")).strip().lower()

        ba_key = str(factors.get("ba_key", "f")).strip().lower()
        da_key = str(factors.get("da_key", "j")).strip().lower()
        ga_key = str(factors.get("ga_key", "k")).strip().lower()
        syllable_to_key = {
            "ba": ba_key if ba_key in valid_keys else valid_keys[0],
            "da": da_key if da_key in valid_keys else (valid_keys[1] if len(valid_keys) > 1 else valid_keys[0]),
            "ga": ga_key if ga_key in valid_keys else valid_keys[-1],
        }

        if condition == "congruent":
            rt_mean = self.rt_congruent_mean_s
            if self._sample_random() < self.p_match_congruent:
                reported = audio_syllable
            else:
                reported = self._pick_other_syllable(audio_syllable)
        elif condition == "incongruent":
            rt_mean = self.rt_incongruent_mean_s
            draw = self._sample_random()
            if draw < self.p_fusion_incongruent:
                reported = "da"
            elif draw < (self.p_fusion_incongruent + self.p_auditory_incongruent):
                reported = audio_syllable
            else:
                reported = "ba" if visual_syllable == "ba" else ("ga" if visual_syllable == "ga" else "da")
        else:
            rt_mean = self.rt_audio_only_mean_s
            if self._sample_random() < self.p_match_audio_only:
                reported = audio_syllable
            else:
                reported = self._pick_other_syllable(audio_syllable)

        chosen_key = syllable_to_key.get(reported, valid_keys[0])
        rt = self._sample_rt(rt_mean)

        return Action(
            key=chosen_key,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "outcome": "choose",
                "condition": condition,
                "reported": reported,
            },
        )
