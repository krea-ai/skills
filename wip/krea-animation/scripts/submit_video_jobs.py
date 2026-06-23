#!/usr/bin/env python3
"""Build approved animation video job payloads for Krea MCP submission."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import read_csv, project_root


def resolve_model(requested: str, quality: str) -> str:
    if requested != "auto":
        return requested
    raise SystemExit("Pass --model explicitly after verifying the live catalog through Krea MCP.")


def payload_for(row: dict[str, str], model: str, quality: str) -> dict[str, object]:
    aspect = row.get("aspect") or "16:9"
    duration_raw = row.get("duration") or "5"
    try:
        duration: int | float = int(float(duration_raw))
    except ValueError:
        duration = duration_raw
    resolution = "1080p" if quality == "final" else "720p"
    selected_model = row.get("model") or model
    input_payload: dict[str, object] = {
        "prompt": row.get("prompt", ""),
        "aspect_ratio": aspect,
        "duration": duration,
        "resolution": resolution,
        "generate_audio": False,
    }
    if row.get("start_image"):
        input_payload["start_image"] = row["start_image"]
    if row.get("end_image"):
        input_payload["end_image"] = row["end_image"]
    refs = [part.strip() for part in row.get("reference_images", "").split(",") if part.strip()]
    if refs and not ("seedance" in selected_model.lower() and row.get("end_image")):
        input_payload["reference_images"] = refs
    return {
        "shot_id": row["shot_id"],
        "tool": "generate_video",
        "model": selected_model,
        "input": input_payload,
        "sync": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    parser.add_argument("--model", default="auto", help="Model ID or auto")
    parser.add_argument("--quality", choices=["draft", "final"], default="draft")
    parser.add_argument("--dry-run", action="store_true", help="Accepted for compatibility; payloads are always written without submission")
    args = parser.parse_args()

    root = project_root(args.project)
    jobs_dir = root / "04_generation/jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    manifest = root / "04_generation/manifests/video_jobs.csv"
    rows = [row for row in read_csv(manifest) if row.get("status") in {"approved_for_video", "retake"}]
    model = resolve_model(args.model, args.quality)
    payloads = [payload_for(row, model, args.quality) for row in rows]

    out = jobs_dir / "mcp-video-jobs.jsonl"
    out.write_text("\n".join(json.dumps(payload, sort_keys=True) for payload in payloads) + ("\n" if payloads else ""), encoding="utf-8")
    print(f"MCP payloads: {out}")
    print(f"Jobs: {len(payloads)}")
    print("Submit these payloads with the connected Krea MCP generate_video tool, then write returned job ids to jobs.tsv.")


if __name__ == "__main__":
    main()
