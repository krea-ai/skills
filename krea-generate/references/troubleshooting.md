# Troubleshooting

## MCP tool missing

```
ToolError: mcp__krea-public-api__... is not available
```

The Krea MCP server isn't installed. The CLI is the default surface, so first check `which krea && krea doctor 2>&1 | head -5`. If the CLI is healthy, use it. If the CLI is unavailable and MCP is missing too, tell the user to install the CLI or connect the MCP. Don't fall back to direct HTTP for normal generation; direct HTTP is only for documented custom workflows like LoRA training or code generated via `krea-build`.

## Authentication

The MCP handles auth on the Krea side. If you see an explicit auth error from a tool call, the MCP server isn't properly configured. Surface it to the user - don't try to work around it.

## Validation errors

- **`Missing required params: prompt`** - the model needs a prompt; ask the user.
- **`Invalid values: aspect_ratio=...`** - call `get_model_schema(model=<id>)` to see allowed values; pick one.
- **`Invalid asset URL`** - the input points at a non-Krea/non-approved host. This commonly appears on fields like `image_url` or `style_images.0.url`. Download the asset if needed, upload it with `krea upload <file> --json` or MCP `upload_asset`, then replace the field with the returned Krea-hosted URL.
- **`Unknown params: <name>`** - the schema doesn't accept that field. Don't guess what the right name is; run `get_model_schema` first.

## Job lifecycle errors

When polling `get_job(jobId=...)`:

- **`status: "failed"`** - server-side failure. The `result` field often has the reason. Common causes:
  - Content moderation (`nsfw`, `ip_detected`) - rephrase
  - Internal model error - retry once; if it fails again, switch model
  - Bad reference image (corrupted, unreadable) - re-upload
- **`status: "failed"` with `result: {}` and no error** - silent model failure. Retry once with a simpler prompt or fewer sequential actions; if it fails again, switch model or ask whether to swap the concept.
- **`status: "cancelled"`** - user or system aborted. Don't auto-retry.
- **`status: "queued"` for >5 minutes** - system capacity issue. Don't resubmit silently; ask the user whether to wait or cancel.

## Direct REST guesses

Do not inspect normal generation jobs by guessing raw REST paths such as `https://api.krea.ai/v1/jobs/<id>`. Unsupported API paths can return an HTML 404 page, not a JSON error, which breaks parsers and wastes time. Use `krea jobs show <id> --json` or MCP `get_job`.

## Cost / quota

- **HTTP 402 "Insufficient credits"** - top up at https://krea.ai/settings/billing.
- **HTTP 402 "Plan required"** - the model is on a higher tier. Surface the upgrade link without judgment.
- **HTTP 429 "Too many requests"** - concurrent job limit. Back off for 10-30s and retry. The MCP retries internally; the agent should not loop on this manually.

## Polling / network

- **Network error on `get_job`** - retry up to 3x with backoff (5s, 15s, 45s). If still failing, surface to user.
- **Timeout exceeded on sync call** - for video, this just means it's still rendering. Switch to async + poll (see `async-polling.md`).

## Quality issues

If you `Read` the output with vision and the result doesn't match the brief:

- **Reference was ignored** (asked for image-to-image, got generic text-to-image) - the reference may be too small; try >= 1024px on the long side.
- **Wrong subject** - prompt may be ambiguous. Refine with more specificity.
- **Missing details / generic** - the user probably wants a higher-fidelity model. Suggest one quietly: "want me to try with a higher-quality model?"
- **Garbled text** - model not strong at typography. Switch to an image archetype that explicitly handles text (see `model-catalog.md`).
- **Wrong style** - describe the style more concretely (medium, era, palette, reference).

Don't pretend a bad output is fine. Saying "here it is" when the result is clearly off is worse than saying "this didn't land - retry?"

## Local file issues

- **`upload_asset` fails with file too large** - files >50 MB often reject. Re-encode at lower bitrate / dimensions.
- **MIME type rejected** - use exact strings (`image/jpeg` not `image/jpg`; `audio/mpeg` not `audio/mp3`).
- **Base64 encoding wrong** - `fileData` must be the raw base64 string, no data-URL prefix unless the schema specifies. When in doubt, send just the base64 payload.

## Known issues / lessons captured 2026-05-17

These were uncovered during a production session that burned ~5,000 CU before producing acceptable video output. Each item is filed in the repository issue tracker or noted here so future agents do not repeat the failure path.

### CLI surface

