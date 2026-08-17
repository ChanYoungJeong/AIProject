#!/usr/bin/env python3
"""Validate a GenerationPlan against the Architecture §53 provenance fields.

Usage:
    python generation_plan_check.py <generation_plan.yaml>

Exit codes:
    0 = valid
    1 = invalid (missing required provenance field)
    2 = usage / input error
"""
import sys

REQUIRED_FIELDS = [
    "generation_plan_id",
    "created_at",
    "character_id",
    "lane",
    "preset_id",
    "preset_prompt_hash",
    "model",
    "reference_asset_ids",
    "reference_order",
    "prompt_text",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: generation_plan_check.py <generation_plan.yaml>", file=sys.stderr)
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
        print(f"MISSING_PLAN: {path} does not exist")
        return 1
    except OSError as e:
        print(f"ERROR: cannot read {path}: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"FAIL: {path} is not valid YAML: {e}")
        return 1

    if not isinstance(data, dict):
        print("FAIL: GenerationPlan root must be a mapping")
        return 1

    missing = [f for f in REQUIRED_FIELDS if data.get(f) in (None, "", [])]
    if missing:
        print(f"FAIL: GenerationPlan missing/empty required field(s): {missing}")
        return 1

    print(f"PASS: {path} has full provenance for reproducibility")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
