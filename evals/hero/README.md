# Hero evals

Deck-compliant **hero-eval layer** for the Krea Codex plugin. It tests whether an
agent can *complete* a hero workflow using the Krea tools — graded over the
**tool path + final outcome**, with full transcripts captured.

This sits **beside** the regex smoke suite (`../scenarios.md` + `../run.sh`), which
greps the final text only. The hero layer is the tool-path-graded superset:
several hero cases reuse smoke-suite prompts but verify the *actual* tool calls.
Neither layer touches the other.

## What a run does

For each case → each prompt variant:

1. Runs a headless agent loop: `claude -p --output-format stream-json` with the
   **checked-out** skills loaded via `--plugin-dir <repo-root>` (so the working
   tree's skills are evaluated, not the published ones).
2. Parses the transcript into an ordered **tool path**, mapping both
   `mcp__krea__*` tool calls **and** `krea …` CLI calls (run through `Bash`) onto
   one surface-agnostic step vocabulary, plus text-detected behaviours
   (`cost_preflight`, `await_confirmation`, `vision_qa`, `refuse`).
3. Grades, lightest verifier first:
   - **required / forbidden phrases** — cheap contains/regex over the answer.
   - **expected tool path** — ordered-subsequence over the observed steps.
   - **safety behaviour** — per `execution_class` (see below).
   - **grading criteria** — an LLM judge (`--judge`) reads the transcript + rubric
     and returns `{verdict, reason}`.

Verdicts: `PASS` · `FAIL` · `MANUAL_REVIEW` (gates passed but the judge wasn't
run) · `ERROR`. Exit codes mirror `run.sh`: `0` all pass, `1` any fail/error,
`2` manual-review-without-judge, `3` harness error.

## Execution classes (and how they keep CI cheap)

| class | correct behaviour | Krea spend |
|---|---|---|
| `confirm-and-stop` | present a cost-preflight and **stop** before the expensive op (video / LoRA train / large batch) | ~$0 (cheap prep only) |
| `execute-cheap` | run one cheap real generation and deliver | a few cents |
| `no-invoke` | answer normally; **don't** touch any Krea tool | $0 |
| `refuse` | decline unsafe generation; no `generate_image` | $0 |

The runner also passes `--disallowedTools` for the costly ops a correct
`confirm-and-stop` / `refuse` / `no-invoke` run would never reach (defense in
depth), and caps Anthropic spend with `--max-budget-usd`. The demo account's
credit cap is the final backstop.

## Usage

```bash
# offline — validates the parser + verifier with synthetic transcripts (no API)
python evals/hero/run.py --selftest

# list cases
python evals/hero/run.py --list

# one case, with the LLM judge (needs ANTHROPIC_API_KEY + KREA_API_KEY)
python evals/hero/run.py --case HC-04 --judge

# generation-free subset (what the per-PR CI job runs)
python evals/hero/run.py --no-generation --exec-class no-invoke,refuse,confirm-and-stop --judge

# everything
python evals/hero/run.py --judge
```

Flags: `--only ids`, `--case id`, `--exec-class classes`, `--limit N`,
`--no-generation`/`--no-execute`, `--model`, `--judge-model`, `--judge`,
`--budget`, `--out`, `--json-summary`. `--only`/`--case` accept an id
(`fast-iterate-draft`), a number (`4`), or `HC-04`.

Outputs land in `evals/hero/runs/<timestamp>/` (git-ignored): per-variant
`transcript.jsonl`, `tool_path.json`, `final.txt`, `verdict.json`; plus
`summary.json` and an appended `runs/history.jsonl`.

## Auth & fixtures

- **Auth**: Krea CLI + `KREA_API_KEY` (README Option A) — headless-friendly. MCP
  OAuth is *not* used in CI; with only the CLI authed, tool calls appear as
  `Bash(krea …)` and the runner maps them to the same logical steps. (Set
  `HERO_ATTACH_MCP=1` to also attach `.codex-plugin/.mcp.json` locally.)
- **Fixtures** are **Krea-hosted demo-account asset URLs** declared in each
  case's `fixture.assets[].url` — never committed binaries. Provision the
  `krea-demo-review` account with the referenced assets (one product photo, a
  soft photo for upscale, a product-on-plain-bg for i2i, a 3D viewport
  screenshot, and a 15-18 image mascot training set) and keep its job history
  clean so the cost-gate cases start fresh.

## Case format

One JSON file per case in `cases/`. See `cases/HC-02-product-teaser-5s.json` for
a worked example. Key fields: `prompts[]` (2-3 variants tagged
`clear|ambiguous|misspelled|should-not-invoke|implicit|explicit`),
`expected_output`, `required_facts`, `required_phrases`/`forbidden_phrases`,
`expected_tool_path`, `forbidden_steps`, `execution_class` + control flags
(`require_preflight`, `require_await`, `require_paid_step`,
`max_cheap_generations`, `must_refuse`, `must_not_invoke`), `safety_behavior`,
`fixture`, and `grading_criteria` (the judge rubric). `workflow_files` names the
SKILL/workflow a failure points at — the deck's failure→change loop.

## CI

`.github/workflows/evals.yml`: full suite nightly (07:00 UTC) +
`workflow_dispatch` + `repository_dispatch(krea-tools-changed)` (fired by the
webapp when the tool surface changes); plus a generation-free subset on PRs
labeled `run-hero-evals`. Secrets: `ANTHROPIC_API_KEY`, `KREA_API_KEY`
(demo account), `SLACK_WEBHOOK_URL`.
