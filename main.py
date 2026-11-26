#!/usr/bin/env python3
"""Entrypoint: write the forecast line to /output/entry.txt.

Reads the line from line.txt (shipped beside this file), checks it against
the competition gate (UTF-8 text, 1 to 120 characters, not only white
space), and writes it to /output/entry.txt for the harness.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINE_PATH = os.path.join(HERE, "line.txt")
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 120


def main() -> int:
    with open(LINE_PATH, "r", encoding="utf-8") as fh:
        line = fh.read().strip()

    if not line or not (1 <= len(line) <= MAX_CHARS):
        print(f"line fails the gate: {len(line)} characters", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(line)

    # Read the artifact back and prove it is exactly the gated line:
    # same characters, valid UTF-8, nothing added or lost on the way out.
    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    if written.decode("utf-8") != line:
        print("written entry does not match the line", file=sys.stderr)
        return 1

    print(line)
    print(f"[{len(line)} characters, gate 1-{MAX_CHARS}: ok]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
