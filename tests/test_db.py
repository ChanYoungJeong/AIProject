import sqlite3

from app.db import init_db


def test_init_db_creates_all_core_tables(tmp_path):
    db_path = tmp_path / "studio.db"
    conn = init_db(db_path)
    tables = {
        row["name"]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    conn.close()
    assert {"assets", "characters", "lanes", "presets"} <= tables


def test_init_db_is_idempotent_and_preserves_data(tmp_path):
    db_path = tmp_path / "studio.db"
    conn = init_db(db_path)
    conn.execute(
        "INSERT INTO assets (asset_id, file_path, asset_type) VALUES (?, ?, ?)",
        ("A1", "assets/x.png", "FACE_ID_MASTER"),
    )
    conn.commit()
    conn.close()

    conn2 = init_db(db_path)
    row = conn2.execute("SELECT * FROM assets WHERE asset_id = ?", ("A1",)).fetchone()
    conn2.close()
    assert row is not None
    assert row["file_path"] == "assets/x.png"


def test_init_db_adds_support_columns_onto_an_ultra_legacy_db(tmp_path):
    """Simulates a real DB created before support_category/support_status/
    functional_role existed at all (phase 1/2's original database/studio.db),
    proving init_db adds them without touching existing rows."""
    db_path = tmp_path / "legacy_studio.db"
    legacy_conn = sqlite3.connect(db_path)
    legacy_conn.execute(
        """
        CREATE TABLE assets (
            asset_id TEXT PRIMARY KEY,
            file_path TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            approved INTEGER NOT NULL DEFAULT 0,
            canonical INTEGER NOT NULL DEFAULT 0,
            locked INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    legacy_conn.execute(
        "INSERT INTO assets (asset_id, file_path, asset_type) VALUES (?, ?, ?)",
        ("FACE_YEOREUM_V1", "assets/face.jpg", "FACE_ID_MASTER"),
    )
    legacy_conn.commit()
    legacy_conn.close()

    conn = init_db(db_path)
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(assets)").fetchall()}
    assert {"support_category", "support_status", "functional_role"} <= columns

    row = conn.execute("SELECT * FROM assets WHERE asset_id = ?", ("FACE_YEOREUM_V1",)).fetchone()
    conn.close()
    assert row["file_path"] == "assets/face.jpg"  # pre-existing row untouched
    assert row["support_category"] is None  # new column, no data lost or invented


def test_init_db_renames_face_package_columns_and_preserves_data(tmp_path):
    """Simulates the real database/studio.db as it existed right after the Face
    Package import (face_package_category/face_package_status columns, populated
    with real values), proving init_db renames them to support_category/
    support_status without losing the existing data."""
    db_path = tmp_path / "pre_rename_studio.db"
    legacy_conn = sqlite3.connect(db_path)
    legacy_conn.execute(
        """
        CREATE TABLE assets (
            asset_id TEXT PRIMARY KEY,
            file_path TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            approved INTEGER NOT NULL DEFAULT 0,
            canonical INTEGER NOT NULL DEFAULT 0,
            locked INTEGER NOT NULL DEFAULT 0,
            face_package_category TEXT,
            face_package_status TEXT,
            functional_role TEXT
        )
        """
    )
    legacy_conn.execute(
        """
        INSERT INTO assets
            (asset_id, file_path, asset_type, face_package_category, face_package_status, functional_role)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "YR_FACE_20_TINY_SMILE",
            "assets/face_package/tiny_smile.jpg",
            "FACE_PACKAGE_CANDIDATE",
            "EXPRESSION_SUPPORT",
            "LIBRARY_APPROVED",
            "TINY_SMILE",
        ),
    )
    legacy_conn.commit()
    legacy_conn.close()

    conn = init_db(db_path)
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(assets)").fetchall()}
    assert "support_category" in columns and "support_status" in columns
    assert "face_package_category" not in columns and "face_package_status" not in columns

    row = conn.execute(
        "SELECT * FROM assets WHERE asset_id = ?", ("YR_FACE_20_TINY_SMILE",)
    ).fetchone()
    conn.close()
    assert row["support_category"] == "EXPRESSION_SUPPORT"  # renamed, value preserved
    assert row["support_status"] == "LIBRARY_APPROVED"
    assert row["functional_role"] == "TINY_SMILE"
