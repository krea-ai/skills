# Krea AI Skills

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![version](https://img.shields.io/badge/version-0.1.0-green.svg)](VERSION)
[![skills](https://img.shields.io/badge/skills-4-purple.svg)](#install-the-skills)
[![discord](https://img.shields.io/badge/discord-join-5865F2?logo=discord&logoColor=white)](https://discord.com/invite/krea-1002244500581798028)

Four Agent Skills for working with [Krea.ai](https://krea.ai). Install once, get all four.

| Skill | When to use |
|---|---|
| **`krea-ai`** | Default router. Image, video, enhancement via the Krea CLI by default, with MCP as fallback. Routes to a vertical skill automatically when the brief is clearly arch-viz or marketing. |
| **`krea-archviz`** | Architectural visualization. 3D-screenshot-to-render, materials vocabulary, lighting recipes, multi-image composition. For architects, interior designers, archviz professionals. |
| **`krea-marketing`** | Commercial creative. Product photography (hero, lifestyle, white-bg, social), video ads (UGC, talking head, demo, before/after), brand-consistent batch generation, click-to-ad from URL. For DTC brands, marketing teams, social media managers. |
| **`krea-build`** | Patterns for developers writing apps that integrate the Krea API: auth, polling, error handling, validation, frontend snippets for SvelteKit / React / Vue. Also the place to generate repeatable pipeline scripts in the user's own stack. |

Works with Claude Code, Cursor, Codex, Windsurf, OpenCode, Gemini CLI, OpenClaw, and any agent that picks up `~/.<agent>/skills/<name>/SKILL.md`.

## Prerequisites — one of these

The skills use the Krea CLI by default. If the CLI is unavailable but your agent has the Krea MCP connected, MCP works as a fallback.

```bash
# Default — Krea CLI (universal, works with any agent that runs bash)
npm install -g @krea-ai/cli
krea auth login          # OAuth, stores in OS keyring
# OR: export KREA_API_KEY=...

# Fallback — Krea MCP server
# Already connected if your agent (Claude Code / Cursor / etc.) supports MCP.
# Nothing to install.
```

Verify the default path with `krea doctor`. If you are using the fallback path, check your agent's MCP tool list for `mcp__krea-public-api__*` tools.

## Install the skills

### npm (works across all agents)

```bash
npx skills add krea-ai/skills
```

Installs all four skills.

### Claude Code marketplace

```
/plugin marketplace add krea-ai/skills
/plugin install krea@krea
```

Registers each skill as `/krea:ai`, `/krea:archviz`, `/krea:marketing`, `/krea:build`.

### Codex CLI

```bash
codex skill install krea-ai/skills
```

### Cursor

```bash
cursor extension install krea-ai/skills
```

### Manual (universal fallback)

```bash
git clone https://github.com/krea-ai/skills.git
cd skills
# Symlink each skill into your agent's expected directory.
```

## Use

### Default — `krea-ai` and the vertical skills auto-route

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

These trigger `krea-archviz` — vertical-specific archviz workflows, materials vocabulary, lighting recipes.

```
> Make a hero product shot of my new perfume bottle.
> Generate a TikTok ad for my sneakers.
> Take this product URL and give me a hero + 4 social variants.
```

These trigger `krea-marketing` — product photography, video ads, click-to-ad from URL, brand-consistent batch generation.

```
> Help me add a Krea image generator to my SvelteKit app.
> Set up server-side polling for video generation in my Next.js app.
> Give me a repeatable pipeline script for my product launch workflow.
```

These trigger `krea-build` — developer-focused integration patterns. The agent generates code in your stack (TypeScript, Python, Bash — whatever fits).

## Updates

The skill includes an opt-in update notification. Once per session, the agent runs `scripts/update-check.sh` which checks `https://raw.githubusercontent.com/krea-ai/skills/main/VERSION` against the local `VERSION` file. If a newer version exists, it prints `UPGRADE_AVAILABLE <local> <remote>` to stdout — the agent surfaces this once, then continues. Snoozes 24h → 48h → 7d to avoid nagging.

**To upgrade**, re-run your install command (`npx skills add krea-ai/skills`, etc.).

**To disable the check**: `touch ~/.krea-skills/update-check-disabled`.

**To force a fresh check**: `bash scripts/update-check.sh --force`.

Single-source version: `VERSION` file at repo root. CI enforces that all SKILL.md frontmatters, plugin manifests, and `package.json` agree.

## Evals

`evals/run.sh` runs 20 regression scenarios through `claude -p` in headless mode and grades responses with regex (PASS / FAIL / MANUAL_REVIEW). See `evals/README.md` for methodology.

```bash
bash evals/run.sh                 # v1 — regex + manual review
bash evals/run.sh --judge         # v2 — Claude-CLI judge (disabled in v1)
```

## License

MIT
