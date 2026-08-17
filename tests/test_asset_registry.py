import pytest

from app.db import init_db
from app.schemas.asset import AssetMetadata, AssetType
from app.services.asset_registry import (
    AssetFileNotFoundError,
    AssetNotRegisteredError,
    get_asset,
    register_asset,
    set_approval_state,
)


@pytest.fixture()
def conn(tmp_path):
    return init_db(tmp_path / "studio.db")


def _make_asset(tmp_path, asset_id="A1", **overrides):
    file_path = tmp_path / f"{asset_id}.png"
    file_path.write_bytes(b"fake-image-bytes")
    kwargs = dict(
        asset_id=asset_id,
        file_path=str(file_path),
        asset_type=AssetType.FACE_ID_MASTER,
        character_id="yeoreum",
    )
    kwargs.update(overrides)
    return AssetMetadata(**kwargs)


def test_register_with_missing_file_fails_clearly(conn, tmp_path):
    asset = AssetMetadata(
        asset_id="A_MISSING",
        file_path=str(tmp_path / "does_not_exist.png"),
        asset_type=AssetType.FACE_ID_MASTER,
    )
    with pytest.raises(AssetFileNotFoundError):
        register_asset(conn, asset)


def test_register_and_get_round_trip(conn, tmp_path):
    asset = _make_asset(tmp_path)
    register_asset(conn, asset)

    fetched = get_asset(conn, "A1")
    assert fetched is not None
    assert fetched.asset_id == "A1"
    assert fetched.asset_type == AssetType.FACE_ID_MASTER
    assert fetched.approved is False
    assert fetched.canonical is False
    assert fetched.locked is False


def test_set_approval_state_changes_only_targeted_flags(conn, tmp_path):
    asset = _make_asset(tmp_path)
    register_asset(conn, asset)

    updated = set_approval_state(conn, "A1", approved=True)
    assert updated.approved is True
    assert updated.canonical is False
    assert updated.locked is False

    updated2 = set_approval_state(conn, "A1", canonical=True)
    assert updated2.approved is True  # untouched by this call
    assert updated2.canonical is True
    assert updated2.locked is False


def test_set_approval_state_unknown_asset_raises(conn):
    with pytest.raises(AssetNotRegisteredError):
        set_approval_state(conn, "NOPE", approved=True)
