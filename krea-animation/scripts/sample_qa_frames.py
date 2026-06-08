#!/usr/bin/env python3
"""Extract QA frames from normalized clips and the final edit."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from _common import command_exists, parse_duration, project_root, read_csv


def extract_frame(video: Path, timestamp: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{max(0.0, timestamp):.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(out),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def active_jobs(root: Path) -> list[dict[str, str]]:
    return [row for row in read_csv(root / "04_generation/manifests/video_jobs.csv") if row.get("status")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    args = parser.parse_args()

    if not command_exists("ffmpeg"):
        raise SystemExit("ffmpeg not found")

    root = project_root(args.project)
    norm_dir = root / "05_edit/shots_norm"
    final = root / "05_edit/final/final.mp4"
    out_dir = root / "06_qa/frame-samples"
    out_dir.mkdir(parents=True, exist_ok=True)

    cumulative = 0.0
    written = 0
    for row in active_jobs(root):
        shot_id = row["shot_id"]
        duration = parse_duration(row.get("duration", "0"))
        video = norm_dir / f"shot-{shot_id}-norm.mp4"
        if not video.exists():
            continue
        sample_points = {
            "first": 0.05,
            "mid": max(0.05, duration / 2),
            "last": max(0.05, duration - 0.08),
        }
        for label, timestamp in sample_points.items():
            extract_frame(video, timestamp, out_dir / f"{shot_id}-{label}.jpg")
            written += 1
        if final.exists() and cumulative > 0:
            extract_frame(final, max(0.0, cumulative - 0.05), out_dir / f"boundary-before-{shot_id}.jpg")
            extract_frame(final, cumulative + 0.05, out_dir / f"boundary-after-{shot_id}.jpg")
            written += 2
        cumulative += duration

    if final.exists():
        extract_frame(final, max(0.05, cumulative / 2), out_dir / "final-midpoint.jpg")
        written += 1

    print(f"QA frames written: {written}")
    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()
