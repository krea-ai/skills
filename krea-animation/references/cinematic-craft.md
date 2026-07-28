# Cinematic Craft — The Language Of Chic, Elegant, Dramatic Motion

This is the taste reference. `references/seedance-prompt-architecture.md` tells you the shape
of a prompt; this file tells you what to put in it so the result looks expensive
instead of merely generated.

The target register: **restrained, deliberate, dark, precise.** The kind of shot
where almost nothing happens and it still holds the eye for eight seconds. Flagship
hardware launch films, luxury watch and fragrance campaigns, high-end architectural
films, gallery-grade CGI. One object, one light, one move, one idea.

The opposite register — which you must actively suppress, because it is Seedance's
default — is music-video maximalism: three lights, four moves, drifting camera,
lens flare, blue grade, glossy everything, and nothing in particular happening.

## The Six Laws Of Elegance

Internalize these. Every recipe in `references/reveal-recipes.md` is an application of them.

### 1. Subtraction, not addition

Elegance is what's left after you remove everything that isn't load-bearing. One
light source, not three. One camera move, not a combination. One event per beat.
An empty frame with a single lit edge is more expensive-looking than a full frame
of detail.

Write the frame as **95% darkness and 5% information**. Then defend that ratio in
the constraints tail: `no additional objects, no props entering frame, no
background detail, no set dressing`.

### 2. Darkness is the primary material

Amateur work lights the whole subject. Premium work lights *an edge* and lets the
rest fall to true black. The shot becomes a negotiation between the eye and what
it can't quite see, which is exactly the tension a reveal needs.

```
The object is 80% in shadow; only the top-left chamfer carries a thin hard
specular. The right two-thirds of frame falls to true black with no visible
detail, no fill light, no bounce.
```

### 3. The camera moves slower than you think

Almost every AI clip moves too fast. The premium grammar is a move so slow you
notice it only by comparing the first and last frame — 15 to 30 centimeters of
travel across six to eight seconds, on a single axis, with no acceleration.

Always quantify it: distance, duration, easing, and the word *continuous*. And
always pair slow camera with realtime physics — see the pace section of
`references/seedance-prompt-architecture.md`, this is the trap.

### 4. Nothing wobbles

A hero object that drifts, bobs, or slowly rotates when it wasn't asked to reads
as fake instantly. Lock the subject with words, explicitly, every time:

```
The object is locked in frame — it does not rotate, tilt, bob, drift, or change
scale. Only the light and the camera move.
```

### 5. Light does the work, not motion

The most sophisticated Seedance move is barely a move at all: the camera holds,
and a **highlight travels**. A specular sweeping along a chamfer, a shadow
retreating across a surface, a caustic crawling over a lens. The frame changes
completely and nothing in it actually moved.

```
Camera locked. Over 5 seconds a single hard specular travels left to right along
the top chamfer, crossing the engraved mark at 3 seconds and igniting it briefly.
```

### 6. End on stillness

Elegant shots land. They don't fade, drift out, or keep wandering. The final beat
resolves to a composed, held frame — the object centered or on a third, the light
settled, the camera stopped. Say it:

```
Final beat: the camera stops dead and the frame holds absolutely still for the
last half second, the object composed on the lower third, mark fully lit.
```

## The Premium Reveal Look — Component Breakdown

The recognizable modern launch-film look is not a style word, it is six concrete
choices. Name them individually; never name a brand as an imitation target.

| Component | What to write |
|---|---|
| Environment | `seamless charcoal-to-black gradient void, no horizon line, no floor seam, no set dressing` |
| Light | `one large soft source high camera-left, hard falloff to true black; one travelling hard specular` |
| Lens | `85mm or 100mm macro, shallow depth of field, focus plane on the front chamfer` |
| Camera | `single continuous push-in, ~20cm across the full duration, motion-control smooth, no acceleration` |
| Grade | `low-key neutral, cold steel and graphite with one warm amber specular; deep blacks, no crush` |
| Negatives | `NO god rays, NO lens flare, NO bloom, NO blue filter, NO on-screen text, NO extra objects` |

Stack all six and the clip reads as a launch film. Drop the negatives and it reads
as stock footage. Drop the environment lock and it reads as a render test.

## Lens Language

Seedance responds to focal length. Use it as a real decision, not decoration.

