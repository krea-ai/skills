# CLI or MCP — Operation Reference

The Krea skills use the Krea CLI (`@krea-ai/cli`) by default. If the CLI is unavailable but the Krea MCP server is connected, use MCP as the fallback. Both hit the same backend.

## Detection (run once per session)

```bash
# 1. CLI preferred — krea on PATH + authenticated
which krea && krea doctor 2>&1 | head -5
#
# 2. MCP fallback — tools appear in the agent's tool list
#    Look for: mcp__krea-public-api__list_models
```

If `which krea` returns a path AND `krea doctor` prints `✓ api auth`, the CLI is ready.

If neither is available, tell the user one of:

- `npm install -g @krea-ai/cli && krea auth login` (universal install path)
- "Connect the Krea MCP" (Claude Code / Cursor / etc. with MCP support)

Don't fall back to direct HTTP calls — then it's a bug or a custom workflow the agent should write code for (see krea-build).

## CLI stdout contract

Bare CLI generation is async. `krea generate image -p "..."` prints a `job_id` on stdout, not a result URL. Use `--wait` when a shell script needs `URL=$(krea generate image -p "..." --wait)`, or capture the job id and call `krea jobs wait <id>`.

The default CLI image model is `krea/krea-2/large`. Krea 2 dimensions use `--aspect` in the CLI, or raw `aspect_ratio` + `resolution` fields when passing schema inputs. Pin another model with `-m` for old `--width`, `--height`, `--quality`, `--steps`, or `--image` workflows.

## Operation reference — MCP vs CLI

| Operation | MCP | CLI |
|---|---|---|
| **List models** | `mcp__krea-public-api__list_models()` | `krea models list --json` |
| **Get model schema** | `get_model_schema(model="<id>")` | `krea models show <id> --json` |
| **Image — sync** | `generate_image(model=<id>, input={prompt, aspectRatio, ...}, sync=true, timeoutSeconds=60)` | `krea generate image -m <id> -p "..." --aspect 16:9 --wait` |
| **Image — async** | `generate_image(..., sync=false)` → returns `{job_id}` | `krea generate image -m <id> -p "..." --json` (no `--wait` ⇒ async) |
| **Video — async + poll** | `generate_video(..., sync=false)` → `get_job(jobId)` in loop | `JOB=$(krea generate video -m <id> -p "..." --json \| jq -r .job_id) && krea jobs wait $JOB --json` |
| **Enhance — sync** | `enhance_image(model=<id>, input={imageUrl, width, height, ...}, sync=true)` | `krea generate enhance -m <id> <url> --width 4096 --height 4096 --wait` |
| **Upload local/downloaded file** | `upload_asset(filename, mimeType, fileData=base64(...))` -> returns Krea asset URL | `krea upload ./photo.png --json \| jq -r .url` (takes file path directly) |
| **Get job status** | `get_job(jobId="<id>")` | `krea jobs show <id> --json` |
| **Wait for terminal status** | poll `get_job` every 10s until terminal | `krea jobs wait <id>` (server-side poll, blocks until done) |
| **Save result to disk** | response URL → curl/Bash download | `-o ./out.png` (implies `--wait`, handles download) |

## When named flags aren't enough — use `-i`

The CLI's named flags (`--start-image`, `--duration`, `--aspect`, `--prompt`, `--width`, `--height`, `--quality`, `--resolution`, `--seed`, etc.) cover the common cases. For everything else in the model schema, use `-i field=value`. This is the primary path for any model whose schema is wider than the named flags - notably `bytedance/seedance-2`, which currently exposes `end_image`, `reference_images` (up to 9), `reference_videos`, `reference_audios`, `generate_audio`, and `effects[]` beyond the named flags.

Always run `krea models show <id> --json` first and inspect `inputSchema.properties`; field names there are exactly what CLI `-i` accepts. MCP tool payloads may use translated camelCase names, so verify the MCP schema separately when using MCP.

### Syntax

```bash
# Scalar (string, number)
-i resolution=720p
-i duration=4
-i seed=42

# Boolean
-i generate_audio=true

# Array of strings — JSON-encoded
-i "reference_images=[\"$KREA_REF_1\",\"$KREA_REF_2\"]"

# Object (nested) — JSON-encoded
-i 'effects={"name":"smear","intensity":0.7}'
```

