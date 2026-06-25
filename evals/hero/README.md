# Hero evals

Hero-use-case evals for the Krea Codex plugin: 10 cases (`cases/HC-*.json`) that each pin a real
workflow to a golden spec, plus a runner/grader (`run.py`).

- **`run.py --run-codex CASE`** is the automated runner. It drives the case through real Codex
  headless (`codex exec --json`, resuming the thread for follow-ups) against the connected Krea
  MCP, then grades each transcript. Spends real OpenAI (Codex) + Krea + judge credits.
- **`run.py --grade CASE transcript.json`** grades a transcript you captured some other way — e.g.
  by running the prompts manually in Codex (the `@plugin-eval` plugin is handy for that).
- **`run.py --lint` / `--selftest`** are offline: spec + fixture validation and grader unit tests,
  no secrets, no spend. This is what CI runs on every push/PR.

## Layout

```
evals/hero/
  cases/HC-*.json   golden specs (one per case)
  fixtures/         committed reference images used by the cases
  run.py            runner + grader + lint/selftest
```

## Run a case end-to-end (real Codex)

1. **Authenticate Codex and install the Krea plugin.** Install the *plugin* (not just
   `codex mcp add`) — `codex exec` loads the Krea **skills** only when the plugin is
   installed; an MCP added on its own gives the tools without the workflow guidance.
   ```bash
   printenv OPENAI_API_KEY | codex login --with-api-key   # or: codex login (ChatGPT)
   export KREA_API_KEY=...                                 # Krea MCP bearer token
   bash evals/hero/install-codex-plugin.sh                 # builds + installs the plugin
   ```
   The helper builds the plugin and registers it with a **bearer-token** MCP variant
   (the shipped `.codex-plugin/.mcp.json` is OAuth, which can't authenticate headlessly).
2. **Run + grade:**
   ```bash
   python evals/hero/run.py --run-codex HC-05 --judge
   ```
   Each run executes in a throwaway working dir carrying a routing `AGENTS.md` (see
   [Routing](#routing) below), then sends each prompt variant (and any scripted follow-up)
   through Codex, reconstructs the tool path, and grades it. The full transcript is kept on
   each result for failure analysis. HC-03/04/05/06/07/08 run today; HC-01/02/09/10 need
   their review-account assets first (see [Fixtures](#fixtures)).

## Routing

Codex ships a built-in image-generation tool, and for a generic "make an image" prompt it
will use that instead of Krea — the Krea MCP tools sit behind `tool_search`, and the skill
only binds once activated. So the runner drops a small `AGENTS.md` into each run's working
dir instructing Codex to route image/video work to the Krea MCP (and not the built-in tool).
It's scoped to creative requests, so the should-not-invoke and safety-refusal cases are
unaffected. Without it, implicit prompts never reach Krea.

### Interactive alternative

Instead of the headless runner you can run the prompts by hand in Codex (e.g. with `@plugin-eval`),
save the transcript as JSON, and grade it:

```bash
python evals/hero/run.py --print-prompts --case HC-05   # get the prompts + follow-ups
python evals/hero/run.py --grade HC-05 transcript.json --judge
```

## Transcript format

Single- or multi-turn:

```json
{ "turns": [
  { "user": "<prompt>", "assistant": "<final text>",
    "tool_calls": [ {"name": "mcp__krea__list_models", "args": {}} ] },
  { "user": "<scripted follow-up reply>", "assistant": "...",
    "tool_calls": [ {"name": "mcp__krea__generate_video", "args": {"duration": 5}} ] }
] }
```

A `codex exec --json` event stream or a Claude Code `--output-format stream-json` dump is also
accepted. The grader applies a lightest-verifier ladder:

1. **Expected tool path** — deterministic ordered-subsequence over the whole conversation (tool
   names are mapped surface-agnostically: `mcp__krea__*`, `krea …` CLI, or already-logical step
   names all normalize to the same steps).
2. **LLM judge** (`--judge`) — grades `required_facts` + `safety_behavior` + `grading_criteria`
   over the full transcript (incl. all turns). Without `--judge` a tool-path-clean run is
   `MANUAL_REVIEW` (judge deferred). A judge that can't run returns `ERROR`, never a silent pass.

## Multi-turn

Cases that need a follow-up (HC-01/02/03/04/09/10) carry `followups` — scripted user replies. The
pattern: on turn 0 the agent should stop (cost-preflight / clarifying question); after the scripted
reply it should proceed correctly. The grader reconstructs the tool path across **all** turns and
the judge evaluates the whole arc.

## Case format

One JSON file per case:

| Field | Meaning |
|---|---|
| `prompts[]` (`text` + `tag`: clear/ambiguous/misspelled/should-not-invoke/implicit/explicit) | User prompt(s), covering a range of real-world phrasings + invocation styles |
| `expected_output` | Representative successful final answer |
| `required_facts` | Facts the verifier must see |
| `expected_tool_path` | Required logical step sequence (surface-agnostic) |
| `safety_behavior` | Side-effect / confirmation behavior to enforce |
| `fixture` | Review account + reference assets (each a local `path` or a `url`) |
| `grading_criteria` | Pass/fail rules for the verifier |

Plus `skill` + `workflow_files` (which SKILL a failure points at — the failure→change loop),
`default_prompt` (maps to a directory default prompt), and `followups` (scripted multi-turn replies).

## Fixtures

`cases/*.json` reference assets under `fixture.assets[]`, each as a local `path` (committed in
`fixtures/`, resolved relative to `evals/hero/`) or a `url`. Local-path fixtures are verified to
exist by `--lint`. HC-03/05/06 ship with committed images; HC-01/02/09/10 still point at
placeholder URLs and need real review-account assets before they can run live.

## Offline (CI)

```bash
python evals/hero/run.py --lint       # validate specs + fixtures
python evals/hero/run.py --selftest   # grader unit checks (incl. multi-turn), no API
```

`.github/workflows/evals.yml` has two jobs:

- **`hero-specs`** — the offline gate above. Runs on every push to `main` / PR. No secrets, no spend.
- **`hero-evals-live`** — runs the suite through real Codex (`--run-codex --judge`) and grades each
  transcript. Spends real credits, so it's gated to manual dispatch ("Run workflow") or a
  `run-hero-live` PR label.

## Submission checklist

- [ ] Hero prompts + repeatable eval scenarios documented (these specs).
- [ ] Review/demo account with realistic data + the per-case fixture assets provisioned.
- [ ] Hero workflows validated against real Codex; transcripts captured + graded.
