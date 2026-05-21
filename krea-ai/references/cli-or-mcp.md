# CLI or MCP — Operation Reference

The Krea skill uses the Krea CLI (`@krea-ai/cli`) by default. If the CLI is unavailable but the Krea MCP server is connected, use MCP as the fallback. Both hit the same backend.

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

The default CLI image model is `krea/krea-2/large`. Krea 2 dimensions use `--aspect` in the CLI, or raw `aspect_ratio` + `resolution` fields when passing `--input`/MCP payloads. Pin another model with `-m` for old `--width`, `--height`, `--quality`, `--steps`, or `--image` workflows.

## Operation reference — MCP vs CLI

| Operation | MCP | CLI |
|---|---|---|
| **List models** | `mcp__krea-public-api__list_models()` | `krea models list --json` |
| **Get model schema** | `get_model_schema(model="<id>")` | `krea models show <id> --json` |
| **Image — sync** | `generate_image(model=<id>, input={prompt, aspectRatio, ...}, sync=true, timeoutSeconds=60)` | `krea generate image -m <id> -p "..." --aspect 16:9 --wait` |
| **Image — async** | `generate_image(..., sync=false)` → returns `{job_id}` | `krea generate image -m <id> -p "..." --json` (no `--wait` ⇒ async) |
| **Video — async + poll** | `generate_video(..., sync=false)` → `get_job(jobId)` in loop | `JOB=$(krea generate video -m <id> -p "..." --json \| jq -r .job_id) && krea jobs wait $JOB --json` |
| **Enhance — sync** | `enhance_image(model=<id>, input={imageUrl, width, height, ...}, sync=true)` | `krea generate enhance -m <id> <url> --width 4096 --height 4096 --wait` |
| **Upload local file** | `upload_asset(filename, mimeType, fileData=base64(...))` → returns asset URL | `krea upload ./photo.png --json \| jq -r .url` (takes file path directly) |
| **Get job status** | `get_job(jobId="<id>")` | `krea jobs show <id> --json` |
| **Wait for terminal status** | poll `get_job` every 10s until terminal | `krea jobs wait <id>` (server-side poll, blocks until done) |
| **Save result to disk** | response URL → curl/Bash download | `-o ./out.png` (implies `--wait`, handles download) |

## When named flags aren't enough — use `-i`

The CLI's named flags (`--start-image`, `--duration`, `--aspect`, `--prompt`, `--width`, `--height`, etc.) cover the common cases. For everything else in the model schema, use `-i field=value`. This is the primary path for any model whose schema is wider than the named flags — notably `bytedance/seedance-2`, which exposes `endImage`, `referenceImages` (up to 9), `referenceVideos`, `referenceAudios`, `generateAudio`, `resolution`, `seed`, and `effects[]` beyond the four fields the named flags cover.

Always run `krea models show <id>` first to see the live schema; field names there are exactly what `-i` accepts.

### Syntax

```bash
# Scalar (string, number)
-i resolution=720p
-i duration=10
-i seed=42

# Boolean
-i generateAudio=true

# Array of strings — JSON-encoded
-i "referenceImages=[\"https://ref1.png\",\"https://ref2.png\"]"

# Object (nested) — JSON-encoded
-i 'effects={"name":"smear","intensity":0.7}'
```

### Worked example — Seedance 2.0 with chain + refs + audio

```bash
krea generate video -m bytedance/seedance-2 \
  --start-image "$START" --duration 10 --aspect 16:9 \
  -i endImage="$END" \
  -i "referenceImages=[\"$HERO\",\"$PROP\"]" \
  -i generateAudio=true \
  -i resolution=720p \
  -i seed=42 \
  -p "<prompt>" \
  --json
```

Without the `-i` block this command would silently drop `endImage` (scene chaining broken), `referenceImages` (character identity drifts), `generateAudio` (silent output), `resolution` (defaults applied), and `seed` (no reproducibility). The CLI does not warn when schema fields are dropped — the only signal is degraded output, so always lead with `-i` for models with wide schemas.

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

For repeatable pipelines or LoRA training in your own stack, the agent generates code via `krea-build`. See `../workflows/full-ad-campaign.md` for orchestration patterns and `../workflows/lora-train-and-use.md` for the LoRA training API surface.

## Cost transparency

Both surfaces show CU cost the same way: model descriptions include CU pricing inline. The CLI prints it after a generation (`Cost: ~X CU`); the MCP returns it in the job response. Same numbers, same accounting.

## What to do on auth failure

- **CLI auth failure**: run `krea auth login` to refresh the stored API key, or set `KREA_API_KEY` in the environment. The CLI stores credentials per machine.
- **MCP auth failure**: the MCP server config in the agent platform needs attention. Re-add the MCP via your agent's config UI. Don't try to set env vars from the skill.
