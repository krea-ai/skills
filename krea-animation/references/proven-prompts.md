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

The flagship request. Four hard cuts through the object at macro scale — different
face, different angle, different key on every one — then a pull to the whole thing.
The launch-film register, cut like a title sequence.

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
scale at any point. All movement belongs to the camera and the light, and every
camera move is quantified below. The object is never shown whole until SHOT 4.
Nothing is speed-ramped; no slow-motion.

SHOT 1 — MACRO EDGE (0–1.6s), extreme close-up, 100mm macro, filling the frame with
the <chamfer/seam/knurl> only — the object is unrecognisable at this scale. Camera
pushes 4 centimeters along the edge over 1.6 seconds at a constant rate. Hard key
raking from top-left at 20 degrees; everything outside the lit edge is true black.
A single hard specular runs the length of the edge as the camera travels. HARD CUT.
SHOT 2 — OPPOSITE FACE (1.6–3.2s), extreme close-up, 100mm macro, camera on the
opposite side of the object and 30 centimeters lower, looking slightly up. HARD CUT
in. Key flips to a hard source directly behind the object: the near face falls to
silhouette and only the rim ignites. Camera locked; the rim light sharpens across
the beat as the source rises. HARD CUT.
SHOT 3 — UNDERLIT DETAIL (3.2–4.6s), extreme close-up, 100mm macro on the
<mark/mechanism/junction>, camera three-quarters and low. HARD CUT in. Hard key from
below, throwing the object's shadow up and out of frame. Focus snaps from the
foreground surface to the <mark> in the first 0.3 seconds and holds. HARD CUT.
SHOT 4 — LANDING (4.6–8s), full frame, 85mm. HARD CUT to the complete object, seen
whole for the first time. The camera pulls back 20 centimeters over the first 1.5
seconds at a constant rate, then stops dead and holds absolutely still for the
remaining time — object composed on the lower third, one large soft source high
camera-left plus a rim, every edge and the <mark> razor sharp and fully legible.

Light: a different hard key per beat as specified above — top-left rake, then rear
rim, then underlit — resolving to one large soft source high camera-left plus rim on
the landing. Hard falloff to true black in every beat. NO god rays, NO light beams,
NO lens flare, NO bloom, NO blue filter; neutral white balance; blacks deep but
never crushed to noise.
Audio: no music; room tone with one soft percussive hit on each cut and a mechanical
settle at 4.6s.
Constraints (reassert): one continuous world, charcoal void, no set dressing; the
object is locked and never rotates, drifts or changes scale; every camera move is
continuous at a constant rate with realtime physics, no speed ramping, no
slow-motion, no floating; every printed line and mark exactly as @Image1, never
re-lettered or warped; four real hard cuts, not morphs or dissolves; no long static
holds before the landing, keep cutting; the whole object is not shown before SHOT 4
and appears exactly once; the sequence plays once, forward, and resolves — after the
landing the frame holds still and does not replay, loop, or return to any earlier
beat or framing; NO god rays, NO lens flare, NO bloom, NO blue grade; no on-screen
text, no captions, no added graphics, no extra objects entering frame, no morphing,
no melting; no light streaks, no shine sweeps, no glints or sparkles, no bars, stripes, bands or rectangles moving across the frame, no swipe or wipe transitions, no gradient sweeps, no bokeh particles, no scan lines, no glow pulses.
```

**Check the output** Scene detection confirms 4 cuts — if it reports fewer, the
beats were under-staged and the piece came back as a drift. First/middle/last frames
show the mark intact and sharp. The object has not rotated. No two beats share a
shot size or key direction. Blacks are black, not grey haze. No flare arrived.

**If you need more than four beats** or ~1-second staccato, generate each angle as
its own 4s clip and trim — see the beat-density section of
`references/cut-architecture.md`.

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

**Settings** `duration` 6s · `aspect_ratio` 16:9 (or the delivery aspect) ·
`resolution` 1080p · `generate_audio` off unless the sting wants a tone · deliver on
`seedance-2` — never ship a mark from a fast variant.

**Read `references/logo-and-mark-motion.md` before writing this shot.** The text lock goes in
three places and the vision QA is per-glyph.

**Pick the treatment first.** For a wordmark or any multi-element lockup, the
default is **per-element ignition** — each letterform lighting and lifting in turn —
and the full worked prompt for it lives in `references/logo-and-mark-motion.md`. The
slot below is the other strong option: a **macro cut chain**, which never asks a
letterform to move at all and so suits fragile, highly detailed or single-element
marks. Both beat a highlight drifting across a static logo, which is the one answer
to "animate this logo" you must not give.

```
Format: Brand mark sting, 6 seconds, 16:9, low-key <metallic> look, no added text.
References: @Image1 as the first frame and the brand mark — every letterform, stroke
weight, counter, kerning pair and proportion is fixed exactly as shown; do not
re-letter, re-draw, re-space, warp, skew or substitute any glyph, and do not add or
remove any character.
Consistent world: seamless charcoal-to-black void, no horizon, no floor seam; the
mark reads as <brushed metal inlaid in a dark matte surface>.
Motion split: the mark is completely locked and pixel-exact in every beat — no
deformation, no scale change, no rotation, no perspective change, no redrawing. The
camera changes position between beats and the key changes direction with it. The
complete lockup is not shown until SHOT 4. Realtime physics, nothing speed-ramped.

