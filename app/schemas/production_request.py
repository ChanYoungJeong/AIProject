from pydantic import BaseModel, ConfigDict


class ProductionRequest(BaseModel):
    """Architecture Sec.5 — normalized production request. Defaults mirror the
    doc's example; missing-field resolution beyond canonical sources (memory,
    successful recipes) is deferred to later items (15/16)."""

    model_config = ConfigDict(extra="forbid")

    character_id: str
    lane: str
    content_type: str | None = None
    framing: str | None = None
    environment: str | None = None
    mood: str | None = None
    outfit_mode: str = "inherit"
    preset_id: str = "auto"
    daily_reference_id: str | None = None
    daily_reference_face_policy: str = "auto"
    identity_priority: str = "maximum"
    realism_priority: str = "high"
    pose_change: str = "low"
    generation_provider: str = "higgsfield"
    generation_mode: str = "manual_unlimited"
    generation_model: str = "auto"
    requested_output_count: int | None = None

    visual_reasoning_mode: str = "manual_external"
    auto_external_vision: bool = False
    allow_duplicate_visual_review: bool = False
