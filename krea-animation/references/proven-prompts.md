# Proven Prompts — The Five Core Use Cases

Five slots covering the animation requests that come in most often. Each slot is a
complete, submittable Seedance prompt plus the setup around it: which fields to
attach, what to check first, and what to look for in the output.

## Status Of This File

Each slot currently holds a **scaffold** — a structurally complete prompt built from
`references/seedance-prompt-architecture.md` that will produce a competent shot today. Each is
marked:

```
<!-- PLACEHOLDER: replace with a verified winning prompt -->
```

These scaffolds are to be replaced with prompts verified to work well in production.
When replacing one:

- Keep the surrounding **Route here when / Attach / Settings / Check the output**
  sections — they are the operating instructions, not the prompt.
- Keep every block of the architecture present in the replacement. If a verified
  winner is missing a constraints tail, add one; drift is not a style choice.
- Remove the `PLACEHOLDER` comment once replaced.
- Note anything the prompt is sensitive to (a specific aspect, a duration floor, a
  material it fails on) under **Notes** so the next person doesn't rediscover it.

Angle brackets `<like this>` mark values to substitute per job. Everything outside
them is load-bearing prompt language — keep it.

---

## Slot 1 — Product Hero Reveal

The flagship request. One object, dark void, glacial camera, shadow or specular
reveal, held landing. The premium launch-film register.

**Route here when** the user wants a product, object, device, bottle, package or
piece of hardware to look expensive; asks for a "reveal", "hero shot", "launch
video", "cinematic product video"; or hands over one product still and says "make
this look premium".

**Attach**
- `start_image` — the hero product still. **Gate this first**: read it with vision;
  if the mark is soft, the crop is wrong, or it's a compressed video frame, fix the
  still before generating. The start image is the ceiling.
- `reference_images` — optional: one product detail, one environment reference.
- No `end_image` if using reference images.

**Settings** `duration` 8s · `aspect_ratio` 21:9 (16:9 if it must cut into standard
delivery) · `resolution` 1080p · `generate_audio` on for standalone, off for an edit
· block on `seedance-2-fast`, deliver on `seedance-2` · best-of-2 seeds for hero.

<!-- PLACEHOLDER: replace with a verified winning prompt -->
```
Format: Single-shot cinematic product reveal, 8 seconds, 21:9, anamorphic cinema
look, low-key deep-shadow grade, no on-screen text.
References: @Image1 as the first frame and the hero object — <product>; keep every
printed line, logo and engraved mark exactly as shown, do not warp or re-letter any
text.
Consistent world across all beats: seamless charcoal-to-black gradient void, no
horizon line, no floor seam, no set dressing; one large soft source high
camera-left falling off to true black on the right; palette is <graphite, cold
steel, one warm amber specular>; shallow depth of field throughout.
Motion split: the object is locked — it does not rotate, wobble, drift, or change
scale at any point. All movement belongs to the camera and the light. Three or four
dust motes drift through the rim light at natural realtime speed. Nothing is
speed-ramped; no slow-motion.

SHOT 1 — VOID HOLD (0–2.5s), extreme wide, 35mm. Camera locked absolutely still.
The object sits centered in near-total darkness, 80% in shadow, only its top
<chamfer/edge> carrying a thin hard specular. Nothing moves but a single dust mote
crossing the rim light. Shadow wipe.
SHOT 2 — SHADOW RETREAT (2.5–5.5s), medium close, 85mm. Camera locked. A hard-edged
shadow retreats left-to-right across the object's face at a constant rate, never
accelerating, uncovering the surface, then the <chamfer>, and the <mark> last. The
object stays locked. Cut on the highlight.
SHOT 3 — LANDING (5.5–8s), medium close, 85mm. One single continuous push-in of
roughly 15 centimeters across the beat, dead level, motion-control smooth, never
accelerating. The camera stops dead and the frame holds absolutely still for the
final half second, the object composed on the lower third, <mark> razor sharp and
fully lit for the first time.

Light: one large soft source high camera-left, hard falloff to true black across the
right two-thirds; a single hard <amber> specular travels the top edge. NO god rays,
NO light beams, NO lens flare, NO bloom, NO blue filter; neutral white balance;
blacks deep but never crushed to noise.
Audio: no music; only room tone and one soft mechanical settle at 5.5s.
Constraints (reassert): one continuous world, charcoal void, single soft top-left
source; the object is locked and never rotates, drifts or changes scale; camera
moves slow, continuous and motion-control smooth with realtime physics, no speed
ramping, no slow-motion, no floating; every printed line and mark exactly as
@Image1, never re-lettered or warped; three real cuts, not morphs; NO god rays, NO
lens flare, NO bloom, NO blue grade; no on-screen text, no captions, no added
graphics, no extra objects entering frame, no morphing, no melting.
```

