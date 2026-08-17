from pydantic import BaseModel, ConfigDict, model_validator

from app.schemas.common import CanonicalState


class PresetModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str


class PresetModules(BaseModel):
    model_config = ConfigDict(extra="forbid")

    identity: str | None = None
    camera: str | None = None
    realism: str | None = None


class Preset(BaseModel):
    """Architecture Sec.12 — Prompt Preset shape.

    A `locked` preset is read-only (Sec.12 rule) and must have a prompt snapshot to
    lock — a locked preset with no snapshot path is a contradiction in terms.
    """

    model_config = ConfigDict(extra="forbid")

    preset_id: str
    status: CanonicalState
    lane: str

    model: PresetModelConfig
    reference_profile: str
    max_prompt_length: int

    prompt_snapshot_path: str | None = None
    prompt_hash: str | None = None

    modules: PresetModules = PresetModules()

    outfit_policy: str
    revision_policy: str

    @model_validator(mode="after")
    def _locked_requires_snapshot(self) -> "Preset":
        if self.status == CanonicalState.LOCKED and not self.prompt_snapshot_path:
            raise ValueError(
                "a locked preset must declare prompt_snapshot_path (Architecture Sec.12)"
            )
        return self
