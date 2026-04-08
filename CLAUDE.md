# Krea AI — Agent Skill

This repository is an agent skill for the Krea.ai API, distributed across multiple channels.

## Project Structure

- `SKILL.md` — Skill instructions (Agent Skills standard with YAML frontmatter)
- `PIPELINES.md` — Pipeline reference: JSON format, examples, advanced features
- `COOKBOOK.md` — 5 real-world recipes
- `scripts/` — Python scripts (uv run, inline dependencies)
- `build_clawhub.sh` — Generates `clawhub/` bundle for ClawHub upload (gitignored output)
- `.claude-plugin/marketplace.json` — Claude Code plugin marketplace config
- `package.json` — npm metadata for skillpm distribution

## Environment

- `KREA_API_TOKEN` — Required. Get one at https://krea.ai/settings/api-tokens

## Distribution Channels

- **Agent Skills** (recommended) — `npx skills add krea-ai/skills`
- **Manual** — Clone repo + set `KREA_API_TOKEN`
- **ClawHub** — Upload `clawhub/` folder to clawhub.ai/upload

## CI

- `.github/workflows/validate.yml` — Runs on push/PR: validates SKILL.md frontmatter, parses all scripts, verifies clawhub build works

## Path Convention

- Root `SKILL.md` uses relative paths (`scripts/generate_image.py`) — portable across all agents
- `clawhub/SKILL.md` uses `~/.codex/skills/krea/scripts/` — OpenClaw-specific convention
