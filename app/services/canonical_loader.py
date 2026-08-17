"""Architecture Sec.46 item 06 — Canonical source loader.

Resolves canonical/manifest.yaml and the character/lane/preset sources it points
to. Files stay authoritative; sync_index() refreshes the characters/lanes/presets
SQLite tables (Sec.27, Sec.04) as a queryable mirror.

Missing critical sources fail with a clearly-named, documented exception rather
than an unexplained crash (Architecture Sec.30: "if a critical source is missing,
stop... and report"). Placeholder canonical text (see PLACEHOLDER_MARKER) is
surfaced via *_is_placeholder flags rather than silently treated as approved.
"""
import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import yaml

from app.schemas.character import CharacterProfile
from app.schemas.lane_policy import LanePolicy
from app.schemas.manifest import Manifest
from app.schemas.preset import Preset

PLACEHOLDER_MARKER = "[[PLACEHOLDER"
DEFAULT_MANIFEST_PATH = "canonical/manifest.yaml"


class MissingManifestError(FileNotFoundError):
    pass


class MissingCanonicalSourceError(FileNotFoundError):
    pass


class UnknownCharacterError(LookupError):
    pass


class UnknownLaneError(LookupError):
    pass


class UnknownPresetError(LookupError):
    pass


@dataclass
class LoadedCharacter:
    profile: CharacterProfile
    bible_path: str
    bible_text: str
    bible_is_placeholder: bool


@dataclass
class LoadedPreset:
    preset: Preset
    prompt_text: str
    prompt_is_placeholder: bool
    computed_prompt_hash: str
    stored_prompt_hash_matches: bool | None  # None if preset.yaml has no stored hash yet


def _resolve(base_dir: Path, relative_path: str) -> Path:
    return base_dir / relative_path


def _read_text(base_dir: Path, relative_path: str, *, what: str) -> str:
    path = _resolve(base_dir, relative_path)
    if not path.exists():
        raise MissingCanonicalSourceError(f"{what} not found: {path}")
    return path.read_text(encoding="utf-8")


def _read_yaml(base_dir: Path, relative_path: str, *, what: str) -> dict:
    text = _read_text(base_dir, relative_path, what=what)
    return yaml.safe_load(text) or {}


def load_manifest(path: str | Path = DEFAULT_MANIFEST_PATH) -> Manifest:
    path = Path(path)
    if not path.exists():
        raise MissingManifestError(
            f"canonical manifest not found at {path} — resolve it before any "
            "production request (Architecture Sec.50, Sec.52)"
        )
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return Manifest(**data)


def load_character(
    manifest: Manifest, character_id: str, base_dir: str | Path = "."
) -> LoadedCharacter:
    base_dir = Path(base_dir)
    entry = manifest.characters.get(character_id)
    if entry is None:
        raise UnknownCharacterError(f"no character {character_id!r} in manifest")

    profile_data = _read_yaml(base_dir, entry.profile, what=f"character profile for {character_id!r}")
    profile = CharacterProfile(**profile_data.get("character", profile_data))

    bible_text = _read_text(base_dir, entry.bible, what=f"character bible for {character_id!r}")
    return LoadedCharacter(
        profile=profile,
        bible_path=entry.bible,
        bible_text=bible_text,
        bible_is_placeholder=bible_text.startswith(PLACEHOLDER_MARKER),
    )


def load_lane_policy(manifest: Manifest, lane: str, base_dir: str | Path = ".") -> LanePolicy:
    base_dir = Path(base_dir)
    entry = manifest.lanes.get(lane)
    if entry is None:
        raise UnknownLaneError(f"no lane {lane!r} in manifest")

    data = _read_yaml(base_dir, entry.policy, what=f"lane policy for {lane!r}")
    return LanePolicy(**data.get("lane_policy", data))


def load_preset(manifest: Manifest, preset_id: str, base_dir: str | Path = ".") -> LoadedPreset:
    base_dir = Path(base_dir)
    entry = manifest.presets.get(preset_id)
    if entry is None:
        raise UnknownPresetError(f"no preset {preset_id!r} in manifest")

    preset_data = _read_yaml(base_dir, entry.metadata, what=f"preset metadata for {preset_id!r}")
    preset = Preset(**preset_data)

    prompt_text = _read_text(base_dir, entry.prompt, what=f"prompt snapshot for {preset_id!r}")
    computed_hash = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    is_placeholder = prompt_text.startswith(PLACEHOLDER_MARKER)

    stored_hash = preset.prompt_hash
    matches = None if stored_hash is None else (stored_hash == computed_hash)

    return LoadedPreset(
        preset=preset,
        prompt_text=prompt_text,
        prompt_is_placeholder=is_placeholder,
        computed_prompt_hash=computed_hash,
        stored_prompt_hash_matches=matches,
    )


