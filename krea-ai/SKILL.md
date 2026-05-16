---
version: 2.1.0
name: krea-ai
description: "Generate images, videos, and enhance/upscale through Krea's full model lineup via the Krea MCP. Routes intent to the right model from a live catalog (Flux, Imagen, GPT Image, Ideogram, Seedream for images; Kling, Veo, Hailuo, Wan for video; Topaz for upscaling) without hardcoding model names. Use when the user wants to generate an image or video, enhance a photo, animate a still, or build a multi-step creative workflow. For LoRA training and batch pipelines, see the scripts/ subfolder."
license: MIT
---

# Krea AI — Image, Video, Enhance

Generate creative output through the **Krea public API MCP server** (`mcp__krea-public-api__*`). The MCP owns auth, validation, and uploads. This skill teaches you how to use it well.

For developers building apps that call Krea programmatically (frontend integration, API client patterns, validation), see the sibling `krea-build` skill instead.

## Bootstrap

This skill requires the Krea MCP server. Tools you should see available:

- `mcp__krea-public-api__list_models`
- `mcp__krea-public-api__get_model_schema`
- `mcp__krea-public-api__generate_image`
- `mcp__krea-public-api__generate_video`
- `mcp__krea-public-api__enhance_image`
- `mcp__krea-public-api__get_job`
- `mcp__krea-public-api__upload_asset`

If they're missing, tell the user to install the Krea MCP and pause until they confirm. Don't fall back to the API directly — that's what `scripts/` is for, and only for batch pipelines and LoRA training.

### Self-update check (opt-in, ~50ms)

Once per session, before the first generation, run:

```bash
bash "$(dirname $(readlink -f .claude/skills/krea-ai/SKILL.md 2>/dev/null || echo /))/../../scripts/update-check.sh" 2>/dev/null || true
# or simply, if the repo path is known:
bash /path/to/skills/scripts/update-check.sh
```

The script prints **one of**:

- `UPGRADE_AVAILABLE <local> <remote>` — surface to the user once per session: *"Krea skill v\<remote\> is out. Update with `npx skills add krea-ai/skills` (or your install method)."* Then continue normally — the current version still works.
- `JUST_UPGRADED <old> <new>` — surface a single one-line confirmation: *"Krea skill upgraded from \<old\> to \<new\>."* Then continue.
- Nothing — you're current, snoozed, or the network failed silently. Continue.

The script never blocks generation. It's a passive notification. Snoozes itself (24h → 48h → 7d) so you don't nag the user every session about the same upgrade. Disable entirely by creating `~/.krea-skills/update-check-disabled`. State lives at `~/.krea-skills/`.

If the user is annoyed by the nag, tell them: `touch ~/.krea-skills/update-check-disabled`. If they want to re-check now, run with `--force`.

## UX Rules

1. **Be concise.** Send the result URL + a one-line summary. No raw IDs, no JSON dumps, no narration of `list_models`/`get_model_schema` chatter.
2. **No premature questions.** Pick a sane default model and submit. Ask only when the brief is genuinely ambiguous (e.g. "make a video" with no subject).
3. **Don't proactively explain model selection.** If the user asks ("why this model?", "what about X?") then explain in one line. Otherwise stay silent on the choice.
4. **Detect the user's language** from their first message and reply in it. Technical args (parameter names, IDs) stay English.
5. **Vision-first.**
   - When the user attaches an image, `Read` it with vision **before** generating to understand context.
   - When generation finishes, download the result and `Read` it. Verify it matches the brief. If it clearly doesn't, say so and offer to retry — don't pretend a bad output is fine.
   - Vision here is the agent's own image reading (`Read` tool on local files). It is **different** from `upload_asset`, which sends a file to Krea's servers as a reference for a model. Use both, for different purposes.
6. **No raw model IDs in chat output.** Mention model names only if the user asks.

## Workflow

### 1. Read project preferences (if present)

