"""Architecture Sec.46 items 10/12 — ties preset retrieval (item 06),
reference selection (items 08/11), and prompt validation (item 10) together
into a GenerationPlan (Sec.13). This is the Prompt Engine's output stage —
nothing here ever calls a generation provider (Sec.16 stays manual)."""
import sqlite3

from app.schemas.generation_plan import GenerationPlan
from app.schemas.manifest import Manifest
from app.schemas.production_request import ProductionRequest
from app.services.canonical_loader import UnknownLaneError, load_lane_policy, load_preset
from app.services.prompt_validation import validate_prompt_length
from app.services.reference_selection import resolve_reference_plan

# Architecture Sec.18 — standard QC dimension set, not invented per-plan.
DEFAULT_QC_TARGETS = [
    "identity",
    "body_proportions",
    "pose",
    "framing",
    "outfit",
    "anatomy_hands",
    "skin",
    "lighting",
    "camera_realism",
    "ai_artifacts",
]


def build_generation_plan(
    manifest: Manifest,
    request: ProductionRequest,
    conn: sqlite3.Connection,
    base_dir: str = ".",
) -> GenerationPlan:
    if request.lane not in manifest.lanes:
        raise UnknownLaneError(f"no lane {request.lane!r} in manifest")

    preset_id = request.preset_id
    if preset_id == "auto":
        preset_id = manifest.lanes[request.lane].preset

    # Locked preset + no requested change -> exact retrieval, never reconstruction (Sec.13).
    loaded_preset = load_preset(manifest, preset_id, base_dir)
    preset = loaded_preset.preset

    validate_prompt_length(loaded_preset.prompt_text, preset.max_prompt_length)

    references = resolve_reference_plan(manifest, conn, request, base_dir)

    lane_policy_priority = _load_lane_priority(manifest, request.lane, base_dir)

    return GenerationPlan(
        provider=preset.model.provider,
        model=preset.model.model,
        generation_mode=request.generation_mode,
        references=references,
        prompt=loaded_preset.prompt_text,
        prompt_length=len(loaded_preset.prompt_text),
        prompt_hash=loaded_preset.computed_prompt_hash,
        expected_behavior=lane_policy_priority,
        high_risk_points=lane_policy_priority[:3],
        qc_targets=DEFAULT_QC_TARGETS,
    )


def _load_lane_priority(manifest: Manifest, lane: str, base_dir: str) -> list[str]:
    return list(load_lane_policy(manifest, lane, base_dir).priority)
