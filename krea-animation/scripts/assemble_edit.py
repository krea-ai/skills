#!/usr/bin/env python3
"""Normalize generated clips and assemble a final edit."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from _common import command_exists, parse_duration, project_root, read_csv, shell_join


def parse_size(value: str) -> tuple[int, int]:
    if "x" not in value:
        raise argparse.ArgumentTypeError("size must be WIDTHxHEIGHT")
    width, height = value.lower().split("x", 1)
    return int(width), int(height)


def active_jobs(root: Path) -> list[dict[str, str]]:
    return [row for row in read_csv(root / "04_generation/manifests/video_jobs.csv") if row.get("status")]


def normalize_clip(raw: Path, out: Path, duration: float, width: int, height: int, fps: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
        f"fps={fps},setsar=1:1"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(raw),
        "-t",
        f"{duration:g}",
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-preset",
        "medium",
        "-pix_fmt",
        "yuv420p",
        "-an",
        str(out),
    ]
    subprocess.run(cmd, check=True)


def concat_clips(clips: list[Path], out: Path) -> None:
    concat_file = out.parent / "concat-list.txt"
    concat_file.write_text("\n".join(f"file '{clip}'" for clip in clips) + "\n", encoding="utf-8")
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(out),
    ]
    subprocess.run(cmd, check=True)


def smooth_xfade(clips: list[Path], durations: list[float], out: Path, fade: float) -> None:
    if len(clips) == 1:
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(clips[0]), "-c", "copy", str(out)],
            check=True,
        )
        return

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for clip in clips:
        cmd.extend(["-i", str(clip)])

    filters: list[str] = []
    current = "0:v"
    elapsed = durations[0]
    for idx in range(1, len(clips)):
        label = f"v{idx}"
        offset = max(0.0, elapsed - fade)
        filters.append(
            f"[{current}][{idx}:v]xfade=transition=dissolve:duration={fade:g}:offset={offset:g}[{label}]"
        )
        current = label
        elapsed += durations[idx] - fade

    cmd.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            f"[{current}]",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "medium",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(out),
        ]
    )
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--size", type=parse_size, default=(1280, 720))
    parser.add_argument("--smooth-transitions", action="store_true", help="Use short xfade transitions")
    parser.add_argument("--fade", type=float, default=0.25, help="Transition duration for --smooth-transitions")
    parser.add_argument("--allow-partial", action="store_true", help="Assemble even when some expected raw clips are missing")
    args = parser.parse_args()

    if not command_exists("ffmpeg"):
        raise SystemExit("ffmpeg not found")

    root = project_root(args.project)
    width, height = args.size
    raw_dir = root / "05_edit/shots_raw"
    norm_dir = root / "05_edit/shots_norm"
    final_dir = root / "05_edit/final"
    final_dir.mkdir(parents=True, exist_ok=True)

    clips: list[Path] = []
    durations: list[float] = []
    missing: list[str] = []
    for row in active_jobs(root):
        shot_id = row["shot_id"]
        duration = parse_duration(row.get("duration", "0"))
        raw = raw_dir / f"shot-{shot_id}-raw.mp4"
        norm = norm_dir / f"shot-{shot_id}-norm.mp4"
        if not raw.exists():
            missing.append(f"{shot_id}: {raw}")
            continue
        normalize_clip(raw, norm, duration, width, height, args.fps)
        clips.append(norm)
        durations.append(duration)
        print(f"normalized {shot_id}")

    if missing and not args.allow_partial:
        details = "\n".join(f"  {item}" for item in missing)
        raise SystemExit(f"Missing raw clips; refusing to assemble partial edit:\n{details}")

    if not clips:
        raise SystemExit("No clips available to assemble")

    final = final_dir / "final.mp4"
    if args.smooth_transitions:
        smooth_xfade(clips, durations, final, args.fade)
    else:
        concat_clips(clips, final)

    print(f"Final edit: {final}")


if __name__ == "__main__":
    main()
