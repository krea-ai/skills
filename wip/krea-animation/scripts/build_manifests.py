#!/usr/bin/env python3
"""Build generation and edit manifests from shot files and bible CSVs."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import load_shots, parse_duration, project_root, read_csv, write_csv


ACTIVE_VIDEO_STATUSES = {"approved_for_video", "retake", "submitted", "complete", "approved_final"}


def asset_rows(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources = [
        ("character", root / "01_bible/characters/characters.csv", "character_id", "model_sheet"),
        ("prop", root / "01_bible/props/props.csv", "prop_id", "path_or_url"),
        ("world", root / "01_bible/worlds/worlds.csv", "world_id", "path_or_url"),
    ]
    for asset_type, path, id_field, path_field in sources:
        for row in read_csv(path):
            asset_id = row.get(id_field, "")
            name = row.get("name", asset_id)
            rows.append(
                {
                    "asset_id": asset_id,
                    "type": asset_type,
                    "name": name,
                    "path_or_url": row.get(path_field, ""),
                    "status": row.get("status", ""),
                    "notes": row.get("notes", ""),
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    args = parser.parse_args()

    root = project_root(args.project)
    manifests = root / "04_generation/manifests"
    manifests.mkdir(parents=True, exist_ok=True)

    shots = load_shots(root)
    assets = asset_rows(root)
    keyframes: list[dict[str, object]] = []
    video_jobs: list[dict[str, object]] = []
    durations: list[tuple[str, float]] = []
    concat_lines: list[str] = []

    for shot in shots:
        shot_id = shot["Shot ID"]
        status = shot.get("Status", "")
        try:
            duration = parse_duration(shot.get("Duration", "0"))
        except ValueError:
            duration = 0.0
        start = shot.get("Start image", "")
        end = shot.get("End image", "")
        refs = shot.get("Reference images", "")

        if start:
            keyframes.append(
                {"shot_id": shot_id, "role": "start", "path_or_url": start, "status": status, "notes": ""}
            )
        if end:
            keyframes.append({"shot_id": shot_id, "role": "end", "path_or_url": end, "status": status, "notes": ""})

        if status in ACTIVE_VIDEO_STATUSES:
            video_jobs.append(
                {
                    "shot_id": shot_id,
                    "duration": f"{duration:g}",
                    "model": shot.get("Model", ""),
                    "aspect": shot.get("Aspect", ""),
                    "start_image": start,
                    "end_image": end,
                    "reference_images": refs,
                    "prompt": shot.get("Prompt", ""),
                    "status": status,
                }
            )
            durations.append((shot_id, duration))
            concat_lines.append(f"file '../../05_edit/shots_norm/shot-{shot_id}-norm.mp4'")

    write_csv(manifests / "assets.csv", ["asset_id", "type", "name", "path_or_url", "status", "notes"], assets)
    write_csv(manifests / "keyframes.csv", ["shot_id", "role", "path_or_url", "status", "notes"], keyframes)
    write_csv(
        manifests / "video_jobs.csv",
        ["shot_id", "duration", "model", "aspect", "start_image", "end_image", "reference_images", "prompt", "status"],
        video_jobs,
    )

    with (manifests / "durations.tsv").open("w", encoding="utf-8") as handle:
        for shot_id, duration in durations:
            handle.write(f"{shot_id}\t{duration:g}\n")

    (manifests / "concat-list.txt").write_text("\n".join(concat_lines) + ("\n" if concat_lines else ""), encoding="utf-8")

    print(f"Assets: {len(assets)}")
    print(f"Keyframes: {len(keyframes)}")
    print(f"Video jobs: {len(video_jobs)}")
    print(f"Wrote manifests to {manifests}")


if __name__ == "__main__":
    main()