def sync_index(conn: sqlite3.Connection, manifest: Manifest, base_dir: str | Path = ".") -> None:
    """Refresh the characters/lanes/presets SQLite index tables from canonical
    files. Canonical files remain authoritative; this only updates the search
    mirror (Architecture Sec.27/Sec.29 — canonical state lives in files)."""
    base_dir = Path(base_dir)

    for character_id in manifest.characters:
        loaded = load_character(manifest, character_id, base_dir)
        p = loaded.profile
        conn.execute(
            """
            INSERT INTO characters
                (id, display_name, adult, age, core_persona, visual_formula,
                 expression_range, primary_content_pillars, bible_path, profile_path)
            VALUES (:id, :display_name, :adult, :age, :core_persona, :visual_formula,
                    :expression_range, :primary_content_pillars, :bible_path, :profile_path)
            ON CONFLICT(id) DO UPDATE SET
                display_name=excluded.display_name, adult=excluded.adult, age=excluded.age,
                core_persona=excluded.core_persona, visual_formula=excluded.visual_formula,
                expression_range=excluded.expression_range,
                primary_content_pillars=excluded.primary_content_pillars,
                bible_path=excluded.bible_path, profile_path=excluded.profile_path
            """,
            {
                "id": p.id,
                "display_name": p.display_name,
                "adult": int(p.adult),
                "age": p.age,
                "core_persona": json.dumps(p.core_persona),
                "visual_formula": json.dumps(p.visual_formula),
                "expression_range": json.dumps(p.expression_range),
                "primary_content_pillars": json.dumps(p.primary_content_pillars),
                "bible_path": loaded.bible_path,
                "profile_path": manifest.characters[character_id].profile,
            },
        )

    for lane_id in manifest.lanes:
        policy = load_lane_policy(manifest, lane_id, base_dir)
        conn.execute(
            """
            INSERT INTO lanes
                (lane, canonical_preset, status, policy_path, model_provider, model_name,
                 max_prompt_length, reference_order, priority, pose_policy, face_policy,
                 outfit_policy, refinement_policy)
            VALUES (:lane, :canonical_preset, :status, :policy_path, :model_provider,
                    :model_name, :max_prompt_length, :reference_order, :priority,
                    :pose_policy, :face_policy, :outfit_policy, :refinement_policy)
            ON CONFLICT(lane) DO UPDATE SET
                canonical_preset=excluded.canonical_preset, status=excluded.status,
                policy_path=excluded.policy_path, model_provider=excluded.model_provider,
                model_name=excluded.model_name, max_prompt_length=excluded.max_prompt_length,
                reference_order=excluded.reference_order, priority=excluded.priority,
                pose_policy=excluded.pose_policy, face_policy=excluded.face_policy,
                outfit_policy=excluded.outfit_policy, refinement_policy=excluded.refinement_policy
            """,
            {
                "lane": policy.lane,
                "canonical_preset": policy.canonical_preset,
                "status": policy.status.value,
                "policy_path": manifest.lanes[lane_id].policy,
                "model_provider": policy.model.provider,
                "model_name": policy.model.model,
                "max_prompt_length": policy.model.max_prompt_length,
                "reference_order": policy.reference_order.model_dump_json(),
                "priority": json.dumps(policy.priority),
                "pose_policy": policy.pose_policy.model_dump_json(),
                "face_policy": policy.face_policy.model_dump_json(),
                "outfit_policy": policy.outfit_policy,
                "refinement_policy": policy.refinement_policy.model_dump_json(),
            },
        )

    for preset_id in manifest.presets:
        loaded = load_preset(manifest, preset_id, base_dir)
        preset = loaded.preset
        conn.execute(
            """
            INSERT INTO presets
                (preset_id, status, lane, model_provider, model_name, reference_profile,
                 max_prompt_length, prompt_snapshot_path, prompt_hash, modules,
                 outfit_policy, revision_policy)
            VALUES (:preset_id, :status, :lane, :model_provider, :model_name,
                    :reference_profile, :max_prompt_length, :prompt_snapshot_path,
                    :prompt_hash, :modules, :outfit_policy, :revision_policy)
            ON CONFLICT(preset_id) DO UPDATE SET
                status=excluded.status, lane=excluded.lane,
                model_provider=excluded.model_provider, model_name=excluded.model_name,
                reference_profile=excluded.reference_profile,
                max_prompt_length=excluded.max_prompt_length,
                prompt_snapshot_path=excluded.prompt_snapshot_path,
                prompt_hash=excluded.prompt_hash, modules=excluded.modules,
                outfit_policy=excluded.outfit_policy, revision_policy=excluded.revision_policy
            """,
            {
                "preset_id": preset.preset_id,
                "status": preset.status.value,
                "lane": preset.lane,
                "model_provider": preset.model.provider,
                "model_name": preset.model.model,
                "reference_profile": preset.reference_profile,
                "max_prompt_length": preset.max_prompt_length,
                "prompt_snapshot_path": preset.prompt_snapshot_path,
                "prompt_hash": loaded.computed_prompt_hash,
                "modules": preset.modules.model_dump_json(),
                "outfit_policy": preset.outfit_policy,
                "revision_policy": preset.revision_policy,
            },
        )

    conn.commit()
