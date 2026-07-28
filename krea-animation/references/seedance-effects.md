# Seedance Effects Library

Krea maintains a curated library of **Seedance effects** — pre-built looks that
reproduce a specific motion, transition, or visual treatment. Each effect is a
reference asset plus a tuned prompt template, packaged so that applying it is one
step instead of an hour of prompt archaeology.

**Check the library before hand-writing a look.** This is a hard rule of this skill,
not a suggestion. A curated effect encodes phrasing that has already been verified
to land; a hand-written approximation of the same look starts from zero. The only
way to know whether one covers the brief is to list them.

## What An Effect Is

An effect entry carries:

| Part | What it does |
|---|---|
| Name | Human label for the look — how the user will refer to it |
| Reference asset | A short video (or image) that demonstrates the effect. This is what the model actually references. |
| Asset type | Whether that asset attaches as a reference **video** or reference **image** |
| Prompt template | The prompt scaffold for the effect, with slots for the user's own assets |
| Preview | Thumbnail for showing the user what they're choosing |

The prompt template is the valuable half. It contains reference slots (`@`-mentions
or an inputs placeholder) that you fill with the user's uploaded assets, keeping the
effect's own phrasing intact.

## Listing Effects — Do This Every Session

List the available Seedance effects through the connected **Krea MCP** before
proposing a look for any Seedance shot.

Discover the capability live, the same way as everything else in this skill:

1. Inspect the connected Krea MCP tool list for an effects-listing capability.
2. Call it and read back the available effect names.
3. Match them against the user's brief.

Do not hardcode a tool name from memory or from this document. A dedicated
effects-listing endpoint is being added to the Krea MCP surface, so the exact tool
name may change or may not be exposed in the user's session yet. Discover it, don't
assume it.

**If no effects-listing capability is exposed in the session:** say so in one line,
then proceed with hand-written prompts from `reveal-recipes.md` and
`dimensional-motion.md`. Never stall the job over it, and never invent effect names
to fill the gap — a fabricated effect name is worse than no effect at all.

## Applying An Effect

Listing gives you a name; applying takes three steps.

1. **Attach the effect's reference asset** through the matching live schema field —
   `reference_videos` for a video effect, `reference_images` for an image effect.
2. **Build the prompt from the effect's template**, substituting the user's assets
   into its reference slots. Keep the template's own language; it is tuned.
3. **Pass the effect attribution** if the live schema exposes an effects field, so
   the generation is correctly attributed to the library effect. Attribution does
   not *apply* the effect — steps 1 and 2 do the work. Never skip 1 and 2 and expect
   the attribution field alone to produce the look.

Then layer this skill's craft on top: the effect governs the *look*, while the
world, light and constraints blocks from `seedance-prompt-architecture.md` keep it
from drifting.

## Budget The Reference Slots

Effect assets consume the same reference budget as your own references. Expect
roughly: up to 9 reference images, up to 3 reference videos, up to 3 reference
audios, with a combined cap across all attached references.

Plan the allocation before uploading. A typical elegant product reveal using one
video effect:

- 1 reference video → the effect asset
- 1 `start_image` → the hero product still
- 1–2 reference images → product detail and environment

That leaves headroom. If you find yourself needing more than one effect asset plus
three of your own references, the shot is trying to be two shots.

## Mutual Exclusivity Still Applies

An effect attached as a reference puts the shot on the **reference path**. That
means no `end_image` in the same call. If the brief needs both a library effect and
a guaranteed final frame, pick one:

- Effect matters more → reference path, describe the landing frame in prose.
- Exact landing frame matters more → `start_image` + `end_image`, and reproduce the
  effect by hand from `reveal-recipes.md`.

Do not attempt both in one call. Full rules in
`../../krea-generate/references/models/seedance-2.md`.

## Presenting Effects To The User

When the library carries something relevant, show it as a choice rather than
silently applying it:

> Three library effects fit this reveal — `<name A>`, `<name B>`, `<name C>`.
> `<name A>` is the closest to what you described. Want that one, or should I write
> the shot by hand for more control over the light?

Two reasons to offer the choice: the user may recognize an effect they've seen
work, and a hand-written shot gives finer control over world and light. Neither is
strictly better.

## When To Skip The Library

- The user supplied their own reference video of the look they want. Their reference
  wins — attach it and fence it off (`reference @Video1's camera behaviour and
  transition timing only, not its subject and not its grade`).
- The brief needs precise multi-beat staging with named cuts. Hand-write it; effects
  are strongest on single-look shots.
- No effect is close. A distant effect drags the shot toward its own look and fights
  your prompt. Half-matching is worse than not using one.

## Effects Do Not Excuse Craft

An effect applied without a world block, a motion split, a light block and a
constraints tail drifts exactly as fast as anything else — often faster, because the
reference asset is also pulling on the grade. Effect first, then the full
architecture around it.
