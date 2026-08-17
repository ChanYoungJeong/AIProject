"""Architecture Sec.46 item 01 / Sec.29 — locked canonical artifacts are immutable
by filename version. A new version must get a new filename; canonical/manifest.yaml
(and any preset/lane metadata pointing at it) must be updated separately to point
at the new file. This module only enforces the "never silently overwrite" half."""
from pathlib import Path


class CanonicalFileExistsError(FileExistsError):
    pass


def write_versioned_canonical_file(path: str | Path, content: str) -> Path:
    path = Path(path)
    if path.exists():
        raise CanonicalFileExistsError(
            f"refusing to overwrite existing canonical file {path}: "
            "locked/versioned artifacts are immutable (Architecture Sec.29) — "
            "write a new version under a new filename instead"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