**Check the output** Scene detection confirms 3 cuts. First/middle/last frames all
show the mark intact and sharp. The object has not rotated. Blacks are black, not
grey haze. No flare arrived.

**Notes** —

---

## Slot 2 — Brand Mark / Logo Sting

**Route here when** the user wants a logo, wordmark, monogram, app icon or brand
lockup to animate; asks for a "logo animation", "brand sting", "logo reveal", or an
intro/outro bumper.

**Attach**
- `start_image` — the mark, from a vector-derived raster at delivery resolution or
  higher. An upscaled small PNG will not survive.
- `reference_images` — optional: one material or environment reference.

**Settings** `duration` 5s · `aspect_ratio` 16:9 (or the delivery aspect) ·
`resolution` 1080p · `generate_audio` off unless the sting wants a tone · deliver on
`seedance-2` — never ship a mark from a fast variant.

**Read `references/logo-and-mark-motion.md` before writing this shot.** The text lock goes in
three places and the vision QA is per-glyph.

<!-- PLACEHOLDER: replace with a verified winning prompt -->
```
Format: Brand mark sting, 5 seconds, 16:9, low-key <metallic> look, no added text.
References: @Image1 as the first frame and the brand mark — every letterform, stroke
weight, counter, kerning pair and proportion is fixed exactly as shown; do not
re-letter, re-draw, re-space, warp, skew or substitute any glyph, and do not add or
remove any character.
Consistent world: seamless charcoal-to-black void, no horizon, no floor seam; the
mark reads as <brushed metal inlaid in a dark matte surface>.
Motion split: the mark is completely locked — no deformation, no scale change, no
rotation, no perspective change. Camera locked absolutely still. Only light and
shadow move, at natural realtime speed. Nothing is speed-ramped.

SHOT 1 — DARK HOLD (0–1.5s), medium close, 85mm. The mark is barely visible in near
darkness, only the faintest edge definition catching a low source. Nothing moves.
SHOT 2 — SPECULAR SWEEP (1.5–4s), medium close, 85mm. A single hard specular
highlight travels left to right across the mark at a perfectly constant rate,
igniting each letterform in turn as it passes and leaving it softly lit behind. The
letterforms do not deform as it crosses them. Camera still locked.
SHOT 3 — SETTLE (4–5s), medium close, 85mm. The highlight clears the right edge; the
mark holds evenly lit, razor sharp, dead center, absolutely still for the final
second.

Light: one hard travelling source, otherwise near-black; NO god rays, NO light
beams, NO lens flare, NO bloom, NO blue grade.
Audio: no music; one low sustained tone resolving at 4s.
Constraints (reassert): the mark is pixel-exact to @Image1 — same letterforms, same
stroke weights, same spacing, same proportions; never re-lettered, never warped,
never substituted; camera locked throughout; light-only motion at realtime speed,
no speed ramping; no additional text, no tagline, no URL, no captions, no
watermark, no added graphics; no morphing, no letters flying or assembling.
```

**Check the output** Per-glyph vision QA on first, middle and last frames — see the
checklist in `references/logo-and-mark-motion.md`. Any glyph error is a retake, not a note.

**Notes** —

---

## Slot 3 — 3D Render / Architectural Camera Move

**Route here when** the user has a finished 3D render, CGI still, product render,
interior or exterior visualization and wants camera motion; asks to "animate this
render", "fly through this space", "make this render a video".

**Attach**
- `start_image` — the approved render.
- `reference_images` — optional: a second render angle as a destination hint, or a
  material reference.

**Settings** `duration` 8s · `aspect_ratio` 21:9 for film feel, 16:9 for standard ·
`resolution` 1080p · `generate_audio` off for architectural work.

**Geometry lock is mandatory.** Without it Seedance redesigns the scene. If the
render itself still needs producing from a 3D/CAD screenshot, route to
the `krea-generate` skill's `workflows/archviz-3d-to-render.md` first, then animate the
approved still here.

