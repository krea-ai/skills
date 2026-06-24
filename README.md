# Krea AI Skills

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![version](https://img.shields.io/badge/version-0.5.2-green.svg)](VERSION)
[![skills](https://img.shields.io/badge/skills-3-purple.svg)](#install-the-skills)
[![discord](https://img.shields.io/badge/discord-join-5865F2?logo=discord&logoColor=white)](https://discord.com/invite/krea-1002244500581798028)

Three packaged Agent Skills for working with [Krea.ai](https://krea.ai). Install once, get the Krea skill suite.

| Skill | When to use |
|---|---|
| **`krea-generate`** | Canonical generic-generation router. Image, video primitives, enhancement, edits, LoRA, portraits, text/poster work, and archviz through connected Krea MCP tools. |
| **`krea-marketing`** | Marketing creative workflow: product photoshoots, marketplace image sets, DTC static ad templates (one product photo → a library of on-brand ad formats), key visuals, UGC/social ads, campaign packs, and optional Meta Ads performance context. |
| **`krea-animation`** | Studio animation workflow: anime series, storyboard-to-video, shotlists, asset bibles, model sheets, keyframes, AI video clips, edit assembly, QA, and retakes. |

Experimental app-integration material lives under `wip/` and is not installed or packaged by default.

Works with Claude Code, Codex, Windsurf, OpenCode, Gemini, OpenClaw, and any agent that picks up `~/.<agent>/skills/<name>/SKILL.md`.

## Install the skills

```bash
npx skills add krea-ai/skills
```

Installs the packaged skills. This is the supported install path across agents that use skill packages.

## Prerequisites

The packaged Codex plugin uses a connected Krea MCP server.

Check your agent's MCP tool list for `mcp__krea__*` tools. If the tools are missing, connect or authenticate the Krea MCP server before using generation skills.

## Use

### Default - `krea-generate` routes generic generation

```
> Generate an image of a cyberpunk cat in neon rain.
> Make a 5-second video of waves at sunset.
> Upscale this photo to 4K.
```

These stay in `krea-generate` and route to the right model via the live MCP catalog.

```
> Render this Sketchup screenshot in golden hour, photoreal.
> Make my Revit model interior look photoreal, midday.
> Take this chair, put it in this room, in this style.
```

These route through `krea-generate/workflows/archviz-3d-to-render.md` for structural-reference archviz rendering.

```
> Make a hero product shot of my new perfume bottle.
> Generate a TikTok ad for my sneakers.
> Turn this one product photo into a set of on-brand static ad formats.
> Take this product URL and give me a marketplace full set plus social variants.
> Use Meta Ads performance context before making new ad creative.
```

These trigger `krea-marketing`. The agent starts with a compact creative intake. For paid-social, performance, campaign-analysis, catalog-performance, or activation work, it asks whether to connect performance context; otherwise it proceeds Krea-only from product refs, brand refs, and goals. Any live launch, budget, status, catalog, or publishing change stays gated and paused/draft by default unless explicitly approved.

## Updates

The `krea-generate` skill includes an opt-in update notification. Once per session, the agent may run `krea-generate/scripts/update-check.sh`, which checks `https://raw.githubusercontent.com/krea-ai/skills/main/VERSION` against the installed `krea-generate/VERSION` file. If a newer version exists, it prints `UPGRADE_AVAILABLE <local> <remote>` to stdout - the agent surfaces this once, then continues. Snoozes 24h -> 48h -> 7d to avoid nagging.

**To upgrade**, re-run your install command (`npx skills add krea-ai/skills`, etc.).

**To disable the check**: `touch ~/.krea-skills/update-check-disabled`.

**To force a fresh check**: `bash krea-generate/scripts/update-check.sh --force`.

Single-source version: `VERSION` file at repo root. CI enforces that `krea-generate/VERSION`, all SKILL.md frontmatters, plugin manifests, and `package.json` agree.

## Evals

`evals/run.sh` runs 40 regression scenarios through `claude -p` in headless mode and grades responses with regex (PASS / FAIL / MANUAL_REVIEW). See `evals/README.md` for methodology.

```bash
bash evals/run.sh                 # v1 — regex + manual review
bash evals/run.sh --judge         # v2 — Claude judge (disabled in v1)
```

## License

MIT
