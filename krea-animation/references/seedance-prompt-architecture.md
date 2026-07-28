# Seedance Prompt Architecture

A Seedance prompt is not a description of a video. It is a **shot order**: a
structured document that tells a camera operator, a gaffer, a physics engine and
an editor what to do, in that order, with no room to improvise.

The difference between a mediocre Seedance clip and a shot that looks like it cost
money is almost never the idea. It is whether the prompt is *architected* or
*narrated*. Narrated prompts drift. Architected prompts hold.

## The Nine Blocks

Write these in order. Every block is load-bearing. Omit a block and Seedance fills
the gap with its defaults — and its defaults are glossy, centered, blue-graded,
lens-flared, and slightly floaty.

```
1. FORMAT      — what kind of film this is, duration, aspect, look
2. REFERENCES  — every attached asset and its exact job, inline
3. WORLD       — one environment, one light source, one palette, held throughout
4. MOTION SPLIT— what moves, how fast, and what is nailed down
5. SHOTS       — per-beat staging: time range, size, lens, one move, one event
6. LIGHT       — the source, its behaviour, and its hard negatives
7. TRANSITIONS — how each beat becomes the next, named
8. AUDIO       — diegetic list or explicit silence
9. CONSTRAINTS — every lock restated at the tail
```

### 1. FORMAT

One line that frames the entire generation. Genre first — it sets the model's
whole prior.

```
Format: Single-shot cinematic product reveal, 8 seconds, 21:9, anamorphic
cinema look, deep-shadow low-key grade, no on-screen text.
```

Name the genre honestly: *cinematic product reveal*, *architectural flythrough*,
*brand mark sting*, *macro material study*, *2D illustrated character beat*.
"A cool video of a watch" is not a format.

### 2. REFERENCES

Attach the assets through the schema fields, then restate each asset's job
**inline in the prompt**. The prompt-side `@Image1` naming and the schema field
are two halves of one instruction — neither works alone.

```
References: @Image1 as the first frame and the hero object — the brushed titanium
case; keep the engraved wordmark and every printed line exactly as shown, do not
warp, re-letter, or re-light the mark. @Image2 for the environment: seamless
charcoal void. @Video1 for camera behaviour only — match its move speed and
easing, not its subject, not its grade.
```

Rules that matter:

- **Name the job, never just the asset.** `reference @Video1` is noise. `reference
  @Video1's camera move speed and easing` is an instruction.
- **Say what NOT to take** from a reference. Reference videos leak grade and
  subject unless you fence them off.
- **Lock text explicitly** whenever a mark or label is in frame. One clause, every
  time: *keep every printed line exactly as shown, do not re-letter*.

### 3. WORLD

One environment. One dominant light. One palette. Held across every beat.

The most common reason a multi-beat clip looks cheap is that beat 3 is in a
different room than beat 1. Seedance will happily relocate between cuts unless
the world is declared as a constant.

```
Consistent world across all beats: seamless charcoal-to-black gradient void, no
horizon line, no visible floor seam; single large soft source from high camera-left;
palette is graphite, cold steel, one warm amber specular; shallow macro focus
throughout.
```

### 4. MOTION SPLIT

The single highest-leverage block in cinematic Seedance work, and the one almost
everyone skips.

State, separately, what moves smoothly, what moves at realtime physical speed, and
what is **nailed down**. Without this, everything drifts a little, which reads as
underwater.

```
Motion split: the object is locked — it does not rotate, wobble, drift, or change
scale unless a beat says so. Camera moves are continuous and mechanically smooth,
as if on a motion-control rig, quantified per beat (distance + duration + constant
rate) rather than described as slow. Atmospherics — dust motes, faint haze,
the travel of the specular highlight — move at natural realtime speed. Nothing is
speed-ramped. No slow-motion.
```

### 5. SHOTS

One block per beat. Every beat carries **five** things:

| Element | Why |
|---|---|
| Time range | `(0–3s)`. Unstaged beats morph into each other instead of cutting. |
| Shot size | ECU / CU / MS / WS / EWS. Forces a real framing decision. |
| Lens | 24 / 35 / 50 / 85 / 100mm macro. Changes compression, and Seedance respects it. |
| Exactly one camera move | Push, orbit, tilt, rack, crane, or locked. Two moves in one beat fight and produce mush. |
| Exactly one physical event | One thing happens, with a consequence. |

```
SHOT 1 — VOID HOLD (0–2.5s), extreme wide, 35mm. The object sits dead center in
near-total darkness, only its top edge catching a thin rim of light. Camera locked
absolutely still. Nothing moves but a single dust mote crossing the rim light.
```

**Never write two camera moves in one beat.** "Slowly orbit while pushing in and
tilting up" is three instructions; you will get a lurch.

### 6. LIGHT

Seedance's untamed default is god rays, lens flare, a blue push, and crushed faces.
Name the source, the behaviour, and the negatives.

