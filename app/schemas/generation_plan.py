from pydantic import BaseModel, ConfigDict


class ReferenceSlot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str
    role: str


class GenerationPlan(BaseModel):
    """Architecture Sec.13 — Prompt Engine output. Never submitted to a
    generation provider automatically (Sec.16) — this is just the validated
    plan a human runs manually."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    generation_mode: str

    references: dict[str, ReferenceSlot]

    prompt: str
    prompt_length: int
    prompt_hash: str

    expected_behavior: list[str]
    high_risk_points: list[str]
    qc_targets: list[str]
