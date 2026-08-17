"""Shared row <-> AssetMetadata conversion for asset_registry / asset_search."""
import sqlite3
from datetime import datetime

from app.schemas.asset import AssetMetadata, AssetType

ASSET_COLUMNS = [
    "asset_id",
    "file_path",
    "asset_type",
    "character_id",
    "lane",
    "shot_type",
    "view_angle",
    "pose_type",
    "camera_angle",
    "camera_distance",
    "body_visibility",
    "environment",
    "lighting",
    "mood",
    "content_pillar",
    "outfit_id",
    "source",
    "created_at",
    "derived_from",
    "face_masked",
    "quality_score",
    "identity_score",
    "realism_score",
    "pose_readability_score",
    "approved",
    "canonical",
    "locked",
    "support_category",
    "support_status",
    "functional_role",
]

_BOOL_COLUMNS = {"face_masked", "approved", "canonical", "locked"}


def asset_to_params(metadata: AssetMetadata) -> dict:
    data = metadata.model_dump()
    data["asset_type"] = metadata.asset_type.value
    data["created_at"] = (
        metadata.created_at.isoformat() if metadata.created_at else None
    )
    for col in _BOOL_COLUMNS:
        data[col] = int(data[col])
    return {col: data[col] for col in ASSET_COLUMNS}


def row_to_asset(row: sqlite3.Row) -> AssetMetadata:
    data = dict(row)
    data["asset_type"] = AssetType(data["asset_type"])
    data["created_at"] = (
        datetime.fromisoformat(data["created_at"]) if data["created_at"] else None
    )
    for col in _BOOL_COLUMNS:
        data[col] = bool(data[col])
    return AssetMetadata(**data)