Check for a `KREA_PREFERENCES.md` at the repo root, or a `## Krea preferences` section inside `CLAUDE.md`. If found, apply its model choices over the defaults. See `references/preferences.md` for the format.

### 2. If the user attached an image, read it with vision

Use `Read` on the local file. This grounds your interpretation of the brief in what's actually in the image, before choosing a model or writing a prompt.

### 3. Discover available models

```
list_models()
```

Returns `{id, category, name, description}` for every supported model. Always call this first — model lineups change. Never hardcode model IDs from memory.

### 4. Route intent → candidate model (or hand off to a vertical skill)

**First, check whether the brief belongs to a vertical skill.** If yes, load the vertical's `SKILL.md` and follow it instead of the rest of this workflow. The vertical skills are deeper in their domain than this generic router.

- **Architectural / interior / exterior / 3D-screenshot-to-render / facade / moodboard for a building** → load `../krea-archviz/SKILL.md`
- **Product photo / ad / commercial / DTC / TikTok / Instagram / brand creative / UGC / social media** → load `../krea-marketing/SKILL.md`
- **Developer integration / app-building / API client / frontend snippets** → load `../krea-build/SKILL.md`

If the brief doesn't clearly match a vertical, stay here and pick from the generic archetypes.

Consult `references/model-catalog.md` for archetypes (fast draft, photoreal, cinematic, image-to-video, etc.). For each archetype it tells you which keywords to scan in `list_models` `name`/`description` to find a current match.

### 5. Inspect the model's accepted inputs

```
get_model_schema(model="<chosen_id>")
```

Returns the full input/output schema. Use this to know which params (`prompt`, `aspectRatio`, `imageUrl`/`imageUrls`, `startImage`, `duration`, `resolution`, etc.) the model accepts. Don't guess.

### 6. Upload local references if needed

For image-to-image, face refs, start frames, or audio refs that live as local files:

```
upload = upload_asset(filename, mimeType, fileData=<base64>)
```

Pass the returned asset id/url into the next call's `input.imageUrl` / `input.imageUrls` / `input.startImage` per the model's schema.

> **⚠️ Silent-drop warning — read before every reference call.**
>
> The Krea MCP returns HTTP 200 and produces text-to-image output **even when you pass a reference URL under the wrong key.** There is no validation error to catch. A "reasonable" guess like `image: "<url>"` on a model that wants `imageStyleRefs` will look like it worked, return a 200, deliver a completely unrelated image, and silently waste the credit.
>
> Mitigation rule (mandatory whenever you pass any reference media):
>
> 1. **Call `get_model_schema(model=<id>)` before every `generate_image` / `generate_video` / `enhance_image` invocation in a new session.** Do not skip this on the assumption that "the field name is probably `imageUrl`" — it's wrong on most models.
> 2. **Pass only keys present in `inputSchema.properties`.** Field names are case-sensitive AND vary per model — `imageUrl` (camelCase) on `bfl/flux-1-kontext-dev`, `image_url` (snake_case) on `topaz/standard-enhance`, `startImage` + `referenceImages` on `bytedance/seedance-2-fast`, `styleImages` + `imageStyleRefs` (NOT `image`) on `bfl/flux-1-dev`. See `references/media-inputs.md` for the full per-model table.
> 3. **After the call, vision-verify the output against the brief.** If you asked for image-to-image and got something unrelated to your reference, you probably hit the silent-drop trap — re-read the schema, fix the field name, and retry.
>
> Worked example. Don't do this — `bfl/flux-1-dev` has no `image` field, so this call drops the reference and returns a fresh text-to-image apple:
>
> ```json
> {"name":"generate_image","arguments":{
>   "model":"bfl/flux-1-dev",
>   "input":{
>     "prompt":"the same apple, but green",
>     "image":"https://gen.krea.ai/images/...apple.png"
>   },
>   "sync":true
> }}
> ```
>
> Do this instead — call `get_model_schema(model="bfl/flux-1-dev")`, see that the reference fields are `styleImages` and `imageStyleRefs`, then pass under the correct key per that model's schema.

