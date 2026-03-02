from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any


@dataclass
class TrialSpec:
    condition: str
    audio_syllable: str
    visual_syllable: str
    expected_percept: str


class Controller:
    """Trial planner for McGurk-style audiovisual speech perception."""

    def __init__(
        self,
        syllables: list[str] | None = None,
        incongruent_pairs: list[list[str]] | None = None,
        random_seed: int | None = None,
        enable_logging: bool = True,
    ):
        self.syllables = [str(s).strip().lower() for s in (syllables or ["ba", "da", "ga"]) if str(s).strip()]
        if not self.syllables:
            self.syllables = ["ba", "da", "ga"]

        raw_pairs = incongruent_pairs or [["ba", "ga"], ["ga", "ba"]]
        pairs: list[tuple[str, str]] = []
        for pair in raw_pairs:
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                continue
            audio = str(pair[0]).strip().lower()
            visual = str(pair[1]).strip().lower()
            if audio and visual:
                pairs.append((audio, visual))
        if not pairs:
            pairs = [("ba", "ga"), ("ga", "ba")]

        self.incongruent_pairs = pairs
        self.random_seed = random_seed
        self.enable_logging = bool(enable_logging)

        self._rng = random.Random(random_seed)
        self._trial_counter = 0
        self.histories: dict[str, list[dict[str, Any]]] = {}

    @classmethod
    def from_dict(cls, config: dict) -> "Controller":
        allowed_keys = {
            "syllables": ["ba", "da", "ga"],
            "incongruent_pairs": [["ba", "ga"], ["ga", "ba"]],
            "random_seed": None,
            "enable_logging": True,
        }
        extra_keys = set(config.keys()) - set(allowed_keys)
        if extra_keys:
            raise ValueError(f"[Controller] Unsupported config keys: {extra_keys}")

        final = {k: config.get(k, default) for k, default in allowed_keys.items()}
        return cls(**final)

    def start_block(self, block_idx: int) -> None:
        _ = block_idx

    def next_trial_id(self) -> int:
        self._trial_counter += 1
        return self._trial_counter

    def sample_duration(self, value: Any, default: float) -> float:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            lo = float(min(value[0], value[1]))
            hi = float(max(value[0], value[1]))
            return float(self._rng.uniform(lo, hi))
        return float(default)

    def _sample_syllable(self) -> str:
        return str(self._rng.choice(self.syllables))

    def build_trial(self, condition: str) -> TrialSpec:
        condition_id = str(condition).strip().lower()
        if condition_id == "congruent":
            syllable = self._sample_syllable()
            return TrialSpec(
                condition="congruent",
                audio_syllable=syllable,
                visual_syllable=syllable,
                expected_percept=syllable,
            )

        if condition_id == "incongruent":
            audio_syllable, visual_syllable = self._rng.choice(self.incongruent_pairs)
            return TrialSpec(
                condition="incongruent",
                audio_syllable=audio_syllable,
                visual_syllable=visual_syllable,
                expected_percept="da",
            )

        if condition_id == "audio_only":
            syllable = self._sample_syllable()
            return TrialSpec(
                condition="audio_only",
                audio_syllable=syllable,
                visual_syllable="none",
                expected_percept=syllable,
            )

        syllable = self._sample_syllable()
        return TrialSpec(
            condition=condition_id or "unknown",
            audio_syllable=syllable,
            visual_syllable="none",
            expected_percept=syllable,
        )

    def record_trial(self, row: dict[str, Any]) -> None:
        condition = str(row.get("condition", "unknown"))
        self.histories.setdefault(condition, []).append(dict(row))
