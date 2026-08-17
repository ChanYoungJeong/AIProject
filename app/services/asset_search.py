"""Architecture Sec.46 item 05 (search half). Filters by core metadata fields
(Sec.7). Computed similarity scoring (Sec.10) is a later, separate concern."""
import sqlite3

from app.schemas.asset import AssetMetadata
from app.services._asset_row import ASSET_COLUMNS, row_to_asset

_FILTERABLE_COLUMNS = set(ASSET_COLUMNS)


def search_assets(conn: sqlite3.Connection, **filters) -> list[AssetMetadata]:
    unknown = set(filters) - _FILTERABLE_COLUMNS
    if unknown:
        raise ValueError(f"unknown asset filter field(s): {sorted(unknown)}")

    params: dict = {}
    where_clauses = []
    for col, value in filters.items():
        if col == "asset_type" and hasattr(value, "value"):
            value = value.value
        if isinstance(value, bool):
            value = int(value)
        where_clauses.append(f"{col} = :{col}")
        params[col] = value

    query = "SELECT * FROM assets"
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    rows = conn.execute(query, params).fetchall()
    return [row_to_asset(row) for row in rows]
