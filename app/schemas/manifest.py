from pydantic import BaseModel, ConfigDict

from app.schemas.common import CanonicalState


class CharacterMasters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    face_id: str | None = None
    character: str | None = None
    body: str | None = None


class ManifestCharacterEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bible: str
    profile: str
    masters: CharacterMasters = CharacterMasters()


class ManifestLaneEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preset: str
    policy: str


class ManifestPresetEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: CanonicalState
    prompt: str
    metadata: str


class Manifest(BaseModel):
    """Architecture Sec.50 — Canonical Manifest shape. First local source resolved
    for any production request (Sec.50, Sec.52)."""

    model_config = ConfigDict(extra="forbid")

    project: str
    workflow_master: str
    characters: dict[str, ManifestCharacterEntry]
    lanes: dict[str, ManifestLaneEntry]
    presets: dict[str, ManifestPresetEntry]
