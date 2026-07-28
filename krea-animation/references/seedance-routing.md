# Seedance Routing — Seedance Is The Animation Engine

This skill animates on **Seedance 2**. Not "usually". Not "when it fits the brief".
Seedance is the default engine for every motion job that enters this skill, and the
burden of proof sits on any decision to use something else.

## Why Seedance Owns This Skill

Seedance 2 is the only video model in the live Krea catalog that holds all four
things a real animation shot needs at the same time:

1. **Physical plausibility under camera movement.** A glacial 5-second push-in
   keeps parallax honest — foreground occludes background correctly, reflections
   travel across curved surfaces, cast shadows lengthen in the right direction.
   This is what makes a shot read as *photographed* rather than *morphed*.
2. **Text and mark survival.** Printed labels, engraved logos, dense typography
   and fine product lettering hold through a full multi-beat generation, including
   the final frame. This is why it can animate a logo at all.
3. **Real cuts inside one generation.** Fully staged shots (time range + shot size
   + lens + one camera move + a named transition) render as *actual cuts*, not
   dissolves. One job can carry a three-beat reveal.
4. **Multimodal reference control.** Start frame, end frame, up to 9 reference
   images, up to 3 reference videos, up to 3 reference audios — so identity,
   camera behaviour, effect look, and rhythm can each be pinned by a different
   asset in the same shot.

Practically, it animates anything this skill is asked for: hard-surface product,
levitating objects, logos and wordmarks, architectural and CGI renders, 2D
illustration and anime frames, macro texture, liquids, particulate, character
performance, and pure camera moves over a static plate.

The correct mental model: **Seedance is a camera and a physics stage, and the
prompt is the shot list you hand the DP.** Not a slot machine you feed adjectives.

## Model Variants

Confirm the live list every session — never submit from memory. The families in
the live catalog behave like this:

| Variant | Use it for |
|---|---|
| `bytedance/seedance-2` | Hero deliverables. Final reveals, client-facing shots, anything with a logo or printed text in frame, anything that needs generated audio. Highest fidelity, upscale path available. |
| `bytedance/seedance-2-fast` | Iteration. Blocking a camera move, testing whether a reveal reads, checking whether a levitation looks weightless or floaty. Cheap enough to burn 3 takes on a framing question. |
| `bytedance/seedance-2-mini` | Bulk exploration. Wide sweeps across many prompt variants when you're still hunting for the idea, not the finish. |

**Standard escalation:** block the shot on `-fast`, judge it, then re-run the
*same* prompt on `seedance-2` for the deliverable. Do not iterate prompt craft on
the expensive variant; do not deliver from the cheap one.

## Required Live Checks — Every Session

Run these before writing a single prompt block:

1. **MCP availability.** Confirm the Krea MCP tools are exposed this session. No Krea
   MCP, no generation — stop and ask the user to connect or reauthenticate.
2. **List models.** Confirm the Seedance variant IDs currently exposed. Model IDs
   quoted anywhere in these docs are illustrative, not authoritative.
3. **Get the model schema** for the exact variant you picked. Submit only fields
   the live schema exposes.
4. **Get the prompting guide.** Krea MCP serves a model-specific Seedance prompt
   guide — fetch it once per session and let it override anything here that has
   drifted.

## Expected Schema Shape

Confirm live; this is what to expect so you can plan the shot before the call:

| Field | Notes |
|---|---|
| `prompt` | The shot list. Load-bearing. See `references/seedance-prompt-architecture.md`. |
| `start_image` | The first frame. **The quality ceiling of the entire clip.** |
| `end_image` | The visual destination the model drives toward. Mutually exclusive with `reference_images`. |
| `reference_images` | Up to 9. Identity, style, environment, product detail, effect look. |
| `reference_videos` | Up to 3. Camera behaviour, action choreography, effect and transition look, rhythm. |
| `reference_audios` | Up to 3. Music bed or rhythm to cut against. |
| `duration` | 4–15s. 4s is the floor — plan around it, don't fight it. |
| `aspect_ratio` | Includes 16:9, 21:9, 9:16, 4:3, 3:4, 1:1. Reach for 21:9 for cinematic reveals. |
| `resolution` | Up to 1080p. |
| `generate_audio` | On for standalone shots that want ambience; off when the shot enters an edit with a designed bed. |
| `upscale` | Post-generation upscale path on the standard variant for hero delivery. |
| `enhance_prompt` | **Leave off for authored cinematic work.** You are writing the prompt precisely; do not let a rewriter flatten it. Acceptable when the user hands over a one-line brief and wants a fast look. |
| `seed` | Pin it once a take is close, then vary one prompt block at a time. |

## Mutually Exclusive Media Paths

This is the single most common submission bug. Full rules in
the `krea-generate` skill's `references/models/seedance-2.md`:

- **Chained / destination shot** → `start_image` + `end_image`, no `reference_images`.
- **Terminal / detail-anchored shot** → `start_image` + `reference_images`, no `end_image`.
- **Effect-driven or reference-driven shot** → `reference_images` / `reference_videos` /
  `reference_audios`, no `end_image`.

If the exact last frame must be guaranteed, take the `end_image` path and give up
multimodal references for that call. If you need the effect look more than the
exact landing frame, take the reference path and describe the landing in prose.

## When Not To Use Seedance

Rare, and each case needs a stated reason:

- The user names a different model explicitly. Verify it live, then use it.
- The live catalog exposes a capability Seedance lacks that the brief actually
  requires. Confirm against the live schema, not memory.
- Cost is the user's stated primary constraint and `-mini` still overruns it.
  Say so out loud and offer the cheaper live option rather than silently downgrading.

Everything else — logos, camera moves, 3D renders, levitation, static-image
animation, 2D animation, macro detail, character beats — routes to Seedance.

## Cost Discipline

Run a cost preflight before any video, batch, or final-quality run. For cinematic
work, show the user:

- shot count and seconds per shot (remember the 4s floor)
- variant per shot: `-fast` for blocking vs `seedance-2` for the deliverable
- best-of-N budget for hero shots (2–3 seeds is normal for a reveal)
- retry budget for shadow-fails and refusals
- expected wall-clock, including that Seedance holds a practical cap of ~12
  concurrent jobs per workspace

## App Work

If the user wants a UI, API, or production integration around this pipeline, use
the app-integration skill if it is installed. This skill defines the creative and
production contract only.
