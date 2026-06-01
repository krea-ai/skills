# Krea AI Skills

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![version](https://img.shields.io/badge/version-0.2.1-green.svg)](VERSION)
[![skills](https://img.shields.io/badge/skills-2-purple.svg)](#install-the-skills)
[![discord](https://img.shields.io/badge/discord-join-5865F2?logo=discord&logoColor=white)](https://discord.com/invite/krea-1002244500581798028)

Two Agent Skills for working with [Krea.ai](https://krea.ai). Install once, get both.

| Skill | When to use |
|---|---|
| **`krea-ai`** | Canonical intent-first router. Image, video, enhancement, LoRA, product photography, archviz, and campaign workflows via the Krea CLI by default, with MCP as fallback. |
| **`krea-build`** | Patterns for developers writing apps that integrate the Krea API: auth, polling, error handling, validation, frontend snippets for SvelteKit / React / Vue. Also the place to generate repeatable pipeline scripts in the user's own stack. |

Works with Claude Code, Cursor, Codex, Windsurf, OpenCode, Gemini CLI, OpenClaw, and any agent that picks up `~/.<agent>/skills/<name>/SKILL.md`.

## Install the skills

```bash
npx skills add krea-ai/skills
```

Installs both skills. This is the supported install path across agents that use skill packages.

## Prerequisites — one of these

The skills use the Krea CLI by default. If the CLI is unavailable but your agent has the Krea MCP connected, MCP works as a fallback.

```bash
# Default — Krea CLI (universal, works with any agent that runs bash)
npm install -g @krea-ai/cli
krea auth login          # prompts for a Krea API key and stores it locally
# OR: export KREA_API_KEY=...

# Fallback — Krea MCP server
# If your agent has Krea MCP connected, this skill can use it as fallback.
```

Verify the default path with `krea doctor`. If you are using the fallback path, check your agent's MCP tool list for `mcp__krea-public-api__*` tools.

## Use

### Default - `krea-ai` routes by intent

```
> Generate an image of a cyberpunk cat in neon rain.
> Make a 5-second video of waves at sunset.
> Upscale this photo to 4K.
```

These stay in `krea-ai` and route to the right model via the live CLI / MCP catalog.

```
> Render this Sketchup screenshot in golden hour, photoreal.
> Make my Revit model interior look photoreal, midday.
> Take this chair, put it in this room, in this style.
```

These route through `krea-ai/workflows/archviz-3d-to-render.md` for structural-reference archviz rendering.

```
> Make a hero product shot of my new perfume bottle.
> Generate a TikTok ad for my sneakers.
> Take this product URL and give me a hero + 4 social variants.
```

These route through `krea-ai/workflows/` recipes for product photography, social video, campaigns, and LoRA-backed consistency.

```
> Help me add a Krea image generator to my SvelteKit app.
> Set up server-side polling for video generation in my Next.js app.
> Give me a repeatable pipeline script for my product launch workflow.
```

These trigger `krea-build` - developer-focused integration patterns. The agent generates code in your stack (TypeScript, Python, Bash - whatever fits).

## Updates

The `krea-ai` skill includes an opt-in update notification. Once per session, the agent may run `krea-ai/scripts/update-check.sh`, which checks `https://raw.githubusercontent.com/krea-ai/skills/main/VERSION` against the installed `krea-ai/VERSION` file. If a newer version exists, it prints `UPGRADE_AVAILABLE <local> <remote>` to stdout — the agent surfaces this once, then continues. Snoozes 24h → 48h → 7d to avoid nagging.

**To upgrade**, re-run your install command (`npx skills add krea-ai/skills`, etc.).

**To disable the check**: `touch ~/.krea-skills/update-check-disabled`.

**To force a fresh check**: `bash krea-ai/scripts/update-check.sh --force`.

Single-source version: `VERSION` file at repo root. CI enforces that `krea-ai/VERSION`, all SKILL.md frontmatters, plugin manifests, and `package.json` agree.

## Evals

`evals/run.sh` runs 22 regression scenarios through `claude -p` in headless mode and grades responses with regex (PASS / FAIL / MANUAL_REVIEW). See `evals/README.md` for methodology.

```bash
bash evals/run.sh                 # v1 — regex + manual review
bash evals/run.sh --judge         # v2 — Claude-CLI judge (disabled in v1)
```

## License

MIT
