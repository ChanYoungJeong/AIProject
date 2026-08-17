import pytest

from app.services.canonical_versioning import (
    CanonicalFileExistsError,
    write_versioned_canonical_file,
)


def test_write_new_file_succeeds(tmp_path):
    target = tmp_path / "presets" / "NAT_v1.4.4_LOCKED_PROMPT.txt"
    written = write_versioned_canonical_file(target, "new locked prompt text")
    assert written.read_text(encoding="utf-8") == "new locked prompt text"


def test_write_existing_file_refuses_to_overwrite(tmp_path):
    target = tmp_path / "NAT_v1.4.3_LOCKED_PROMPT.txt"
    target.write_text("original locked text", encoding="utf-8")

    with pytest.raises(CanonicalFileExistsError):
        write_versioned_canonical_file(target, "attempted overwrite")

    assert target.read_text(encoding="utf-8") == "original locked text"
