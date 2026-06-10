# Async Polling

The Krea MCP exposes a `sync` flag on `generate_image`, `generate_video`, and `enhance_image`. When `sync=true`, the tool blocks until the job is done — capped at `timeoutSeconds` (max **300 seconds**).

## When to use sync

| Operation | Use sync? | Why |
|---|---|---|
| Image generation | ✅ `sync=true, timeoutSeconds=60` | Most finish in 5–30s. The 300s cap is comfortable headroom. |
| Image enhancement | ✅ `sync=true, timeoutSeconds=60` | Typically 5–60s. Same headroom. |
| Video generation | ❌ never sync | Routinely runs 30s to 5+ minutes. Hitting the 300s cap leaves the job orphaned mid-run and you can't tell from the timeout whether it failed or is still going. |

## Video polling pattern

```
# 1. Submit, get the job back immediately
job = generate_video(
    model="<id>",
    input={prompt: "...", aspect_ratio: "16:9", duration: 5},
    sync=false,
)
# job has shape: { job_id: "uuid-...", status: "queued", ... }

# 2. Poll every 10 seconds
loop:
    status = get_job(jobId=job.job_id)
    # status.status is one of:
    #   "backlogged" | "queued" | "scheduled" | "processing" | "sampling" |
    #   "intermediate-complete" | "completed" | "failed" | "cancelled"
    # Terminal states: completed | failed | cancelled
    if status.status == "completed":
        # status.result.urls has the output URL(s)
        break
    if status.status in ("failed", "cancelled"):
        # surface the error and stop
        break
    sleep 10  # seconds
```

Non-terminal states are progress signals — the agent doesn't need to interpret them individually. Just keep polling until terminal.

## Why 10 seconds between polls

- Faster than 10s burns the Krea API rate limit and adds chat noise.
- Slower than 10s makes the user wait longer than necessary for short videos.
- 10s is the sweet spot for typical video durations (30s–3min).

For very long jobs (4K renders, long durations), bump to 20s. For short Hailuo-style budget videos, 5s is fine.

## CLI gotchas (`krea jobs wait` shell capture)

`krea jobs wait <id> --json` writes BOTH a progress spinner and the final JSON to stdout. Naive capture like `RESULT=$(krea jobs wait $JOB --json)` produces a string shaped like `"processing... processing... {actual JSON}"` and breaks downstream `jq` parsing.

Two reliable workarounds:

```bash
# Workaround A — grep the JSON line out of the noisy stream
RESULT=$(krea jobs wait "$JOB" --json 2>/dev/null | grep -E '^\{')

# Workaround B — separate progress from JSON
krea jobs wait "$JOB" --json 2>/dev/null | tail -n 1 > /tmp/result.json
URL=$(jq -r '.result.urls[0]' /tmp/result.json)
```

## Result URL — handle both response shapes

Video job completion payloads return URLs at one of two paths depending on model + completion timing:

- Most models (Seedance-2, Kling, Veo) terminal payload: `.result.urls[0]`
- Some intermediate or older models: `.urls[0]` at top level

Always use the defensive jq path:

```bash
URL=$(echo "$JSON" | jq -r '.result.urls[0] // .urls[0]')
```

If both return null, the job is either still processing OR shadow-failed (per `models/seedance-2.md` "Content-filter shadow-fail" — empty `result:{}` with `status:"completed"`). Distinguish by checking `.status` and `.result` separately.

## What goes in chat output

Don't narrate every poll. The user doesn't need to see `queued... queued... running... running...`. Acceptable progress signals:

- A single line when the job starts: `Generating video (model: <id>)…`
- An update every ~30 seconds if the job is still running: `Still rendering (1m elapsed)…`
- The final result: `Done. <URL>`

Bad output:
```
queued...
queued...
running...
running...
running...
```

Good output:
```
Generating video (~30s typical for this model)...
Done. https://krea.ai/.../output.mp4
```

## Errors during polling

- **`status.status === "failed"`** → check `status.result` or `status.error` for the reason. Common causes: NSFW content detection, prompt violations, internal model error. Surface a one-line summary to the user and offer to retry with adjusted prompt.
- **`status.status === "cancelled"`** → the user or the system aborted. Don't retry automatically.
- **Network error on `get_job`** → retry up to 3 times with exponential backoff (5s, 15s, 45s) before giving up.
- **Job stuck in `queued` for >5 minutes** → mention it to the user. Don't retry the submission silently — it's probably waiting on system capacity, not lost.

## Timeout guidance

A reasonable wall-clock ceiling for video polling: **10 minutes** for standard work, **30 minutes** for 4K / long-duration jobs.

If the loop exceeds that, surface to the user:
```
Job is still running after 10 minutes. The result will appear at <URL> when ready, or you can check status with the job ID: <id>.
```

Then stop polling and let the user follow up.
