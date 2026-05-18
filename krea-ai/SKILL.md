---
version: 0.2.0
name: krea-ai
description: "Generate images, videos, enhance/upscale, train LoRAs, and run campaign workflows through Krea. Intent-first workflow prefabs route common asks to hard recipes for social video, image generation, product photography, archviz, enhancement, LoRA training, and ad campaigns."
license: MIT
---

# Krea AI - Generation, animation, enhancement

Use Krea through the CLI by default, with the Krea MCP server as fallback. This skill is organized around intent-first workflow prefabs: classify the user's verb + modality + flavor, load the matching `workflows/*.md`, and follow that recipe instead of improvising from a model menu.

For developers building apps that call Krea programmatically, use the sibling `krea-build/` skill instead.

## Bootstrap

Prefer the Krea CLI whenever it is installed and authenticated:

```bash
which krea && krea doctor 2>&1 | head -5
```

A healthy CLI prints `api auth` success for `list_models`. If the CLI is missing:

```bash
npm install -g @krea-ai/cli
krea auth login
# or export KREA_API_KEY=...
```

Use MCP only when the CLI is unavailable and Krea tools such as `list_models`, `get_model_schema`, `generate_image`, `generate_video`, `enhance_image`, `get_job`, and `upload_asset` are connected. If neither surface is available, stop and ask the user to install the CLI or connect MCP. Do not use direct HTTP for normal generation except documented flows such as LoRA training.

Before the first generation in a session, optionally run the passive update check if the installed repo path is known:

```bash
bash /path/to/skills/scripts/update-check.sh 2>/dev/null || true
```

It never blocks generation. Surface `UPGRADE_AVAILABLE` or `JUST_UPGRADED` once; otherwise stay quiet.

## Universal UX rules

1. Concise output. Send result path/URL plus one useful sentence. No raw IDs or JSON dumps.
2. Detect the user's language from their first message and reply in it. Technical params stay English.
3. Vision-first. Read attached images before generating, and read generated outputs before delivery.
4. No premature questions for cheap ops. For cheap images/enhance, pick sane defaults. For expensive ops, clarify once and run `references/cost-preflight.md`.
5. Progress reporting is mandatory for async polling over 30 seconds. Use `references/progress-reporting.md`.
6. Always call `list_models` before choosing a model. Use `references/model-catalog.md` to resolve archetypes to live IDs.
7. Always inspect the model schema before submitting. Do not guess field names such as `imageUrl`, `imageUrls`, `startImage`, `duration`, or `resolution`.
8. Upload local references to Krea before generation. Some models reject non-Krea-hosted URLs.
9. Honor `KREA_PREFERENCES.md` or a `## Krea preferences` section in project docs when present.
10. Do not pretend bad outputs are fine. Name the mismatch and offer a concrete retry path.

## Routing - intent -> workflow

| Intent (verb + modality + flavor) | Workflow |
|---|---|
| make a short vertical / social / TikTok / Reels / Shorts / GRWM video, <=15s | `workflows/social-video-short.md` |
| make a longer narrative video with hard cuts, >15s | `workflows/narrative-video-long.md` |
| animate a still / image-to-video / make this picture move | `workflows/image-to-video-animate.md` |
| make me an image (no quality bar stated, exploring) | `workflows/image-fast-iterate.md` |
| production-quality image / for delivery / hero asset | `workflows/image-final-render.md` |
| transform / edit / restyle this image | `workflows/image-edit-i2i.md` |
| poster / typography / text-heavy image | `workflows/image-text-poster.md` |
| portrait with face refs | `workflows/portrait-with-refs.md` |
| product hero photo / e-com hero shot | `workflows/product-photo-hero.md` |
| product lifestyle / model wearing / scene composition | `workflows/product-photo-lifestyle.md` |
| 3D screenshot -> photoreal render (archviz) | `workflows/archviz-3d-to-render.md` |
| upscale / 4K / enhance / make sharper | `workflows/enhance-upscale.md` |
| creative enhance / restyle / re-light | `workflows/enhance-creative.md` |
| train a LoRA / fine-tune on these images | `workflows/lora-train-and-use.md` |
| product URL -> full campaign | `workflows/full-ad-campaign.md` |

**Hard rule**: never call `generate video` without first loading a `workflows/*.md` file. Workflows enforce cost-preflight, clarify-once, storyboard approval for short video, progress pings, and banned-move lists. Bypassing them is what wasted ~5,000 CU on 2026-05-17.

## References

Load only what the active workflow needs:

- `references/cli-or-mcp.md` - side-by-side CLI and MCP operations.
- `references/model-catalog.md` - archetypes to resolve through live `list_models`.
- `references/media-inputs.md` - uploads, local files, image refs, start/end frames.
- `references/async-polling.md` - job lifecycle semantics.
- `references/prompt-engineering.md` - prompt handling by modality.
- `references/troubleshooting.md` - known CLI/model issues and recovery.
- `references/preferences.md` - project-level overrides.
- `references/cost-preflight.md` - mandatory approval before >100 CU or video/training jobs.
- `references/progress-reporting.md` - mandatory pings during long async polling.

## Related skill

Use `krea-build/` for developer integration work: API clients, frontend snippets, validation, and repeatable app code.

Marketing, product, campaign, and architectural visualization requests stay in this skill and route to `krea-ai/workflows/`:

- Marketing/product work: `workflows/product-photo-hero.md`, `workflows/product-photo-lifestyle.md`, `workflows/social-video-short.md`, `workflows/full-ad-campaign.md`.
- Architectural visualization: `workflows/archviz-3d-to-render.md`.

## Filename pattern

For local outputs, use `yyyy-mm-dd-hh-mm-ss-short-name.ext` with `.png` for images and `.mp4` for videos. Keep short names lowercase and hyphenated.
