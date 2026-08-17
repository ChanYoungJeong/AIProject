import sqlite3
from pathlib import Path

from app.db.schema import SCHEMA_DDL

DEFAULT_DB_PATH = "database/studio.db"

# Columns added to `assets` after the table already existed in real databases.
# CREATE TABLE IF NOT EXISTS (in SCHEMA_DDL) only helps a brand-new DB file —
# an existing one needs an explicit, idempotent ALTER TABLE for each addition.
_ASSETS_ADDED_COLUMNS = {
    "support_category": "TEXT",
    "support_status": "TEXT",
    "functional_role": "TEXT",
}

# Columns renamed after real data already existed under the old name (Face Package
# was the first user of these fields; renamed to a generic name once Body Master
# Package v2 needed the same concept). (old_name, new_name) pairs, applied with
# RENAME COLUMN so existing values survive.
_ASSETS_RENAMED_COLUMNS = [
    ("face_package_category", "support_category"),
    ("face_package_status", "support_status"),
]


def get_connection(path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _migrate_assets_columns(conn: sqlite3.Connection) -> None:
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(assets)").fetchall()}

    for old_name, new_name in _ASSETS_RENAMED_COLUMNS:
        if old_name in existing and new_name not in existing:
            conn.execute(f"ALTER TABLE assets RENAME COLUMN {old_name} TO {new_name}")
            existing.discard(old_name)
            existing.add(new_name)

    for column, sql_type in _ASSETS_ADDED_COLUMNS.items():
        if column not in existing:
            conn.execute(f"ALTER TABLE assets ADD COLUMN {column} {sql_type}")
            existing.add(column)


def init_db(path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Create the Studio DB schema if it doesn't already exist. Idempotent — safe to
    call on an existing DB; never drops or truncates existing tables/data. Also
    applies any pending additive/rename column migrations to an already-existing DB."""
    conn = get_connection(path)
    conn.executescript(SCHEMA_DDL)
    _migrate_assets_columns(conn)
    conn.commit()
    return conn
