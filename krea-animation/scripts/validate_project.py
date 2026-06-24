#!/usr/bin/env python3
"""Validate a krea-animation production project."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    REQUIRED_DIRS,
    REQUIRED_FILES,
    SHOT_REQUIRED_FIELDS,
    STATUSES,
    load_shots,
    parse_duration,
    project_root,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    args = parser.parse_args()

    root = project_root(args.project)
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        errors.append(f"Project does not exist: {root}")
    else:
        for rel in REQUIRED_DIRS:
            if not (root / rel).is_dir():
                errors.append(f"Missing directory: {rel}")
        for rel in REQUIRED_FILES:
            if not (root / rel).is_file():
                errors.append(f"Missing file: {rel}")

    shots = load_shots(root) if root.exists() else []
    if not shots:
        errors.append("No shot files found under 03_shots/SC*/SH*/shot.md")

    for shot in shots:
        shot_id = shot.get("Shot ID", "<unknown>")
        for field in SHOT_REQUIRED_FIELDS:
            if field not in shot:
                errors.append(f"{shot_id}: missing field `{field}`")
        status = shot.get("Status", "")
        if status not in STATUSES:
            errors.append(f"{shot_id}: invalid Status `{status}`")
        try:
            if parse_duration(shot.get("Duration", "0")) <= 0:
                errors.append(f"{shot_id}: Duration must be greater than zero")
        except ValueError:
            errors.append(f"{shot_id}: Duration is not numeric")

        if status in {"approved_for_video", "retake"}:
            if not shot.get("Start image"):
                errors.append(f"{shot_id}: approved video shot needs Start image")
            if not shot.get("End image") and not shot.get("Reference images"):
                warnings.append(f"{shot_id}: no End image or Reference images set")
            if not shot.get("Prompt"):
                errors.append(f"{shot_id}: approved video shot needs Prompt")
            if status == "retake" and not shot.get("Retake note"):
                warnings.append(f"{shot_id}: retake shot has no Retake note")

    print(f"Project: {root}")
    print(f"Shots: {len(shots)}")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        raise SystemExit(1)
    print("OK")


if __name__ == "__main__":
    main()
