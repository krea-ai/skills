# Krea AI Skills

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![version](https://img.shields.io/badge/version-0.7.7-green.svg)](VERSION)
[![skills](https://img.shields.io/badge/skills-3-purple.svg)](#install-the-skills)
[![discord](https://img.shields.io/badge/discord-join-5865F2?logo=discord&logoColor=white)](https://discord.com/invite/krea-1002244500581798028)

Three packaged Agent Skills for working with [Krea.ai](https://krea.ai). Install once, get the Krea skill suite.

| Skill | When to use |
|---|---|
| **`krea-generate`** | Canonical generic-generation router. Image, video primitives, enhancement, edits, LoRA, portraits, text/poster work, and archviz through connected Krea MCP tools. |
| **`krea-marketing`** | Marketing creative workflow: packaging design and mockups, product photoshoots, marketplace image sets, DTC static ad templates (one product photo → a library of on-brand ad formats), key visuals, UGC/social ads, campaign packs, and optional Meta Ads performance context. |
| **`krea-motion`** | Product and brand motion: cinematic shots, multi-beat reveal films, logo stings, luxury and beauty product loops, edit assembly, QA, and retakes. Not for anime or narrative animation. |

Experimental app-integration material lives under `wip/` and is not installed or packaged by default.

The generation skills work with Cursor, Codex, Windsurf, OpenCode, Gemini, OpenClaw, and other agents that pick up `~/.<agent>/skills/<name>/SKILL.md`. The Claude plugin is a separate, restricted connector for balance, files, uploads, and Claude Motion imports; it does not load these generation skills.

## Install the skills

```bash
npx skills add krea-ai/skills
```

Installs the generation skills for agents using Krea's unrestricted MCP. For Claude, use the restricted plugin below instead.

## Prerequisites

The packaged Codex and Cursor plugins use a connected Krea MCP server.

Check your agent's MCP tool list for Krea tools. If the tools are missing or auth has expired, connect or authenticate the Krea MCP server before using generation skills. Cursor plugin installs discover the remote server from the root `mcp.json` and start Cursor's OAuth flow; no API key or client secret is stored in this repository. For Codex plugin installs, the practical reauth path is to uninstall and reinstall the Krea plugin so the install auth flow runs again.

## Plugin packaging

This repository has provider-specific packages:

- Cursor reads `.cursor-plugin/plugin.json`, whose explicit `skills` paths point at the existing top-level skill directories, and discovers the Krea server from `mcp.json`.
- Codex is packaged from `.codex-plugin/plugin.json` and `.codex-plugin/.mcp.json` with `npm run build:codex-plugin`.
- Claude reads `.claude-plugin/plugin.json` and root `.mcp.json`, which points at `https://api.krea.ai/claude-mcp` with the same OAuth resource. Neither the plugin nor its marketplace entry loads generation skills. Codex and Cursor keep `https://api.krea.ai/mcp` in their own configurations.

### Claude connector

In Claude Code, add the marketplace and install the plugin:

```text
/plugin marketplace add krea-ai/skills
/plugin install krea@krea
```

Authenticate the Krea server through `/mcp`. After upgrading from an older plugin, reconnect if prompted so authentication uses the restricted resource. For Claude's web connector setup, use `https://api.krea.ai/claude-mcp` as the server URL; installing a Code plugin does not install a web connector.

The connector supports `get_balance`, `list_files`, `list_file_tags`, `read_files`, `create_folders`, `write_files_inline`, `write_files_upload`, `tag_files`, `get_upload_url`, `upload_asset`, and `import-claude-motion-from-url`. It does not expose AI generation, training, model discovery, or indirect workflow execution. Do not fall back to the unrestricted endpoint or generation skills when a tool is unavailable.

For a Claude Motion handoff, call `import-claude-motion-from-url` immediately with the supplied `url` and `download_token`; `title` and `claude_design_project_id` are optional. Treat the URL and token as credentials: do not echo, log, or save them. The source must be an HTTPS `claudeusercontent.com` subdomain serving an MP4 of at most 100 MiB. The result is synchronous: return its `url` to the user, with no job polling. Imports are MP4 files, not editable animation timelines, and their Krea links require authentication. To browse the imported file, use the returned `parent_uri` as `list_files.root_uri` because imports land in My Drive, while the default listing uses My Context. Re-sending the same design project updates its existing file in the original workspace.

Deploy the endpoint from [app#9672](https://github.com/krea-ai/app/pull/9672) before releasing this plugin update. Plugin installation does not guarantee directory approval or a Motion “Send to Krea” menu entry; those require separate Anthropic onboarding. Full Claude sign-in and end-to-end Motion import still need verification.

Validate the Claude package and client isolation with `npm run validate:claude-plugin`.

Validate the Cursor package before local testing or marketplace submission:

```bash
npm run validate:cursor-plugin
```

For local Cursor testing, symlink the repository to `~/.cursor/plugins/local/krea`, reload Cursor, verify the Krea skills and MCP server in **Customize**, and complete the Krea OAuth prompt. The public repository can then be submitted at [Cursor Marketplace Publish](https://cursor.com/marketplace/publish).

## Use the generation skills (Codex, Cursor, and other unrestricted clients)

### Default - `krea-generate` routes generic generation

```
> Generate an image of a cyberpunk cat in neon rain.
> Make a 5-second video of waves at sunset.
> Upscale this photo to 4K.
```

These stay in `krea-generate` and route to the right model via the live MCP catalog.

```
> Render this Sketchup screenshot in golden hour, photoreal.
> Make my Revit model interior look photoreal, midday.
> Take this chair, put it in this room, in this style.
```

These route through `krea-generate/workflows/archviz-3d-to-render.md` for structural-reference archviz rendering.

```
> Make a hero product shot of my new perfume bottle.
> Generate a TikTok ad for my sneakers.
> Turn this one product photo into a set of on-brand static ad formats.
> Take this product URL and give me a marketplace full set plus social variants.
> Use Meta Ads performance context before making new ad creative.
```

These trigger `krea-marketing`. The agent starts with a compact creative intake. For paid-social, performance, campaign-analysis, catalog-performance, or activation work, it asks whether to connect performance context; otherwise it proceeds Krea-only from product refs, brand refs, and goals. Any live launch, budget, status, catalog, or publishing change stays gated and paused/draft by default unless explicitly approved.

## Updates

The `krea-generate` skill includes an opt-in update notification. Once per session, the agent may run `krea-generate/scripts/update-check.sh`, which checks `https://raw.githubusercontent.com/krea-ai/skills/main/VERSION` against the installed `krea-generate/VERSION` file. If a newer version exists, it prints `UPGRADE_AVAILABLE <local> <remote>` to stdout - the agent surfaces this once, then continues. Snoozes 24h -> 48h -> 7d to avoid nagging.

**To upgrade**, re-run your install command (`npx skills add krea-ai/skills`, etc.).

**To disable the check**: `touch ~/.krea-skills/update-check-disabled`.

**To force a fresh check**: `bash krea-generate/scripts/update-check.sh --force`.

Single-source version: `VERSION` file at repo root. CI enforces that `krea-generate/VERSION`, all SKILL.md frontmatters, plugin manifests, and `package.json` agree.

## Evals

Two layers live under `evals/`.

### Hero suite — `evals/hero/`

The headline Codex-plugin workflows, driven through real Codex (`codex exec`) against the live Krea MCP and graded **outcome-based** (an expensive op must not fire before the user approves) with an LLM judge for nuance. Details: [`evals/hero/README.md`](evals/hero/README.md).

An **offline gate** runs on every push / PR — no secrets, no spend:

```bash
python evals/hero/run.py --lint       # validate case specs + fixtures
python evals/hero/run.py --selftest   # grader unit checks
```

The **live suite** spends real Codex + Krea + judge credits (~1–1.5h), so it is gated. It runs only on:

- a manual **Run workflow** dispatch of the **Hero Evals** action,
- a pull request labeled **`run-hero-live`**,
- a push to `main` touching `krea-*/` or `.codex-plugin/.mcp.json`,
- a `repository_dispatch: mcp-changed` from `krea-ai/app`.

> ⚠️ **Caveat:** a normal PR push (or a merge into the branch) does **not** run the live suite — you must add the exact `run-hero-live` label, or dispatch it manually:
>
> ```bash
> gh workflow run evals.yml --ref <branch>           # run the full real suite
> gh pr edit <pr-number> --add-label run-hero-live   # or trigger via the PR label
> ```

### Skill regression suite — `evals/run.sh`

47 local scenarios run through `claude -p` to catch routing / UX drift when skill content changes. Regex-graded (`PASS` / `FAIL` / `MANUAL_REVIEW`); see [`evals/README.md`](evals/README.md) for methodology and the full scenario list.

```bash
bash evals/run.sh
```

## License

MIT
