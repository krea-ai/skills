---
version: 0.2.0
name: krea-build
description: "Patterns for building applications that integrate the Krea API. Auth, polling discipline, error handling, validation, frontend integration (SvelteKit/React/Vue), and the 'prototype in chat, productize in app' workflow. Use when the user is writing code that calls the Krea API directly — building a generator UI, a content pipeline, a creative tool — not when they just want to generate one image. For interactive generation use the sibling krea-ai skill instead."
license: MIT
---

# Krea Build — Integration Patterns for Developers

This skill is for **building apps that integrate Krea**. Not for one-off generations — that's the sibling `krea-ai` skill, which uses the Krea CLI by default and MCP as fallback.

Use this skill when the user is:

- Writing a TypeScript/Python/Go client that calls the Krea API directly
- Building a frontend that lets users generate content (SvelteKit, Next.js, etc.)
- Designing a content pipeline that runs in CI or production
- Embedding Krea outputs in a portfolio, document, or tool

## Self-update check (opt-in)

Once per session: run `bash /path/to/skills/scripts/update-check.sh`. Prints `UPGRADE_AVAILABLE <local> <remote>` if a newer version is out. Surface that to the user once, then continue. Snoozes 24h→48h→7d. Disable with `touch ~/.krea-skills/update-check-disabled`.

## When to use this skill vs. `krea-ai`

| Situation | Use |
|---|---|
| "Generate me an image of X" | `krea-ai` (CLI-first generation) |
| "Build me a moodboard app that uses Krea" | `krea-build` (this) |
| "Write a TypeScript helper to call Krea" | `krea-build` |
| "Run a one-off pipeline now" | `krea-ai` |
| "Add Krea generation to my React form" | `krea-build` |

## Critical workflow rule: prototype in chat, productize in the app

The single most expensive mistake when building Krea apps is writing app code around unproven generation output. Always:

1. **Prototype** — run the generation manually with `krea-ai` (CLI by default, MCP fallback) to see what the actual output looks like.
2. **Confirm** — show the user the result. Iterate on prompt, model, parameters until it's right.
3. **Productize** — once the output is approved, hardcode the URLs and parameters into the app.

If you skip step 1–2 and go straight to writing SvelteKit pages with placeholder prompts, the app will look broken when generation fails or returns unexpected results. Validating in chat takes seconds; debugging a broken app takes minutes.

See `references/integration-patterns.md` for the full workflow.

## Architecture recommendation: server-side only

The Krea API key must **never** be exposed to the browser. All Krea calls go through your server:

- **SvelteKit:** `+page.server.ts`, `+server.ts`, or `actions` in `+page.server.ts`
- **Next.js:** API routes (`app/api/*/route.ts`), server actions, or `getServerSideProps`
- **Express/Hono/Fastify:** standard server routes

The client triggers a generation by hitting your server, which hits Krea, polls until done, and streams the result back.

## Auth, polling, errors

All three live in `references/api-client.md` with reusable TypeScript and Python snippets. The key shapes:

- **Auth:** `Authorization: Key ${KREA_API_KEY}` header.
- **Submit:** `POST /generate/image/<provider>/<model>` with `{ prompt, ... }` → returns `{ job_id }`.
- **Poll:** `GET /jobs/<job_id>` every 3–10s until `status` is `completed` or `failed`.
- **Errors:** see `references/validation.md` for the full table.

## Frontend integration

See `references/frontend-snippets.md` for ready-to-paste TypeScript that handles common patterns:

- Generation form with progress UI
- Image preview with click-to-expand
- Multi-image gallery with state
- Video player with loading states
- Hardcoded asset arrays (the "productize" step)

## Validation discipline

User-provided prompts, image URLs, and parameter values must be validated server-side before forwarding to Krea. See `references/validation.md` for the validation checklist and content moderation handling.

## Reference docs

- `references/integration-patterns.md` — prototype→productize workflow, app structure, when to chat-first
- `references/api-client.md` — auth, polling, retries, error handling (TS + Python)
- `references/validation.md` — input checks, content moderation, common API errors
- `references/frontend-snippets.md` — ready-to-paste TS for SvelteKit/React/Vue

## Quick-start

If the user is starting a brand new app and asks "how do I integrate Krea":

1. Read `references/api-client.md` to understand the auth+poll shape.
2. Drop the TypeScript helper from `references/frontend-snippets.md` into `src/lib/krea/index.ts` (or wherever fits the project).
3. Build a server route that calls the helper.
4. Build a client component that hits the server route.
5. For each user-facing generation, **prototype the prompt in chat with `krea-ai` first**, then hardcode the approved version.
