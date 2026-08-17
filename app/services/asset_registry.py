"""Architecture Sec.46 item 05 (registration half) + Sec.7 / Sec.29 promotion rule.

register_asset never moves/copies files — it only records an already-placed file.
Registration always leaves approved/canonical/locked False; the only way to flip
those flags is the explicit set_approval_state call (Sec.7: "metadata should
describe the asset; it should not silently promote it").
"""
import sqlite3
from pathlib import Path

from app.schemas.asset import AssetMetadata
from app.services._asset_row import ASSET_COLUMNS, asset_to_params, row_to_asset


class AssetFileNotFoundError(FileNotFoundError):
    pass


class AssetNotRegisteredError(LookupError):
    pass


def register_asset(conn: sqlite3.Connection, metadata: AssetMetadata) -> str:
    if not Path(metadata.file_path).exists():
        raise AssetFileNotFoundError(
            f"cannot register asset {metadata.asset_id!r}: "
            f"file_path {metadata.file_path!r} does not exist on disk"
        )

    params = asset_to_params(metadata)
    columns = ", ".join(ASSET_COLUMNS)
    placeholders = ", ".join(f":{c}" for c in ASSET_COLUMNS)
    conn.execute(f"INSERT INTO assets ({columns}) VALUES ({placeholders})", params)
    conn.commit()
    return metadata.asset_id


def get_asset(conn: sqlite3.Connection, asset_id: str) -> AssetMetadata | None:
    row = conn.execute(
        "SELECT * FROM assets WHERE asset_id = ?", (asset_id,)
    ).fetchone()
    return row_to_asset(row) if row is not None else None


def set_approval_state(
    conn: sqlite3.Connection,
    asset_id: str,
    *,
    approved: bool | None = None,
    canonical: bool | None = None,
    locked: bool | None = None,
) -> AssetMetadata:
    updates = {
        k: int(v)
        for k, v in {"approved": approved, "canonical": canonical, "locked": locked}.items()
        if v is not None
    }
    if not updates:
        raise ValueError("set_approval_state requires at least one flag to change")

    set_clause = ", ".join(f"{col} = :{col}" for col in updates)
    cur = conn.execute(
        f"UPDATE assets SET {set_clause} WHERE asset_id = :asset_id",
        {**updates, "asset_id": asset_id},
    )
    if cur.rowcount == 0:
        raise AssetNotRegisteredError(f"no registered asset with asset_id {asset_id!r}")
    conn.commit()

    updated = get_asset(conn, asset_id)
    assert updated is not None
    return updated