### Worked example — Seedance 2.0 chained vs terminal

Seedance 2 rejects end-frame and reference-image paths together (HTTP 422). In the current CLI schema, pick either `end_image` or `reference_images` per call:

```bash
# Chained shot — end_image hook, identity rides via --start-image.
# Use 4s for shot-grammar clips; use a longer accepted duration only for deliberate long beats.
krea generate video -m bytedance/seedance-2 \
  --start-image "$START" --duration "${DURATION:-4}" --aspect 16:9 \
  -i end_image="$END" \
  -i generate_audio=true \
  -i resolution=720p \
  -i seed=42 \
  -p "<prompt>" \
  --json

# Terminal shot — reference_images for fine-detail identity anchor.
krea generate video -m bytedance/seedance-2 \
  --start-image "$START" --duration "${DURATION:-4}" --aspect 16:9 \
  -i "reference_images=[\"$HERO\",\"$PROP\"]" \
  -i generate_audio=true \
  -i resolution=720p \
  -i seed=42 \
  -p "<prompt>" \
  --json
```

Without `-i` these commands would silently drop most schema fields (the CLI does not warn). Lead with `-i` for any wide-schema model.

### Per-model field-name variance

Reference-image fields are not standardized across the model catalog:

| Model | Reference field |
|---|---|
| `bytedance/seedance-2` | `reference_images` (CLI schema, array up to 9) |
| `google/nano-banana-pro` | inspect live schema; recent image models commonly use `image_urls` or translated MCP `imageUrls` |
| `google/imagen-4-ultra` | no reference field — image-to-image not supported |
| `bfl/flux-1-kontext-dev` | inspect live schema; commonly singular image reference |

Always run `krea models show <id> --json` and read `inputSchema.properties` before guessing. The CLI's `-i` does not validate field names against the schema until the API rejects the call.

### Asset URL validation

Generation inputs that point at media must use Krea-hosted or explicitly approved asset URLs. If the user gives an ordinary external URL, first download it to a temp file and run `krea upload <file> --json`; then pass the returned `.url` through the schema field. Current CLI schemas commonly use snake_case fields such as `image_url`, `image_urls`, `reference_images`, `start_image`, `end_image`, `style_images[].url`, and `image_style_references[].url`; MCP may expose translated camelCase fields. A 422 `Invalid asset URL` is usually fixed by rehosting the asset with `krea upload`, not by changing the model.

## Notable CLI conveniences over MCP

- **`krea upload <path>`** takes a file path directly — no base64 encoding required.
- **`krea generate image ... -o ./out.png`** generates AND downloads to disk in one call.
- **`krea jobs wait <id>`** does the polling server-side; no loop needed in your code.
- **`--json`** flag on every command produces machine-readable output for scripting.
- **`KREA_API_KEY`** env var or `krea auth login` (keyring-backed) — no token in every call.

## Notable MCP conveniences over CLI

- **No local CLI install** when the agent already has Krea MCP connected.
- **Schema-validated inputs** at tool-call time — fewer typos make it to the API.
- **No subprocess overhead** — agent calls the tool directly.

## When you must pick one

The skill's workflow examples default to CLI syntax. If you're operating in MCP mode, mentally substitute via the table above.

For repeatable pipelines in your own stack, the agent generates code via `krea-build`. See `../../krea-marketing/workflows/full-ad-campaign.md` for marketing orchestration patterns and `../workflows/lora-train-and-use.md` for the LoRA training API surface.

## Cost transparency

Both surfaces show CU cost the same way: model descriptions include CU pricing inline. The CLI prints it after a generation (`Cost: ~X CU`); the MCP returns it in the job response. Same numbers, same accounting.

## What to do on auth failure

- **CLI auth failure**: run `krea auth login` to refresh the stored API key, or set `KREA_API_KEY` in the environment. The CLI stores credentials per machine.
- **MCP auth failure**: the MCP server config in the agent platform needs attention. Re-add the MCP via your agent's config UI. Don't try to set env vars from the skill.
