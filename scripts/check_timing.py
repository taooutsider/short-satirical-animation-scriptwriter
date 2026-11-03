#!/usr/bin/env python3
"""Estimate spoken-dialogue duration from word count, pace, and pauses."""

import argparse
import re
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*")


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    parser.add_argument("--wpm", type=float, default=165.0)
    parser.add_argument("--pause-seconds", type=float, default=0.0)
    parser.add_argument("--target-min", type=float)
    parser.add_argument("--target-max", type=float)
    args = parser.parse_args()

    text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    words = WORD_RE.findall(text)
    seconds = len(words) * 60.0 / args.wpm + args.pause_seconds

    status = "unbounded"
    if args.target_min is not None and args.target_max is not None:
        status = "pass" if args.target_min <= seconds <= args.target_max else "fail"

    print(f"words={len(words)}")
    print(f"wpm={args.wpm:g}")
    print(f"pause_seconds={args.pause_seconds:g}")
    print(f"estimated_seconds={seconds:.2f}")
    print(f"target_status={status}")


if __name__ == "__main__":
    main()
