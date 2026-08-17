#!/usr/bin/env python3
"""Validate a canonical manifest YAML against the Architecture §50 shape.

Usage:
    python manifest_check.py <manifest.yaml>

Exit codes:
    0 = valid
    1 = invalid (missing/malformed required fields)
    2 = usage / input error (e.g. missing file, PyYAML not installed)
"""
import sys

REQUIRED_TOP_LEVEL = ["project", "workflow_master", "characters", "lanes", "presets"]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: manifest_check.py <manifest.yaml>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML not installed (pip install pyyaml)", file=sys.stderr)
        return 2

    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"MISSING_MANIFEST: {path} does not exist")
        return 1
    except OSError as e:
        print(f"ERROR: cannot read {path}: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # yaml.YAMLError etc.
        print(f"FAIL: {path} is not valid YAML: {e}")
        return 1

    if not isinstance(data, dict):
        print("FAIL: manifest root must be a mapping")
        return 1

    missing = [k for k in REQUIRED_TOP_LEVEL if k not in data]
    if missing:
        print(f"FAIL: manifest missing required top-level key(s): {missing}")
        return 1

    for char_id, char in (data.get("characters") or {}).items():
        if "bible" not in char:
            print(f"FAIL: character '{char_id}' missing 'bible' path")
            return 1

    for preset_id, preset in (data.get("presets") or {}).items():
        if "status" not in preset:
            print(f"FAIL: preset '{preset_id}' missing 'status'")
            return 1
        if preset["status"] == "locked" and "prompt" not in preset:
            print(f"FAIL: locked preset '{preset_id}' missing 'prompt' path")
            return 1

    print(f"PASS: {path} matches the manifest shape")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
