#!/usr/bin/env python3
"""Build a self-contained Codex plugin zip for Krea."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path
from typing import Any


PLUGIN_NAME = "krea"
DEFAULT_OUTPUT = Path("codex-plugin/dist/krea-codex-plugin.zip")
SOURCE_MANIFEST = Path(".codex-plugin/plugin.json")
OVERRIDES_PATH = Path("codex-plugin/plugin-overrides.json")
MCP_SOURCE = Path("codex-plugin/.mcp.json")
ASSETS_SOURCE = Path("codex-plugin/assets")
SKILLS_DEST = Path("skills")

SKIP_DIRS = {
    ".git",
    ".github",
    ".claude-plugin",
    ".codex-plugin",
    ".cursor-plugin",
    ".cursor",
    "codex-plugin",
    "node_modules",
    "__pycache__",
    "runs",
    "research",
    "clawhub",
}
SKIP_SUFFIXES = {
    ".pyc",
    ".pdf",
    ".mp4",
    ".mov",
    ".wav",
    ".aiff",
    ".psd",
}
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Zip path to write. Defaults to {DEFAULT_OUTPUT}.",
    )
    parser.add_argument(
        "--staging-dir",
        type=Path,
        help="Optional directory to keep the assembled plugin root for inspection.",
    )
    parser.add_argument(
        "--include-wip",
        action="store_true",
        help="Package skills currently stored under wip/.",
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="Assemble and validate the plugin root but do not write a zip.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    output_path = (repo_root / args.output).resolve() if not args.output.is_absolute() else args.output

    if args.staging_dir is not None:
        staging_root = (
            repo_root / args.staging_dir
            if not args.staging_dir.is_absolute()
            else args.staging_dir
        ).resolve()
        if staging_root.exists():
            shutil.rmtree(staging_root)
        staging_root.mkdir(parents=True)
        cleanup = None
    else:
        cleanup = tempfile.TemporaryDirectory(prefix="krea-codex-plugin-")
        staging_root = Path(cleanup.name)

    try:
        build_plugin_root(
            repo_root=repo_root,
            staging_root=staging_root,
            include_wip=args.include_wip,
        )
        validate_plugin_root(staging_root)

        if not args.no_zip:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            write_zip(staging_root, output_path)
            print(f"Wrote {output_path.relative_to(repo_root)}")
        if args.staging_dir is not None:
            print(f"Staged plugin root at {staging_root}")
    finally:
        if cleanup is not None:
            cleanup.cleanup()

    return 0


def build_plugin_root(*, repo_root: Path, staging_root: Path, include_wip: bool) -> None:
    manifest = load_json(repo_root / SOURCE_MANIFEST)
    overrides = load_json(repo_root / OVERRIDES_PATH)
    manifest = deep_merge(manifest, overrides)
    manifest["name"] = PLUGIN_NAME
    manifest["skills"] = "./skills/"
    manifest["mcpServers"] = "./.mcp.json"
    manifest.pop("apps", None)
    normalize_manifest(manifest)

    write_json(staging_root / ".codex-plugin" / "plugin.json", manifest)
    copy_mcp_config(repo_root, staging_root)
    copy_assets(repo_root, staging_root)
    copy_skills(repo_root, staging_root, include_wip=include_wip)

    for extra in ("README.md", "LICENSE", "VERSION"):
        source = repo_root / extra
        if source.is_file():
            shutil.copy2(source, staging_root / extra)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def normalize_manifest(manifest: dict[str, Any]) -> None:
    interface = manifest.setdefault("interface", {})
    if not isinstance(interface, dict):
        raise ValueError("plugin.json interface must be an object")

    prompts = interface.get("defaultPrompt")
    if isinstance(prompts, list):
        interface["defaultPrompt"] = [str(prompt)[:128] for prompt in prompts[:3]]
    elif isinstance(prompts, str):
        interface["defaultPrompt"] = prompts[:128]

    manifest["keywords"] = sorted({str(keyword) for keyword in manifest.get("keywords", [])})


def copy_mcp_config(repo_root: Path, staging_root: Path) -> None:
    source = repo_root / MCP_SOURCE
    if not source.is_file():
        raise FileNotFoundError(f"Missing MCP config: {source}")
    shutil.copy2(source, staging_root / ".mcp.json")


def copy_assets(repo_root: Path, staging_root: Path) -> None:
    source_root = repo_root / ASSETS_SOURCE
    if not source_root.is_dir():
        return
    for source in sorted(source_root.rglob("*")):
        if not source.is_file() or should_skip_asset_file(source):
            continue
        relative = source.relative_to(source_root)
        target = staging_root / "assets" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def copy_skills(repo_root: Path, staging_root: Path, *, include_wip: bool) -> None:
    skills = discover_skills(repo_root, include_wip=include_wip)
    if not skills:
        raise ValueError("No skill directories found")

    seen: set[str] = set()
    for skill_name, source_root in skills:
        if skill_name in seen:
            raise ValueError(f"Duplicate skill name discovered: {skill_name}")
        seen.add(skill_name)

        target_root = staging_root / SKILLS_DEST / skill_name
        shutil.copytree(
            source_root,
            target_root,
            ignore=ignore_skill_entries,
            copy_function=shutil.copy2,
        )


def discover_skills(repo_root: Path, *, include_wip: bool) -> list[tuple[str, Path]]:
    skills: list[tuple[str, Path]] = []
    for skill_md in sorted(repo_root.rglob("SKILL.md")):
        relative = skill_md.relative_to(repo_root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if not include_wip and relative.parts[0] == "wip":
            continue
        skill_root = skill_md.parent
        skill_name = read_skill_name(skill_md) or skill_root.name
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", skill_name):
            raise ValueError(f"Invalid skill name `{skill_name}` in {relative}")
        skills.append((skill_name, skill_root))
    return skills


def read_skill_name(skill_md: Path) -> str | None:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    for line in text[4:end].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def ignore_skill_entries(directory: str, entries: list[str]) -> set[str]:
    ignored: set[str] = set()
    for entry in entries:
        path = Path(directory) / entry
        if entry in SKIP_DIRS or entry.startswith(".env"):
            ignored.add(entry)
        elif path.is_file() and should_skip_file(path, Path(directory)):
            ignored.add(entry)
    return ignored


def should_skip_file(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    return any(part in SKIP_DIRS for part in relative.parts)


def should_skip_asset_file(path: Path) -> bool:
    if path.name.startswith(".") or path.suffix.lower() in SKIP_SUFFIXES:
        return True
    return any(part.startswith(".") or part == "__pycache__" for part in path.parts)


def validate_plugin_root(staging_root: Path) -> None:
    manifest_path = staging_root / ".codex-plugin" / "plugin.json"
    mcp_path = staging_root / ".mcp.json"
    skills_root = staging_root / "skills"

    manifest = load_json(manifest_path)
    required_manifest_fields = ("name", "version", "description", "author", "skills", "mcpServers", "interface")
    for field in required_manifest_fields:
        if field not in manifest:
            raise ValueError(f"Packaged manifest is missing `{field}`")
    if manifest["name"] != PLUGIN_NAME:
        raise ValueError(f"Packaged manifest name must be `{PLUGIN_NAME}`")
    if manifest["skills"] != "./skills/":
        raise ValueError("Packaged manifest skills path must be `./skills/`")
    if manifest["mcpServers"] != "./.mcp.json":
        raise ValueError("Packaged manifest mcpServers path must be `./.mcp.json`")

    mcp = load_json(mcp_path)
    if not isinstance(mcp.get("mcpServers"), dict):
        raise ValueError(".mcp.json must contain an `mcpServers` object")

    if not skills_root.is_dir():
        raise ValueError("Packaged plugin is missing skills/")
    missing_skill_md = [
        path.name
        for path in sorted(skills_root.iterdir())
        if path.is_dir() and not (path / "SKILL.md").is_file()
    ]
    if missing_skill_md:
        raise ValueError(f"Packaged skills are missing SKILL.md: {', '.join(missing_skill_md)}")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise ValueError("Packaged manifest interface must be an object")
    for field in ("composerIcon", "logo"):
        assert_packaged_file(staging_root, interface.get(field), f"interface.{field}")
    for index, screenshot in enumerate(interface.get("screenshots", [])):
        assert_packaged_file(staging_root, screenshot, f"interface.screenshots[{index}]")


def assert_packaged_file(staging_root: Path, raw_path: Any, label: str) -> None:
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError(f"{label} must be a non-empty asset path")
    path = (staging_root / raw_path).resolve()
    if not path.is_relative_to(staging_root.resolve()) or not path.is_file():
        raise ValueError(f"{label} points to a missing file: {raw_path}")


def write_zip(staging_root: Path, output_path: Path) -> None:
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(staging_root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(staging_root).as_posix()
            info = zipfile.ZipInfo(relative)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = path.stat().st_mode
            permissions = stat.S_IMODE(mode)
            info.external_attr = permissions << 16
            archive.writestr(info, path.read_bytes())


if __name__ == "__main__":
    raise SystemExit(main())
