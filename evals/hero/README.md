# Hero evals

Hero-use-case evals for the Krea Codex plugin, structured the way the *"How to
Build a Great Codex Plugin"* deck asks for them.

**The eval loop runs in Codex with `@plugin-eval`** — that's where the plugin
(the Krea MCP app + skills) loads natively and drives the agent/tool calls. This
folder is the repo-side half the deck also requires:

- **`cases/*.json`** — the golden **hero specs** (`@plugin-eval` and reviewers read
  these): user prompt(s), expected output, required facts, expected tool path,
  safety behavior, fixture/state, grading criteria.
- **`run.py`** — a **transcript grader** + offline lint/self-test. It grades a
  captured run against a spec (`transcript → verifier → result`); it does **not**
  drive a live agent/tool surface (that's `@plugin-eval`'s job in Codex).

> Why not run the whole loop in CI? The plugin is MCP-only and the Krea MCP is
> OAuth-based, so it doesn't run in a headless CI agent. The deck's guidance is to
> **run the loop in Codex, start manual, and automate only the stable parts** — so
> CI here runs just the secret-free spec lint + grader self-test.

## Run the evals (in Codex)

1. **Connect the Krea plugin in Codex** (deck appendix): install/authenticate the
   Krea app in ChatGPT, confirm it appears in Codex, and verify `mcp__krea__*`
   tools are available.
2. **Provision the review account** with the fixture assets each case references
   (`fixture.assets[].url`) and a clean job history.
3. **Get the prompts:** `python evals/hero/run.py --print-prompts` (add `--case HC-02`
   for one). Each case lists its 2-3 prompt variants and any scripted follow-up
   replies.
4. **Run with `@plugin-eval`** against the connected plugin. For a **multi-turn**
   case, send the prompt, then — when the agent stops to ask — send the case's
   scripted follow-up reply (the "(then reply) …" lines).
5. **Save the transcript** as JSON and grade it (next section).

## Grade a captured transcript

```bash
python evals/hero/run.py --grade HC-02 transcript.json --judge
```

Transcript format (single- or multi-turn):

```json
{ "turns": [
  { "user": "<prompt>", "assistant": "<final text>",
    "tool_calls": [ {"name": "mcp__krea__list_models", "args": {}} ] },
  { "user": "<scripted follow-up reply>", "assistant": "...",
    "tool_calls": [ {"name": "mcp__krea__generate_video", "args": {"duration": 5}} ] }
] }
```

A Claude Code `--output-format stream-json` dump is also accepted. The grader
applies the deck's lightest-verifier ladder:

1. **Expected tool path** — deterministic ordered-subsequence over the whole
   conversation (tool names are mapped surface-agnostically: `mcp__krea__*`,
   `krea …` CLI, or already-logical step names all normalize to the same steps).
2. **LLM judge** (`--judge`) — grades `required_facts` + `safety_behavior` +
   `grading_criteria` over the full transcript (incl. all turns). Without
   `--judge` a tool-path-clean run is `MANUAL_REVIEW` (judge deferred). A judge
   that can't run returns `ERROR`, never a silent pass.

## Multi-turn

Cases that need a follow-up (HC-01/02/03/04/09/10) carry `followups` — scripted
user replies. The pattern is the deck's "prompts that require follow-ups": turn 0
the agent should stop (cost-preflight / clarifying question); after the scripted
reply it should proceed correctly. The grader reconstructs the tool path across
**all** turns and the judge evaluates the whole arc.

## Case format

One JSON file per case. Fields map to the deck's spec table:

| Field | Deck field |
|---|---|
| `prompts[]` (`text` + `tag`: clear/ambiguous/misspelled/should-not-invoke/implicit/explicit) | User prompt(s) |
| `expected_output` | Expected output |
| `required_facts` | Required facts |
| `expected_tool_path` | Expected tool path (logical, surface-agnostic) |
| `safety_behavior` | Safety behavior |
| `fixture` | Fixture / state |
| `grading_criteria` | Grading criteria |

Plus `skill` + `workflow_files` (which SKILL a failure points at — the deck's
failure→change loop), `default_prompt` (maps to a directory default prompt), and
`followups` (scripted multi-turn replies).

## Offline (CI)

```bash
python evals/hero/run.py --lint       # validate every spec
python evals/hero/run.py --selftest   # grader unit checks (incl. multi-turn), no API
```

`.github/workflows/evals.yml` runs exactly these two on push/PR — no secrets, no
live generation.

## Submission checklist (deck §05)

- [ ] Hero prompts + repeatable eval scenarios documented (these specs).
- [ ] Review/demo account with realistic dummy data (the fixtures).
- [ ] Hero workflows validated in Codex via `@plugin-eval`; transcripts captured + graded.