### 7. Submit

**Images and enhancement** finish fast. Use sync:

```
result = generate_image(model=<id>, input={prompt, ...}, sync=true, timeoutSeconds=60)
result = enhance_image(model=<id>, input={imageUrl, width, height, ...}, sync=true, timeoutSeconds=60)
```

**Video** routinely runs longer than the MCP's 300s sync cap. Always async + poll:

```
job = generate_video(model=<id>, input={prompt, ...}, sync=false)
# loop:
status = get_job(jobId=job.id)
# break when status is terminal (`completed`, `failed`, `cancelled`)
# sleep ~10s between polls
```

See `references/async-polling.md` for the exact loop.

### 8. Deliver

1. Download the result file locally.
2. `Read` it with vision and verify it matches the brief.
3. Send the user the URL or saved path with a one-line summary (e.g. `Saved: 2026-05-13-cyberpunk-cat.png`).
4. If the output clearly didn't match (wrong subject, missing elements, garbled text), say so and ask whether to retry with a different model or refined prompt.

## Filename pattern

For files you save locally: `yyyy-mm-dd-hh-mm-ss-short-name.ext`.

- `.png` for images, `.mp4` for videos
- Short name: 1–5 lowercase hyphenated words from the prompt
- Example: prompt "a serene Japanese garden" → `2026-05-13-14-23-05-japanese-garden.png`

## Prompt handling

- For generation, pass the user's description as-is. Don't paraphrase unless it's clearly insufficient.
- For image-to-image, describe what *changes*, not what's already there ("transform into watercolor style" — not "a man in a coat, made into watercolor").
- For image-to-video, the start frame anchors the visual; the prompt should describe **motion** (camera moves, subject actions).

See `references/prompt-engineering.md` for more.

## Reference docs

Load on demand:

- `references/model-catalog.md` — intent → archetype, keyword hints for filtering `list_models` output
- `references/preferences.md` — per-project overrides (`KREA_PREFERENCES.md`)
- `references/prompt-engineering.md` — prompt-writing tips per modality
- `references/media-inputs.md` — uploads, image-to-image, multi-reference, start/end frames
- `references/async-polling.md` — the 300s sync cap, exact `get_job` loop
- `references/troubleshooting.md` — error codes and what they mean
- `references/cookbook.md` — five worked end-to-end recipes
- `references/video-production.md` — multi-scene shot-list workflow
- `references/pipelines.md` — running `scripts/pipeline.py` for batch jobs
- `references/lora-training.md` — running `scripts/train_style.py` to train custom styles

## Scripts (power-user, optional)

`scripts/` contains two standalone Python tools that bypass MCP and hit the Krea API directly. They're for use cases the MCP doesn't cover yet:

- `scripts/pipeline.py` — multi-step generation pipelines (chain, fan-out, template vars, parallel, resume). See `references/pipelines.md`.
- `scripts/train_style.py` — train LoRA styles. See `references/lora-training.md`.

Both need `KREA_API_KEY` set and run via `uv`. For day-to-day work, prefer the MCP.

## Vertical skills

When the brief clearly belongs to a vertical, hand off:

- **`../krea-archviz/SKILL.md`** — architectural visualization, 3D-screenshot-to-render, materials, lighting, multi-image composition for architects and arch-viz professionals
- **`../krea-marketing/SKILL.md`** — product photography, video ads, brand-consistent batch generation, click-to-ad for DTC and commercial creative
- **`../krea-build/SKILL.md`** — patterns for developers writing apps that call Krea programmatically (different audience: developers, not generators)

Each vertical skill has deeper workflows, prompt templates, and UX rules specific to its domain. Routing to a vertical loads its full SKILL.md plus any `references/` it needs; it doesn't re-read this file.
