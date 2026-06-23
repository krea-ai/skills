# Progress Reporting

Use this reference during async polling for any job expected to run longer than 30 seconds, especially video generation, LoRA training, and large batches.

## Rule

While polling, send the user one concise progress ping about every 30 seconds:

```text
Still processing at <elapsed>m / ~<expected>m total. I will ping when it finishes or if anything goes wrong.
```

The 2026-05-17 production session went 30+ minutes with silent polling. That silence damaged trust more than the failed output did. Never repeat it.

## Cadence

- Ping immediately when a job enters a new visible state: `queued`, `processing`, `completed`, `failed`, or `cancelled`.
- During a long unchanged state, ping every 25-35 seconds.
- Do not ping more often than every 25 seconds unless the status changed or the user asked.
- For multiple parallel jobs, aggregate in one line instead of sending one message per job.

## MCP Loop

Call `get_job(jobId=<id>)`, inspect the status, sleep roughly 20 seconds, and repeat until terminal. Ping the user on status changes and every 25-35 seconds during unchanged processing.

## What to Say

Good:

- `Queued: video job submitted. Expected 10-15 minutes.`
- `Still processing at 6m / ~12m total. I will keep checking.`
- `Completed. Downloading and checking frames now.`
- `Failed after 4m. I am checking the error before deciding whether to retry.`

Bad:

- Raw job IDs without context.
- Full JSON dumps.
- Repeated "still working" every few seconds.
- Silence for a long poll loop.

## On Delay

If a video job remains queued for more than 5 minutes, tell the user it is likely capacity-related and ask whether to keep waiting or stop. If a job exceeds the workflow's expected upper bound by more than 50%, explain the delay before continuing to poll.
