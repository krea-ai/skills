# Troubleshooting

## MCP tool missing

```
ToolError: mcp__krea-public-api__... is not available
```

The Krea MCP server isn't installed. The CLI is the default surface, so first check `which krea && krea doctor 2>&1 | head -5`. If the CLI is healthy, use it. If the CLI is unavailable and MCP is missing too, tell the user to install the CLI or connect the MCP. Don't fall back to direct HTTP for normal generation; direct HTTP is only for documented custom workflows like LoRA training or code generated via `krea-build`.

## Authentication

The MCP handles auth on the Krea side. If you see an explicit auth error from a tool call, the MCP server isn't properly configured. Surface it to the user — don't try to work around it.

## Validation errors

- **`Missing required params: prompt`** — the model needs a prompt; ask the user.
- **`Invalid values: aspectRatio=...`** — call `get_model_schema(model=<id>)` to see allowed values; pick one.
- **`Unknown params: <name>`** — the schema doesn't accept that field. Don't guess what the right name is; run `get_model_schema` first.

## Job lifecycle errors

When polling `get_job(jobId=...)`:

- **`status: "failed"`** — server-side failure. The `result` field often has the reason. Common causes:
  - Content moderation (`nsfw`, `ip_detected`) — rephrase
  - Internal model error — retry once; if it fails again, switch model
  - Bad reference image (corrupted, unreadable) — re-upload
- **`status: "cancelled"`** — user or system aborted. Don't auto-retry.
- **`status: "queued"` for >5 minutes** — system capacity issue. Don't resubmit silently; ask the user whether to wait or cancel.

## Cost / quota

- **HTTP 402 "Insufficient credits"** — top up at https://krea.ai/settings/billing.
- **HTTP 402 "Plan required"** — the model is on a higher tier. Surface the upgrade link without judgment.
- **HTTP 429 "Too many requests"** — concurrent job limit. Back off for 10–30s and retry. The MCP retries internally; the agent should not loop on this manually.

## Polling / network

- **Network error on `get_job`** — retry up to 3× with backoff (5s, 15s, 45s). If still failing, surface to user.
- **Timeout exceeded on sync call** — for video, this just means it's still rendering. Switch to async + poll (see `async-polling.md`).

## Quality issues

If you `Read` the output with vision and the result doesn't match the brief:

- **Reference was ignored** (asked for image-to-image, got generic text-to-image) — the reference may be too small; try ≥ 1024px on the long side.
- **Wrong subject** — prompt may be ambiguous. Refine with more specificity.
- **Missing details / generic** — the user probably wants a higher-fidelity model. Suggest one quietly: "want me to try with a higher-quality model?"
- **Garbled text** — model not strong at typography. Switch to an image archetype that explicitly handles text (see `model-catalog.md`).
- **Wrong style** — describe the style more concretely (medium, era, palette, reference).

Don't pretend a bad output is fine. Saying "here it is" when the result is clearly off is worse than saying "this didn't land — retry?"

## Local file issues

- **`upload_asset` fails with file too large** — files >50 MB often reject. Re-encode at lower bitrate / dimensions.
- **MIME type rejected** — use exact strings (`image/jpeg` not `image/jpg`; `audio/mpeg` not `audio/mp3`).
- **Base64 encoding wrong** — `fileData` must be the raw base64 string, no data-URL prefix unless the schema specifies. When in doubt, send just the base64 payload.

## Known issues / lessons captured 2026-05-17

These were uncovered during a production session that burned ~5,000 CU before producing acceptable video output. Each is filed as an issue on `krea-ai/skills` or noted here so future agents don't hit the same wall. If you read this section before generating, you save the user money and trust.

### CLI surface

