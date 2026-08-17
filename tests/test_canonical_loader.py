from pathlib import Path

import pytest

from app.db import init_db
from app.services.canonical_loader import (
    MissingManifestError,
    load_character,
    load_lane_policy,
    load_manifest,
    load_preset,
    sync_index,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_missing_manifest_reports_clearly(tmp_path):
    with pytest.raises(MissingManifestError):
        load_manifest(tmp_path / "does_not_exist" / "manifest.yaml")


def test_load_real_manifest_and_lane_and_character():
    manifest = load_manifest(PROJECT_ROOT / "canonical" / "manifest.yaml")

    lane = load_lane_policy(manifest, "natural_mirror", base_dir=PROJECT_ROOT)
    assert lane.lane == "natural_mirror"
    assert lane.canonical_preset == "NAT_v1.4.3"
    assert lane.reference_order.image4 == "DAILY_REFERENCE_FACE_MASKED"

    character = load_character(manifest, "yeoreum", base_dir=PROJECT_ROOT)
    assert character.profile.display_name == "Han Yeoreum"
    assert character.profile.primary_content_pillars["home_just_outside"] == 45
    assert character.bible_is_placeholder is False  # real bible migrated from Project Sources
    assert "CHARACTER_BIBLE_YEOREUM_v1.1" in character.bible_text


def test_load_real_preset_flags_placeholder_prompt():
    manifest = load_manifest(PROJECT_ROOT / "canonical" / "manifest.yaml")
    loaded = load_preset(manifest, "NAT_v1.4.3", base_dir=PROJECT_ROOT)

    assert loaded.preset.status.value == "locked"
    assert loaded.prompt_is_placeholder is False  # real locked prompt migrated from Project Sources
    assert loaded.computed_prompt_hash
    assert loaded.stored_prompt_hash_matches is True  # preset.yaml's prompt_hash matches the real snapshot


def test_sync_index_populates_search_tables(tmp_path):
    manifest = load_manifest(PROJECT_ROOT / "canonical" / "manifest.yaml")
    conn = init_db(tmp_path / "studio.db")

    sync_index(conn, manifest, base_dir=PROJECT_ROOT)

    char_row = conn.execute("SELECT * FROM characters WHERE id = ?", ("yeoreum",)).fetchone()
    lane_row = conn.execute("SELECT * FROM lanes WHERE lane = ?", ("natural_mirror",)).fetchone()
    preset_row = conn.execute(
        "SELECT * FROM presets WHERE preset_id = ?", ("NAT_v1.4.3",)
    ).fetchone()

    assert char_row is not None and char_row["display_name"] == "Han Yeoreum"
    assert lane_row is not None and lane_row["canonical_preset"] == "NAT_v1.4.3"
    assert preset_row is not None and preset_row["status"] == "locked"


def test_sync_index_is_rerunnable_without_duplicating_rows(tmp_path):
    manifest = load_manifest(PROJECT_ROOT / "canonical" / "manifest.yaml")
    conn = init_db(tmp_path / "studio.db")

    sync_index(conn, manifest, base_dir=PROJECT_ROOT)
    sync_index(conn, manifest, base_dir=PROJECT_ROOT)  # run twice

    count = conn.execute("SELECT COUNT(*) AS c FROM presets").fetchone()["c"]
    assert count == 1