| Lens | Character | Reach for it when |
|---|---|---|
| 24mm | Wide, dramatic perspective, objects loom | Architecture, interiors, a hero object made monumental from low angle |
| 35mm | Natural wide, honest space | Establishing, environment-in-frame, character beats |
| 50mm | Neutral, human, unshowy | Two-shots, dialogue, "just look at the thing" |
| 85mm | Compression, flattering, isolating | The default premium product lens — subject separates from a black void |
| 100mm macro | Extreme intimacy, texture as landscape | Detail reveals, engraving, weave, liquid meniscus, dust on a surface |
| Anamorphic 2.39 / 21:9 | Cinema letterbox, oval bokeh, horizontal flare | Whenever the brief says *cinematic* — the aspect alone does real work |

Pair lens with distance for compression control: `85mm from two meters, subject
isolated against void` reads differently from `24mm from thirty centimeters,
foreground edge looming`.

## Light Setups Worth Naming

Each of these produces a distinct, recognizable look. State the setup, then the
negatives.

- **Single soft top-left** — the default premium look. Broad soft source high and
  to one side, hard falloff, black on the opposite side.
- **Rim only / edge light** — subject in near-silhouette, a single bright line
  describing its outline. Maximum drama, minimum information.
- **Underlight / plinth glow** — light from below, subject floating above a glowing
  base. Reads as reverence; also reads as sci-fi if overdone.
- **Travelling specular** — the light source itself moves, or the object's chamfer
  catches a sweeping highlight. The elegant move that isn't a move.
- **Practical-motivated** — the light has a visible in-world source: a window slat,
  a screen, a candle. Name the source or Seedance invents god rays.
- **High-key void** — pure white seamless, soft shadowless light, one thin contact
  shadow. The clean-tech alternative to darkness; needs even stricter negatives
  because Seedance loves adding gradients.
- **Chiaroscuro slat light** — hard blinds or louvre shadows striping the subject.
  Instant drama; specify the slat direction and that the pattern is static unless
  a beat moves it.

Universal light negatives, every time:

```
NO god rays, NO visible light beams, NO lens flare, NO anamorphic streaks unless
named, NO bloom, NO haze glow, NO blue grade, NO rainbow prism artifacts.
```

## Shadow As A Verb

Shadows are the most under-used tool in AI video and the most effective for
elegant reveals. Treat a shadow as something that *acts*.

| Move | Prompt phrasing |
|---|---|
| Shadow retreat | `a hard-edged shadow retreats left-to-right across the object's face at a constant rate over 3 seconds, uncovering the engraved mark last` |
| Shadow wipe transition | `the shadow sweeps across frame and fills it completely, and the next beat emerges from the same darkness — shadow wipe, not a dissolve` |
| Shadow cast reveal | `the object stays unlit; its cast shadow on the wall behind is the only thing we see clearly, sharpening as the light approaches` |
| Slat crawl | `hard blind shadows crawl 20cm across the surface as the source moves, striping the object then clearing it` |
| Silhouette bloom | `the object reads as pure black silhouette against a dim ground; light rises behind it until the silhouette is rimmed, then the front fills in last` |

Always state the shadow's **edge quality** (hard or soft), its **direction of
travel**, and its **rate** (`at a constant rate`, `never accelerating`).

## Focus As A Verb

Rack focus is a real reveal mechanism and Seedance handles it well.

```
Camera locked, 100mm macro. Focus opens on the foreground edge, entirely soft
beyond it; over 4 seconds the focus plane travels backward and the engraved mark
resolves from complete blur into razor sharpness. Nothing else in frame moves.
```

Variants worth knowing:

- **Blur-in reveal** — start fully defocused, resolve to sharp. The most reliable
  "premium reveal" opener that exists. Specify *the whole frame begins as soft
  bokeh with no readable form* and the resolve rate.
- **Blur-out landing** — resolve then fall back to bokeh for an end card.
- **Focus handoff** — sharpness travels from one object to another, front to back;
  the eye follows without a cut.
- **Breathing focus** — a barely-perceptible focus drift that keeps a static
  frame alive. Use sparingly; it can read as an autofocus fault.

## Materials And What They Buy You

Naming material behaviour is what makes a render read as photographed. Seedance
models these convincingly if you describe the *behaviour*, not the noun.

