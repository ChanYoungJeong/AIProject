import pytest

from app.db import init_db
from app.schemas.asset import AssetMetadata, AssetType
from app.services.asset_registry import register_asset
from app.services.asset_search import search_assets


@pytest.fixture()
def conn(tmp_path):
    return init_db(tmp_path / "studio.db")


def _register(conn, tmp_path, asset_id, **overrides):
    file_path = tmp_path / f"{asset_id}.png"
    file_path.write_bytes(b"fake-image-bytes")
    kwargs = dict(asset_id=asset_id, file_path=str(file_path), asset_type=AssetType.FACE_ID_MASTER)
    kwargs.update(overrides)
    register_asset(conn, AssetMetadata(**kwargs))


def test_search_by_type_and_character(conn, tmp_path):
    _register(conn, tmp_path, "A1", character_id="yeoreum", asset_type=AssetType.FACE_ID_MASTER)
    _register(conn, tmp_path, "A2", character_id="yeoreum", asset_type=AssetType.BODY_MASTER)
    _register(conn, tmp_path, "A3", character_id="someone_else", asset_type=AssetType.FACE_ID_MASTER)

    results = search_assets(conn, asset_type=AssetType.FACE_ID_MASTER, character_id="yeoreum")
    assert {r.asset_id for r in results} == {"A1"}


def test_search_no_filters_returns_all(conn, tmp_path):
    _register(conn, tmp_path, "A1")
    _register(conn, tmp_path, "A2")
    results = search_assets(conn)
    assert {r.asset_id for r in results} == {"A1", "A2"}


def test_search_unknown_filter_field_raises(conn):
    with pytest.raises(ValueError):
        search_assets(conn, not_a_real_field="x")
