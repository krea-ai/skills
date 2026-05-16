# Krea AI Skills

Four Agent Skills for working with [Krea.ai](https://krea.ai). Install once, get all four.

| Skill | When to use |
|---|---|
| **`krea-ai`** | Default router. Image, video, enhancement via the Krea MCP. Routes to a vertical skill automatically when the brief is clearly arch-viz or marketing. Ships standalone power-user Python scripts for multi-step pipelines and LoRA training. |
| **`krea-archviz`** | Architectural visualization. 3D-screenshot-to-render, materials vocabulary, lighting recipes, multi-image composition. For architects, interior designers, archviz professionals. |
| **`krea-marketing`** | Commercial creative. Product photography (hero, lifestyle, white-bg, social), video ads (UGC, talking head, demo, before/after), brand-consistent batch generation, click-to-ad from URL. For DTC brands, marketing teams, social media managers. |
| **`krea-build`** | Patterns for developers writing apps that integrate the Krea API: auth, polling, error handling, validation, frontend snippets for SvelteKit / React / Vue. |

Works with Claude Code, Cursor, Codex, Windsurf, OpenCode, Gemini CLI, OpenClaw, and any agent that picks up `~/.<agent>/skills/<name>/SKILL.md`.

## Install

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

These stay in `krea-ai` and route to the right model via the live MCP catalog.

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
```

These trigger `krea-build` — developer-focused integration patterns.

### Power-user scripts (optional)

For multi-step batch pipelines or LoRA training, the package ships standalone Python scripts:

- `krea-ai/scripts/pipeline.py` — multi-step pipelines (chain, fan-out, parallel, resume)
- `krea-ai/scripts/train_style.py` — LoRA training for brand styles, products, characters

Both require `KREA_API_KEY` set and `uv` installed.

## Repository structure

```
.
├── VERSION                        # repo-wide version (source of truth)
├── krea-ai/                       # router / generic generation
│   ├── SKILL.md
│   ├── references/                # loaded on demand
│   │   ├── model-catalog.md       # intent → archetype, no hardcoded IDs
│   │   ├── prompt-engineering.md
│   │   ├── media-inputs.md
│   │   ├── async-polling.md
│   │   ├── preferences.md
│   │   ├── video-production.md
│   │   ├── pipelines.md
│   │   ├── lora-training.md
│   │   ├── cookbook.md
│   │   └── troubleshooting.md
│   └── scripts/                   # power-user, bypass MCP
│       ├── pipeline.py
│       ├── train_style.py
│       └── krea_helpers.py
├── krea-archviz/                  # architectural visualization vertical
│   ├── SKILL.md
│   └── references/
│       ├── screenshot-to-render.md
│       ├── materials.md
│       ├── lighting.md
│       ├── composition.md
│       └── aspect-ratios.md
├── krea-marketing/                # commercial creative vertical
│   ├── SKILL.md
│   └── references/
│       ├── product-photography.md
│       ├── video-ads.md
│       ├── brand-consistency.md
│       ├── ad-formats.md
│       └── marketing-prompts.md
├── krea-build/                    # developer integration patterns
│   ├── SKILL.md
│   └── references/
│       ├── integration-patterns.md
│       ├── api-client.md
│       ├── validation.md
│       └── frontend-snippets.md
├── evals/                         # regression tests (20 scenarios)
│   ├── README.md
│   ├── scenarios.md
│   └── run.sh
├── scripts/
│   └── update-check.sh            # opt-in version check (run once per session)
├── .claude-plugin/                # Claude Code marketplace + plugin manifest
├── .codex-plugin/                 # Codex plugin manifest
├── .cursor-plugin/                # Cursor plugin manifest
├── .github/workflows/validate.yml # CI: frontmatter + version sync + path resolution + eval syntax
├── package.json
├── LICENSE
└── README.md
```

## Updates

The skill includes an opt-in update notification. Once per session, the agent runs `scripts/update-check.sh` which checks `https://raw.githubusercontent.com/krea-ai/skills/main/VERSION` against the local `VERSION` file. If a newer version exists, it prints `UPGRADE_AVAILABLE <local> <remote>` to stdout — the agent surfaces this once, then continues. Snoozes 24h → 48h → 7d to avoid nagging.

**To upgrade**, re-run your install command (`npx skills add krea-ai/skills`, etc.).

**To disable the check**: `touch ~/.krea-skills/update-check-disabled`.

**To force a fresh check**: `bash scripts/update-check.sh --force`.

Single-source version: `VERSION` file at repo root. CI enforces that `VERSION`, `package.json`, all four `SKILL.md` files, and all four plugin manifests agree.

## API key (only for power-user scripts)

Get your key at [krea.ai/settings/api-tokens](https://krea.ai/settings/api-tokens). Set it as `KREA_API_KEY` for `pipeline.py` and `train_style.py`. The MCP-backed skills handle auth on their own. (Legacy `KREA_API_TOKEN` is still honored as a fallback, but is deprecated.)

## Evals

`evals/run.sh` runs 20 regression scenarios through `claude -p` in headless mode and grades responses with regex (PASS / FAIL / MANUAL_REVIEW). See `evals/README.md` for methodology.

```bash
bash evals/run.sh                 # v1 — regex + manual review
bash evals/run.sh --judge         # v2 — Claude-CLI judge (disabled in v1)
```

## License

MIT
