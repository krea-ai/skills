# Troubleshooting

## MCP tool missing

```
ToolError: mcp__krea-public-api__... is not available
```

The Krea MCP server isn't installed. Tell the user to install it and pause. Don't fall back to the API directly — that's what `scripts/` is for, and only for batch pipelines or LoRA training.

## Authentication

The MCP handles auth on the Krea side. If you see an explicit auth error from a tool call, the MCP server isn't properly configured. Surface it to the user — don't try to work around it.

## Validation errors

- **`Missing required params: prompt`** — the model needs a prompt; ask the user.
- **`Invalid values: aspectRatio=...`** — call `get_model_schema(model=<id>)` to see allowed values; pick one.
- **`Unknown params: <name>`** — the schema doesn't accept that field. Don't guess what the right name is; run `get_model_schema` first.

## Silent-drop on unknown params

**The biggest footgun in the Krea MCP.** Unknown input fields are silently dropped — the call returns HTTP 200 and produces output as if the missing-but-named-wrong field never existed. There is no validation error and no warning. If you pass a reference under the wrong key, the model falls back to pure text-to-image and you get an unrelated result while believing you ran image-to-image.

Verified repro: `bfl/flux-1-dev` does not have an `image` field (its image-reference fields are `imageStyleRefs` and `styleImages`). This call returns 200 and produces a generic, completely unrelated text-to-image apple:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"generate_image","arguments":{
  "model":"bfl/flux-1-dev",
  "input":{
    "prompt":"the same apple, but green",
    "image":"https://gen.krea.ai/images/...apple.png"
  },
  "sync":true
}}}
```

Vision-verified output: no identity preservation, different apple, different background.

### Why this is so easy to trip

Camel/snake casing is inconsistent across models. There is no rule like "always camelCase." Per-model, verified in trial:

| Model | Reference field(s) | Casing |
|---|---|---|
| `bfl/flux-1-kontext-dev` | `imageUrl` | camel |
| `bytedance/seedance-2-fast` | `startImage`, `referenceImages` | camel |
| `topaz/standard-enhance` | `image_url`, `output_format`, `face_enhancement` | snake |
| `bfl/flux-1-dev` | `styleImages`, `imageStyleRefs` (NOT `image`) | camel |

### How to avoid

1. `get_model_schema(model=<id>)` **every time** you pass reference media in a new session. Don't guess.
2. Use only keys present in `inputSchema.properties`. Don't map between casings — copy the schema's exact spelling.
3. Vision-verify the result. If you asked for a green version of the user's specific apple and got a generic stock apple, you almost certainly hit silent-drop. Re-read the schema and retry under the right key.

See also `media-inputs.md` for the per-model field-name table.

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