```
Light: one large soft source high camera-left, falling off to true black on the
right two-thirds of frame; a single hard amber specular travels along the top edge
as the camera moves. NO god rays, NO light beams, NO lens flare, NO bloom, NO
blue filter; neutral white balance; blacks are deep but never crushed to noise.
```

### 7. TRANSITIONS

Name the transition at the end of every beat except the last. Unnamed boundaries
become dissolves.

Cut vocabulary that lands: `hard cut`, `whip-pan cut`, `snap cut`, `punch-in cut`,
`match cut on the same curve`, `shadow wipe`, `speed-blur cut`, `light-flash cut`.

For elegant work, prefer the quiet ones: `match cut on the same curve`,
`shadow wipe`, `rack-focus transition`, `cut on the highlight`.

### 8. AUDIO

Either name the diegetic sound list or ban sound outright. Silence is a choice —
say it, or you get stock trailer scoring.

```
Audio: no music. Only room tone, one soft mechanical click as the case settles,
and the faint air movement of the camera travel.
```

### 9. CONSTRAINTS

Long prompts decay. The last 20% of the generation drifts back toward defaults
unless every lock is restated at the tail. This block is not redundant — it is
the anti-drift mechanism.

```
Constraints (reassert): one continuous world, charcoal void, single soft
top-left source; the object is locked and never rotates or drifts; camera moves
slow, continuous, motion-control smooth, realtime physics, no speed ramping, no
slow-motion; engraved wordmark and printed lines exactly as @Image1, never
re-lettered or warped; NO god rays, NO lens flare, NO bloom, NO blue grade; no
on-screen text, no captions, no added graphics, no extra objects entering frame;
no morphing, no melting, no scale changes.
```

## The Skeleton

```
Format: <genre>, <duration>, <aspect>, <look>, <text policy>.
References: @Image1 as <role> — <lock clauses>. @Image2 for <role>. @Video1 for
  <specific attribute only> — not its <attributes to exclude>.
Consistent world across all beats: <environment>, <light>, <palette>, <focus>.
Motion split: <what is locked>; <camera behaviour and speed>; <atmospherics at
  realtime>; no speed ramping.
SHOT 1 — <NAME> (0–Xs), <size>, <lens>. <one camera move>. <one physical event>.
  <named transition>.
SHOT 2 — <NAME> (X–Ys), <size>, <lens>. <one camera move>. <one physical event>.
  <named transition>.
SHOT 3 — <NAME> (Y–Zs), <size>, <lens>. <one camera move>. <one physical event>.
Light: <source and behaviour>. <hard negatives>.
Audio: <diegetic list> OR no music, <room tone only>.
Constraints (reassert): <world> <locks> <camera> <pace> <text> <light negatives>
  <content negatives>.
```

## Pace: Commanded Stillness vs Accidental Slow-Motion

Elegant, dramatic, slow-feeling work is the whole point of this skill — and it is
also where the most expensive mistake lives.

**The trap.** Words like `slow`, `slowly`, `gently`, `softly`, `dreamy float`,
`drifting` read to Seedance as *slow down the footage*. You get a speed ramp:
fabric at 0.3×, particles hanging in air like syrup, everything faintly rubbery.
That is not elegance, it is a stretched clip.

**The fix.** Slowness belongs to the **camera**, not the **physics**. Say both
halves explicitly:

```
Camera: one continuous push-in traveling roughly 20 centimeters across the full
6 seconds, mechanically smooth, motion-control steady, never accelerating.
Everything in frame moves at natural realtime speed — no speed ramping, no
slow-motion, no floating.
```

That combination — glacial camera, realtime physics, a nearly static subject — is
the entire grammar of the premium reveal. Read it as a rule:

| Want | Write | Never write |
|---|---|---|
| Elegant slowness | "one continuous push-in traveling 20cm across 6 seconds, motion-control smooth" | "slow dreamy push in" |
| Weightless hang | "the object holds still in mid-air, absolutely level, no bobbing; realtime physics" | "floating gently, softly drifting" |
| Restrained reveal | "the shadow retreats across the surface over 3 seconds at a constant rate" | "shadows slowly and softly reveal" |
| Deliberate settle | "the lid settles in one motion and stops dead" | "gently comes to rest" |

If the user genuinely wants slow-motion as a style — a splash at 120fps, fabric
unfurling — ask for it explicitly and budget the shot around it. Then it is a
decision, not an accident.

## Length Comes From Beats, Never Adjectives

To make a clip richer, **add a staged shot**. Do not add adjectives.

Adjective inflation is the classic image-model instinct and it actively degrades
video: `stunning, beautiful, hyper-detailed, masterpiece, 8k, award-winning`
contributes nothing to motion and dilutes the instructions that do. Every added
word competes for attention with the camera move that actually matters.

