import pytest

from app.db import init_db
from app.schemas.asset import AssetMetadata, AssetType
from app.services.asset_registry import register_asset
from app.services.daily_reference_prep import (
    RawAssetNotRegisteredError,
    find_face_masked_derivative,
    register_face_masked_derivative,
)


@pytest.fixture()
def conn(tmp_path):
    return init_db(tmp_path / "studio.db")


def _register_raw_daily(conn, tmp_path, asset_id="DAILY_RAW_1"):
    file_path = tmp_path / f"{asset_id}.png"
    file_path.write_bytes(b"raw-daily-bytes")
    register_asset(
        conn,
        AssetMetadata(
            asset_id=asset_id,
            file_path=str(file_path),
            asset_type=AssetType.DAILY_REFERENCE,
            character_id="yeoreum",
            lane="natural_mirror",
        ),
    )
    return asset_id


def test_find_derivative_returns_none_when_absent(conn, tmp_path):
    raw_id = _register_raw_daily(conn, tmp_path)
    assert find_face_masked_derivative(conn, raw_id) is None


def test_register_derivative_round_trip(conn, tmp_path):
    raw_id = _register_raw_daily(conn, tmp_path)
    derived_path = tmp_path / "DAILY_RAW_1_MASKED.png"
    derived_path.write_bytes(b"masked-bytes")

    derived = register_face_masked_derivative(
        conn,
        raw_asset_id=raw_id,
        derived_asset_id="DAILY_RAW_1_MASKED",
        derived_file_path=str(derived_path),
        character_id="yeoreum",
        lane="natural_mirror",
    )
    assert derived.face_masked is True
    assert derived.derived_from == raw_id

    found = find_face_masked_derivative(conn, raw_id)
    assert found is not None
    assert found.asset_id == "DAILY_RAW_1_MASKED"


def test_register_derivative_unknown_raw_asset_fails(conn, tmp_path):
    derived_path = tmp_path / "MASKED.png"
    derived_path.write_bytes(b"masked-bytes")
    with pytest.raises(RawAssetNotRegisteredError):
        register_face_masked_derivative(
            conn,
            raw_asset_id="NOT_REGISTERED",
            derived_asset_id="MASKED_1",
            derived_file_path=str(derived_path),
            character_id="yeoreum",
            lane="natural_mirror",
        )


def test_register_derivative_missing_file_fails(conn, tmp_path):
    raw_id = _register_raw_daily(conn, tmp_path)
    with pytest.raises(FileNotFoundError):
        register_face_masked_derivative(
            conn,
            raw_asset_id=raw_id,
            derived_asset_id="MASKED_MISSING_FILE",
            derived_file_path=str(tmp_path / "does_not_exist.png"),
            character_id="yeoreum",
            lane="natural_mirror",
        )
