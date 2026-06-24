# Budget Tracking — Session CU Counter

`cost-preflight.md` catches *upcoming* expensive operations. Budget tracking catches the *accumulation* of cheap ones — the iterative re-rolls, asset-sheet batches, and scene variations that silently exhaust a session before the user notices.

Use this whenever a workflow spans multiple billable operations: narrative video, full ad campaign, LoRA training, multi-scene anything.

## Protocol

1. **Initialize at session start.** Record `session_cu_spent = 0` in your working memory. If the user shares a budget or token balance, record `session_cu_budget` too; otherwise treat budget as unknown.
2. **Add each successful job's cost** as it returns. MCP job responses surface CU per job when available - capture it from the result.
3. **Surface the running total at logical breakpoints**: after each asset batch, after each scene approval, before any single op estimated above 500 CU. Keep the line short: `Session spend: ~840 CU.`
4. **Warn early.** When `session_cu_spent` is climbing toward `session_cu_budget` (if known) or past ~2000 CU (if unknown), recommend a checkpoint: "Spend so far ~X CU — keep going or pause to checkpoint?"
5. **Handle 402 Payment Required as a first-class outcome.** On the first 402, stop submitting jobs, surface the current spend, and tell the user: "Your account hit the credit limit. Top up at https://www.krea.ai/settings/billing, or authenticate Krea MCP with an account that has credits. Work is saved; we resume when you're ready."

## What counts as billable

- Every successful `generate image`, `generate video`, `generate enhance` job.
- Every LoRA training run.
- Every re-roll. Aborted (validation-rejected) submissions are not billed; do not count them.

Uploads and schema reads are free.

## Where to read the cost

- The job response includes a cost field once terminal. Read `get_job(...).result.cost` or the equivalent schema-declared field.

## Aggregating across asynchronous jobs

For parallel batches, wait for all `get_job` results before reporting the batch total. Don't report partial spend mid-batch — it reads as flicker.