| # | Symptom | Reality | Workaround |
|---|---|---|---|
| #6 | Older `krea upload --json` returned `{"url":"", "id":"<asset-id>"}` | Current CLI returns `.url`; stale installs may still show the old shape | Upgrade the CLI. If blocked on an old install, resolve the asset by ID as a fallback |
| #7 | Kontext / Seedream-4 reject generation inputs containing external URLs (`image_url`, `style_images.0.url`, etc.) | Public API asset validation intentionally expects Krea-hosted/approved assets | Download external URLs when needed, `krea upload` every local/non-Krea file first, then use the returned Krea-hosted URL |
| #9 | `krea jobs wait --timeout 600` exits at 300s | Older CLI versions silently cap sync wait | Use manual `krea jobs show <id> --json` polling with 15-25s sleep |
| #11 | Video output is horizontal despite `--aspect 9:16` or `-i aspect_ratio="9:16"` | A landscape `--start-image` or landscape `reference_images[0]` can override aspect in Seedance-style models | Do not pass `--start-image` for vertical social video; pad the storyboard to portrait or drop the landscape storyboard ref; see `../../krea-marketing/workflows/social-video-short.md` |
| - | `krea generate image --image-url <url>` fails as unknown flag | The flag is `--image`, or multi-ref models expect `-i image_urls='[...]'` | Check `krea generate image --help` and model schema |
| - | `krea generate image --quality high` fails as unknown flag | `quality` is a schema input, not a top-level CLI flag | Use `-i quality=high` when the schema supports it |
| - | `krea jobs get <id>` prints help | The subcommand is `jobs show` | Use `krea jobs show <id> --json` |

### Model behavior

| Model | Symptom | Workaround |
|---|---|---|
| Seedance-style video models | Output is in slow motion | Strip `slow`, `gentle`, `soft`, and `slow motion`; use `smooth`, `steady`, `fluid`, or `natural realtime` |
| Seedance-style video models | 15s clips with many sequential actions fail or collapse | Compress to 5-8 visible beats, or use `../../krea-marketing/workflows/social-video-short.md` storyboard + timestamped timeline |
| Seedance-style video models | Subject identity drifts across cuts | Pass 2-3 varied face refs; for brand-critical likeness use `../workflows/lora-train-and-use.md` |
| Text-friendly image models | Storyboards with large technical fiches produce weak videos | Keep annotations editorial: tiny panel numbers, short action labels, side icons, header/footer |
| OpenAI-style image models | Portrait dimensions rejected | Use dimensions accepted by schema, often multiples of 16 such as `1024x1824` for 9:16 |

### Workflow disasters to avoid

- Do not submit a video job without loading a `workflows/*.md` recipe first.
- Do not submit a short social video without showing the user an approved storyboard first.
- Do not generate per-panel images separately and ffmpeg-concatenate them for a social short; use one storyboard sheet and one timeline-driven video job.
- Do not silently poll for long-running jobs. Follow `progress-reporting.md`.
- Do not include slow-motion trigger words anywhere in Seedance-style prompts.
- Do not spend >100 CU without `cost-preflight.md`, unless the user has explicitly set a per-session override.

## Known issues / lessons captured 2026-05-19

These came from a campaign session where ambiguous "storyboard" vocabulary and skipped creative gates caused unnecessary campaign spend.

### Routing and creative gates

- **Ambiguous storyboard request**: in CPG/FMCG/agency contexts, "storyboard" may mean a campaign key-visual sheet, not film pre-vis. Ask for a layout reference and route to `../../krea-marketing/workflows/key-visual-sheet.md`.
- **Boring output after fidelity success**: changing only the scene/content often misses the note. Identify whether the user wants format, content, palette, voice, or fidelity changed before regenerating.
- **"Surprise me"**: permission to take taste risks, not permission to skip storyboard/key-visual approval gates.

### Model behavior