The upgrade path for a shot that feels thin:

1. Add a beat with its own time range, size, lens, move and event.
2. Give an existing beat a physical *consequence* — the highlight crosses the
   engraving, the dust disturbs, the reflection sweeps.
3. Tighten the negatives so the model stops spending frames on defaults.

## Beat Budget

Live-verified behaviour: Seedance commits to roughly **three to four strongly
distinct beats per generation**. Beyond that, the extra beats merge into their
neighbours. Plan to that ceiling rather than discovering it.

- **Four fully staged beats in one 8s generation is the working maximum.** Every
  beat needs its own time range, size, lens, move, event and named transition.
- **Buy only the seconds you have staged.** Duration is not free headroom — the
  model fills unstaged time by replaying an earlier beat, usually degraded. Three
  staged beats is a 4–5s clip, not a 6s one. If the piece resolves at 3s, the
  request should have been 3s worth of duration, rounded up to the 4s floor.
- **The payoff appears once.** Reveal the whole subject on the final beat and stop.
  Cutting back to a detail *after* the reveal and then showing the whole thing again
  reads as a loop, and it invites the model to actually loop.
- Keep detail beats at 1–1.8s and the landing at 2–2.5s.
- Put `no long static holds, keep cutting` in the constraints tail on every
  multi-beat prompt.
- Never end on a long hold *before* the landing — the model front-loads its good
  beats and coasts the back half on one lazy rotation if you let it.
- **For five or more beats, or true ~1s staccato, stop fighting one generation.**
  The duration floor is 4s, so a 1-second beat cannot be generated directly.
  Generate each angle as its own 4s clip, trim it to its usable core, and
  assemble — see `references/cut-architecture.md`. Trimming is exact and free.
- **The single-move exception.** One continuous 6–8s move is legitimate for an
  architectural interior, a landscape, or a brand that has explicitly asked for
  restraint. It is a deliberate choice you name out loud, not the default. For
  objects, products and marks, the default is the cut sequence.

## Verify That Cuts Actually Cut

"HARD CUT" between under-staged beats renders as a soft morph. Prove the cuts
landed on the output, don't eyeball it:

```bash
ffmpeg -i shot-raw.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```

An empty result on a multi-beat prompt means the cuts morphed. Fix by fully
staging each beat (time range + size + lens + one move + one event + named
transition), not by shouting HARD CUT louder.

## The Start Image Is The Ceiling

Nothing in the prompt can rescue a bad first frame. Verified repeatedly: a
cropped or garbled product reference garbles the label in *every* generation
regardless of prompt quality, while a clean, sharp, correctly-lit still holds
dense printed text through an entire multi-beat timeline including the final frame.

Before submitting: read the start image with vision. If the mark is soft, the
crop is wrong, the lighting fights the intended look, or there is compression
mush on an edge — fix the still first. Generate a clean hero still, or ask the
user for a better source. Do not proceed and hope.

## Failure Modes And Their Prompt Fixes

| Symptom | Cause | Fix in the prompt |
|---|---|---|
| Everything looks underwater | No motion split; mushy pace adverbs | Add the motion split block; lock the subject; "realtime physics, no speed ramping" |
| Beat 3 is in a different room | No world block | Declare one world; restate it in constraints |
| Cuts became dissolves | Under-staged beats | Full staging per beat + named transition |
| Logo re-lettered or warped | No text lock | "keep every printed line exactly as shown, do not re-letter or warp" in references AND constraints |
| Random god rays and flare | Unnamed light | Light block with explicit negatives |
| Camera lurches | Two moves in one beat | One move per beat |
| Object slowly rotates for no reason | Subject not locked | "the object is locked — no rotation, no drift, no scale change" |
| Back half goes lazy | Long final hold | Cap beats at ~2.5s; "no long static holds, keep cutting" |
| Great first 2s, drifts after | No constraints tail | Restate every lock at the tail |
| Stock trailer music appears | No audio direction | Name diegetic sound or ban music explicitly |

## Content-Filter Shadow-Fail

Seedance can return `status: "completed"` with an empty `result` payload. That is
a refusal, not a success. Treat a completed job with no result URL as failed and
retry once with a sanitized prompt: drop proper nouns and IP-like phrases, drop
specific signage text that isn't essential, keep the `start_image` if it carries
identity. If it still fails, drop `end_image` and retry start-image-only.

## Retake Prompting

A retake fixes **one** thing. Changing three blocks at once means you learn
nothing about which one mattered.

```
Retake SC001_SH020. Keep the approved start image, the world, the light and the
grade exactly as before. One change: the camera move becomes a single continuous
push-in traveling 20cm across the full 6 seconds instead of an orbit. The object
stays locked — no rotation. Reassert: realtime physics, no speed ramping, no
slow-motion, wordmark exactly as @Image1.
```

Pin the seed once a take is close, then change one block per run.