<!-- PLACEHOLDER: replace with a verified winning prompt -->
```
Format: <Architectural / CGI product> film, 8 seconds, 21:9, photoreal natural
light, no on-screen text.
References: @Image1 as the first frame — the approved render. Geometry, materials,
textures, layout and proportions are fixed exactly as shown; no elements are added,
removed, moved, resized or restyled.
Consistent world: <single daylight source through the existing opening>, neutral
white balance, the render's own palette held exactly.
Motion split: every physical element in the scene is completely static — the
structure, surfaces and objects do not move, deform or change. ALL movement belongs
to the camera. Only atmospherics move: <fine dust in the light shaft, the faintest
leaf movement beyond the glass> at natural realtime speed. Nothing is speed-ramped.

SHOT 1 — APPROACH (0–4s), wide, 24mm. One single continuous forward dolly of roughly
<1.5 meters> across the beat, dead level, at a perfectly constant rate —
architectural-camera smooth, no handheld, no bob, no roll, no tilt. Parallax reveals
the depth of the space as foreground edges pass frame. Hard cut.
SHOT 2 — MATERIAL HOLD (4–8s), medium close, 85mm. Camera locked absolutely still on
<the material detail>. A hard daylight shadow edge travels <15 centimeters> across
the surface over the beat at a constant rate. Nothing physical moves. The frame
holds still for the final half second.

Light: <single daylight source through the existing opening>; NO god rays, NO light
beams, NO lens flare, NO bloom, NO blue grade, NO added practical lights.
Audio: no music; faint room tone only.
Constraints (reassert): geometry, materials and layout fixed exactly as @Image1,
nothing added, moved or restyled; camera-only motion at a constant rate,
architecturally smooth; realtime atmospherics, no speed ramping, no slow-motion; two
real cuts, not morphs; no people appearing, no vehicles appearing, no furniture
changes; no text, no graphics, no god rays, no flare; no morphing, no re-modelling.
```

**Check the output** Compare the last frame against the source render side by side —
same geometry, same material, same layout. Straight lines stayed straight. Nothing
was invented in the background.

**Notes** —

---

## Slot 4 — Still Image → Cinematic Motion

The general-purpose animator: a photograph, illustration, painting, keyframe, or
anime/2D frame that should move without becoming a different picture.

**Route here when** the user hands over one image and says "animate this"; wants a
photo, artwork or illustration to move; wants a 2D or anime frame animated; or wants
subtle life added to a static image.

**Attach**
- `start_image` — the image.
- `reference_images` — optional: style or character identity references for 2D work.
- `end_image` instead of reference images **only** when there is a clear, close
  destination pose within story-time of the start.

**Settings** `duration` 5s (4s is the model floor; trim afterward if the useful
motion lands early) · aspect matching the source · `resolution` 1080p ·
`generate_audio` off unless ambience is wanted.

**Read the image with vision first** and list what must stay stable. Composition and
identity come from the image; the prompt supplies motion, timing and locks only.

For non-photoreal work, name the medium and cadence explicitly — see the authored
style patterns in the `krea-generate` skill's `references/models/seedance-2.md`. 2D animation
that inherits Seedance's default smooth interpolation looks like a filtered photo,
not animation.

<!-- PLACEHOLDER: replace with a verified winning prompt -->
```
Format: <Cinematic still-to-motion / hand-drawn 2D animated> shot, 5 seconds,
<aspect>, <look>, no on-screen text.
References: @Image1 as the first frame. The composition, subject identity, costume,
palette, background and framing of @Image1 are preserved exactly — nothing is
added, removed, restyled or recomposed.
Consistent world: the environment, light direction and palette of @Image1, held
unchanged for the full duration.
Motion split: <the subject holds their pose and position; only the named motions
below occur>. <Secondary motion — hair, fabric, steam, dust, foliage, water — moves
at natural realtime speed>. Camera motion is single and continuous. Nothing is
speed-ramped; no slow-motion.

SHOT 1 — <NAME> (0–5s), <shot size>, <lens>. One single continuous <push-in of
roughly 15 centimeters / lateral track of 20 centimeters / locked hold>, dead level,
at a constant rate, never accelerating. <One specific subject motion with a
consequence: eyes open and settle; the hand closes around the cup; steam rises and
dissipates; the fabric falls under its own weight and stops>. The camera stops dead
for the final half second.

Light: <the light of @Image1, unchanged — source direction and quality held>; NO god
rays, NO light beams, NO lens flare, NO bloom, NO blue grade, NO re-lighting.
Audio: <silent / room tone only / named diegetic sounds>.
Constraints (reassert): composition, identity, costume, palette and background
exactly as @Image1; one continuous camera move at a constant rate with realtime
physics, no speed ramping, no slow-motion, no floating; no new subjects, no extra
limbs, no extra characters, no costume changes, no text changes; no morphing, no
melting, no scale changes; no god rays, no flare; no on-screen text.
```

