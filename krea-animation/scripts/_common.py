#!/usr/bin/env python3
"""Shared helpers for krea-animation scripts."""

from __future__ import annotations

import csv
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


STATUSES = {
    "draft",
    "needs_assets",
    "needs_keyframes",
    "approved_for_video",
    "submitted",
    "complete",
    "retake",
    "approved_final",
}


REQUIRED_DIRS = [
    "00_brief",
    "01_bible/characters",
    "01_bible/props",
    "01_bible/worlds",
    "01_bible/style",
    "02_story",
    "03_shots",
    "04_generation/manifests",
    "04_generation/jobs",
    "05_edit/audio",
    "05_edit/subtitles",
    "05_edit/shots_raw",
    "05_edit/shots_norm",
    "05_edit/final",
    "06_qa/frame-samples",
]


REQUIRED_FILES = [
    "00_brief/brief.md",
    "01_bible/style/style-guide.md",
    "01_bible/characters/characters.csv",
    "01_bible/props/props.csv",
    "01_bible/worlds/worlds.csv",
    "02_story/script.md",
    "02_story/beat-sheet.md",
    "02_story/storyboard.md",
    "06_qa/retakes.csv",
    "06_qa/delivery-checklist.md",
]


SHOT_REQUIRED_FIELDS = [
    "Shot ID",
    "Scene",
    "Duration",
    "Status",
    "Start image",
    "Prompt",
    "Camera",
    "Action",
    "Continuity",
    "Audio",
]


def project_root(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def template_dir() -> Path:
    return skill_root() / "assets" / "templates"


def ensure_dirs(root: Path) -> None:
    for rel in REQUIRED_DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)


def render_template(name: str, values: dict[str, str]) -> str:
    text = (template_dir() / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def write_if_missing(path: Path, content: str, force: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def read_markdown_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if not key or key.startswith("#"):
            continue
        fields[key] = value.strip()
    return fields


def shot_files(root: Path) -> list[Path]:
    return sorted((root / "03_shots").glob("SC*/SH*/shot.md"))


def shot_sort_key(path: Path) -> tuple[str, str]:
    parts = path.parts
    scene = next((p for p in parts if re.fullmatch(r"SC\d+", p)), "")
    shot = next((p for p in parts if re.fullmatch(r"SH\d+", p)), "")
    return (scene, shot)


def load_shots(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(shot_files(root), key=shot_sort_key):
        fields = read_markdown_fields(path)
        shot_id = fields.get("Shot ID") or f"{path.parent.parent.name}_{path.parent.name}"
        fields["Shot ID"] = normalize_shot_id(shot_id)
        fields["_path"] = str(path)
        rows.append(fields)
    return rows


def normalize_shot_id(value: str) -> str:
    value = value.strip().replace(".", "_").replace("-", "_")
    value = re.sub(r"[^A-Za-z0-9_]+", "_", value)
    return value.upper()


def parse_duration(value: str) -> float:
    value = value.strip().lower().replace("seconds", "").replace("second", "").replace("s", "")
    return float(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def run_json(cmd: list[str], cwd: Path | None = None) -> dict:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "command failed")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"command did not return JSON: {' '.join(cmd)}") from exc


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def shell_join(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def result_url(data: dict) -> str:
    candidates: list[object] = [
        data.get("url"),
        data.get("urls", [None])[0] if isinstance(data.get("urls"), list) and data.get("urls") else None,
    ]
    result = data.get("result")
    if isinstance(result, dict):
        candidates.extend(
            [
                result.get("url"),
                result.get("urls", [None])[0] if isinstance(result.get("urls"), list) and result.get("urls") else None,
            ]
        )
        videos = result.get("videos")
        if isinstance(videos, list) and videos:
            first = videos[0]
            if isinstance(first, dict):
                candidates.append(first.get("url"))
    for item in candidates:
        if isinstance(item, str) and item:
            return item
    return ""


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def repo_relative(path: Path) -> str:
    try:
        return os.path.relpath(path, Path.cwd())
    except ValueError:
        return str(path)
