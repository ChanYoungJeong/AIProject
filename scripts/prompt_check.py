#!/usr/bin/env python3
"""Deterministic prompt length + duplicate-phrase check.

Usage:
    python prompt_check.py <prompt_file.txt> [--max-length N]

Exit codes:
    0 = PASS
    1 = FAIL (length or duplication issue found)
    2 = usage / input error (e.g. missing file)
"""
import argparse
import re
import sys
from collections import Counter


def find_duplicate_phrases(text: str, min_words: int = 6) -> list[str]:
    words = re.findall(r"\S+", text.lower())
    phrases = [
        " ".join(words[i : i + min_words])
        for i in range(len(words) - min_words + 1)
    ]
    counts = Counter(phrases)
    return [phrase for phrase, n in counts.items() if n > 1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_file")
    parser.add_argument("--max-length", type=int, default=3000)
    args = parser.parse_args()

    try:
        text = open(args.prompt_file, encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR: cannot read {args.prompt_file}: {e}", file=sys.stderr)
        return 2

    ok = True
    length = len(text)
    byte_length = len(text.encode("utf-8"))
    if length > args.max_length:
        print(f"FAIL: length {length} exceeds max_length {args.max_length}")
        ok = False
    else:
        print(f"OK: length {length} <= max_length {args.max_length}")

    non_ascii = sorted({c for c in text if ord(c) > 127})
    if non_ascii:
        print(
            f"WARN: {len(non_ascii)} non-ASCII character(s) found {non_ascii!r} — "
            f"character count ({length}) and UTF-8 byte count ({byte_length}) differ. "
            "Some tools (browser text fields, other counters) may count bytes or may "
            "mangle these on copy-paste, showing a higher/different length than this "
            "script reports. Prefer plain ASCII (e.g. '-' instead of an em dash) in any "
            "prompt that gets pasted into an external tool."
        )
        if byte_length > args.max_length:
            print(
                f"FAIL: UTF-8 byte length {byte_length} exceeds max_length "
                f"{args.max_length}, even though character length does not"
            )
            ok = False

    dupes = find_duplicate_phrases(text)
    if dupes:
        print(f"FAIL: {len(dupes)} duplicated phrase(s) found, e.g. {dupes[:3]!r}")
        ok = False
    else:
        print("OK: no duplicated phrases found")

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
