from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class AssetType(str, Enum):
    """Architecture Sec.6 — primary image asset types."""

    FACE_ID_MASTER = "FACE_ID_MASTER"
    CHARACTER_MASTER = "CHARACTER_MASTER"
    BODY_MASTER = "BODY_MASTER"
    DAILY_REFERENCE = "DAILY_REFERENCE"
    OUTFIT_REFERENCE = "OUTFIT_REFERENCE"
    STYLE_REFERENCE = "STYLE_REFERENCE"
    ENVIRONMENT_REFERENCE = "ENVIRONMENT_REFERENCE"
    GENERATED_RESULT = "GENERATED_RESULT"
    APPROVED_RESULT = "APPROVED_RESULT"
    REJECTED_RESULT = "REJECTED_RESULT"
    # Not a Sec.6 master category — a non-production QC/support library asset
    # (e.g. Face Package candidates). Deliberately distinct from FACE_ID_MASTER so
    # reference_selection.py's master lookup can never select one by accident.
    FACE_PACKAGE_CANDIDATE = "FACE_PACKAGE_CANDIDATE"
    # Same idea for BODY_MASTER: core-view/pose QC evidence that is never itself a
    # production body master. A *candidate replacement* master (e.g. Body Master
    # Package v2's primary) still uses asset_type=BODY_MASTER with canonical=False —
    # only this support-evidence content gets the distinct type.
    BODY_MASTER_SUPPORT = "BODY_MASTER_SUPPORT"


class AssetMetadata(BaseModel):
    """Architecture Sec.7 — recommended core asset metadata.

    `approved` / `canonical` / `locked` default False: metadata describes an asset,
    it does not promote it (Sec.7 closing rule). Promotion is only ever an explicit
    call to app.services.asset_registry.set_approval_state.
    """

    model_config = ConfigDict(extra="forbid")

    asset_id: str
    file_path: str
    asset_type: AssetType

    character_id: str | None = None
    lane: str | None = None

    shot_type: str | None = None
    view_angle: str | None = None
    pose_type: str | None = None
    camera_angle: str | None = None
    camera_distance: str | None = None
    body_visibility: str | None = None

    environment: str | None = None
    lighting: str | None = None
    mood: str | None = None
    content_pillar: str | None = None

    outfit_id: str | None = None

    source: str | None = None
    created_at: datetime | None = None
    derived_from: str | None = None
    face_masked: bool = False

    quality_score: float | None = None
    identity_score: float | None = None
    realism_score: float | None = None
    pose_readability_score: float | None = None

    approved: bool = False
    canonical: bool = False
    locked: bool = False

    # Only meaningful for non-canonical support/candidate library assets (e.g.
    # FACE_PACKAGE_CANDIDATE, BODY_MASTER_SUPPORT). Free-text, not an enum: the
    # source package's own vocabulary (e.g. "CORE_VIEW / GAZE_SUPPORT") doesn't
    # always fit a fixed set, and real data shouldn't be rejected over a taxonomy
    # mismatch. Renamed from face_package_* once a second package (body) needed
    # the same fields — see app/db/connection.py's migration for the rename.
    support_category: str | None = None
    support_status: str | None = None
    functional_role: str | None = None
