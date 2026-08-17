from pathlib import Path

import pytest

from app.db import init_db
from app.schemas.asset import AssetMetadata, AssetType
from app.schemas.production_request import ProductionRequest
from app.services.asset_registry import register_asset
from app.services.canonical_loader import load_manifest
from app.services.daily_reference_prep import register_face_masked_derivative
from app.services.reference_selection import (
    GenericReferencePlanningNotImplementedError,
    MissingFaceMaskedDerivativeError,
    resolve_reference_plan,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _register_real_masters_and_daily(conn):
    """Mirrors the real registration done for database/studio.db, but into an
    isolated temp DB, using the real image files already on disk."""
    base = PROJECT_ROOT / "assets" / "characters" / "yeoreum" / "masters"
    register_asset(conn, AssetMetadata(
        asset_id="FACE_YEOREUM_V1", file_path=str(base / "face_id" / "01_FACE_ID_MASTER.jpg"),
        asset_type=AssetType.FACE_ID_MASTER, character_id="yeoreum", canonical=True, approved=True,
    ))
    register_asset(conn, AssetMetadata(
        asset_id="CHARACTER_YEOREUM_V1", file_path=str(base / "character" / "01_CHARACTER_MASTER.jpg"),
        asset_type=AssetType.CHARACTER_MASTER, character_id="yeoreum", canonical=True, approved=True,
    ))
    register_asset(conn, AssetMetadata(
        asset_id="BODY_YEOREUM_V1", file_path=str(base / "body" / "02_BODY_MASTER.jpg"),
        asset_type=AssetType.BODY_MASTER, character_id="yeoreum", canonical=True, approved=True,
    ))
    daily_path = PROJECT_ROOT / "assets" / "daily" / "raw" / "DAILY_REF_A_NATURAL_MIRROR_SELFIE.jpg"
    register_asset(conn, AssetMetadata(
        asset_id="DAILY_YEOREUM_20260815_001", file_path=str(daily_path),
        asset_type=AssetType.DAILY_REFERENCE, character_id="yeoreum", lane="natural_mirror",
    ))


@pytest.fixture()
def conn(tmp_path):
    return init_db(tmp_path / "studio.db")


@pytest.fixture()
def manifest():
    return load_manifest(PROJECT_ROOT / "canonical" / "manifest.yaml")


def test_missing_masked_derivative_stops_with_clear_error(conn, manifest):
    _register_real_masters_and_daily(conn)
    request = ProductionRequest(
        character_id="yeoreum", lane="natural_mirror", daily_reference_id="DAILY_YEOREUM_20260815_001"
    )
    with pytest.raises(MissingFaceMaskedDerivativeError):
        resolve_reference_plan(manifest, conn, request, base_dir=str(PROJECT_ROOT))


def test_resolves_real_masters_and_masked_derivative(conn, manifest, tmp_path):
    _register_real_masters_and_daily(conn)

    masked_path = tmp_path / "daily_masked.jpg"
    masked_path.write_bytes(b"synthetic-masked-bytes")  # pixel content irrelevant to registration
    register_face_masked_derivative(
        conn,
        raw_asset_id="DAILY_YEOREUM_20260815_001",
        derived_asset_id="DAILY_YEOREUM_20260815_001_MASKED",
        derived_file_path=str(masked_path),
        character_id="yeoreum",
        lane="natural_mirror",
    )

    request = ProductionRequest(
        character_id="yeoreum", lane="natural_mirror", daily_reference_id="DAILY_YEOREUM_20260815_001"
    )
    slots = resolve_reference_plan(manifest, conn, request, base_dir=str(PROJECT_ROOT))

    assert slots["image1"].asset_id == "FACE_YEOREUM_V1"
    assert slots["image1"].role == "FACE_ID_MASTER"
    assert slots["image2"].asset_id == "CHARACTER_YEOREUM_V1"
    assert slots["image3"].asset_id == "BODY_YEOREUM_V1"
    assert slots["image4"].asset_id == "DAILY_YEOREUM_20260815_001_MASKED"
    assert slots["image4"].role == "DAILY_REFERENCE_FACE_MASKED"


def test_face_package_candidates_never_get_picked_as_the_face_master(conn, manifest, tmp_path):
    """Regression: registering Face Package support images (asset_type=
    FACE_PACKAGE_CANDIDATE) for the same character must never change which asset
    resolve_reference_plan picks for image1 — proves the "never auto-substitute"
    rule holds structurally, not just by convention in a doc."""
    _register_real_masters_and_daily(conn)

    face_package_dir = PROJECT_ROOT / "assets" / "characters" / "yeoreum" / "face_package"
    candidates = [
        ("YR_FACE_11_3Q_NEUTRAL_VIEWER_LEFT", "10_library_core_approved"),
        ("YR_FACE_20_TINY_SMILE", "20_library_expression_approved"),
        ("YR_FACE_30_OPPOSITE_3Q_GENERATED_REVIEW", "30_experimental_not_for_production"),
    ]
    for asset_id, subfolder in candidates:
        candidate_path = face_package_dir / subfolder
        found = list(candidate_path.glob(f"{asset_id}.*")) if candidate_path.exists() else []
        file_path = found[0] if found else tmp_path / f"{asset_id}.jpg"
        if not found:
            file_path.write_bytes(b"placeholder-face-package-bytes")
        register_asset(conn, AssetMetadata(
            asset_id=asset_id,
            file_path=str(file_path),
            asset_type=AssetType.FACE_PACKAGE_CANDIDATE,
            character_id="yeoreum",
            support_category="CORE_VIEW",
            support_status="LIBRARY_APPROVED",
            functional_role="TEST_ROLE",
        ))

    masked_path = tmp_path / "daily_masked.jpg"
    masked_path.write_bytes(b"synthetic-masked-bytes")
    register_face_masked_derivative(
        conn,
        raw_asset_id="DAILY_YEOREUM_20260815_001",
        derived_asset_id="DAILY_YEOREUM_20260815_001_MASKED",
        derived_file_path=str(masked_path),
        character_id="yeoreum",
        lane="natural_mirror",
    )

    request = ProductionRequest(
        character_id="yeoreum", lane="natural_mirror", daily_reference_id="DAILY_YEOREUM_20260815_001"
    )
    slots = resolve_reference_plan(manifest, conn, request, base_dir=str(PROJECT_ROOT))

    assert slots["image1"].asset_id == "FACE_YEOREUM_V1"  # unchanged despite 3 more "face" rows


def test_body_master_candidate_never_gets_picked_over_the_canonical_body(conn, manifest, tmp_path):
    """Regression: a BODY_MASTER candidate (same asset_type as the real canonical
    master, only canonical=False) must never be selected by resolve_reference_plan —
    the one case where a support/candidate asset shares asset_type with the real
    master, so the canonical=True filter is what has to hold, not just asset_type."""
    _register_real_masters_and_daily(conn)

    candidate_path = tmp_path / "body_v2_candidate.png"
    candidate_path.write_bytes(b"placeholder-body-candidate-bytes")
    register_asset(conn, AssetMetadata(
        asset_id="BODY_YEOREUM_V2_CANDIDATE",
        file_path=str(candidate_path),
        asset_type=AssetType.BODY_MASTER,
        character_id="yeoreum",
        approved=True,
        canonical=False,
    ))

    masked_path = tmp_path / "daily_masked.jpg"
    masked_path.write_bytes(b"synthetic-masked-bytes")
    register_face_masked_derivative(
        conn,
        raw_asset_id="DAILY_YEOREUM_20260815_001",
        derived_asset_id="DAILY_YEOREUM_20260815_001_MASKED",
        derived_file_path=str(masked_path),
        character_id="yeoreum",
        lane="natural_mirror",
    )

    request = ProductionRequest(
        character_id="yeoreum", lane="natural_mirror", daily_reference_id="DAILY_YEOREUM_20260815_001"
    )
    slots = resolve_reference_plan(manifest, conn, request, base_dir=str(PROJECT_ROOT))

    assert slots["image3"].asset_id == "BODY_YEOREUM_V1"  # not the candidate


def test_generic_lane_not_implemented(conn, tmp_path):
    unvalidated_manifest_dir = tmp_path / "canonical"
    (unvalidated_manifest_dir / "presets" / "future_lane").mkdir(parents=True)

    lane_policy_path = unvalidated_manifest_dir / "presets" / "future_lane" / "lane_policy.yaml"
    lane_policy_path.write_text(
        """
lane_policy:
  lane: future_lane
  canonical_preset: FUTURE_v0.1
  status: working
  model: {provider: higgsfield, model: seedream_4_5, max_prompt_length: 3000}
  reference_order: {image1: FACE_ID_MASTER, image2: CHARACTER_MASTER, image3: BODY_MASTER}
  priority: [face_identity]
  pose_policy: {reference_led: true, invent_new_pose: false}
  face_policy: {preserve_identity: true, copy_master_expression: false, adapt_gaze_head_angle_perspective: true}
  outfit_policy: preset_defined
  refinement_policy: {mandatory_second_pass: false}
""",
        encoding="utf-8",
    )

    from app.schemas.manifest import Manifest, ManifestCharacterEntry, ManifestLaneEntry, ManifestPresetEntry

    (unvalidated_manifest_dir / "characters" / "yeoreum").mkdir(parents=True)
    (unvalidated_manifest_dir / "characters" / "yeoreum" / "bible.txt").write_text("x", encoding="utf-8")
    (unvalidated_manifest_dir / "characters" / "yeoreum" / "profile.yaml").write_text(
        "id: yeoreum\ndisplay_name: X\nadult: true\nage: 19\ncore_persona: []\n"
        "visual_formula: []\nexpression_range: []\nprimary_content_pillars: {}\n",
        encoding="utf-8",
    )

    manifest = Manifest(
        project="Test",
        workflow_master="canonical/characters/yeoreum/bible.txt",
        characters={
            "yeoreum": ManifestCharacterEntry(
                bible="canonical/characters/yeoreum/bible.txt",
                profile="canonical/characters/yeoreum/profile.yaml",
            )
        },
        lanes={
            "future_lane": ManifestLaneEntry(
                preset="FUTURE_v0.1", policy="canonical/presets/future_lane/lane_policy.yaml"
            )
        },
        presets={},
    )

    request = ProductionRequest(character_id="yeoreum", lane="future_lane")
    with pytest.raises(GenericReferencePlanningNotImplementedError):
        resolve_reference_plan(manifest, conn, request, base_dir=str(tmp_path))
