# Pipelines — Multi-Step Workflows

There are **two ways** to run multi-step Krea workflows:

1. **Agent-orchestrated** (default). The agent chains MCP calls in sequence — generate, then upload the result, then animate it, etc. This is what you'll do for most conversational requests. It's fully visible, the user sees each step.
2. **`scripts/pipeline.py`** (batch). A standalone Python tool that hits the Krea API directly (no MCP). Useful for: long automated batch jobs, CI/CD, scheduled workflows, fan-out branching, parallel execution, resumable runs, dry-run cost estimates. Use when the user wants a repeatable pipeline file they can re-run.

## Agent-orchestrated example

User: *"Generate a dragon image, upscale to 4K, then animate it."*

```
# Step 1: generate
result = generate_image(
    model="<a high-fidelity image model>",  # from list_models
    input={prompt: "a majestic dragon on a cliff over a stormy ocean", aspectRatio: "16:9"},
    sync=true, timeoutSeconds=60,
)
# Download and Read the result, verify it matches

# Step 2: upscale
enhanced = enhance_image(
    model="<a topaz upscaler>",  # from list_models
    input={imageUrl: result.url, width: 4096, height: 4096},
    sync=true, timeoutSeconds=120,
)

# Step 3: animate
job = generate_video(
    model="<an image-to-video model>",  # from list_models
    input={
        prompt: "the dragon spreads its wings and roars, lightning strikes",
        startImage: enhanced.url,
        duration: 6,
        aspectRatio: "16:9",
    },
    sync=false,
)
# Poll get_job(jobId=job.id) until terminal — see async-polling.md
```

This is the right approach for one-off creative requests. The user watches each step land.

## `scripts/pipeline.py` — when to use it

Reach for `pipeline.py` when:

- The user wants a **repeatable file** they can rerun (e.g. "I'll need this for every new product launch").
- There's **fan-out** branching — one step produces N outputs, the next step runs N times in parallel.
- The pipeline is **long** and could be interrupted (resume support).
- You want a **dry-run cost estimate** before committing.

It bypasses the MCP and hits the Krea API directly. Needs `KREA_API_KEY` set.

```bash
uv run scripts/pipeline.py --pipeline pipeline.json
```

## Pipeline JSON format

```json
{
  "steps": [
    {
      "action": "generate_image | generate_video | enhance | fan_out",
      "model": "model-id-or-alias",
      "prompt": "...",
      "filename": "base-name",
      "use_previous": true,
      "...": "any other model-specific params (camelCase: aspectRatio, batchSize, generateAudio, startImage)"
    }
  ]
}
```

**Actions:**
- `generate_image` — image generation
- `generate_video` — video generation
- `enhance` — upscale/enhance
- `fan_out` — run a sub-step for EACH result from the previous step

**Special fields:**
- `use_previous: true` — use the previous step's URLs as input
- `fan_out` has a `step` field containing the template to run per source URL
- In `fan_out` prompts/filenames, `{i}` is replaced with the iteration number (1, 2, 3...)

**Key casing.** Pipeline-own fields are `snake_case` (`use_previous`, `fan_out`, `image_url`). Krea API fields are `camelCase` (`aspectRatio`, `batchSize`, `generateAudio`, `startImage`). Match the examples.

**Template substitution.** Two kinds:
- `{i}` — fan_out iteration index. Only inside `fan_out` sub-steps.
- `{{key}}` — user-provided template variables via `--var key=value`. Replaced globally.

## CLI flags

| Flag | Description | Default |
|---|---|---|
| `--pipeline` | Path to JSON file or inline JSON string (required) | — |
| `--api-key` | Krea API key | env `KREA_API_KEY` |
| `--output-dir` | Output directory for generated files | cwd |
| `--dry-run` | Estimate CU cost without executing | false |
| `--resume` | Skip completed steps (uses `.pipeline-state.json`) | false |
| `--max-parallel` | Max concurrent jobs for parallel fan-out | 3 |
| `--var key=value` | Template variable (repeatable) | — |
| `--notify` | Desktop notification when finished | false |

## Worked example: generate → 4 angles → 4 videos

```json
{
  "steps": [
    {
      "action": "generate_image",
      "model": "<draft image model id>",
      "prompt": "a red sports car on an empty highway, golden hour, cinematic",
      "filename": "car-concept"
    },
    {
      "action": "fan_out",
      "use_previous": true,
      "step": {
        "action": "generate_image",
        "model": "<high-fidelity image model id>",
        "prompt": "same red sports car, angle {i} of 4, professional automotive photography, studio lighting, white background",
        "filename": "car-angle-{i}"
      }
    },
    {
      "action": "fan_out",
      "use_previous": true,
      "parallel": true,
      "step": {
        "action": "generate_video",
        "model": "<image-to-video model id>",
        "prompt": "the red sports car slowly rotates on a turntable, smooth motion, studio lighting",
        "duration": 5,
        "filename": "car-spin-{i}"
      }
    }
  ]
}
```

```bash
uv run scripts/pipeline.py --pipeline car.json --output-dir ./renders
```

## Worked example: image → upscale → animate with audio

```json
{
  "steps": [
    {
      "action": "generate_image",
      "model": "<high-fidelity model>",
      "prompt": "a majestic dragon perched on a cliff overlooking a stormy ocean",
      "filename": "dragon"
    },
    {
      "action": "enhance",
      "use_previous": true,
      "enhancer": "<creative upscaler>",
      "width": 4096,
      "height": 4096,
      "creativity": 3,
      "filename": "dragon-4k"
    },
    {
      "action": "generate_video",
      "use_previous": true,
      "model": "<video model with audio support>",
      "prompt": "the dragon spreads its wings and roars, lightning strikes, waves crash below",
      "duration": 8,
      "generateAudio": true,
      "filename": "dragon-epic"
    }
  ]
}
```

## Template variables

```bash
uv run scripts/pipeline.py --pipeline template.json --var subject="red sports car" --var style="cinematic"
```

JSON can reference `{{subject}}`, `{{style}}`. Missing vars exit non-zero.

## Parallel fan_out

Add `"parallel": true` to a `fan_out` step. Sub-jobs run concurrently up to `--max-parallel` (default 3).

## Resume

`--resume` restores from `.pipeline-state.json` written next to the output. Lets you re-run after a crash without re-paying for completed steps.

## Picking model IDs to put in the pipeline JSON

`pipeline.py` resolves model names against the Krea OpenAPI spec. To know what IDs are valid right now, you can:

- Use the MCP from inside Claude: `mcp__krea-public-api__list_models()` and pick from the result.
- Or hit the spec directly: `curl https://api.krea.ai/openapi.json | jq '.paths | keys'`.

Don't hardcode IDs from memory; the lineup changes.

## Inline pipelines (no JSON file)

For one-liners:

```bash
uv run scripts/pipeline.py --pipeline '{"steps":[{"action":"generate_image","model":"<id>","prompt":"a cat astronaut","filename":"cat"},{"action":"enhance","use_previous":true,"enhancer":"<upscaler>","width":4096,"height":4096,"filename":"cat-4k"}]}'
```
