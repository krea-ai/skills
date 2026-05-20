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
- **`Invalid values: aspectRatio=...`** - call `get_model_schema(model=<id>)` to see allowed values; pick one.
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

These were uncovered during a production session that burned ~5,000 CU before producing acceptable video output. Each item is filed as an issue on `krea-ai/skills` or noted here so future agents do not repeat the failure path.

### CLI surface

| # | Symptom | Reality | Workaround |
|---|---|---|---|
| #6 | `krea upload --json` returns `{"url":"", "id":"<asset-id>"}` | The CLI does not always resolve the hosted URL on upload | `curl -H "Authorization: Bearer $KREA_API_KEY" "https://api.krea.ai/assets/<id>"` and read `.image_url` |
| #7 | Kontext / Seedream-4 reject `imageUrls` containing non-`app-uploads.krea.ai` URLs | These models only accept Krea-hosted assets | Always `krea upload` local files first; use the Krea-hosted URL |
| #9 | `krea jobs wait --timeout 600` exits at 300s | Older CLI versions silently cap sync wait | Use manual `krea jobs show <id> --json` polling with 15-25s sleep |
| #11 | Video output is horizontal despite `--aspect 9:16` or `-i aspectRatio="9:16"` | A landscape `--start-image` or landscape `referenceImages[0]` can override aspect in Seedance-style models | Do not pass `--start-image` for vertical social video; pad the storyboard to portrait or drop the landscape storyboard ref; see `../workflows/social-video-short.md` |
| - | `krea generate image --image-url <url>` fails as unknown flag | The flag is `--image`, or multi-ref models expect `-i imageUrls='[...]'` | Check `krea generate image --help` and model schema |
| - | `krea generate image --quality high` fails as unknown flag | `quality` is a schema input, not a top-level CLI flag | Use `-i quality=high` when the schema supports it |
| - | `krea jobs get <id>` prints help | The subcommand is `jobs show` | Use `krea jobs show <id> --json` |

### Model behavior

| Model | Symptom | Workaround |
|---|---|---|
| Seedance-style video models | Output is in slow motion | Strip `slow`, `gentle`, `soft`, and `slow motion`; use `smooth`, `steady`, `fluid`, or `natural realtime` |
| Seedance-style video models | 15s clips with many sequential actions fail or collapse | Compress to 5-8 visible beats, or use `../workflows/social-video-short.md` storyboard + timestamped timeline |
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

- **Ambiguous storyboard request**: in CPG/FMCG/agency contexts, "storyboard" may mean a campaign key-visual sheet, not film pre-vis. Ask for a layout reference and route to `../workflows/key-visual-sheet.md`.
- **Boring output after fidelity success**: changing only the scene/content often misses the note. Identify whether the user wants format, content, palette, voice, or fidelity changed before regenerating.
- **"Surprise me"**: permission to take taste risks, not permission to skip storyboard/key-visual approval gates.

### Model behavior

| Model | Symptom | Workaround |
|---|---|---|
| Seedance-2 style video models | Macro prompts with tiny flying subjects such as butterflies, bees, or hummingbirds can fail repeatedly with empty result payloads | Retry once; if it fails again, swap to non-animal motion such as petals, leaves, bubbles, condensation, or light rays, or switch model |
| Seedance-2 style video models | Hand placing product into frame can fail or look awkward | Start with the product already placed; animate environment, light, condensation, or camera motion |
| GPT-image style models | Large simultaneous image batches can hit account concurrency limits, especially after orphaned timeout jobs | Submit campaign sheets or drafts in waves of 8 or fewer and retry 429s with 20s backoff |
