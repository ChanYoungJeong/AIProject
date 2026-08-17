"""Architecture Sec.46 item 09 / Sec.51 — Daily Reference preparation.

Provenance-only: the face-masked derivative image itself is created externally
(no CV/face-detection dependency in this stack, Architecture Sec.40). This
module only registers an already-created derivative with correct provenance
and never overwrites or edits the raw reference file."""
import sqlite3

from app.schemas.asset import AssetMetadata, AssetType
from app.services.asset_registry import get_asset, register_asset
from app.services.asset_search import search_assets


class RawAssetNotRegisteredError(LookupError):
    pass


def register_face_masked_derivative(
    conn: sqlite3.Connection,
    *,
    raw_asset_id: str,
    derived_asset_id: str,
    derived_file_path: str,
    character_id: str,
    lane: str,
) -> AssetMetadata:
    raw = get_asset(conn, raw_asset_id)
    if raw is None:
        raise RawAssetNotRegisteredError(
            f"cannot prepare a derivative of {raw_asset_id!r}: it isn't registered"
        )

    derived = AssetMetadata(
        asset_id=derived_asset_id,
        file_path=derived_file_path,
        asset_type=AssetType.DAILY_REFERENCE,
        character_id=character_id,
        lane=lane,
        derived_from=raw_asset_id,
        face_masked=True,
    )
    register_asset(conn, derived)
    return derived


def find_face_masked_derivative(conn: sqlite3.Connection, raw_asset_id: str) -> AssetMetadata | None:
    matches = search_assets(
        conn,
        asset_type=AssetType.DAILY_REFERENCE,
        derived_from=raw_asset_id,
        face_masked=True,
    )
    return matches[0] if matches else None