SHOT 1 — MACRO CORNER (0–1.4s), extreme close-up, 100mm macro filling the frame with
the outer corner of a single letterform — the mark is unreadable at this scale.
Camera locked. Hard key raking from top-left at 20 degrees picks out the machined
edge and the material grain; everything else is true black. HARD CUT.
SHOT 2 — COUNTER (1.4–2.8s), extreme close-up, 100mm macro on the enclosed counter
of a different letterform, camera 40 degrees around the mark and slightly below.
HARD CUT in. Key flips to a hard rear source: the near edge silhouettes and the
inner curve catches a thin rim. Camera locked. HARD CUT.
SHOT 3 — JUNCTION (2.8–4.2s), extreme close-up, 100mm macro on the junction where
two strokes meet, camera three-quarters and low. HARD CUT in. Hard key from below.
A single specular crosses the junction at a constant rate, showing the thickness of
the inlay. HARD CUT.
SHOT 4 — LOCKUP (4.2–6s), full frame, 85mm. HARD CUT to the complete mark, seen
whole for the first time, dead center. The camera pulls back 15 centimeters over the
first second at a constant rate then stops dead and holds absolutely still, the mark
evenly lit by one soft top key plus rim, every letterform razor sharp and legible.

Light: a different hard key per beat as specified — top-left rake, rear rim, then
underlit — resolving to soft top key plus rim on the lockup. NO god rays, NO light
beams, NO lens flare, NO bloom, NO blue grade.
Audio: no music; one soft tick per cut and a low tone resolving at 4.2s.
Constraints (reassert): the mark is pixel-exact to @Image1 — same letterforms, same
stroke weights, same spacing, same proportions; never re-lettered, never warped,
never redrawn, never substituted; the mark itself never moves, scales or rotates in
any beat — only the camera position and the key direction change; four real hard
cuts, not morphs or dissolves; no long static holds before the lockup, keep cutting;
the complete mark appears exactly once, on SHOT 4; the sequence plays once, forward,
and resolves — after the lockup the frame holds still and does not replay, loop, or
return to any earlier beat or framing; realtime physics, no speed ramping; no additional text, no tagline, no URL, no
captions, no watermark, no added graphics; no morphing, no letters flying or
assembling; no light streaks, no shine sweeps, no glints or sparkles, no bars, stripes, bands or rectangles moving across the frame, no swipe or wipe transitions, no gradient sweeps, no bokeh particles, no scan lines, no glow pulses.
```

**Check the output** Scene detection confirms 4 cuts. Per-glyph vision QA on the last
frame of every beat, not just the final frame — see the checklist in
`references/logo-and-mark-motion.md`. Any glyph error is a retake, not a note.

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
