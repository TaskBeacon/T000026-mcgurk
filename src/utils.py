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
        self.enable_logging = bool(enable_logging)

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

        final = {k: config.get(k, default) for k, default in allowed_keys.items() if k != "random_seed"}
        return cls(**final)

    def start_block(self, block_idx: int) -> None:
        _ = block_idx

    def build_trial(self, condition: str, rng: random.Random) -> TrialSpec:
        condition_id = str(condition).strip().lower()
        if condition_id == "congruent":
            syllable = str(rng.choice(self.syllables))
            return TrialSpec(
                condition="congruent",
                audio_syllable=syllable,
                visual_syllable=syllable,
                expected_percept=syllable,
            )

        if condition_id == "incongruent":
            audio_syllable, visual_syllable = rng.choice(self.incongruent_pairs)
            return TrialSpec(
                condition="incongruent",
                audio_syllable=audio_syllable,
                visual_syllable=visual_syllable,
                expected_percept="da",
            )

        if condition_id == "audio_only":
            syllable = str(rng.choice(self.syllables))
            return TrialSpec(
                condition="audio_only",
                audio_syllable=syllable,
                visual_syllable="none",
                expected_percept=syllable,
            )

        syllable = str(rng.choice(self.syllables))
        return TrialSpec(
            condition=condition_id or "unknown",
            audio_syllable=syllable,
            visual_syllable="none",
            expected_percept=syllable,
        )

    def record_trial(self, row: dict[str, Any]) -> None:
        condition = str(row.get("condition", "unknown"))
        self.histories.setdefault(condition, []).append(dict(row))


def generate_mcgurk_conditions(
    n_trials: int,
    condition_labels: list[Any] | None = None,
    *,
    seed: int = 0,
    syllables: list[str] | None = None,
    incongruent_pairs: list[list[str]] | None = None,
) -> list[tuple[str, str, str, str]]:
    """Build concrete McGurk trial specs during block scheduling."""
    labels = [str(label).strip().lower() for label in (condition_labels or ["congruent", "incongruent", "audio_only"])]
    if not labels:
        labels = ["congruent", "incongruent", "audio_only"]
    controller = Controller(syllables=syllables, incongruent_pairs=incongruent_pairs, enable_logging=False)
    rng = random.Random(int(seed))

    schedule: list[str] = []
    while len(schedule) < int(n_trials):
        schedule.extend(labels)
    schedule = schedule[: int(n_trials)]
    rng.shuffle(schedule)

    trials: list[tuple[str, str, str, str]] = []
    for condition_name in schedule:
        spec = controller.build_trial(condition_name, rng)
        trials.append(
            (
                str(spec.condition),
                str(spec.audio_syllable),
                str(spec.visual_syllable),
                str(spec.expected_percept),
            )
        )
    return trials


def mcgurk_condition_to_trial_spec(condition: Any) -> TrialSpec:
    """Decode a scheduled McGurk condition tuple."""
    if isinstance(condition, (tuple, list)) and len(condition) >= 4:
        condition_name, audio_syllable, visual_syllable, expected_percept = condition[:4]
        return TrialSpec(
            condition=str(condition_name).strip().lower(),
            audio_syllable=str(audio_syllable).strip().lower(),
            visual_syllable=str(visual_syllable).strip().lower(),
            expected_percept=str(expected_percept).strip().lower(),
        )
    raise ValueError(f"Expected scheduled McGurk condition tuple, got {condition!r}")
