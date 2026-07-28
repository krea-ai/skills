# Logo And Mark Motion

Animating a logo is the hardest easy request in AI video. Every other subject
tolerates a little drift; a wordmark does not. One re-lettered character, one warped
counter, one shifted kerning pair and the shot is unusable no matter how beautiful
the light is.

Seedance is unusually good at this — printed and engraved marks survive full
multi-beat generations — but only when the prompt treats the mark as **inviolable
geometry** rather than as an image element.

## The Text Lock

This is mandatory in **three** places for any shot with a mark in frame: the
references block, the motion split, and the constraints tail. Repetition is the
anti-drift mechanism, not sloppiness.

```
References: @Image1 as the first frame and the brand mark. Every letterform,
stroke weight, counter, kerning pair and proportion is fixed exactly as shown —
do not re-letter, re-draw, re-space, warp, skew, bold, italicize, or substitute
any glyph. Do not add or remove any character. Do not translate the mark.
```

```
Motion split: the mark itself is completely locked — no deformation, no scale
change, no rotation, no perspective change unless a beat names it. Only light,
shadow, focus and camera move.
```

```
Constraints (reassert): the mark is pixel-exact to @Image1 — same letterforms,
same weights, same spacing, same proportions; never re-lettered, never warped,
never substituted; no additional text, no tagline, no captions, no watermark, no
URL, no added graphics.
```

That last line matters as much as the first: unprompted, Seedance likes to add a
tagline underneath a logo. Ban it explicitly.

## First: Is The Mark Flat Or Dimensional?

This decides everything below, and getting it wrong is what produces cheap results.

**A flat 2D vector mark** — solid fills, no material, no thickness, no lighting baked
in — has nothing to reveal at macro scale. Push into it and you get a large area of
flat colour, which is why a zoom into a vector logo looks like a mistake. It also has
no surface to rake light across, so lighting recipes degrade into bars and streaks
sliding over the artwork: the free-template look. For a flat mark, motion must come
from the **elements themselves** — their brightness, colour, position and order — or
from giving the mark real material first.

- Use: per-element choreography, scale and position builds, focus resolve.
- Do not use: macro detail beats, raking or travelling light, slat crawl, shadow
  wipes, camera orbit, depth emergence.
- Or: render the mark as a physical object first (inlaid metal, embossed, extruded)
  with an image generation, approve that still, then animate it as a dimensional
  mark.

**A dimensional mark** — inlaid, embossed, extruded, printed on a real surface, or a
3D render — has material and depth. Everything below applies.

## What Actually Reads Well

A logo sting is a **cut sequence through the mark**, not a lighting effect applied
to it. The letterforms stay pixel-exact — that constraint never relaxes — but the
camera, the scale, the key and the per-element lighting all change hard between
beats. Ranked by impact, with the reliability caveat noted on each.

### 1. Per-Element Choreography (the default for any mark with separable parts)

Break the mark into its actual vector parts — for a wordmark the letterforms, for a
monogram or symbol the individual bowls, counters, strokes and dots — and give each
part **a different small action**, staggered in time, all converging on exact final
registration.

The mistake is giving every part the same action in sequence. Four shapes that each
rise four millimetres in turn is a queue, not choreography. Four shapes where one
rotates, one lifts and drops with a little overshoot, one slides along its own axis
and one counter-rotates against its neighbour is a mark with personality — and it is
no harder to prompt.

**The payoff is the snap, not a light sweep.** Everything arrives at exact
registration on the same frame, and that click into place is the moment the piece is
built around.

A menu to draw from, one per part:

| Action | Magnitude |
|---|---|
| Rigid rotation, settling back | 5–10°, with a small overshoot |
| Lift and drop | 4–6mm, landing with a slight bounce |
| Slide along its own axis and return | 3–5mm |
| Breathe — scale up and return | 2–3% |
| Counter-rotate against an adjacent part | 5–8° the opposite way |
| Ignite in its own colour | black to full saturation |

**What keeps it safe:** rigid transforms only, small magnitudes, and an exact return.
Each part keeps its drawn form at every frame — it rotates, it does not redraw. Say
the maximum for each transform and say that the final frame is pixel-exact to the
source.

