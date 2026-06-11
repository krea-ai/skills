---
version: 0.5.2
name: krea-generate
description: "Generate and transform media through Krea. Use for generic image generation, generic short video, image editing, enhancement/upscale, LoRA training, portraits, text-heavy images, and architectural visualization from 3D/CAD screenshots. For product, campaign, UGC, marketplace, or paid-social creative use krea-marketing. For professional animation, anime, storyboards, shotlists, and retakes use krea-animation. For app/API integration use krea-build."
license: MIT
---

# Krea Generate - Media Generation

Use Krea through whichever supported surface is available: an authenticated Krea CLI or connected Krea MCP tools. This skill handles Krea generation primitives and non-marketing creative workflows. It is not the marketing router and not the animation production router.

For developers building apps that call Krea programmatically, use `../krea-build/SKILL.md`.

## Bootstrap

Verify at least one Krea surface before generation. For CLI, check that `krea` exists and can reach the API:

```bash
command -v krea && krea doctor
```

For MCP, use the Krea tools only when they are present in the current agent tool list. If neither CLI nor MCP is available, ask the user to install/authenticate the CLI or connect MCP.

When using CLI, discover command shapes from `krea --help` and subcommand help. When using MCP, use the tool schemas exposed in the current session.

Before the first generation in a session, optionally run the passive update check only if this skill directory contains `scripts/update-check.sh`:

```bash
bash /path/to/krea-generate/scripts/update-check.sh 2>/dev/null || true
```

Surface `UPGRADE_AVAILABLE` or `JUST_UPGRADED` once; otherwise stay quiet.

## Universal Rules

1. Concise output. Send result path/URL plus one useful sentence. No raw IDs or JSON dumps.
2. Detect the user's language from their first message and reply in it. Technical params stay English.
3. Vision-first. Read attached images before generating, and read generated stills/frames before approving or reusing them. Use `references/vision-qa.md`.
4. For cheap images/enhance, pick the best live-discovered schema match. For video, training, batches, 4K, or >100 CU, run `references/cost-preflight.md`.
5. Progress reporting is mandatory for async polling over 30 seconds. Use `references/progress-reporting.md`.
6. Always list live models through the available surface before choosing a model, then inspect the selected model schema through that same surface. Do not choose from remembered model IDs or baked-in recommendations.
7. Normalize generation references to Krea-hosted assets before generation. Local files and arbitrary external media URLs must be uploaded to Krea first; already-Krea asset URLs can be passed directly.
8. Generic generation does not honor persistent model preference files. If the user explicitly names a model for the current request, verify it live and use it only if the schema fits.
9. Do not pretend bad outputs are fine. Name the mismatch and offer a concrete retry path.

## Routing

| Intent | Workflow |
|---|---|
| generic image / quick image draft | `workflows/image-fast-iterate.md` |
| production-quality image / final hero asset without product-marketing context | `workflows/image-final-render.md` |
| transform / edit / restyle this image | `workflows/image-edit-i2i.md` |
| poster / typography / text-heavy image | `workflows/image-text-poster.md` |
| portrait with face refs | `workflows/portrait-with-refs.md` |
| generic short video / text-to-video / non-ad clip | `workflows/video-generic-short.md` |
| 3D screenshot -> photoreal render / archviz | `workflows/archviz-3d-to-render.md` |
| upscale / 4K / enhance / make sharper | `workflows/enhance-upscale.md` |
| creative enhance / relight / faithful restyle | `workflows/enhance-creative.md` |
| train a LoRA / fine-tune on these images | `workflows/lora-train-and-use.md` |
| product photo / campaign / ad / UGC / key visual / marketplace card / paid social | use `../krea-marketing/SKILL.md` |
| professional animation / anime / storyboard-to-video / shotlist / retakes | use `../krea-animation/SKILL.md` |

Never submit a video generation job without loading a workflow. For marketing video, route to `krea-marketing`; for production animation or storyboarded narrative, route to `krea-animation`.

## References

Load only what the active workflow needs:

- `references/cli-or-mcp.md` - verify that CLI or MCP is available; discover operation shape from the chosen surface.
- `references/model-catalog.md` - archetypes to resolve through live `list_models`.
- `references/media-inputs.md` - uploads, local files, image refs, start/end frames.
- `references/async-polling.md` - job lifecycle semantics.
- `references/prompt-engineering.md` - prompt handling by modality.
- `references/vision-qa.md` - output inspection and retake discipline.
- `references/preferences.md` - model-selection boundary: no generic model pins.
- `references/cost-preflight.md` - approval before expensive operations.
- `references/budget-tracking.md` - running CU tracker.
- `references/progress-reporting.md` - mandatory pings during long async polling.
- `references/troubleshooting.md` - known CLI/model issues and recovery.
- `references/models/` - per-model prompting playbooks. Load only after resolving that model; for resolved Krea 2 or any moodboard work - discovery, preset-gallery search, or moodboard-driven generation - load `references/models/krea-2.md`.

## Related Skills

- `../krea-marketing/SKILL.md` - product photos, marketplace cards, campaigns, UGC/social ads, Meta Ads CLI/MCP performance context, and paid-social activation.
- `../krea-animation/SKILL.md` - studio-style animation production, anime, shotlists, keyframes, generated clips, edit assembly, QA, and retakes.
- `../krea-build/SKILL.md` - API clients, frontend snippets, validation, and repeatable app code.

## Filename Pattern

For local outputs, use `yyyy-mm-dd-hh-mm-ss-short-name.ext` with `.png` for images and `.mp4` for videos. Keep short names lowercase and hyphenated.
