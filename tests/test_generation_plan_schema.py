import pytest
from pydantic import ValidationError

from app.schemas import GenerationPlan


def _valid_kwargs(**overrides):
    kwargs = dict(
        provider="higgsfield",
        model="seedream_4_5",
        generation_mode="manual_unlimited",
        references={
            "image1": {"asset_id": "FACE_YEOREUM_V1", "role": "FACE_ID_MASTER"},
            "image2": {"asset_id": "CHARACTER_YEOREUM_V1", "role": "CHARACTER_MASTER"},
        },
        prompt="a short prompt",
        prompt_length=14,
        prompt_hash="abc123",
        expected_behavior=["face_identity", "daily_pose_composition"],
        high_risk_points=["identity drift"],
        qc_targets=["identity", "pose"],
    )
    kwargs.update(overrides)
    return kwargs


def test_generation_plan_parses_valid_example():
    plan = GenerationPlan(**_valid_kwargs())
    assert plan.references["image1"].asset_id == "FACE_YEOREUM_V1"
    assert plan.references["image1"].role == "FACE_ID_MASTER"


def test_generation_plan_rejects_malformed_reference_slot():
    with pytest.raises(ValidationError):
        GenerationPlan(**_valid_kwargs(references={"image1": {"asset_id": "X"}}))