```
Format: Brand mark sting, 5 seconds, 16:9, pure black void, no added text.
References: @Image1 as the first frame and the mark — every shape, curve, weight, gap
and colour pixel-exact as shown; do not redraw, warp, re-space or substitute any part.
Consistent world: seamless pure-black void, no horizon, no floor seam, no set
dressing. The mark sits dead centre and its final position is identical to @Image1.
Motion split: the mark is composed of separate rigid shapes. Each shape keeps its
exact drawn form at all times — the only permitted motion is a rotation of at most 8
degrees, a translation of at most 5 millimetres, or a scale change of at most 3
percent, always returning to its exact position in @Image1. No shape deforms,
stretches, squashes or redraws. Camera locked. Realtime physics, no speed ramping.

SHOT 1 — STAGGERED PLAY (0–3s), medium close, 85mm, camera locked. The parts of the
mark move one at a time, 0.15 seconds apart, each doing something different: the
upper-left shape rotates 8 degrees counter-clockwise and settles back with a small
overshoot; the lower-left shape lifts 5 millimetres and drops, landing with a slight
bounce; the diagonal stroke slides 4 millimetres along its own axis and returns; the
upper-right shape counter-rotates 6 degrees clockwise, the opposite way to its
neighbour, and settles. Each shape holds its exact drawn form throughout and moves as
one rigid piece.
SHOT 2 — SNAP (3–3.4s), medium close, 85mm. Every shape arrives at its exact final
registration on the same frame with one quick ease-out. The mark is now pixel-exact
to @Image1.
SHOT 3 — HOLD (3.4–5s), medium close, 85mm. Absolutely still, mark composed dead
centre, razor sharp, for the remaining time.

Light: flat even illumination on the mark, pure black surround. NO god rays, NO lens
flare, NO bloom, NO gradient sweeping across the mark.
Audio: no music; one soft tick per part as it moves, one low resolving tone at 3.4s.
Constraints (reassert): the final frame is pixel-exact to @Image1 — same shapes, same
weights, same spacing, same proportions; per-part motion is rigid rotation under 8
degrees, translation under 5 millimetres, or scale under 3 percent, always returning
to exact registration; no part deforms or redraws; no masks, no wipes, no straight
edge travelling across the mark; no circles, rings, ripples, halos or arcs appearing
around the mark; no uniform scale-down of the whole mark as the only motion; the
sequence plays once, forward, and resolves; realtime physics, no speed ramping; no
additional text, no tagline, no captions, no watermark.
```

Run per-part vision QA on the last frame of the staggered beat and on the snap — a
part that drifted mid-chain often settles back correctly and hides the error.

### 2. Macro Cut Chain Through The Mark

Three to four extreme close-ups of different parts of the mark — a corner, a
counter, the junction of two strokes — each from a different angle under a
different key, cut hard, then a pull out to the full lockup. Shows off material and
craft, and never asks a letterform to move at all, so it is the safest way to get
maximal energy out of a mark.

Build it on the standard five-beat structure in `references/cut-architecture.md`,
with `the letterforms are pixel-exact and completely static throughout` in the
motion split.

### 3. Blur Reveal On A Pull-Out

The frame opens as unreadable bokeh at macro scale; as the camera pulls back the
focus plane travels left to right and the mark snaps sharp exactly as it becomes
whole. One continuous move, but the frame transforms completely.

```
Motion split: the mark is locked and pixel-exact. The camera pulls back 35cm over 4
seconds at a constant rate while the focus plane travels across the mark left to
right at a constant rate; the leftmost letterform resolves first, sharpness
sweeping right, the complete lockup razor sharp and fully composed at 4s. Only
sharpness and framing change — the mark does not move, scale or deform.
```

The `only sharpness and framing change` clause is what stops Seedance from
animating the letters into existence, which is where re-lettering happens.

### 4. Specular Sweep Across The Mark (most reliable, least exciting)

The safe fallback: camera locked, one hard highlight travelling across a static
mark. Use it when the mark is fragile, extremely detailed, or has already failed a
more ambitious treatment twice — **not** as the first answer to "animate this
logo," which is the timid-drift failure this skill exists to prevent.

```
Format: Brand mark sting, 5 seconds, 16:9, low-key metallic, no added text.
References: @Image1 as the first frame and the brand mark — every letterform fixed
exactly as shown, never re-lettered or warped.
Consistent world: seamless charcoal-to-black void, no horizon, no floor seam; the
mark rendered as brushed metal inlaid in a dark surface.
Motion split: the mark is completely locked — no deformation, no scale change, no
rotation. Camera locked absolutely still. Only the light moves, at realtime speed.

SHOT 1 — DARK HOLD (0–1.5s), medium close, 85mm. The mark is barely visible in near
darkness, only the faintest edge definition. Nothing moves.
SHOT 2 — SPECULAR SWEEP (1.5–4s), medium close, 85mm. A single hard specular
highlight travels left to right across the mark at a constant rate, igniting each
letterform in turn as it passes and leaving it softly lit behind. Camera still
locked.
SHOT 3 — SETTLE (4–5s), medium close, 85mm. The highlight clears the right edge;
the mark holds evenly lit and razor sharp, dead center, absolutely still for the
final second.

Light: one hard travelling source, otherwise near-black; NO god rays, NO lens flare,
NO bloom, NO blue grade.
Audio: no music; one low sustained tone that resolves at 4s.
Constraints (reassert): the mark is pixel-exact to @Image1 — same letterforms,
weights and spacing, never re-lettered, never warped; camera locked throughout;
light-only motion at realtime speed, no speed ramping; no additional text, no
tagline, no captions, no watermark, no added graphics; no morphing.
```

