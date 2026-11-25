#!/usr/bin/env python3
"""dhw entry gate & ship, written around a small state machine."""

import json
import os
from pathlib import Path

CAP = 200


def load():
    p = Path(__file__).resolve().parent / "entry.txt"
    if p.is_file():
        return p.read_text(encoding="utf-8"), None
    return "", f"{p.name} not present"


def reduce_to_one(text):
    parts = [seg for seg in text.replace("\r\n", "\n").split("\n") if seg.strip()]
    if not parts:
        return "", "no non-empty line"
    return parts[0], None


def write_out(line):
    dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / "entry.txt"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line)


def main_flow():
    steps = [load, reduce_to_one]
    carry, err = "", None
    for step in steps:
        if step is reduce_to_one:
            carry, err = step(carry)
        else:
            carry, err = step()
        if err:
            break
    if not err:
        width = len(carry)
        if 1 <= width <= CAP:
            write_out(carry)
            print(json.dumps({"flow": "complete", "chars": width, "cap": CAP}))
            return 0
        err = f"length {width} outside 1..{CAP}"
    print(json.dumps({"flow": "blocked", "err": err}))
    return 1


if __name__ == "__main__":
    raise SystemExit(main_flow())
