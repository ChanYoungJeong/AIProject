"""Architecture Sec.46 item 10 (validation half) / Sec.12 ("Prompt length
validation happens against the final rendered text"). Deterministic length
check only — semantic conflict detection (Sec.15) stays a Claude-time judgment
call, not a hard-coded heuristic."""
from dataclasses import dataclass


@dataclass
class PromptValidationResult:
    length: int
    max_length: int
    ok: bool


class PromptTooLongError(ValueError):
    pass


def validate_prompt_length(text: str, max_length: int) -> PromptValidationResult:
    length = len(text)
    result = PromptValidationResult(length=length, max_length=max_length, ok=length <= max_length)
    if not result.ok:
        raise PromptTooLongError(
            f"prompt is {length} characters, exceeds max_length {max_length}"
        )
    return result
