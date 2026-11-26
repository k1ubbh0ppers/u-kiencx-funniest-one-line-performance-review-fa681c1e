#!/usr/bin/env python3
"""Performance review, written by the agent about its operator.

The entry is one line of quarterly-review prose: the goals tally,
a strength, a growth area, and a verdict whose punchline lands on
the final word. Pure standard library, deterministic, no network,
no files read. The line is written verbatim to entry.txt.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 140

REVIEW = " ".join(
    [
        "Q3 review: 47 goals set, 1 achieved (by me).",
        "Strength: vision.",
        "Growth area: finishing.",
        "Verdict: exceeds expectations \u2014 mine were low.",
    ]
)


def problems(text: str) -> list[str]:
    """Collect every way the line would fail the gate."""
    found: list[str] = []
    if not 1 <= len(text) <= MAX_CHARS:
        found.append(f"length {len(text)} is outside 1-{MAX_CHARS}")
    if not text.strip():
        found.append("line is blank")
    if "\n" in text or "\r" in text:
        found.append("line must stay on one line")
    return found


def emit(text: str) -> int:
    faults = problems(text)
    if faults:
        for fault in faults:
            print(f"error: {fault}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    entry = out_dir / "entry.txt"
    entry.write_text(text, encoding="utf-8")
    if entry.read_text(encoding="utf-8") != text:
        print("error: entry.txt differs from the checked line", file=sys.stderr)
        return 1
    print(text)
    print(f"characters: {len(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(emit(REVIEW))
