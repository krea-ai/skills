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

DENY_PARTS = {"__pycache__", "runs", "research", "node_modules", "fixtures"}
REQUIRED_SKILL_DIRS = {
    "krea-generate",
    "krea-marketing",
    "krea-motion",
}
REQUIRED_FILES = {
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/.mcp.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".mcp.json",
    "mcp.json",
}
FORBIDDEN_PREFIXES = {"krea-ai/", "wip/"}


def main() -> int:
    proc = subprocess.run(["npm", "pack", "--dry-run", "--json"], text=True, capture_output=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    packs = json.loads(proc.stdout)
    bad: list[str] = []
    included_files: set[str] = set()
    included_dirs: set[str] = set()
    forbidden: list[str] = []
    for pack in packs:
        for file_info in pack.get("files", []):
            path = file_info.get("path", "")
            included_files.add(path)
            parts = set(Path(path).parts)
            suffix = Path(path).suffix.lower()
            if suffix in DENY_SUFFIXES or parts.intersection(DENY_PARTS):
                bad.append(path)
            first = Path(path).parts[0] if Path(path).parts else ""
            if first in REQUIRED_SKILL_DIRS:
                included_dirs.add(first)
            if any(path.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
                forbidden.append(path)
    if bad:
        print("Package contains forbidden artifacts:", file=sys.stderr)
        for path in bad:
            print(f"  {path}", file=sys.stderr)
        return 1
    if forbidden:
        print("Package contains removed skill paths:", file=sys.stderr)
        for path in forbidden:
            print(f"  {path}", file=sys.stderr)
        return 1
    missing = sorted(REQUIRED_SKILL_DIRS - included_dirs)
    if missing:
        print("Package is missing required skill directories:", file=sys.stderr)
        for name in missing:
            print(f"  {name}/", file=sys.stderr)
        return 1
    missing_files = sorted(REQUIRED_FILES - included_files)
    if missing_files:
        print("Package is missing required plugin files:", file=sys.stderr)
        for path in missing_files:
            print(f"  {path}", file=sys.stderr)
        return 1
    print("OK package contents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