| Material | Describe its behaviour |
|---|---|
| Brushed metal | `anisotropic streak highlight that stretches along the grain as the camera travels` |
| Polished metal / chrome | `mirror reflection carrying the void and a single soft source; the reflection travels as the camera moves` |
| Glass | `refraction bending the background edge, a bright caustic on the surface below, thin bright edge at the rim` |
| Matte ceramic | `broad soft falloff, no specular, dust-fine surface texture visible at macro` |
| Anodized aluminium | `low-gloss satin sheen, soft wide highlight with no hotspot` |
| Leather / textile | `visible weave or grain at macro, light catching the raised fibres, soft self-shadow in the seams` |
| Liquid | `surface tension at the meniscus, one clean caustic below, realtime physics` |
| Fabric | `weight and drape at realtime speed — it falls, it does not float` |
| Skin | `subsurface warmth at the edges, visible pores at macro, never plastic` |

## Composition

- **Center for reverence, thirds for tension.** A dead-centered object under one
  light reads as ceremonial. Off-center with negative space reads as editorial.
  Choose, and say which.
- **Negative space is content.** `the object occupies the lower-left third; the
  remaining two-thirds is empty black, and stays empty`.
- **Use one strong graphic line** — a horizon, a chamfer, a shadow edge — and let
  the camera move relative to it.
- **Frame for the aspect.** 21:9 wants horizontal separation and headroom above a
  low object. 9:16 wants vertical stacking and a subject that fills the middle third.

## Tempo And The Shape Of A Cut

A cinematic sequence has a rhythm, not a uniform pulse.

- **Held opener** (2.5–3s) — near-still, establishes darkness and scale. Earns
  everything after.
- **Two or three information beats** (2–2.5s each) — each shows something new:
  a detail, an angle, a mechanism.
- **One accent** (1–1.5s) — the fast one. A snap push, a whip, a hard light hit.
  Contrast makes the slow beats read as intentional rather than sluggish.
- **Landing** (2–3s) — composed, still, resolved.

Silence between accents is what makes an accent land. If every beat is exciting,
nothing is.

## Colour And Grade

Say the grade explicitly or accept Seedance's teal-and-orange instinct.

- `low-key neutral: graphite, cold steel, true blacks, one warm amber specular`
- `monochrome charcoal, no colour cast at all, single white highlight`
- `warm document look: bone white, sand, brass; no cool tones anywhere`
- `clean high-key: bone white seamless, neutral white balance, no gradient`

And the negative every time: `NO blue filter, NO teal-orange grade, NO heavy
vignette unless named`.

## Atmosphere In Small Doses

A tiny amount of atmosphere makes a void feel like a photographed space. Too much
makes it a fog machine.

Good: `three or four dust motes drifting through the rim light, realtime speed`;
`the faintest haze only where the light source enters frame`; `a single thread of
vapour rising and dissipating within one second`.

Bad: `atmospheric fog`, `smoke everywhere`, `dreamy particles` — these fill the
frame, kill the blacks and invite god rays.

## Audio For Elegance

Restraint applies to sound too.

- Default for a hero reveal: `no music; only room tone and one precise mechanical
  sound at the moment of the event`.
- If music is wanted: `one sustained low tone that swells once at the reveal, no
  percussion, no build-drop structure`.
- Ban the defaults: `no trailer hits, no whoosh transitions, no risers, no
  voiceover, no captions`.

## The Anti-Patterns Checklist

Run this against any prompt before submitting. Each item is something Seedance
will do unasked.

- [ ] Two or more camera moves inside one beat
- [ ] Pace adverbs (`slowly`, `gently`, `softly`, `dreamily`) with no quantified move
- [ ] No motion split, so the subject drifts
- [ ] No world lock, so beat 3 relocates
- [ ] No light negatives, so god rays and flare arrive
- [ ] No text lock with a mark in frame
- [ ] Adjective inflation instead of an added beat
- [ ] Long final hold in a multi-beat prompt
- [ ] No constraints tail
- [ ] Music not specified, so trailer scoring appears
- [ ] Brand named as an imitation target instead of the look described in craft terms

## Where To Go Next

- Named, ready-to-adapt effect recipes → `references/reveal-recipes.md`
- Floating, orbiting, exploded, macro-dive, 3D-render motion → `references/dimensional-motion.md`
- Logos and wordmarks → `references/logo-and-mark-motion.md`
- The prompt's structural rules → `references/seedance-prompt-architecture.md`
