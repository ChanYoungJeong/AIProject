#!/usr/bin/env python3
"""Deterministically extract one section from a large Markdown file by heading,
so Claude doesn't have to load the whole file to answer a scoped question.

Usage:
    python extract_md_section.py <file.md> "<heading text or number prefix>"
    python extract_md_section.py <file.md> --list

Matches a line starting with 1-6 '#' characters whose remaining text contains the
given string (case-insensitive). Prints from that heading up to (not including) the
next heading of the same or shallower level.

Exit codes:
    0 = found and printed
    1 = heading not found
    2 = usage / input error
"""
import re
import sys

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    path = sys.argv[1]
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as e:
        print(f"ERROR: cannot read {path}: {e}", file=sys.stderr)
        return 2

    headings = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2)))

    if len(sys.argv) == 3 and sys.argv[2] == "--list":
        for _, level, text in headings:
            print(f"{'#' * level} {text}")
        return 0

    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    query = sys.argv[2].lower()
    match = next(
        ((i, level, text) for i, level, text in headings if query in text.lower()),
        None,
    )
    if match is None:
        print(f"NOT_FOUND: no heading matching {sys.argv[2]!r}", file=sys.stderr)
        return 1

    start_idx, level, _ = match
    end_idx = len(lines)
    for i, lvl, _ in headings:
        if i > start_idx and lvl <= level:
            end_idx = i
            break

    print("\n".join(lines[start_idx:end_idx]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
