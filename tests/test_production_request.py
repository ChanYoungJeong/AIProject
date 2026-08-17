import pytest
from pydantic import ValidationError

from app.schemas import ProductionRequest


def test_defaults_match_architecture_example():
    request = ProductionRequest(character_id="yeoreum", lane="natural_mirror")
    assert request.outfit_mode == "inherit"
    assert request.preset_id == "auto"
    assert request.daily_reference_id is None
    assert request.identity_priority == "maximum"
    assert request.realism_priority == "high"
    assert request.pose_change == "low"
    assert request.generation_provider == "higgsfield"
    assert request.generation_mode == "manual_unlimited"
    assert request.requested_output_count is None
    assert request.visual_reasoning_mode == "manual_external"
    assert request.auto_external_vision is False
    assert request.allow_duplicate_visual_review is False


def test_unknown_field_rejected():
    with pytest.raises(ValidationError):
        ProductionRequest(character_id="yeoreum", lane="natural_mirror", not_a_real_field=1)
