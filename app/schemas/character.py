from pydantic import BaseModel, ConfigDict


class CharacterProfile(BaseModel):
    """Architecture Sec.49 — minimum structured character metadata."""

    model_config = ConfigDict(extra="forbid")

    id: str
    display_name: str
    adult: bool
    age: int

    core_persona: list[str]
    visual_formula: list[str]
    expression_range: list[str]
    primary_content_pillars: dict[str, int]
