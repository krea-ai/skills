# Multi-Step Pipelines

The Krea skill ships no scripts. Multi-step workflows happen through **agent orchestration** of CLI or MCP calls, with CLI as the default surface. For repeatable pipelines in the user's own stack (Python, Node, Bash, Go — whatever the project uses), hand off to `../../krea-build/SKILL.md` which generates code in the user's language.

## Two shapes of "pipeline"

### 1. One-off, agent-driven

User says: *"Generate a dragon image, upscale to 4K, then animate it."*

The agent chains operations directly:

**MCP:**
```
result = generate_image(model="<high-fidelity image>", input={prompt, ...}, sync=true)
enhanced = enhance_image(model="<upscaler>", input={imageUrl: result.url, width: 4096, height: 4096}, sync=true)
job = generate_video(model="<image-to-video>", input={startImage: enhanced.url, prompt: "...", duration: 6}, sync=false)
# loop get_job(jobId=job.id) until terminal
```

**CLI:**
```bash
HERO=$(krea generate image -m <id> -p "a dragon on a cliff" --aspect 16:9 --wait --json | jq -r '.urls[0]')
HERO_4K=$(krea generate enhance -m topaz/standard-enhance "$HERO" --width 4096 --height 4096 --wait --json | jq -r '.urls[0]')
JOB=$(krea generate video -m <id> --start-image "$HERO_4K" -p "the dragon roars" --json | jq -r .job_id)
krea jobs wait "$JOB" --json | jq -r '.urls[0]'
```

This is what the agent does in chat. No external script needed.

### 2. Repeatable, user's-stack-driven (via `krea-build`)

User says: *"I need to run this pipeline for every new product launch — give me a script I can re-run."*

The agent loads `krea-build` and writes the pipeline in the user's stack:

- **Python project** → a `pipeline.py` with `requests` + the polling pattern
- **Node project** → a `pipeline.ts` with `fetch` + async helpers
- **Bash-only** → a `pipeline.sh` using `krea` CLI + `jq`
- **Existing TS app** → an `app/api/generate/route.ts` server endpoint

`krea-build/references/api-client.md` has both TypeScript and Python helpers ready to drop in. `krea-build/references/integration-patterns.md` covers the orchestration shape.

The skill doesn't pick the language; the user's stack does.

## Common pipeline patterns

### Chain (output → input)

Each step uses the previous step's output URL.

```bash
# Bash + CLI
A=$(krea generate image -m <id> -p "..." --aspect 16:9 --wait --json | jq -r '.urls[0]')
B=$(krea generate enhance -m <upscaler> "$A" --width 4096 --height 4096 --wait --json | jq -r '.urls[0]')
echo "Final: $B"
```

### Fan-out (one input → N parallel children)

Submit N video jobs in parallel from one hero frame, poll each.

```bash
HERO=$(krea generate image -m <id> -p "hero shot" --wait --json | jq -r '.urls[0]')

JOBS=()
for prompt in "camera pushes in" "slow rotation" "fade to night"; do
  JOB=$(krea generate video -m <id> --start-image "$HERO" -p "$prompt" --json | jq -r .job_id)
  JOBS+=("$JOB")
done

for JOB in "${JOBS[@]}"; do
  krea jobs wait "$JOB" --json | jq -r '.urls[0]'
done
```

### Resume / state

The CLI doesn't track state across runs. If the user wants resumability (skip already-completed steps on re-run), the agent writes a small script in their stack that persists job IDs / output URLs to a JSON file between steps. `krea-build` covers this pattern.

### Cost preflight

Both MCP and CLI surface CU cost in the model description. Before a large pipeline, the agent should sum estimated costs and confirm with the user. The check itself is just `krea models show <id> --json` per model used and reading the CU section.

## When NOT to write a pipeline script

- One-off requests (just chain in chat)
- Exploratory work (the agent iterating with the user)
- Anything where the prompt or step list might change next time

Scripts are for the moment the *exact same flow* repeats. Until then, agent orchestration is faster.

## Migrating from older versions

Previous Krea skill versions shipped `pipeline.py`. It's been removed in favor of agent orchestration + `krea-build`. If you used it, the agent can reproduce the equivalent flow:

- `--fan_out + parallel` → loop in bash/TS, collect job IDs, poll each
- `--var key=value` → shell variable interpolation
- `--resume` → write a small state file (`pipeline-state.json`) with completed step URLs, check on re-run
- `--dry-run` → loop `krea models show <id> --json` for each step, sum CU

The agent walks the user through the migration on request.
