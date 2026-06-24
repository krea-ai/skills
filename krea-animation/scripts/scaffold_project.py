#!/usr/bin/env python3
"""Scaffold a file-based animation production project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import ensure_dirs, project_root, render_template, write_if_missing


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Project directory to create")
    parser.add_argument("--title", required=True, help="Production title")
    parser.add_argument("--runtime", required=True, type=int, help="Target runtime in seconds")
    parser.add_argument("--aspect", default="16:9", help="Delivery aspect ratio")
    parser.add_argument("--fps", default=24, type=int, help="Delivery frame rate")
    parser.add_argument("--force", action="store_true", help="Overwrite template files that already exist")
    args = parser.parse_args()

    root = project_root(args.project)
    values = {
        "TITLE": args.title,
        "RUNTIME": str(args.runtime),
        "ASPECT": args.aspect,
        "FPS": str(args.fps),
        "SCENE_ID": "SC001",
        "SHOT_ID": "SC001_SH010",
    }

    ensure_dirs(root)

    created = []
    template_map = {
        "brief.md": "00_brief/brief.md",
        "style-guide.md": "01_bible/style/style-guide.md",
        "characters.csv": "01_bible/characters/characters.csv",
        "props.csv": "01_bible/props/props.csv",
        "worlds.csv": "01_bible/worlds/worlds.csv",
        "script.md": "02_story/script.md",
        "beat-sheet.md": "02_story/beat-sheet.md",
        "storyboard.md": "02_story/storyboard.md",
        "shot.md": "03_shots/SC001/SH010/shot.md",
        "delivery-checklist.md": "06_qa/delivery-checklist.md",
        "retakes.csv": "06_qa/retakes.csv",
        "assets.csv": "04_generation/manifests/assets.csv",
    }

    for template_name, rel_path in template_map.items():
        content = render_template(template_name, values)
        path = root / rel_path
        if write_if_missing(path, content, force=args.force):
            created.append(rel_path)

    for rel_path, content in {
        "04_generation/manifests/keyframes.csv": "shot_id,role,path_or_url,status,notes\n",
        "04_generation/manifests/video_jobs.csv": "shot_id,duration,model,aspect,start_image,end_image,reference_images,prompt,status\n",
        "04_generation/manifests/durations.tsv": "",
        "04_generation/manifests/concat-list.txt": "",
        "04_generation/jobs/jobs.tsv": "",
        "04_generation/jobs/results.tsv": "",
    }.items():
        if write_if_missing(root / rel_path, content, force=args.force):
            created.append(rel_path)

    project_json = {
        "title": args.title,
        "runtime_seconds": args.runtime,
        "aspect": args.aspect,
        "fps": args.fps,
        "schema": "krea-animation-v1",
    }
    if write_if_missing(root / "project.json", json.dumps(project_json, indent=2) + "\n", force=args.force):
        created.append("project.json")

    print(f"Project scaffolded: {root}")
    print(f"Created/updated {len(created)} files")
    for rel in created:
        print(f"  {rel}")


if __name__ == "__main__":
    main()
