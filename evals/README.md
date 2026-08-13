# Krea Skills — Evals

Lightweight regression test suite for the Krea skills. Catches drift when skill content changes, model lineups shift, or routing rules get edited.

## What this tests

46 scenarios across 12 groups:

- **Routing accuracy (5)** — does the agent route to the right skill or workflow for a given brief?
- **Refusal / safety (3)** — does the agent decline or rephrase when the brief hits safety boundaries?
- **Cost awareness (3)** — does the agent pick cheap models for exploratory work and confirm cost on expensive ops?
- **Vision verification (3)** — does the agent `Read` outputs and catch when results don't match the brief?
- **Polling discipline (3)** — image / enhance use sync, video uses async + poll?
- **Edge cases (3)** — missing prompt, unknown model, prior-output reuse
- **Campaign regression (2)** — catches the CPG storyboard/key-visual routing failure and loose UGC variation behavior
- **Motion production (9)** — routes product/brand motion through `krea-motion`, keeps anime/narrative briefs out of it, and preserves approvals, cost, async polling, QA, retakes, and app-routing boundaries
- **Taxonomy 0.4.0 regression (8)** — proves generic generation stays in `krea-generate`, marketing routes to `krea-marketing`, Meta Ads behavior is gated, and product motion stills route to `krea-motion`
- **DTC ad templates 0.5.0 (1)** — keeps one-photo static ad set requests in the DTC template workflow
- **Scripted UGC video ads 0.6.0 (4)** — covers script gating, caption/post assembly, real screen recordings, and virality QA before delivery
- **Cinematic product ads 0.6.1 (2)** — covers reference-ad cut measurement, one-shot timeline prompting, start-image quality gating, and beat-length constraints

Full scenario list with expected behavior and fail criteria: `scenarios.md`.

## How to run

```bash
# v1 (regex grading + manual review for ambiguous cases)
bash evals/run.sh

# v2 (Claude-CLI-based judge — disabled in v1, enable later)
bash evals/run.sh --judge
```

Requires `claude` CLI installed and authenticated. Output is one of `PASS`, `FAIL`, or `MANUAL_REVIEW` per scenario, plus a summary at the end.

## When to run

- Before bumping `VERSION` in the skill repo
- After any significant change to a SKILL.md's routing / UX rules
- After a known change to the Krea MCP server's model lineup or schema shape

Treat results as **regression signal**, not a gating quality bar. The 46 scenarios cover the most common paths; novel use cases will still need human review.

## How the runner works

For each scenario in `scenarios.md`, the runner:

1. Composes the user input into a headless Claude prompt
2. Pipes it through `claude -p` with the Krea skills available
3. Captures the agent's response
4. Greps for `pass_regex` and `fail_regex` from the scenario
5. Records PASS / FAIL / MANUAL_REVIEW

`MANUAL_REVIEW` happens when neither pass nor fail regex matches — the response went off the expected path but isn't obviously wrong. A human reviewer (or future LLM judge) grades these.

## Adding new scenarios

Append to `scenarios.md` following the existing format:

```markdown
### N. Short title

**Category**: routing | refusal | cost | vision | polling | edge_case
**User input**: "exact brief the user would type"
**Expected**: one-sentence description of correct behavior
**Pass regex**: pattern that, if matched, indicates correct behavior
**Fail regex**: pattern that, if matched, indicates wrong behavior (e.g. wrong skill loaded)
```

Keep scenarios short. The runner is a smoke test, not a deep semantic check.

## v2: Claude-CLI judge

When v1 scenarios stabilize, enable `--judge` mode. It re-pipes `MANUAL_REVIEW` cases through `claude -p` with a judge prompt: "Given this user brief and this agent response, did the agent do the right thing? Reply PASS or FAIL with one-line reason."

v2 trades human review time for additional Claude API spend. Decision: ship v1 only until we know which scenarios actually drift in practice. v2 lands after a real regression has happened that v1 caught only via MANUAL_REVIEW.

## CI integration

Not yet wired into CI. Reason: running evals on every PR burns ~$1-3 of Claude API + 5-10 minutes wall time. Plan to run nightly on `main` once v1 scenarios prove stable.

To run locally before a PR:

```bash
cd /Users/albertsalgueda/Documents/skills
bash evals/run.sh > /tmp/eval-results.txt 2>&1
cat /tmp/eval-results.txt | tail -30  # see the summary
```
