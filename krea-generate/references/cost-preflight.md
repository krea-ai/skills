# Cost Preflight

Use this reference before any operation or workflow expected to spend more than 100 compute units, any video generation, any LoRA training run, or any batch whose total cost is uncertain.

## Rule

Show the user the estimated cost and wall-clock time, then wait for an explicit yes before submitting. Do not auto-proceed if the user goes silent.

```text
This workflow = <N jobs> x <M CU> = total ~<T> compute units, expected wall-clock ~<W> minutes. Proceed?
```

For Pro or unlimited-credit users, still show the estimate. They may not care about credit balance, but they still care about time, queue pressure, and avoiding wrong expensive outputs.

## When to run it

- Any video job.
- Any LoRA training job.
- Any batch over 100 CU total.
- Any 4K or premium render whose cost is materially higher than a draft.
- Any user request that says "campaign", "batch", "all variants", or "full workflow".

## What to estimate

1. Resolve the workflow and model archetypes.
2. Inspect live schema/model details through the available Krea tools.
3. Estimate per-job CU from live model details or the workflow's documented default.
4. Multiply by the planned number of jobs.
5. Add expected wall-clock time from the workflow doc.

If model details do not expose CU, say so and use the workflow's documented approximation:

```text
I cannot read live CU pricing for this model, so I am using the workflow estimate: ~1564 CU per 15s video, ~10-15 minutes per run. Proceed?
```

That fallback is for a single short social-style video job. Do not reuse it for shot-grammar animation workflows; estimate per-shot video cost from the approved shot count and live model details.

## Session Override

If the user says "skip the preflight", "just go", "do not ask again", or equivalent, record a per-session override and do not ask again in that session. Still keep the workflow's internal approval gates when they are creative gates, such as storyboard approval before social video animation.

Example note to self:

```text
Krea cost-preflight override active for this session: user approved skipping repeated cost prompts.
```

Do not persist the override to project files unless the user explicitly asks.

## Hard Gates

- No `quality=high` on more than 3 outputs without prior contact-sheet, storyboard, or key-visual-sheet approval.
- No video generation without an approved storyboard, key-visual sheet, or equivalent user-approved motion brief.
- No regeneration of finals after "boring", "meh", or "not what I wanted" feedback without first identifying which lever should change: format, content, palette, voice, or fidelity.
- No expensive campaign batch when the deliverable vocabulary is ambiguous. Disambiguate with `artifact-taxonomy.md` and a reference image first.

## Bad patterns

- Do not hide cost because the user has unlimited credits.
- Do not bury the estimate in a long explanation.
- Do not start video while asking for permission.
- Do not treat "sounds good" from an earlier unrelated step as approval for a new expensive operation.
- Do not split the cost question across multiple messages; ask once, plainly.
