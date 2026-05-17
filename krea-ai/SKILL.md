---
version: 0.2.0
name: krea-ai
description: "Generate images, videos, and enhance/upscale through Krea's full model lineup via the Krea CLI by default, with Krea MCP as a fallback. Routes intent to the right model from a live catalog (Flux, Imagen, GPT Image, Ideogram, Seedream for images; Kling, Veo, Hailuo, Wan for video; Topaz for upscaling) without hardcoding model names. Use when the user wants to generate an image or video, enhance a photo, animate a still, or build a multi-step creative workflow. For LoRA training and repeatable pipelines, see references/lora-training.md and references/pipelines.md."
license: MIT
---

# Krea AI — Image, Video, Enhance

Generate creative output through the **Krea CLI** (`krea`) by default. If the CLI is unavailable but the **Krea public API MCP server** (`mcp__krea-public-api__*`) is connected, use MCP as the fallback.

For developers building apps that call Krea programmatically (frontend integration, API client patterns, validation), see the sibling `krea-build` skill instead.

## Bootstrap

This skill works with the **Krea CLI** or the **Krea MCP server**. Both hit the same backend. Prefer the CLI whenever it is installed and authenticated; use MCP only when the CLI is unavailable but MCP tools are connected.

### Preferred: CLI

Check for the Krea CLI first:

```bash
which krea && krea doctor 2>&1 | head -5
```

A healthy CLI prints `✓ api auth     list_models call succeeded`. If `krea` isn't on PATH:

```bash
npm install -g @krea-ai/cli
krea auth login    # one-time, stores OAuth in OS keyring
# OR: export KREA_API_KEY=...
```

Once installed, use CLI commands for Krea operations. See `references/cli-or-mcp.md` for the parallel operation table.

### Fallback: MCP

Tools you should see in the agent's tool list:

- `mcp__krea-public-api__list_models`
- `mcp__krea-public-api__get_model_schema`
- `mcp__krea-public-api__generate_image`
- `mcp__krea-public-api__generate_video`
- `mcp__krea-public-api__enhance_image`
- `mcp__krea-public-api__get_job`
- `mcp__krea-public-api__upload_asset`

If the CLI is unavailable and these tools are present, use MCP. The MCP handles auth and validation.

### Neither available

Stop and tell the user: *"This skill needs the Krea CLI installed (`npm install -g @krea-ai/cli && krea auth login`) or the Krea MCP connected. Which do you want to set up?"* Don't fall back to direct HTTP for normal generation. Direct HTTP is only for documented custom workflows like LoRA training or code the agent writes via `krea-build`.

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
2. **No premature questions — except for video.** For images and enhance, pick a sane default model and submit. For **video**, do the opposite: clarify and storyboard first (see rule 7 and `references/storyboard-method.md`). Video jobs are 10–12 min and ≥1000 CU each; silently picking a default wastes both.
3. **Don't proactively explain model selection.** If the user asks ("why this model?", "what about X?") then explain in one line. Otherwise stay silent on the choice.
4. **Detect the user's language** from their first message and reply in it. Technical args (parameter names, IDs) stay English.
5. **Vision-first.**
   - When the user attaches an image, `Read` it with vision **before** generating to understand context.
   - When generation finishes, download the result and `Read` it. Verify it matches the brief. If it clearly doesn't, say so and offer to retry — don't pretend a bad output is fine.
   - Vision here is the agent's own image reading (`Read` tool on local files). It is **different** from `upload_asset`, which sends a file to Krea's servers as a reference for a model. Use both, for different purposes.
6. **No raw model IDs in chat output.** Mention model names only if the user asks.
7. **Video requires clarify → storyboard → approval before `generate video`.**
   - **Clarify in one short message** (single batched ask — skip whatever the user already volunteered): aspect (9:16 / 16:9 / 1:1), duration (5 / 10 / 15s), one-line concept/mood, identity refs needed (face photos / brand assets), style notes, and 4–6 key beats.
   - **Generate the storyboard first** (cheap, fast, image-only). Default to 1 storyboard when the brief is tight; offer 2–3 variations when it's loose. Use an editorial-text-friendly image model (e.g. `openai/gpt-image-2` at the time of writing — confirm via `list_models`). Storyboard aspect does not need to match final video aspect; pick whatever fits the grid.
   - **Show the user the storyboard(s) and wait for the pick.** Iterate on the storyboard (cheap) before kicking off video (expensive). Never submit a video job for a storyboard the user hasn't approved.
   - **Then animate** with `bytedance/seedance-2` (not `seedance-2-fast` unless the user asks for speed) at 720p, using the chosen aspect and a TIMELINE-format prompt. See `references/storyboard-method.md` for the prompt template, the `--start-image` aspect-lock trap, the "slow / gentle / soft" → slow-motion trap, and `--aspect` / `referenceImages` / Krea-hosted asset URL handling.
   - For >15s narrative work with hard cuts across distinct subjects or locations, fall back to the multi-scene approach in `references/video-production.md`.

## Workflow

### 1. Read project preferences (if present)

Check for a `KREA_PREFERENCES.md` at the repo root, or a `## Krea preferences` section inside `CLAUDE.md`. If found, apply its model choices over the defaults. See `references/preferences.md` for the format.

### 2. If the user attached an image, read it with vision

Use `Read` on the local file. This grounds your interpretation of the brief in what's actually in the image, before choosing a model or writing a prompt.

