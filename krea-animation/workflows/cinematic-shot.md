# Cinematic Shot

## Trigger

Use for **one superb Seedance shot**. This is the default entry point of this skill
and covers most requests that arrive:

- one still, keyframe, illustration, render, product photo, logo or plate to animate
- "make this look cinematic / premium / dramatic"
- a reveal, a camera move, a levitation, a rotation, a detail zoom
- a logo or brand mark sting
- a 2D or anime frame to put in motion
- prompt-only motion with no source image

For a multi-beat reveal film assembled from several shots, use `workflows/reveal-sequence.md`.
For narrative animation with characters, story and continuity across scenes, use
`workflows/series-from-scratch.md` or `workflows/shotlist-to-sequence.md`.

## Recipe

### 1. Read the source

If the user supplied an image, read it with vision before anything else. Write down:

- what must stay stable (identity, composition, palette, mark, geometry)
- what the light is doing and where the source is
- what material behaviour is visible
- **whether this still can carry a shot at all**

The start image is the quality ceiling. A soft mark, a wrong crop, a compressed
video frame, or mush on a key edge will appear in every generation regardless of
prompt quality. If the still is not good enough, say so and fix it first — generate
a clean hero still or ask for a better source. Do not proceed and hope.

### 2. Ask only what changes the shot

At most three questions, and only for things you cannot infer:

- register: elegant and restrained, or energetic?
- deliverable aspect and duration
- does it need audio, and is text going in later?

Do not interrogate. Infer defaults from `references/cinematic-craft.md` — 21:9,
8 seconds, low-key void, one glacial move, no on-screen text — and state what you
assumed.

### 3. Resolve Seedance

Per `references/seedance-routing.md`:

1. Confirm Krea MCP availability.
2. List models; confirm the live Seedance variant IDs.
3. Get the schema for the variant you'll use.
4. Fetch the Krea prompting guide for the model.

### 4. Choose the move

Pick from the recipe tables rather than inventing:

- reveals, shadow, focus, transitions → `references/reveal-recipes.md`
- levitation, orbit, explode, macro dive, render camera → `references/dimensional-motion.md`
- logos and wordmarks → `references/logo-and-mark-motion.md`
- taste, light, lens, materials, tempo → `references/cinematic-craft.md`

**One camera move.** If two moves are tempting, that is two beats.

### 5. Cost preflight

Price the run before submitting. Show variant, duration, seed count, and the retry
budget. Get the go-ahead before spending.

### 6. Write the prompt

Build all nine blocks from `references/seedance-prompt-architecture.md`. Or start
from a slot in `references/proven-prompts.md` and substitute.

Non-negotiable before submitting:

- motion split present, with the subject explicitly locked or its motion quantified
- one world, one light source, both declared
- realtime physics stated alongside any slow camera move
- text lock present if any mark or label is in frame
- light negatives present
- constraints tail restating every lock

### 7. Upload, then submit

Upload local assets and pass the returned Krea URLs through the live schema fields.
Prompt-side `@Image1` naming alone attaches nothing.

Respect the mutually exclusive paths: `end_image` **or** `reference_images`, never
both.

Block on `seedance-2-fast` first. One take, then judge.

### 8. Judge the block

Download and inspect. Extract first, middle and last frames:

```bash
ffmpeg -i shot-raw.mp4 -vf "select='eq(n\,0)'" -vsync 0 -q:v 2 frame-first.png
ffmpeg -sseof -0.1 -i shot-raw.mp4 -update 1 -frames:v 1 -q:v 2 frame-last.png
```

Read them with vision and answer honestly:

- Does the camera move read as deliberate, or does it drift?
- Is the subject locked, or is it wobbling / rotating / breathing?
- Is the physics realtime, or did it come back speed-ramped?
- Did the light stay where you put it, or did flare and god rays arrive?
- Is the mark intact in the **last** frame? Drift is progressive.
- Did the cuts cut? For multi-beat prompts, prove it:

```bash
ffmpeg -i shot-raw.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```

### 9. Retake one thing

One change per retake, seed pinned. See the retake pattern in
`references/seedance-prompt-architecture.md`. Diagnose from the failure table there
rather than rewriting the prompt wholesale.

### 10. Deliver on the quality variant

Re-run the approved prompt on `bytedance/seedance-2`. Best-of-2 seeds for hero
deliverables. Upscale if the live schema exposes it and the delivery needs it.

Deliver the clip path plus one honest line on what the shot does and anything it
still doesn't. If a compromise was made — the mark needed compositing, the levitation
needed a shorter rise — say so.

## Defaults For Elegant Work

Apply unless the brief says otherwise, and state that you did:

| Setting | Default |
|---|---|
| Aspect | 21:9 for cinematic, 16:9 for standard delivery, 9:16 for vertical |
| Duration | 8s single hero shot; 5s for a logo sting; 4s floor |
| Resolution | 1080p |
| Environment | seamless charcoal-to-black void, no horizon, no set dressing |
| Light | one large soft source high camera-left, hard falloff to true black |
| Lens | 85mm hero, 100mm macro detail, 24mm architectural |
| Camera | one continuous move, ~15–20cm across the full duration, constant rate |
| Subject | locked — no rotation, drift, or scale change unless named |
| Physics | realtime; no speed ramping, no slow-motion |
| Grade | low-key neutral, one warm specular; no teal-orange |
| Text | none in-frame; type is composed in post |
| Audio | none, or room tone plus one precise diegetic sound |

## Banned

- Do not submit a hero shot from a start image you haven't inspected with vision.
- Do not write two camera moves in one beat.
- Do not use `slow`, `gently`, `softly`, `dreamy` as the only pace instruction.
- Do not skip the constraints tail on any shot over 4 seconds.
- Do not deliver a logo shot without per-glyph QA on the last frame.
- Do not describe a scene that isn't in the source still.
- Do not fire several variants before inspecting the first result.
- Do not claim identity preservation through aggressive action.
- Do not name a brand as an imitation target. Describe the look in craft terms.