**Check the output** First and last frames both match the source's identity and
composition. No extra limbs or figures appeared. The motion is the motion you asked
for and nothing else.

**Notes** —

---

## Slot 5 — Macro Detail Reveal

Close-up exposure of craft: engraving, stitching, machining, weave, mechanism,
material grain. The shot that makes an object feel made rather than manufactured.

**Route here when** the user wants to "show the details", "zoom in on the
craftsmanship", "show the texture/material/finish", or wants macro/detail coverage
of a product or object.

**Attach**
- `start_image` — the object, ideally already framed reasonably close. A wide start
  makes the dive travel too far for the duration.
- `reference_images` — the detail itself at high resolution, so the model knows what
  it is arriving at.

**Settings** `duration` 6s · `aspect_ratio` 21:9 or 16:9 · `resolution` 1080p ·
`generate_audio` off.

The two things that make macro work: a **named destination** (not "zoom in on the
details" but a specific field of view on a specific feature) and **focus coupled to
the camera move** so you arrive sharp.

<!-- PLACEHOLDER: replace with a verified winning prompt -->
```
Format: Macro detail study, 6 seconds, 21:9, low-key cinema look, no on-screen text.
References: @Image1 as the first frame and the object — <product>; keep every
printed line and mark exactly as shown, never re-lettered. @Image2 for the detail
being revealed: <the engraved mark / the stitched seam / the machined edge>.
Consistent world: seamless charcoal-to-black void, one large soft source high
camera-left, hard falloff to true black; palette <graphite and cold steel with one
warm specular>; shallow macro depth of field throughout.
Motion split: the object is locked — no rotation, no drift, no wobble, no scale
change. All movement belongs to the camera and the focus plane. <A few dust
particles> move at natural realtime speed. Nothing is speed-ramped; no slow-motion.

SHOT 1 — DETAIL DIVE (0–4s), medium close opening to extreme macro, 100mm macro. One
single continuous push-in across the beat, traveling from the full object down to a
<3-centimeter> field of view centered on <the detail>. The focus plane travels with
the camera so <the detail> is razor sharp at the end of the move while the surround
falls entirely to bokeh. Constant rate, dead level, no rotation, no searching, no
hunting adjustments. Cut on the highlight.
SHOT 2 — SURFACE TRAVERSE (4–6s), extreme macro, 100mm macro. The camera tracks
laterally <4 centimeters> across the surface at a constant rate, dead level and
parallel to it. <Brushed grain, micro-scratches and fine dust> pass through the
shallow focus plane; the specular streak stretches along the grain as the camera
travels. The camera stops dead and holds still for the final half second.

Light: one large soft source high camera-left with a single hard travelling
specular; NO god rays, NO light beams, NO lens flare, NO bloom, NO blue grade.
Audio: no music; room tone only.
Constraints (reassert): the object is locked and never rotates or drifts; camera and
focus only, constant rate, motion-control smooth, realtime physics, no speed
ramping, no slow-motion; focus coupled to the move so the detail arrives razor
sharp; printed lines and marks exactly as @Image1, never re-lettered; two real cuts,
not morphs; NO god rays, NO lens flare, NO bloom, NO blue grade; no on-screen text,
no added graphics, no extra objects, no morphing.
```

**Check the output** The arrival frame is sharp on the intended feature, not near it.
No focus hunting mid-move. The detail is the real detail from the reference, not an
invented texture.

**Notes** —

---

## Using A Slot

1. Pick the slot; read the referenced craft file if the shot is a logo, a
   dimensional move, or a detail dive.
2. Gate the start image with vision. Fix it before generating, not after.
3. Substitute every `<bracketed>` value. Delete nothing outside the brackets.
4. Cost preflight, then block on `-fast`.
5. Judge the block: does the camera move read as deliberate? Is the subject locked?
   Did the cuts cut?
6. Re-run the same prompt on `seedance-2` for delivery, best-of-2 for hero work.
7. Vision QA first, middle and last frames. Drift is progressive; the last frame is
   where failure hides.
