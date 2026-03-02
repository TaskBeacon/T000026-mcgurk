from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _as_duration(controller, value: Any, default_value: float) -> float:
    if hasattr(controller, "sample_duration"):
        return float(controller.sample_duration(value, default_value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return float(default_value)
    return float(default_value)


def _response_to_syllable(response_key: str | None, *, ba_key: str, da_key: str, ga_key: str) -> str | None:
    key = str(response_key or "").strip().lower()
    if key == ba_key:
        return "ba"
    if key == da_key:
        return "da"
    if key == ga_key:
        return "ga"
    return None


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one McGurk trial with audiovisual presentation and syllable report."""
    condition_name = str(condition).strip().lower()
    trial_id = int(controller.next_trial_id()) if hasattr(controller, "next_trial_id") else 1
    block_idx_val = int(block_idx) if block_idx is not None else 0

    trial_spec = controller.build_trial(condition_name)

    ba_key = str(getattr(settings, "ba_key", "f")).strip().lower()
    da_key = str(getattr(settings, "da_key", "j")).strip().lower()
    ga_key = str(getattr(settings, "ga_key", "k")).strip().lower()
    response_keys = [ba_key, da_key, ga_key]

    fixation_duration = _as_duration(controller, settings.fixation_duration, 0.6)
    av_duration = float(settings.av_duration)
    decision_deadline = float(settings.decision_deadline)
    feedback_duration = float(settings.feedback_duration)
    iti_duration = _as_duration(controller, settings.iti_duration, 0.7)

    trial_data = {
        "trial_id": trial_id,
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "condition": trial_spec.condition,
        "audio_syllable": trial_spec.audio_syllable,
        "visual_syllable": trial_spec.visual_syllable,
        "expected_percept": trial_spec.expected_percept,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=_deadline_s(fixation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=trial_spec.condition,
        task_factors={
            "stage": "fixation",
            "condition": trial_spec.condition,
            "audio_syllable": trial_spec.audio_syllable,
            "visual_syllable": trial_spec.visual_syllable,
            "expected_percept": trial_spec.expected_percept,
            "block_idx": block_idx_val,
        },
        stim_id="fixation",
    )
    fixation.show(
        duration=fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    av_stimulus = make_unit(unit_label="av_stimulus")
    av_stimulus.add_stim(stim_bank.get("avatar_face"))
    av_stimulus.add_stim(stim_bank.get("eye_left"))
    av_stimulus.add_stim(stim_bank.get("eye_right"))
    av_stimulus.add_stim(stim_bank.get("nose"))
    av_stimulus.add_stim(stim_bank.get(f"mouth_{trial_spec.visual_syllable}"))
    av_stimulus.add_stim(stim_bank.get("speech_prompt"))
    av_stimulus.add_stim(stim_bank.get(f"audio_{trial_spec.audio_syllable}"))
    set_trial_context(
        av_stimulus,
        trial_id=trial_id,
        phase="av_stimulus",
        deadline_s=_deadline_s(av_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=trial_spec.condition,
        task_factors={
            "stage": "av_stimulus",
            "condition": trial_spec.condition,
            "audio_syllable": trial_spec.audio_syllable,
            "visual_syllable": trial_spec.visual_syllable,
            "expected_percept": trial_spec.expected_percept,
            "block_idx": block_idx_val,
        },
        stim_id=f"audio_{trial_spec.audio_syllable}+mouth_{trial_spec.visual_syllable}",
    )
    av_stimulus.show(
        duration=av_duration,
        onset_trigger=settings.triggers.get(f"{trial_spec.condition}_av_onset"),
    ).to_dict(trial_data)

    decision = make_unit(unit_label="decision")
    decision.add_stim(stim_bank.get("decision_prompt"))
    decision.add_stim(
        stim_bank.get_and_format(
            "key_hint",
            ba_key=ba_key.upper(),
            da_key=da_key.upper(),
            ga_key=ga_key.upper(),
        )
    )
    set_trial_context(
        decision,
        trial_id=trial_id,
        phase="decision",
        deadline_s=_deadline_s(decision_deadline),
        valid_keys=response_keys,
        block_id=trial_data["block_id"],
        condition_id=trial_spec.condition,
        task_factors={
            "stage": "decision",
            "condition": trial_spec.condition,
            "audio_syllable": trial_spec.audio_syllable,
            "visual_syllable": trial_spec.visual_syllable,
            "expected_percept": trial_spec.expected_percept,
            "ba_key": ba_key,
            "da_key": da_key,
            "ga_key": ga_key,
            "block_idx": block_idx_val,
        },
        stim_id="decision_prompt+key_hint",
    )
    decision.capture_response(
        keys=response_keys,
        duration=decision_deadline,
        onset_trigger=settings.triggers.get(f"{trial_spec.condition}_decision_onset"),
        response_trigger=None,
        timeout_trigger=settings.triggers.get(f"{trial_spec.condition}_no_response"),
    )
    decision.to_dict(trial_data)

    response_key = str(decision.get_state("response", "")).strip().lower()
    reported_syllable = _response_to_syllable(
        response_key,
        ba_key=ba_key,
        da_key=da_key,
        ga_key=ga_key,
    )
    timed_out = reported_syllable is None

    if reported_syllable == "ba":
        trigger_runtime.send(settings.triggers.get("response_ba"))
    elif reported_syllable == "da":
        trigger_runtime.send(settings.triggers.get("response_da"))
    elif reported_syllable == "ga":
        trigger_runtime.send(settings.triggers.get("response_ga"))

    feedback_stim = "feedback_timeout" if timed_out else "feedback_recorded"
    feedback_onset = "timeout_fb_onset" if timed_out else "response_recorded_fb_onset"

    feedback = make_unit(unit_label="feedback").add_stim(
        stim_bank.get_and_format(
            feedback_stim,
            reported_syllable=reported_syllable or "---",
            response_key=response_key.upper() if response_key else "---",
        )
    )
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="feedback",
        deadline_s=_deadline_s(feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=trial_spec.condition,
        task_factors={
            "stage": "feedback",
            "condition": trial_spec.condition,
            "reported_syllable": reported_syllable,
            "timed_out": timed_out,
            "block_idx": block_idx_val,
        },
        stim_id=feedback_stim,
    )
    feedback.show(
        duration=feedback_duration,
        onset_trigger=settings.triggers.get(feedback_onset),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=_deadline_s(iti_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=trial_spec.condition,
        task_factors={"stage": "inter_trial_interval", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    rt = decision.get_state("rt", None)
    key_press = decision.get_state("key_press", None)

    trial_data["decision_response"] = response_key
    trial_data["decision_rt"] = float(rt) if isinstance(rt, (int, float)) else None
    trial_data["decision_key_press"] = bool(key_press) if key_press is not None else not timed_out
    trial_data["decision_timed_out"] = bool(timed_out)
    trial_data["reported_syllable"] = reported_syllable or "none"
    trial_data["matches_expected"] = bool((not timed_out) and (reported_syllable == trial_spec.expected_percept))
    trial_data["fusion_da"] = bool(trial_spec.condition == "incongruent" and reported_syllable == "da")

    controller.record_trial(trial_data)

    return trial_data