| # | Symptom | Reality | Workaround |
|---|---|---|---|
| #6 | `krea upload --json` returns `{"url":"", "id":"<asset-id>"}` | The CLI doesn't resolve the hosted URL on upload | `curl -H "Authorization: Bearer $KREA_API_KEY" "https://api.krea.ai/assets/<id>"` and read `.image_url` |
| #7 | Kontext / Seedream-4 reject `imageUrls` containing non-`app-uploads.krea.ai` URLs | These models only accept Krea-hosted assets | Always `krea upload` local files first; use the returned Krea-hosted URL |
| #9 | `krea jobs wait --timeout 600` exits at 300s | The CLI silently caps `--timeout` to 300s for HTTP sync | Use manual `krea jobs show <id> --json` polling loop with 15–25s sleep |
| #11 | Video output is horizontal despite `--aspect 9:16` (or `-i aspectRatio="9:16"`) | A landscape `--start-image` OR a landscape `referenceImages[0]` overrides aspect in seedance-2 | Pad source to portrait before uploading, OR drop the landscape ref entirely and rely on face refs + timeline prompt; see `storyboard-method.md` |
| — | `krea generate image --image-url <url>` — "unknown flag" | The flag is `--image` (singular), or for multiple refs use `-i imageUrls='["<url>", "<url>"]'` | Use the documented flag names; check `krea generate image --help` |
| — | `krea generate image --quality high` — "unknown flag" | `--quality` is not a CLI flag; the underlying schema field is `quality` | Use `-i quality=high` (or `medium`/`low`/`auto`) |
| — | `krea jobs get <id>` — prints help instead of fetching | The subcommand is `krea jobs show <id>`, not `get` | Use `krea jobs show <id> --json` |
| — | `curl https://api.krea.ai/v1/jobs/<id>` returns an HTML 404 page | There is no public REST endpoint at that path; the CLI / MCP wraps the canonical job API | Use `krea jobs show <id> --json` for inspection |

### Model behavior

| Model | Symptom | Workaround |
|---|---|---|
| `bytedance/seedance-2` | Output is in slow motion | Strip the words **`slow`, `gentle`, `soft`, `slow motion`** from the prompt — seedance interprets them literally. Use **`smooth`, `steady`, `fluid`** instead. |
| `bytedance/seedance-2` | Job ends with `"status":"failed", "result":{}` and no error reason | Often content moderation or model overload. Simplify the prompt (fewer sequential actions, less violent verbs) and retry once. If it fails twice, try `bytedance/seedance-2-fast` to see if it's a quality-tier capacity issue. |
| `bytedance/seedance-2` | A 15s clip with `>3` sequential narrative actions ("she walks, then opens the door, then sits, then waves") fails more often than a single-action prompt | Compress to 1–2 actions per clip, or chain shorter clips via a single storyboard sheet + timeline prompt (see `storyboard-method.md`) |
| `bytedance/seedance-2` | Subject identity drifts across cuts | Pass 2–3 face refs from varied angles in `referenceImages`. For brand-critical likeness, train a LoRA (see `lora-training.md`); face-ref-only identity is moderate (5–7/10 average). |
| `openai/gpt-image-2` | `width=1024, height=1820` rejected with `Dimensions must be multiples of 16` | All dimensions must be multiples of 16. For portrait 9:16 use `1024×1824`; for landscape 16:9 use `1536×1024`; for square use `1024×1024`. |
| `openai/gpt-image-2` | Generated face only loosely resembles `imageUrls` reference | Identity preservation peaks ~7/10 with multiple varied face angles. Put the clearest frontal photo as `imageUrls[0]` and put extra weight by duplicating the strongest ref (`[ref, ref, second_angle]`). For exact likeness use a LoRA pipeline. |
| `openai/gpt-image-2`, `bytedance/seedream-4` | Storyboard layout with per-panel technical fiches ("camera: 50mm / light: warm / style: editorial / notes: ...") produces low-quality video downstream | Keep storyboard annotations editorial: tiny panel numbers + short action verb under each cell + side category icons + header/footer. No on-panel info blocks. |

### Workflow disasters to avoid

These are not bugs — they are agent behaviors that wasted credits in the 2026-05-17 session and are now hard-prohibited in `SKILL.md`:

- **Don't submit a video job without showing the user a storyboard first.** A 15s seedance-2 job costs ~1564 CU and takes 10–15 min. Burning that on an un-approved brief is unforgivable. See `storyboard-method.md` and `SKILL.md` UX rule 7.
- **Don't generate per-panel images separately and ffmpeg-concatenate.** The result feels like "varis videos enganxats" (stitched snippets), not a coherent video. Use one storyboard sheet + one seedance job with a TIMELINE prompt instead.
- **Don't silently poll for 30+ minutes.** If a video job is stuck `processing` for >15 min, tell the user it's slow and offer to keep waiting or cancel. The user is blind to your background work; over-communicate progress.
- **Don't include slow-mo trigger words anywhere in seedance prompts** — even in style notes. "Slow gentle pacing" gets you slow motion playback. Use "smooth steady pacing" or "natural realtime speed".
