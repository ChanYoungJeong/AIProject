import pytest

from app.services.prompt_validation import PromptTooLongError, validate_prompt_length


def test_under_length_passes():
    result = validate_prompt_length("short prompt", max_length=100)
    assert result.ok is True
    assert result.length == len("short prompt")


def test_over_length_raises():
    with pytest.raises(PromptTooLongError):
        validate_prompt_length("x" * 101, max_length=100)


def test_exact_length_passes():
    result = validate_prompt_length("x" * 100, max_length=100)
    assert result.ok is True
