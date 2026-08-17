import hashlib
from pathlib import Path

import pytest

from app.db import init_db
from app.schemas.asset import AssetMetadata, AssetType
from app.schemas.production_request import ProductionRequest
from app.services.asset_registry import register_asset
from app.services.canonical_loader import load_manifest
from app.services.daily_reference_prep import register_face_masked_derivative
from app.services.generation_planner import build_generation_plan
from app.services.prompt_validation import PromptTooLongError

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def conn(tmp_path):
    return init_db(tmp_path / "studio.db")


@pytest.fixture()
def manifest():
    return load_manifest(PROJECT_ROOT / "canonical" / "manifest.yaml")


def _register_real_masters_and_masked_daily(conn, tmp_path):
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


def test_build_generation_plan_end_to_end_with_real_data(conn, manifest, tmp_path):
    _register_real_masters_and_masked_daily(conn, tmp_path)

    request = ProductionRequest(
        character_id="yeoreum", lane="natural_mirror", daily_reference_id="DAILY_YEOREUM_20260815_001"
    )
    plan = build_generation_plan(manifest, request, conn, base_dir=str(PROJECT_ROOT))

    real_prompt_text = (
        PROJECT_ROOT / "canonical" / "presets" / "natural_mirror" / "NAT_v1.4.3_LOCKED_PROMPT.txt"
    ).read_text(encoding="utf-8")
    assert plan.prompt == real_prompt_text
    assert plan.prompt_hash == hashlib.sha256(real_prompt_text.encode("utf-8")).hexdigest()
    assert plan.prompt_length < 3000
    assert plan.provider == "higgsfield"
    assert plan.model == "seedream_4_5"

    assert set(plan.references.keys()) == {"image1", "image2", "image3", "image4"}
    assert plan.references["image1"].asset_id == "FACE_YEOREUM_V1"
    assert plan.references["image2"].asset_id == "CHARACTER_YEOREUM_V1"
    assert plan.references["image3"].asset_id == "BODY_YEOREUM_V1"
    assert plan.references["image4"].asset_id == "DAILY_YEOREUM_20260815_001_MASKED"

    assert "identity" in plan.qc_targets


def test_build_generation_plan_stops_on_over_length_prompt(conn, manifest, tmp_path):
    _register_real_masters_and_masked_daily(conn, tmp_path)

    # Point manifest at an over-length prompt snapshot instead of the real one. An
    # absolute path here resolves correctly regardless of base_dir (pathlib: joining
    # base_dir with an absolute path yields the absolute path unchanged).
    oversized = tmp_path / "oversized_prompt.txt"
    oversized.write_text("x" * 3500, encoding="utf-8")

    from app.schemas.manifest import ManifestPresetEntry

    manifest.presets["NAT_v1.4.3"] = ManifestPresetEntry(
        status="locked",
        prompt=str(oversized),
        metadata="canonical/presets/natural_mirror/preset.yaml",
    )

    request = ProductionRequest(
        character_id="yeoreum", lane="natural_mirror", daily_reference_id="DAILY_YEOREUM_20260815_001"
    )

    with pytest.raises(PromptTooLongError):
        build_generation_plan(manifest, request, conn, base_dir=str(PROJECT_ROOT))
