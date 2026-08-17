from pydantic import BaseModel, ConfigDict

from app.schemas.common import CanonicalState


class LaneModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    max_prompt_length: int


class ReferenceOrder(BaseModel):
    """Role labels per reference slot (Architecture Sec.48). These are descriptive
    roles, not strictly app.schemas.asset.AssetType values — Sec.48 uses
    'DAILY_REFERENCE_FACE_MASKED', which is a derived-provenance label rather than
    a distinct asset_type (see Architecture Sec.6 closing note on derived assets)."""

    model_config = ConfigDict(extra="forbid")

    image1: str
    image2: str
    image3: str
    image4: str | None = None


class PosePolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_led: bool
    invent_new_pose: bool


class FacePolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preserve_identity: bool
    copy_master_expression: bool
    adapt_gaze_head_angle_perspective: bool


class RefinementPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mandatory_second_pass: bool


class LanePolicy(BaseModel):
    """Architecture Sec.48 — Canonical Natural / Mirror Integration Profile shape,
    generalized to any lane."""

    model_config = ConfigDict(extra="forbid")

    lane: str
    canonical_preset: str
    status: CanonicalState

    model: LaneModelConfig
    reference_order: ReferenceOrder
    priority: list[str]

    pose_policy: PosePolicy
    face_policy: FacePolicy
    outfit_policy: str
    refinement_policy: RefinementPolicy
