#!/usr/bin/env python3
"""Submit approved animation shots to Krea or print dry-run commands."""

from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from _common import command_exists, read_csv, run_json, shell_join, project_root


DRAFT_MODELS = ["bytedance/seedance-2-fast", "minimax/hailuo-2.3-fast", "alibaba/wan-2.5"]
FINAL_MODELS = ["bytedance/seedance-2", "google/veo-3.1", "kling/kling-3.0", "runway/gen-4.5"]


def available_models() -> set[str]:
    if not command_exists("krea"):
        return set()
    try:
        data = run_json(["krea", "models", "list", "--json"])
    except Exception:
        return set()
    if not isinstance(data, list):
        return set()
    return {item.get("id", "") for item in data if isinstance(item, dict)}


def resolve_model(requested: str, quality: str) -> str:
    if requested != "auto":
        return requested
    candidates = FINAL_MODELS if quality == "final" else DRAFT_MODELS
    live = available_models()
    for candidate in candidates:
        if candidate in live:
            return candidate
    return candidates[0]


def command_for(row: dict[str, str], model: str, quality: str) -> list[str]:
    aspect = row.get("aspect") or "16:9"
    duration = row.get("duration") or "5"
    resolution = "1080p" if quality == "final" else "720p"
    selected_model = row.get("model") or model
    cmd = [
        "krea",
        "generate",
        "video",
        "-m",
        selected_model,
        "--aspect",
        aspect,
        "--duration",
        duration,
        "--resolution",
        resolution,
        "-i",
        f"generate_audio=false",
        "-p",
        row.get("prompt", ""),
    ]
    if row.get("start_image"):
        cmd.extend(["--start-image", row["start_image"]])
    if row.get("end_image"):
        cmd.extend(["-i", f"end_image={row['end_image']}"])
    refs = [part.strip() for part in row.get("reference_images", "").split(",") if part.strip()]
    if refs and not ("seedance" in selected_model.lower() and row.get("end_image")):
        cmd.extend(["-i", "reference_images=" + json.dumps(refs)])
    cmd.append("--json")
    return cmd


def submit(row: dict[str, str], cmd: list[str], cwd: Path) -> dict[str, str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        return {"shot_id": row["shot_id"], "job_id": "FAILED", "status": "failed", "error": proc.stderr.strip()}
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"shot_id": row["shot_id"], "job_id": "FAILED", "status": "failed", "error": proc.stdout.strip()}
    job_id = data.get("job_id") or data.get("id") or ""
    return {"shot_id": row["shot_id"], "job_id": job_id or "FAILED", "status": data.get("status", "submitted"), "error": ""}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    parser.add_argument("--model", default="auto", help="Model ID or auto")
    parser.add_argument("--quality", choices=["draft", "final"], default="draft")
    parser.add_argument("--parallel", type=int, default=2, help="Concurrent submissions")
    parser.add_argument("--dry-run", action="store_true", help="Write commands without submitting jobs")
    args = parser.parse_args()

    root = project_root(args.project)
    jobs_dir = root / "04_generation/jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    manifest = root / "04_generation/manifests/video_jobs.csv"
    rows = [row for row in read_csv(manifest) if row.get("status") in {"approved_for_video", "retake"}]
    model = resolve_model(args.model, args.quality)
    commands = [(row, command_for(row, model, args.quality)) for row in rows]

    if args.dry_run:
        out = jobs_dir / "dry-run-commands.sh"
        out.write_text("\n".join(shell_join(cmd) for _, cmd in commands) + ("\n" if commands else ""), encoding="utf-8")
        print(f"Dry-run commands: {out}")
        print(f"Jobs: {len(commands)}")
        return

    if not command_exists("krea"):
        raise SystemExit("krea CLI not found")

    results: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
        futures = [pool.submit(submit, row, cmd, root) for row, cmd in commands]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"{result['shot_id']}\t{result['job_id']}\t{result['status']}")

    with (jobs_dir / "jobs.tsv").open("w", encoding="utf-8") as handle:
        for result in sorted(results, key=lambda item: item["shot_id"]):
            handle.write(f"{result['shot_id']}\t{result['job_id']}\t{result['status']}\t{result['error']}\n")
    print(f"Wrote {jobs_dir / 'jobs.tsv'}")


if __name__ == "__main__":
    main()
