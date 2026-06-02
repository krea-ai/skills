#!/usr/bin/env python3
"""Fail if npm package contents include generated caches or media artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


DENY_SUFFIXES = {
    ".pdf",
    ".pyc",
    ".mp4",
    ".mov",
    ".wav",
    ".aiff",
    ".psd",
}

DENY_PARTS = {"__pycache__", "runs", "research", "node_modules"}


def main() -> int:
    proc = subprocess.run(["npm", "pack", "--dry-run", "--json"], text=True, capture_output=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    packs = json.loads(proc.stdout)
    bad: list[str] = []
    for pack in packs:
        for file_info in pack.get("files", []):
            path = file_info.get("path", "")
            parts = set(Path(path).parts)
            suffix = Path(path).suffix.lower()
            if suffix in DENY_SUFFIXES or parts.intersection(DENY_PARTS):
                bad.append(path)
    if bad:
        print("Package contains forbidden artifacts:", file=sys.stderr)
        for path in bad:
            print(f"  {path}", file=sys.stderr)
        return 1
    print("OK package contents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