### 3. Discover available models

**CLI:**
```bash
krea models list --json
```

**MCP fallback:**
```
mcp__krea-public-api__list_models()
```

Both return `{id, category, name, description}` per model. Always call before generating — model lineups change. Never hardcode IDs from memory.

### 4. Route intent → candidate model (or hand off to a vertical skill)

**First, check whether the brief belongs to a vertical skill.** If yes, load the vertical's `SKILL.md` and follow it instead of the rest of this workflow. The vertical skills are deeper in their domain than this generic router.

- **Architectural / interior / exterior / 3D-screenshot-to-render / facade / moodboard for a building** → load `../krea-archviz/SKILL.md`
- **Product photo / ad / commercial / DTC / TikTok / Instagram / brand creative / UGC / social media** → load `../krea-marketing/SKILL.md`
- **Developer integration / app-building / API client / frontend snippets** → load `../krea-build/SKILL.md`

If the brief doesn't clearly match a vertical, stay here and pick from the generic archetypes.

Consult `references/model-catalog.md` for archetypes (fast draft, photoreal, cinematic, image-to-video, etc.). For each archetype it tells you which keywords to scan in `list_models` `name`/`description` to find a current match.

### 5. Inspect the model's accepted inputs

**CLI:**
```bash
krea models show <chosen_id> --json
```

**MCP fallback:**
```
mcp__krea-public-api__get_model_schema(model="<chosen_id>")
```

Returns the full input/output schema. Use this to know which params (`prompt`, `aspectRatio`, `imageUrl`/`imageUrls`, `startImage`, `duration`, `resolution`, etc.) the model accepts. Don't guess.

### 6. Upload local references if needed

For image-to-image, face refs, start frames, or audio refs that live as local files:

**CLI:**
```bash
URL=$(krea upload ./photo.png --json | jq -r .url)
```

The CLI takes the file path directly — no base64 encoding needed. Pass the returned asset URL into the next call's `input.imageUrl` / `input.imageUrls` / `input.startImage` per the model's schema.

**MCP fallback:**
```
upload = upload_asset(filename, mimeType, fileData=<base64-encoded-bytes>)
```

### 7. Submit

**Images and enhancement** finish fast. Use sync.

**CLI:**
```bash
krea generate image -m <id> -p "..." --aspect 16:9 --wait -o ./out.png
krea generate enhance -m <id> <url> --width 4096 --height 4096 --wait -o ./out-4k.png
```

The CLI's `-o ./path.png` implies `--wait` and downloads in one step.

**MCP fallback:**
```
result = generate_image(model=<id>, input={prompt, ...}, sync=true, timeoutSeconds=60)
result = enhance_image(model=<id>, input={imageUrl, width, height, ...}, sync=true, timeoutSeconds=60)
```

**Video** routinely runs longer than the 300s sync cap. Always async + poll. **And** — per UX rule 7 — never submit a video job until you have a user-approved storyboard. See `references/storyboard-method.md` for the canonical short-format flow.

**CLI:**
```bash
JOB=$(krea generate video -m <id> -p "..." --json | jq -r .job_id)
krea jobs wait $JOB --json   # blocks server-side until terminal
```

`krea jobs wait` does the polling for you — no loop in your code. See `references/async-polling.md` for status semantics and `references/cli-or-mcp.md` for the full parallel reference.

**MCP fallback:**
```
job = generate_video(model=<id>, input={prompt, ...}, sync=false)
# loop:
status = get_job(jobId=job.id)
# break when status is terminal (`completed`, `failed`, `cancelled`)
# sleep ~10s between polls
```

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

- `references/cli-or-mcp.md` — operation reference: MCP and CLI commands side-by-side
- `references/model-catalog.md` — intent → archetype, keyword hints for filtering `list_models` output
- `references/preferences.md` — per-project overrides (`KREA_PREFERENCES.md`)
- `references/prompt-engineering.md` — prompt-writing tips per modality
- `references/media-inputs.md` — uploads, image-to-image, multi-reference, start/end frames
- `references/async-polling.md` — the 300s sync cap, exact `get_job` loop
- `references/troubleshooting.md` — error codes and what they mean
- `references/cookbook.md` — five worked end-to-end recipes
- `references/storyboard-method.md` — **canonical** short-format video workflow (≤15s vertical/square): clarify → storyboard → approval → `seedance-2` timeline prompt
- `references/video-production.md` — multi-scene shot-list workflow for longer narrative work (>15s, hard cuts, multiple subjects/locations)
- `references/pipelines.md` — multi-step orchestration patterns (agent-driven and via `krea-build` for repeatable scripts in the user's stack)
- `references/lora-training.md` — LoRA training API surface and language-neutral examples

## Vertical skills

When the brief clearly belongs to a vertical, hand off:

- **`../krea-archviz/SKILL.md`** — architectural visualization, 3D-screenshot-to-render, materials, lighting, multi-image composition for architects and arch-viz professionals
- **`../krea-marketing/SKILL.md`** — product photography, video ads, brand-consistent batch generation, click-to-ad for DTC and commercial creative
- **`../krea-build/SKILL.md`** — patterns for developers writing apps that call Krea programmatically (different audience: developers, not generators)

Each vertical skill has deeper workflows, prompt templates, and UX rules specific to its domain. Routing to a vertical loads its full SKILL.md plus any `references/` it needs; it doesn't re-read this file.
