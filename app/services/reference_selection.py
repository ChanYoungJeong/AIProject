"""Architecture Sec.46 items 08/11 — Reference Selection Engine, Production Mode
only (Sec.8.1). Optimization Audit Mode (Sec.8.2) is out of scope here.

Branch 1/2 (approved/locked lane policy declares exact reference roles/order)
are fully implemented, driven by the LanePolicy already built in item 02/06.
Branch 3 (generic planning for an unvalidated lane) is intentionally a clear
NotImplementedError rather than a fabricated scoring engine — see Sec.10:
"the exact numerical formula does not need to be finalized during MVP."
"""
import sqlite3

from app.schemas.asset import AssetType
from app.schemas.common import CanonicalState
from app.schemas.generation_plan import ReferenceSlot
from app.schemas.manifest import Manifest
from app.schemas.production_request import ProductionRequest
from app.services.asset_search import search_assets
from app.services.canonical_loader import UnknownLaneError, load_lane_policy
from app.services.daily_reference_prep import find_face_masked_derivative

MASTER_ROLE_TO_ASSET_TYPE = {
    "FACE_ID_MASTER": AssetType.FACE_ID_MASTER,
    "CHARACTER_MASTER": AssetType.CHARACTER_MASTER,
    "BODY_MASTER": AssetType.BODY_MASTER,
}


class GenericReferencePlanningNotImplementedError(NotImplementedError):
    pass


class AmbiguousOrMissingMasterError(LookupError):
    pass


class MissingDailyReferenceIdError(ValueError):
    pass


class MissingFaceMaskedDerivativeError(LookupError):
    pass


def resolve_reference_plan(
    manifest: Manifest,
    conn: sqlite3.Connection,
    request: ProductionRequest,
    base_dir: str = ".",
) -> dict[str, ReferenceSlot]:
    if request.lane not in manifest.lanes:
        raise UnknownLaneError(f"no lane {request.lane!r} in manifest")

    lane_policy = load_lane_policy(manifest, request.lane, base_dir)

    if lane_policy.status not in (CanonicalState.LOCKED, CanonicalState.APPROVED):
        raise GenericReferencePlanningNotImplementedError(
            f"lane {request.lane!r} has no locked/approved reference profile "
            f"(status={lane_policy.status.value}); generic reference-scoring "
            "planning (Architecture Sec.8.1 branch 3, Sec.10) isn't implemented yet"
        )

    role_by_slot = lane_policy.reference_order.model_dump()
    slots: dict[str, ReferenceSlot] = {}

    for image_key, role in role_by_slot.items():
        if role is None:
            continue

        if role in MASTER_ROLE_TO_ASSET_TYPE:
            matches = search_assets(
                conn,
                character_id=request.character_id,
                asset_type=MASTER_ROLE_TO_ASSET_TYPE[role],
                canonical=True,
            )
            if len(matches) != 1:
                raise AmbiguousOrMissingMasterError(
                    f"expected exactly one canonical {role} for character "
                    f"{request.character_id!r}, found {len(matches)}"
                )
            slots[image_key] = ReferenceSlot(asset_id=matches[0].asset_id, role=role)

        elif role == "DAILY_REFERENCE_FACE_MASKED":
            if not request.daily_reference_id:
                raise MissingDailyReferenceIdError(
                    f"lane {request.lane!r} requires request.daily_reference_id "
                    f"to resolve the {image_key} slot"
                )
            derived = find_face_masked_derivative(conn, request.daily_reference_id)
            if derived is None:
                raise MissingFaceMaskedDerivativeError(
                    f"no registered face-masked derivative for daily reference "
                    f"{request.daily_reference_id!r} — create and register one "
                    "before building a plan (Architecture Sec.51); the raw/"
                    "unmasked reference is never used as a silent fallback"
                )
            slots[image_key] = ReferenceSlot(asset_id=derived.asset_id, role=role)

        else:
            raise ValueError(f"unknown reference role {role!r} in lane policy for {image_key}")

    return slots
