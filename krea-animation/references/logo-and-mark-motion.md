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

## What Actually Reads Well

Logo animation is a light-and-camera discipline. The mark holds still and the
world around it changes. Ranked by how reliably they land:

### 1. Specular Sweep Across The Mark (most reliable)

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

### 2. Shadow Retreat Off The Mark

Same structure, shadow instead of highlight. See recipe 1 in `reveal-recipes.md`.
Add: `the shadow edge is hard and travels at a constant rate; the letterforms
themselves never deform as it passes`.

### 3. Blur-In Resolve

```
SHOT 1 — RESOLVE (0–3s), medium close, 85mm. Camera locked. The frame opens as
complete soft bokeh with no readable letterform. Over 3 seconds the focus plane
travels until the mark resolves into razor-sharp definition, its edges perfectly
crisp. Focus travels at a constant rate. The mark does not move, scale, or deform
at any point — only sharpness changes.
```

The `only sharpness changes` clause is what stops Seedance from *animating the
letters into existence*, which is where re-lettering happens.

### 4. Depth Emergence

The mark comes forward out of the surface. Effective, slightly riskier.

```
SHOT 2 — EMERGE (1.5–4s), medium close, 85mm. Camera locked. The mark rises 4
millimeters out of the surrounding surface in one continuous move across 2.5
seconds at a constant rate, becoming a raised inlay with its own cast shadow
appearing beneath its edges. The letterforms keep their exact shape, weight and
spacing throughout — they extrude, they do not redraw.
```

### 5. Reflected Approach

```
SHOT 1 — REFLECTION (0–2.5s), macro, 100mm. Camera locked low on a polished black
surface; the mark is visible only as its own mirror reflection. At 2s the camera
tilts up 20 degrees in one continuous move and arrives on the mark itself, sharp
and composed, and stops dead.
```

### 6. Material Reveal

The mark is the only lit element; the material of the surrounding surface changes
under travelling light. Elegant and very safe for the mark itself, since the mark
never moves at all.

## What To Avoid

| Don't ask for | Why | Instead |
|---|---|---|
| Letters flying in and assembling | Each letter gets re-drawn in flight; kerning collapses | Blur-in resolve, or specular sweep |
| Handwriting / draw-on animation | The model invents letterforms stroke by stroke | Shadow retreat uncovering a finished mark |
| Morphing one mark into another | Both marks end up wrong | Two shots with a hard cut between them |
| Liquid or smoke forming the logo | Letterforms deform as the medium settles | Particle/haze *around* a locked mark |
| 3D logo tumbling in space | Perspective change re-renders the glyphs | Camera orbit ≤ 20° with the mark locked |
| Adding a tagline or URL | It will be invented and misspelled | Ban added text; composite type in post |

## Type In Frame

If the deliverable needs real typographic layout — kinetic type, an end card,
a tagline with exact copy, a lockup with legal lines — **do not ask Seedance for
it.** Generate the textless cinematic footage here and compose type deterministically
in post. `../../krea-marketing/workflows/launch-teaser.md` covers that handoff.

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
