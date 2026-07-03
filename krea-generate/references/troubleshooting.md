# Troubleshooting

## MCP tool missing

```
ToolError: mcp__krea__... is not available
```

The Krea MCP server is not installed, not authenticated, or not exposed in the current session. Tell the user to connect or authenticate Krea MCP. Do not use non-MCP fallbacks.

## Authentication

The MCP handles auth on the Krea side. If you see an explicit auth error from a tool call, the MCP server isn't properly configured. Surface it to the user - don't try to work around it.

## Validation errors

- **`Missing required params: prompt`** - the model needs a prompt; ask the user.
- **`Invalid values: aspect_ratio=...`** - call `get_model_schema(model=<id>)` to see allowed values; pick one.
- **`Invalid asset URL`** - the input points at a non-Krea/non-approved host. This commonly appears on fields like `image_url` or `style_images.0.url`. Download the asset if needed, upload it with MCP `upload_asset`, then replace the field with the returned Krea-hosted URL.
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

## Endpoint guesses

Do not inspect normal generation jobs by guessing API paths such as `https://api.krea.ai/v1/jobs/<id>`. Unsupported paths can return an HTML 404 page, not a JSON error, which breaks parsers and wastes time. Use MCP `get_job`.

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

### MCP surface

| # | Symptom | Reality | Workaround |
|---|---|---|---|
| #7 | Kontext / Seedream-4 reject generation inputs containing external URLs (`image_url`, `style_images.0.url`, etc.) | Asset validation intentionally expects Krea-hosted/approved assets | Download external URLs when needed, upload every local/non-Krea file through MCP first, then use the returned Krea-hosted URL |
| #9 | Long video generation exceeds sync wait limits | Sync generation waits cap at 300s | Submit async, then use MCP `get_job` polling |
| #11 | Video output is horizontal despite `aspect_ratio="9:16"` | A landscape `start_image` or landscape `reference_images[0]` can override aspect in Seedance-style models | Do not pass a landscape `start_image` for vertical social video; pad the storyboard to portrait or drop the landscape storyboard ref; see `../../krea-marketing/workflows/social-video-short.md` |
| - | `quality` is ignored or rejected by a specific model | The selected model may not support `quality` | Check the MCP model schema; use only fields present in the schema |
| - | Slow image models exceed the synchronous gateway window | The timeout response may not include a usable job id, even if the running job is billed | Prefer async when the model is slow; retry transient 502/524 with backoff |
| - | `gpt-image-2` rejects dimensions such as 1080x1350, or `aspect_ratio` alone | The model requires explicit `width`/`height` in multiples of 16 | Use ÷16 sizes: 1024x1280 (4:5), 1024x1024 (1:1), 1024x1360 (3:4), 1024x1824 (9:16) |

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
| Seedance-2 / videoV2 | `status:"failed"` with an explicit `error.code:"content_policy"` and message "An external provider's moderation systems rejected the generation" | Distinct from shadow-fail and hard-fail: this is a real error payload, not a silent/empty one, and can fire on a compliant still that already passed vision QA. Observed on dark/moody single-source-rim-light framing with an orbiting camera. Retry once with simplified, brighter wording (drop "dark", moody lighting descriptors, and atmospheric haze/dust language); if it fails twice, swap to a brighter treatment rather than retrying indefinitely — this can be provider-side flakiness, not a real policy violation. |
| ffmpeg | `drawtext=` / `subtitles=` filter not found / `No such filter` | Stock Homebrew `ffmpeg` 8.x ships without libfreetype/libass. Verified fix: `brew install ffmpeg-full` (keg-only) and call its binary directly at `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg` — it includes `drawtext` and `subtitles`. Simpler than a PNG-overlay fallback when available. If `ffmpeg-full` can't be installed, fall back to a PNG-overlay approach; reference at `runs/anime-v2/logs/make_subs.py`. |
| ffmpeg | `ffmpeg -sseof -0.1 -i shot.mp4 -frames:v 1 last.png` returns "Output file is empty" | Use the working pattern: `ffmpeg -sseof -1 -i shot.mp4 -update 1 -frames:v 1 -q:v 2 last.png`. The `-update 1` flag is required for single-frame extraction. |
| Some image models | Image model returns 1024x1024 square despite `aspect_ratio: "16:9"` | `google/imagen-4-ultra` and `google/nano-banana-pro` may ignore aspect-only inputs. Pass explicit schema-supported width and height when available. |
| GPT-image style models | Large simultaneous image batches can hit account concurrency limits, especially after orphaned timeout jobs | Submit campaign sheets or drafts in waves of 8 or fewer and retry 429s with 20s backoff |

## Known issues / lessons captured 2026-05-21

### Kling 3.0 — model id and required fields

- The user-facing name `kling-video-v3.0-pro` resolves to model id `kling/kling-3.0` with `mode=pro`. There is no separate `-pro` model id in the catalog. Always use MCP `list_models` and inspect matching Kling entries to confirm.
- Required fields per schema: `prompt`, `aspect_ratio` (enum `16:9` or `9:16`), `duration` (3-15), `generate_audio` (bool), `mode` (`std` / `pro` / `4k`). Use MCP schema-declared fields only.
- Schema has no `reference_images` field. Identity continuity for chained narrative work rides entirely on the still-compose pass and the `end_image` hook.

### Krea 2 (`krea/krea-2/*`) MCP notes

For MCP use, rely on the connected tool schema rather than public endpoint details:

- Krea 2 moodboard generation uses `moodboards: [{id, strength}]` in the observed public-API schema, with observed `maxItems: 1`. For moodboard discovery and K2-specific rules, load `models/krea-2.md`.
- MCP may expose `aspect_ratio`, `aspectRatio`, or another schema-declared field shape. Inspect the tool schema before submitting.
- Response job id fields are schema-dependent. Use the id returned by the MCP call when polling with `get_job`.

This is consistent with `media-inputs.md`: inspect MCP schemas instead of guessing field names.
