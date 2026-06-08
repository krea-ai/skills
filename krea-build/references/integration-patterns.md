# Integration Patterns

The core principle for building Krea-powered apps: **prototype in chat, productize in the app.** This file explains why and how.

## The trap

When a user says "build me a moodboard app with sci-fi cityscapes", the wrong move is:

```ts
// WRONG — placeholder prompts, no validation
const moodImages = [
  await generateImage("a sci-fi city, neon", { ... }),
  await generateImage("a sci-fi city, rainy", { ... }),
  await generateImage("a sci-fi city, dawn", { ... }),
]
```

You haven't seen what these prompts produce. Three things can go wrong:

1. The prompts produce generic output that doesn't match the user's vision.
2. The model you guessed at handles the genre badly.
3. The aspect ratio you chose looks terrible for moodboards.

By the time the user sees the live preview, you've spent ~3 minutes of compute on stuff they'll reject.

## The pattern: explore → confirm → build

### 1. Explore (use the `krea-generate` MCP skill)

Generate 2–3 sample images interactively. Show them in chat. Iterate on prompts, models, and aspect ratios until the user nods.

```
User: "build me a moodboard of sci-fi cityscapes"
Agent: "Let me generate 3 sample frames first so we can pick a direction."
       → calls mcp__krea-public-api__generate_image 3 times with varied prompts
       → shows results to user
User: "love the second one — go heavier on rain and night"
Agent: → regenerates with refined prompts
User: "perfect, use this style"
```

Now the prompts, model, and parameters are **proven**.

### 2. Confirm

Get explicit user approval. "Want me to build the moodboard with these?" — pause until they say yes.

### 3. Build

Hardcode the approved asset URLs (or approved prompt + model + parameters) into the app:

```ts
// RIGHT — proven outputs hardcoded
export const moodImages = [
  { url: "https://krea.../approved-1.png", title: "Rainy neon" },
  { url: "https://krea.../approved-2.png", title: "Night towers" },
  { url: "https://krea.../approved-3.png", title: "Wet streets" },
];
```

The app loads instantly, no API calls at runtime, no failure modes.

## When the app *does* need runtime Krea calls

Some products are genuinely dynamic — a generator the end user controls, a creative tool, an interactive prompt explorer. Those need server-side API calls.

Structure:

```
User → client app → your server route → Krea API → poll → response → client
```

Critical rules for runtime calls:

1. **API key stays server-side only.** Never in client code, never in `NEXT_PUBLIC_*` envs, never in bundled JS.
2. **Stream progress to the client.** Don't make them stare at a blank screen for 30s.
3. **Treat every call as fallible.** Content moderation, rate limits, network blips — handle all of them.
4. **Cache aggressively.** Same prompt + same params = same result. Cache by hash to avoid re-running identical jobs.

See `api-client.md` for the auth+poll shape, `frontend-snippets.md` for the client/server split.

## App structure (SvelteKit example)

```
src/
  lib/
    krea/
      index.ts          # API client (auth, submit, poll, errors)
      types.ts          # Result types
  routes/
    +page.svelte                       # static moodboard with hardcoded URLs
    api/
      generate/+server.ts              # POST → submits Krea job, returns job_id
      jobs/[id]/+server.ts             # GET → polls and returns status
    generator/
      +page.svelte                     # interactive generator
      +page.server.ts                  # SSR data loading
```

The static `+page.svelte` is your default; reach for `/generator/` style routes only when the user explicitly needs interactive generation.

## App structure (Next.js example)

```
app/
  page.tsx                             # static moodboard with hardcoded URLs
  api/
    generate/route.ts                  # POST → submits Krea job
    jobs/[id]/route.ts                 # GET → polls and returns status
  generator/
    page.tsx                           # interactive generator (client component)
  lib/
    krea/
      index.ts                         # API client
```

## Dev server discipline

Don't start the dev server before you have real content. An empty skeleton or broken placeholder is worse than no preview at all — it makes the user think something is wrong.

Correct sequence:

1. Generate assets, write the page code, prepare data — everything needed for the page to render with real content.
2. Then start the dev server.
3. The user sees a finished page on first paint.

This applies whether you're prototyping new pages or iterating on an existing one. If a major change is mid-flight, the dev server can still be running — but show the user finished work, not partial work.

## Hardcoding vs. dynamic data

The default for app pages is **hardcode generated asset URLs.** This gives:

- Instant page loads
- Zero API cost at runtime
- Reproducible behavior
- No moving parts

Use dynamic data only when:

- The user explicitly asks for a tool the end user can drive (generator, explorer, mixer)
- The content needs to change per request (user-specific output, time-of-day, A/B test)
- The dataset is too large to hardcode (a content calendar with 100s of items)

When iterating, regenerate with `krea-generate` and update the hardcoded data. Don't rebuild the runtime path just because the asset changed.

## User uploads

When users attach images:

- Save uploads to a known directory (`static/uploads/` in SvelteKit, `public/uploads/` in Next.js, etc.).
- To use as a Krea reference: pass the **absolute local path** to your server, which uploads it to Krea (via `/assets` or via `upload_asset` MCP) and uses the returned URL.
- To display in your app: serve from the public uploads directory (`/uploads/filename.png`).

## Anti-patterns (don't do these)

- **Generate-then-build without showing the user.** You're guessing what they want. Show first.
- **Hardcode model names you've never tested.** Models retire, rename, and change behavior. Always validate live first.
- **Live API calls in `+page.svelte` / client components.** API key exposure, terrible UX (waiting on render), no caching.
- **Polling from the browser.** Even with auth on the server, polling from the browser hits Krea's rate limits per user and burns concurrent slots. Poll server-side.
- **Returning the Krea response object directly to the client.** Shape it. Strip internal fields. Return only the URL(s) and metadata you control.

## When the user asks "why isn't it working"

Common debugging order:

1. **Did you generate in chat first?** If they say "I just wrote the app code", that's the bug. Validate the prompt with `krea-generate` and update the hardcoded data.
2. **Is the API key set server-side?** Check the env. Confirm it's not leaked to client.
3. **Are you polling?** Krea returns `job_id` synchronously; the result comes from a separate poll.
4. **Are you handling job failures?** A failed job returns `status: "failed"` — surface this, don't pretend success.
5. **Is the model still active?** Krea retires models; check the OpenAPI spec or the MCP `list_models` for current IDs.
