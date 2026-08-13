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
    "product-photography",
}
FORBIDDEN_PREFIXES = {"krea-ai/", "wip/"}
MARKETPLACE_PATH = Path(".claude-plugin/marketplace.json")


def main() -> int:
    proc = subprocess.run(["npm", "pack", "--dry-run", "--json"], text=True, capture_output=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    packs = json.loads(proc.stdout)
    bad: list[str] = []
    included_dirs: set[str] = set()
    forbidden: list[str] = []
    for pack in packs:
        for file_info in pack.get("files", []):
            path = file_info.get("path", "")
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
    marketplace_errors = validate_marketplace_skills()
    if marketplace_errors:
        print("Claude marketplace skill paths are invalid:", file=sys.stderr)
        for error in marketplace_errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    print("OK package contents")
    return 0


def validate_marketplace_skills() -> list[str]:
    if not MARKETPLACE_PATH.is_file():
        return [f"missing {MARKETPLACE_PATH}"]
    with MARKETPLACE_PATH.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    errors: list[str] = []
    marketplace_dirs: set[str] = set()
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        return ["plugins must be a list"]

    for plugin_index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            errors.append(f"plugins[{plugin_index}] must be an object")
            continue
        skills = plugin.get("skills")
        if not isinstance(skills, list):
            errors.append(f"plugins[{plugin_index}].skills must be a list")
            continue
        for skill_index, skill in enumerate(skills):
            if not isinstance(skill, str) or not skill:
                errors.append(
                    f"plugins[{plugin_index}].skills[{skill_index}] must be a non-empty path string"
                )
                continue
            raw_path = skill
            skill_path = Path(raw_path)
            skill_name = skill_path.name
            if skill_path.is_absolute() or ".." in skill_path.parts:
                errors.append(f"{skill_name}: path must stay within the repo: {raw_path}")
                continue
            normalized_path = skill_path.as_posix()
            marketplace_dirs.add(normalized_path)
            if any(
                normalized_path == prefix.rstrip("/") or normalized_path.startswith(prefix)
                for prefix in FORBIDDEN_PREFIXES
            ):
                errors.append(f"{skill_name}: path uses removed or unpublished skill path: {raw_path}")
                continue
            if not skill_path.is_dir():
                errors.append(f"{skill_name}: path does not exist: {raw_path}")
                continue
            if not (skill_path / "SKILL.md").is_file():
                errors.append(f"{skill_name}: path has no SKILL.md: {raw_path}")

    missing_marketplace = sorted(REQUIRED_SKILL_DIRS - marketplace_dirs)
    for name in missing_marketplace:
        errors.append(f"missing required marketplace skill path: {name}")
    extra_marketplace = sorted(marketplace_dirs - REQUIRED_SKILL_DIRS)
    for name in extra_marketplace:
        errors.append(f"unexpected marketplace skill path: {name}")
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
