"""SQLite DDL for the Studio database (Architecture Sec.27).

Scoped to what Sec.46 items 05/06 need right now: assets (full metadata, Sec.7) plus
thin characters/lanes/presets search indexes populated from the canonical/*.yaml files
by app.services.canonical_loader. The canonical files remain the source of truth —
these tables only exist so Claude/services don't have to re-parse YAML on every query.

prompts/experiments/qc/feedback/memory tables (also listed in Sec.27) back later
Sec.46 items (12-16) and are intentionally not created yet.
"""

SCHEMA_DDL = """
CREATE TABLE IF NOT EXISTS assets (
    asset_id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    asset_type TEXT NOT NULL,

    character_id TEXT,
    lane TEXT,

    shot_type TEXT,
    view_angle TEXT,
    pose_type TEXT,
    camera_angle TEXT,
    camera_distance TEXT,
    body_visibility TEXT,

    environment TEXT,
    lighting TEXT,
    mood TEXT,
    content_pillar TEXT,

    outfit_id TEXT,

    source TEXT,
    created_at TEXT,
    derived_from TEXT,
    face_masked INTEGER NOT NULL DEFAULT 0,

    quality_score REAL,
    identity_score REAL,
    realism_score REAL,
    pose_readability_score REAL,

    approved INTEGER NOT NULL DEFAULT 0,
    canonical INTEGER NOT NULL DEFAULT 0,
    locked INTEGER NOT NULL DEFAULT 0,

    support_category TEXT,
    support_status TEXT,
    functional_role TEXT
);

CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    adult INTEGER NOT NULL,
    age INTEGER NOT NULL,
    core_persona TEXT NOT NULL,
    visual_formula TEXT NOT NULL,
    expression_range TEXT NOT NULL,
    primary_content_pillars TEXT NOT NULL,
    bible_path TEXT NOT NULL,
    profile_path TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lanes (
    lane TEXT PRIMARY KEY,
    canonical_preset TEXT NOT NULL,
    status TEXT NOT NULL,
    policy_path TEXT NOT NULL,
    model_provider TEXT NOT NULL,
    model_name TEXT NOT NULL,
    max_prompt_length INTEGER NOT NULL,
    reference_order TEXT NOT NULL,
    priority TEXT NOT NULL,
    pose_policy TEXT NOT NULL,
    face_policy TEXT NOT NULL,
    outfit_policy TEXT NOT NULL,
    refinement_policy TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS presets (
    preset_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    lane TEXT NOT NULL,
    model_provider TEXT NOT NULL,
    model_name TEXT NOT NULL,
    reference_profile TEXT NOT NULL,
    max_prompt_length INTEGER NOT NULL,
    prompt_snapshot_path TEXT,
    prompt_hash TEXT,
    modules TEXT NOT NULL,
    outfit_policy TEXT NOT NULL,
    revision_policy TEXT NOT NULL
);
"""
