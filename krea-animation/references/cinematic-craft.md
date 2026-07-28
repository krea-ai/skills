# Cinematic Craft — The Language Of Dramatic, Maximal Motion

This is the taste reference. `references/seedance-prompt-architecture.md` tells you the shape
of a prompt and `references/cut-architecture.md` tells you how to structure the
beats; this file tells you what to put inside them so the result looks expensive
instead of merely generated.

The target register: **dramatic, kinetic, high-contrast, cut hard.** Title-sequence
energy. Flagship hardware launch films, fragrance and watch campaigns shot as a
rapid chain of macro details, sneaker and hardware reveals that show you the stitch
before they show you the shoe. Every second earns its place; the whole subject
arrives last.

Two opposite registers to suppress, and the first one is the more common failure:

- **Timid drift** — one continuous move over eight seconds, one lighting state, the
  whole subject visible from frame one, a highlight wandering across it. This reads
  as a screensaver. It is what the model returns when the prompt did not commit to
  anything, and it is the single most likely way to disappoint.
- **Untamed maximalism** — Seedance's own default: three lights at once, drifting
  handheld, lens flare, blue grade, glossy everything, and nothing in particular
  happening. Cutting hard is not the same as flailing.

The distinction that matters: **density belongs to the edit, restraint belongs to
the frame.** Each individual beat is still mostly darkness with one lit subject and
one quantified move. There are just four or five of them in eight seconds, each from
a different angle under a different light.

## The Six Laws Of Dramatic Motion

Internalize these. Every recipe in `references/reveal-recipes.md` is an application of them.

### 1. Spend on cuts, not on clutter

Every frame is subtracted; the *sequence* is maximal. One light source per beat,
not three. One camera move per beat, not a combination. One event per beat. But
four or five beats in eight seconds, each from a new angle under a new key.

Write each frame as **95% darkness and 5% information**, then defend that ratio in
the constraints tail: `no additional objects, no props entering frame, no
background detail, no set dressing`. Richness comes from cutting between five such
frames, never from filling one of them.

When a piece feels thin, the fix is another staged beat — never another adjective
and never another light in the same frame.

### 2. Darkness is the primary material

Amateur work lights the whole subject. Premium work lights *an edge* and lets the
rest fall to true black. The shot becomes a negotiation between the eye and what
it can't quite see, which is exactly the tension a reveal needs.

```
The object is 80% in shadow; only the top-left chamfer carries a thin hard
specular. The right two-thirds of frame falls to true black with no visible
detail, no fill light, no bounce.
```

### 3. Short beats, controlled motion inside them

The beats are fast. The motion *within* a beat is not frantic — a 1.2-second beat
carries one small, exact move, or no camera move at all with the light doing the
work. Cutting supplies the energy; the camera stays composed.

Quantify every move regardless of length: distance, duration, constant rate, and
the word *continuous*. This matters more at speed, not less — an unquantified
"quick push in" comes back as a smeared whip, and `slowly` / `gently` / `softly` as
the only pace instruction comes back speed-ramped. See the pace section of
`references/seedance-prompt-architecture.md`.

```
SHOT 3 — RAKE (3.0–4.2s), extreme close-up, 100mm macro. Camera pushes in 6
centimeters over 1.2 seconds at a constant rate, realtime physics, no ramping.
```

The single long glacial move still has a place — a 6–8 second continuous push is
legitimate for an architectural interior or a landing beat. It is a deliberate
choice for a specific job, not the default answer to "animate this."

### 4. Nothing wobbles

A hero object that drifts, bobs, or slowly rotates when it wasn't asked to reads
as fake instantly. Lock the subject with words, explicitly, every time:

```
The object is locked in frame — it does not rotate, tilt, bob, drift, or change
scale. Only the light and the camera move.
```

### 5. Light is an event per beat, not a wash across the piece

Moving the key between beats is the cheapest way to make four cuts read as four
shots. Give every beat its own lighting state and name the direction: hard rake
from top-left at 20°, then rim-only from directly behind, then underlit throwing
shadow up the wall, then broad top light as the piece opens out.

Within a beat, a travelling highlight is a legitimate *event* — a specular crossing
an engraving, a shadow clearing a surface, a caustic crawling over glass. What it
cannot be is the entire piece.

```
SHOT 2 — IGNITION (1.4–2.6s), extreme close-up, 100mm macro, camera on the opposite
face from SHOT 1. HARD CUT in. Key flips to a hard source directly behind the
object; the front face drops to silhouette and a single specular fires along the
top chamfer, crossing the engraving at 2.1s.
```

**The anti-pattern this replaces:** one locked camera, one full view of the subject,
and a highlight drifting across it for eight seconds. That is the shot the model
returns when nothing was asked of it. If your prompt could be summarized as "a
shimmer passes over it," throw it away and build the beats.

### 6. The whole subject arrives last, and lands dead still

Withhold the full view. Beats one through three live inside the object; the pull
begins on beat four; the complete subject appears only on the final beat — fully
lit, composed, camera stopped. After a fast chain of macro cuts, that stillness is
what makes the reveal feel earned.

```
Final beat: HARD CUT to full frame. The camera stops dead and holds absolutely
still for the last two seconds, the object composed on the lower third, key plus
rim, every edge legible.
```

Never fade out, never drift past the landing, and never open the piece on the shot
you intend to end it with.

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

A cinematic sequence has a rhythm, and for this skill that rhythm is front-loaded
and fast. The full build lives in `references/cut-architecture.md`; the shape:

- **Macro chain** (three beats, 1–1.8s each) — three details, three angles, three
  lighting states. No establishing shot. The viewer does not yet know the whole.
- **The pull** (1–1.5s) — the subject becomes readable but is still not complete.
- **Landing** (2–2.5s) — the whole subject, fully lit, composed, camera stopped.

The contrast that makes this work is **fast cuts against a still landing**, not
slow beats against one accent. Three quick macro cuts make the final held frame
feel like an arrival; an eight-second drift makes it feel like nothing happened.

Where the older grammar still applies: an architectural interior, a landscape, or
a long product hero for a brand that has explicitly asked for restraint. Say out
loud that you are choosing it, and why.

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
- [ ] Any of the cheap motion-graphics defaults below

### The cheap list — ban these explicitly in every constraints tail

These are the stock-template moves. They arrive unasked, they look free, and one of
them ruins an otherwise good piece:

```
no light streaks, no shine sweeps, no glints or sparkles, no bars, stripes, bands or
rectangles moving across the frame, no swipe or wipe transitions, no gradient sweeps,
no lens flare, no bokeh particles, no dust overlays, no scan lines, no glow pulses
```

Two of these are legitimate *only* on a physical object with real surfaces — a
travelling specular on a chamfer, blind shadows crawling across a wall. On flat
artwork they degenerate into sliding bars, which is the single most recognisable
cheap-animation tell.

## Where To Go Next

- Named, ready-to-adapt effect recipes → `references/reveal-recipes.md`
- Floating, orbiting, exploded, macro-dive, 3D-render motion → `references/dimensional-motion.md`
- Logos and wordmarks → `references/logo-and-mark-motion.md`
- The prompt's structural rules → `references/seedance-prompt-architecture.md`
