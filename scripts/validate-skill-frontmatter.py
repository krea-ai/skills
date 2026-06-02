#!/usr/bin/env python3
"""Validate repo SKILL.md frontmatter without depending on external CLI drift."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ALLOWED = {"version", "name", "description", "license"}
REQUIRED = {"version", "name", "description", "license"}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        values[key] = value
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    repo = Path.cwd()
    version = (repo / "VERSION").read_text(encoding="utf-8").strip()
    ok = True
    for raw in args.paths:
        path = Path(raw)
        try:
            values = parse_frontmatter(path)
            extra = set(values) - ALLOWED
            missing = REQUIRED - set(values)
            if extra:
                raise ValueError(f"unexpected keys: {', '.join(sorted(extra))}")
            if missing:
                raise ValueError(f"missing keys: {', '.join(sorted(missing))}")
            if values["version"] != version:
                raise ValueError(f"version {values['version']} != VERSION {version}")
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", values["name"]):
                raise ValueError(f"invalid skill name: {values['name']}")
            if not values["description"]:
                raise ValueError("description is empty")
            print(f"OK {path}")
        except Exception as exc:
            ok = False
            print(f"ERROR {path}: {exc}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
