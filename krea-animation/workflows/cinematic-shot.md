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
8 seconds, low-key void, four staged beats opening on macro detail and landing on
the whole subject, no on-screen text — and state what you assumed.

### 3. Resolve Seedance

Per `references/seedance-routing.md`:

1. Confirm Krea MCP availability.
2. List models; confirm the live Seedance variant IDs.
3. Get the schema for the variant you'll use.
4. Fetch the Krea prompting guide for the model.

### 4. Build the beats

Structure the piece before choosing any individual move. Four or five beats, macro
first, whole subject last — the standard build is in `references/cut-architecture.md`.

Then pick each beat's move from the recipe tables rather than inventing:

- reveals, shadow, focus, transitions → `references/reveal-recipes.md`
- levitation, orbit, explode, macro dive, render camera → `references/dimensional-motion.md`
- logos and wordmarks → `references/logo-and-mark-motion.md`
- environment, surface and palette for a desirable object → `references/luxury-showcase.md`
- taste, light, lens, materials, tempo → `references/cinematic-craft.md`

**One camera move per beat** — but four or five beats. Two moves inside one beat is
the mistake; one move across the whole clip is the bigger one.

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

Download and build a contact sheet. Sampled frames cannot see a clip that resolves
early and then replays — the first, middle and last frames of a looped piece all
look correct. The contact sheet shows the whole timeline at once:

```bash
ffmpeg -i shot-raw.mp4 -vf "fps=3,scale=300:-1,tile=6x4" -frames:v 1 contact.png
```

The tile is 24 cells and `-frames:v 1` writes only the first one, so the sheet covers
`24 ÷ fps` seconds. At `fps=3` that is 8s — the default deliverable. **Set `fps` to at
least `24 ÷ duration` or the sheet silently stops early and the landing, the beat
these checks are about, never appears on it.** A 6s sting wants `fps=4`.

Read it with vision and answer honestly:

- **Does the whole subject appear exactly once, on the last beat?** Seeing it in the
  opening cells, or twice, is a failed generation — the reveal was spent early and
  the remaining time was padded.
- **Does the timeline progress, or does it alternate?** A full → detail → full
  pattern is a loop, not a build.
- Is any beat a run of near-identical cells? That beat had no event in it.
- Does the camera move read as deliberate, or does it drift?
- Is the subject locked, or is it wobbling / rotating / breathing?
- Is the physics realtime, or did it come back speed-ramped?
- Did the light stay where you put it, or did flare and god rays arrive?
- Is the mark intact in the final cells? Drift is progressive.

Then prove the cuts landed, and count them against the beats you staged:

```bash
ffmpeg -i shot-raw.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```

Two cuts a frame apart is a glitch, not a beat. Fewer real cuts than staged beats
means the beats merged — restage, or cut a beat and shorten the clip to match.

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
| Duration | 8s; 6s for a logo sting; 4s floor |
| Structure | 4–5 staged beats, macro first, whole subject on the final beat |
| Beat length | 1–1.8s for detail beats, 2–2.5s for the landing |
| Resolution | 1080p |
| Environment | seamless charcoal-to-black void, no horizon, no set dressing |
| Light | one hard key per beat, direction changing on every cut, hard falloff to true black |
| Lens | 100mm macro for detail beats, 85mm for the landing, 24mm architectural |
| Camera | one quantified move per beat, or locked with the light carrying the beat |
| Transitions | hard cuts, named per beat; no dissolves unless the brief asks |
| Subject | locked — no rotation, drift, or scale change unless named |
| Physics | realtime; no speed ramping, no slow-motion |
| Grade | low-key neutral, one warm specular; no teal-orange |
| Text | none in-frame; type is composed in post |
| Audio | none, or room tone plus one precise hit per cut |

## Banned

- Do not answer "animate this" with one continuous move over the full duration. That
  is the timid-drift failure; build the beats.
- Do not open on the whole subject. The complete view is the last beat, not the first.
- Do not run two adjacent beats at the same shot size, camera height, or key direction.
- Do not submit a hero shot from a start image you haven't inspected with vision.
- Do not write two camera moves in one beat.
- Do not use `slow`, `gently`, `softly`, `dreamy` as the only pace instruction.
- Do not skip the constraints tail on any shot over 4 seconds.
- Do not deliver a logo shot without per-glyph QA on the last frame.
- Do not describe a scene that isn't in the source still.
- Do not fire several variants before inspecting the first result.
- Do not claim identity preservation through aggressive action.
- Do not name a brand as an imitation target. Describe the look in craft terms.