| Model | Symptom | Workaround |
|---|---|---|
| Seedance-2 style video models | Macro prompts with tiny flying subjects such as butterflies, bees, or hummingbirds can fail repeatedly with empty result payloads | Retry once; if it fails again, swap to non-animal motion such as petals, leaves, bubbles, condensation, or light rays, or switch model |
| Seedance-2 style video models | Hand placing product into frame can fail or look awkward | Start with the product already placed; animate environment, light, condensation, or camera motion |
| Seedance-2 / videoV2 | **Shadow-fail**: job returns `status:"completed"` with `result:{}` (no `urls[]`). No error message. | Silent content-filter refusal — not a render failure. Detect by checking `result.urls` presence, not status. Retry with sanitized prompt: drop proper nouns, drop role descriptors (`salaryman` → `man`), drop IP-suggestive phrases, drop specific signage text. Keep `start_image` — image carries identity. If still empty, drop `end_image` and retry start-image-only. See `models/seedance-2.md` "Content-filter shadow-fail". |
| Seedance-2 / videoV2 | `status:"failed"` with empty result and NO error message in payload | Hard-fail (distinct from shadow-fail) — usually caused by `end_image` being too visually divergent from `start_image`. Seedance can't interpolate the transition within the clip duration. Per `models/seedance-2.md` "end_image = visual destination": keep end_image within ~2-3s of story-time from start_image. Workaround: drop `end_image` entirely and retry start-image-only. |
| Seedance-2 / videoV2 | HTTP 429 `CONCURRENCY_LIMIT_REACHED` on the 13th+ parallel job | Hard cap is 12 concurrent videoV2 jobs per workspace. Throttle parallel submission to batches of ≤12; poll until in-flight count drops, submit next batch. See `models/seedance-2.md` "Concurrency cap". |
| Seedance-2 / videoV2 | Schema error on `duration` < 4 | Seedance-2 minimum duration is 4s. For shot-grammar runs (2-3s cuts), submit at 4s and ffmpeg-trim to spec at the assembly step. |
| ffmpeg | `subtitles=` filter not found / `No such filter` | Stock Homebrew ffmpeg 8.x ships without libass. Use the PNG-overlay fallback in `dialogue-and-audio.md` instead of trying to rebuild ffmpeg. Working reference at `runs/anime-v2/logs/make_subs.py`. |
| ffmpeg | `ffmpeg -sseof -0.1 -i shot.mp4 -frames:v 1 last.png` returns "Output file is empty" | Use the working pattern: `ffmpeg -sseof -1 -i shot.mp4 -update 1 -frames:v 1 -q:v 2 last.png`. The `-update 1` flag is required for single-frame extraction. |
| krea CLI | `krea jobs wait <id> --json` output captured into a shell var breaks jq parsing | Spinner progress + JSON share stdout. Use `... 2>/dev/null \| grep -E '^\{'` or `... 2>/dev/null \| tail -n 1` to extract just the JSON line. See `async-polling.md` "CLI gotchas". |
| krea CLI | Image model returns 1024×1024 square despite `--aspect 16:9` | `google/imagen-4-ultra` and `google/nano-banana-pro` silently ignore `--aspect`. Pass `--width 1280 --height 720` (or `-i width=1280 -i height=720`) explicitly. See `cli-or-mcp.md` "`--aspect` not universally honored". |
| GPT-image style models | Large simultaneous image batches can hit account concurrency limits, especially after orphaned timeout jobs | Submit campaign sheets or drafts in waves of 8 or fewer and retry 429s with 20s backoff |

## Known issues / lessons captured 2026-05-21

### Kling 3.0 — model id and required fields

- The user-facing name `kling-video-v3.0-pro` resolves to model id `kling/kling-3.0` with `-i mode=pro`. There is no separate `-pro` model id in the catalog. Always run `krea models list --json | jq '.[] | select(.id | test("kling"))'` to confirm.
- Required fields per schema: `prompt`, `aspect_ratio` (enum `16:9` or `9:16`), `duration` (3-15), `generate_audio` (bool), `mode` (`std` / `pro` / `4k`). Named CLI flags cover `--start-image`, `--aspect`, `--duration`, `--prompt`; use `-i end_image=`, `-i generate_audio=true`, `-i mode=pro` for the rest.
- Schema has no `reference_images` field. Identity continuity for chained narrative work rides entirely on the still-compose pass and the `end_image` hook.

### Krea 2 (`krea/krea-2/*`) direct-HTTP cheatsheet

For agents writing direct HTTP against the public Krea 2 endpoint (only justified for K2 which is not exposed via the CLI's named flags / not in the public model menu yet), the on-wire shape differs from MCP camelCase:

- Auth header: `Authorization: Bearer $KREA_API_KEY` (the same key used by the CLI; do not invent an `x-api-key` header — that is not the public-API convention).
- Body field names use snake_case: `aspect_ratio` (not `aspect_ratio`), `resolution` (e.g. `"1K"`), `prompt`, `image_style_references[]`.
- Response uses `job_id` (not `id`). Poll with `GET https://api.krea.ai/v1/jobs/<job_id>` using the same Bearer header, or `krea jobs show <job_id> --json` if the CLI is available.
- MCP `generate_image(model="krea/krea-2/*", input={aspect_ratio, ...})` still uses camelCase — the MCP server translates. Only the raw HTTP body needs snake_case.

This is consistent with `media-inputs.md` ("Krea 2 image endpoints use `aspect_ratio` + `resolution` in the public API") but was not previously consolidated for the auth header and `job_id` response shape.