### 5. Shadow Retreat Off The Mark

Same structure, shadow instead of highlight. See recipe 1 in `references/reveal-recipes.md`.
Add: `the shadow edge is hard and travels at a constant rate; the letterforms
themselves never deform as it passes`.

### 6. Depth Emergence

The mark comes forward out of the surface. Effective, slightly riskier.

```
SHOT 2 — EMERGE (1.5–4s), medium close, 85mm. Camera locked. The mark rises 4
millimeters out of the surrounding surface in one continuous move across 2.5
seconds at a constant rate, becoming a raised inlay with its own cast shadow
appearing beneath its edges. The letterforms keep their exact shape, weight and
spacing throughout — they extrude, they do not redraw.
```

### 7. Reflected Approach

```
SHOT 1 — REFLECTION (0–2.5s), macro, 100mm. Camera locked low on a polished black
surface; the mark is visible only as its own mirror reflection. At 2s the camera
tilts up 20 degrees in one continuous move and arrives on the mark itself, sharp
and composed, and stops dead.
```

### 8. Material Reveal

The mark is the only lit element; the material of the surrounding surface changes
under travelling light. Elegant and very safe for the mark itself, since the mark
never moves at all.

## What To Avoid

The line is **building versus lighting**. A glyph that already exists can be lit,
lifted, cut to, or pulled away from as hard as you like. A glyph the model has to
construct comes back misspelled.

| Don't ask for | Why | Instead |
|---|---|---|
| Letters flying in and assembling | Each letter is re-drawn in flight; kerning collapses | Per-element choreography — parts already present, moving as rigid pieces |
| Handwriting / draw-on animation | The model invents letterforms stroke by stroke | Shadow retreat or blur reveal uncovering a finished mark |
| Morphing one mark into another | Both marks end up wrong | Two shots with a hard cut between them |
| Liquid or smoke forming the logo | Letterforms deform as the medium settles | Particle/haze *around* a locked mark |
| 3D logo tumbling in space | Perspective change re-renders the glyphs | Macro cut chain — hard cuts between fixed angles, each ≤ 20° off axis |
| Adding a tagline or URL | It will be invented and misspelled | Ban added text; composite type in post |
| A straight edge or mask sliding across the mark | The 2D overlay tell — it is a slide transition, not motion the mark is doing | Per-element choreography; the parts move, nothing sweeps over them |
| Rings, circles, ripples, halos or arcs around the mark | Free-template radar-ping preset; adds geometry that is not in the logo | Stagger the mark's own parts instead of decorating around it |
| The whole mark uniformly scaling up or down | Not animation, just a zoom; reads as a placeholder | Give each part its own action, converging on a snap |

What is explicitly **not** banned, and should be your default reach: cutting hard
between macro views of the mark, per-letter illumination, per-letter translation
within a few millimeters, colour igniting element by element, and pulling out from
a detail to the full lockup. All of these keep the drawn glyph intact.

## Type In Frame

If the deliverable needs real typographic layout — kinetic type, an end card,
a tagline with exact copy, a lockup with legal lines — **do not ask Seedance for
it.** Generate the textless cinematic footage here and compose type deterministically
in post. the `krea-marketing` skill's `workflows/launch-teaser.md` covers that handoff.

The division of labour: Seedance owns light, camera, material and motion. A layout
tool owns letterforms it did not invent.

## Vision QA For Marks

Non-negotiable before delivering any logo shot. Extract and inspect **first, middle
and last** frames — drift is progressive, so the last frame is where failure hides:

```bash
ffmpeg -i mark-raw.mp4 -vf "select='eq(n\,0)+eq(n\,60)'" -vsync 0 -q:v 2 frame-%02d.png
ffmpeg -sseof -0.1 -i mark-raw.mp4 -update 1 -frames:v 1 -q:v 2 frame-last.png
```

Read each frame with vision and check, letter by letter:

- [ ] Every glyph is the correct character
- [ ] Stroke weights match the source
- [ ] Counters (enclosed shapes in a, e, o, R) are open and correctly shaped
- [ ] Kerning matches the source — no collisions, no gaps
- [ ] No character added, dropped, or duplicated
- [ ] No warp, skew, or perspective change that wasn't asked for
- [ ] No tagline, URL, or watermark invented
- [ ] The mark is as sharp in the last frame as the first

Any failure is a retake, not a note. A mark that is 95% right is 100% wrong.

## Fallback Path

If three seeds all drift the mark:

1. Check the start image at full resolution. A soft or upscaled-from-small mark
   cannot survive — the start image is the ceiling. Get a clean vector-derived
   raster.
2. Reduce the ambition: drop to camera-locked, light-only motion. The mark that
   never moves cannot be re-lettered.
3. Split the shot: generate the cinematic environment footage with the mark
   *absent*, then composite the real mark in post.

Option 3 is not a defeat. For a brand deliverable it is frequently the
professional answer, and it is always the right answer when legal copy is involved.
