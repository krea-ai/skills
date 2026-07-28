# Reveal Recipes — Named Effects And How To Get Them

A cookbook of the reveal and transition effects users actually ask for, each stated
as: what it is, the prompt language that produces it, what to attach, and how it
fails. Copy the **Write** block into the relevant SHOT line of the prompt
architecture and adapt the nouns.

Before hand-writing any of these, check whether the Krea effects library already
carries the look — see `seedance-effects.md`. A library effect brings a reference
asset and a tuned prompt template, which beats reinventing it.

Every recipe assumes the surrounding blocks from
`seedance-prompt-architecture.md` are present: format, references, world, motion
split, light, audio, constraints.

---

## Group 1 — Light And Shadow Reveals

### 1. Shadow Retreat

The single most elegant reveal available. The object never moves; darkness
uncovers it.

**Write**
```
SHOT 1 — SHADOW RETREAT (0–4s), medium close, 85mm. Camera locked absolutely
still. The object begins entirely inside a hard-edged shadow, only its silhouette
readable. Over 4 seconds the shadow edge travels left-to-right across its face at
a constant rate, never accelerating, uncovering the surface, then the chamfer,
and the engraved mark last. The object is locked — no rotation, no drift.
Realtime physics.
```

**Attach** `start_image` = the object already in shadow, or a fully lit still plus
the shadow described in prose (Seedance will build the shadow).

**Fails when** the shadow edge is described as "soft" and "slow" — it becomes a
global brightness ramp instead of a travelling edge. Say **hard-edged** and give it
a direction and a rate.

---

### 2. Silhouette Bloom

Drama from nothing. Pure black shape against a dim ground, then light arrives from
behind, rims it, and finally fills the front.

**Write**
```
SHOT 1 — SILHOUETTE BLOOM (0–3s), wide, 50mm. Camera locked. The object reads as
a pure black silhouette against a charcoal ground, no front detail at all. A
source rises behind it over 2 seconds until a hard bright rim describes its entire
outline. At 2.5s a soft front source lifts just enough for the surface material to
resolve — never fully lit, the far side stays black.
```

**Fails when** the frame goes fully lit too early. Add: `the far side of the object
remains in true black for the entire shot`.

---

### 3. Travelling Specular

The camera holds; only a highlight moves. Maximum sophistication, minimum motion.

**Write**
```
SHOT 1 — SPECULAR TRAVEL (0–5s), macro, 100mm. Camera locked. A single hard
specular highlight travels left to right along the top chamfer at a constant rate,
crossing the engraved mark at 3s and igniting it briefly before continuing off the
right edge. Nothing else in frame changes. The object is locked.
```

**Fails when** you don't say the camera is locked — Seedance adds a drift and the
highlight travel gets lost inside it.

---

### 4. Slat / Louvre Crawl

Chiaroscuro drama with an in-world excuse for the light.

**Write**
```
SHOT 1 — SLAT CRAWL (0–3.5s), medium, 85mm. Camera locked. Hard-edged horizontal
blind shadows stripe the object and the wall behind it. Over 3.5s the entire slat
pattern crawls 20 centimeters to the right as the unseen source moves, sweeping
bright bands across the object's face and clearing the mark. The object does not
move.
```

**Fails when** the slats shimmer or reflow — add `the slat pattern holds its shape
exactly; it translates, it does not deform`.

---

### 5. Light-Wipe Transition

A beat-to-beat transition that reads as designed rather than as an edit accident.

**Write**
```
...end of SHOT 2: a hard bright band sweeps across frame left to right and blows
the frame to near-white for four frames — light-wipe cut into SHOT 3, which begins
already in its new framing. Not a dissolve, not a fade.
```

**Fails when** it becomes a bloom-and-return on the same shot. Specify that the
next beat begins in a *different framing* and name it a cut.

---

### 6. Shadow Wipe Transition

The quiet version of the light wipe, and the more elegant one.

**Write**
```
...end of SHOT 1: a shadow sweeps across frame and fills it to true black for
three frames; SHOT 2 emerges out of that same darkness in a new framing —
shadow wipe, a real cut, not a dissolve.
```

---

## Group 2 — Focus And Optical Reveals

### 7. Blur-In Reveal

The most reliable premium opener in existence: the frame resolves out of nothing.

**Write**
```
SHOT 1 — BLUR-IN (0–3s), macro, 100mm. Camera locked. The frame opens as complete
soft bokeh — no readable form, only warm and dark masses. Over 3 seconds the focus
plane travels until the object resolves into razor-sharp detail, the engraved mark
last to arrive. Focus travels at a constant rate. Nothing in frame moves.
```

**Attach** `start_image` can be the sharp final frame — describe the blur as the
*starting* state in prose and Seedance will open soft and resolve.

**Fails when** it resolves in the first half second and then sits. Add `the focus
travel is spread evenly across the full 3 seconds`.

---

### 8. Rack-Focus Handoff

Attention moves without a cut. Two subjects, one continuous frame.

**Write**
```
SHOT 2 — FOCUS HANDOFF (2.5–5s), medium close, 85mm. Camera locked. Focus opens on
the foreground edge, razor sharp, with the object behind it completely soft. Over
2.5 seconds the focus plane travels backward; the foreground edge falls to bokeh
exactly as the object's mark becomes sharp. One continuous move, no cut.
```

---

### 9. Reflection Reveal

The object appears first as a reflection, then in itself. Sophisticated misdirection.

**Write**
```
SHOT 1 — REFLECTION FIRST (0–3s), macro, 100mm. Camera locked on a polished black
surface; the object is visible only as an upside-down mirror reflection in it.
At 2s the camera begins a single continuous tilt upward, 20 degrees over 1 second,
lifting off the reflection and arriving on the object itself, sharp and composed.
```

**Fails when** the reflection and the real object appear simultaneously. Add `the
object itself is out of frame entirely until the tilt begins`.

---

### 10. Caustic Crawl

Glass, liquid and gem work. Light bent through the subject paints the surface below.

**Write**
```
SHOT 1 — CAUSTIC CRAWL (0–4s), macro, 100mm. Camera locked. A hard source behind
the glass throws a bright caustic pattern onto the surface below. Over 4 seconds
the caustic travels 10 centimeters across the surface as the source moves, its
edges sharpening as it crosses. Realtime physics. The glass is locked.
```

---

## Group 3 — Camera-Driven Reveals

### 11. Glacial Push-In

The workhorse. Quantify it or it will be too fast.

**Write**
```
SHOT 1 — PUSH (0–6s), medium close to close, 85mm. One single continuous push-in
traveling roughly 20 centimeters across the full 6 seconds, dead level, on a
motion-control rig — mechanically smooth, never accelerating, never stopping. The
object is locked and does not rotate. Everything in frame moves at natural
realtime speed; no speed ramping, no slow-motion.
```

---

### 12. Slow Pull-Reveal (Context Arrives)

The reverse: start intimate, pull back to disclose where you were.

**Write**
```
SHOT 1 — PULL (0–6s), extreme macro opening to wide, 50mm. One continuous pull
back across the full 6 seconds. We open on an abstract lit edge with no readable
context; as the camera retreats the full object assembles in frame, then the
void around it, ending on a composed wide with the object on the lower third.
The camera stops dead for the final half second.
```

**Fails when** the pull accelerates at the end and overshoots. Add `constant rate
throughout; the final framing is held still, not arrived at in motion`.

---

### 13. Crane Down To Level

A vertical move that changes the object's status from viewed to met.

**Write**
```
SHOT 1 — CRANE DOWN (0–5s), wide to medium, 35mm. The camera begins high, looking
down at 40 degrees, and descends in one continuous crane move to dead level with
the object across 5 seconds, arriving at eye height. Constant rate, no pan, no
roll. The object is locked.
```

---

### 14. Low-Angle Hero Rise

Makes an object monumental. Wide lens, low camera, upward move.

**Write**
```
SHOT 1 — HERO RISE (0–4s), low wide, 24mm, camera 15 centimeters off the ground
looking up. One continuous rise of 25 centimeters across 4 seconds, the object
looming above the lens, its top edge cutting into a black field. No tilt, no roll,
no pan. Realtime physics.
```

---

### 15. Dolly-Zoom (Vertigo)

Use rarely and deliberately. It is a statement, not a texture.

**Write**
```
SHOT 3 — VERTIGO (5–7s), medium, focal length pulling from 85mm to 35mm while the
camera pushes in — the object holds exactly the same size in frame while the
background void expands behind it. One continuous move across 2 seconds.
```

---

### 16. Whip-Pan Accent Cut

The fast beat that makes the slow beats read as intentional.

**Write**
```
...end of SHOT 3: a hard whip-pan right, heavy horizontal motion blur for four
frames — whip-pan cut into SHOT 4, which lands already settled in its new framing
with no residual movement.
```

---

## Group 4 — Object And Matter Events

### 17. Precision Settle

An object arrives and stops dead. Reads as engineered; the opposite of floaty.

**Write**
```
SHOT 2 — SETTLE (2.5–4.5s), medium close, 85mm. The lid descends 4 centimeters in
one single motion at realtime speed and seats with a precise stop — no bounce, no
overshoot, no secondary wobble. Camera locked. One soft mechanical click at the
moment of contact.
```

**Fails when** the object floats down. The fix is explicit: `at realtime speed
under normal gravity; it does not float`.

---

### 18. Unfold / Assemble

Components arrive into place. Cousin of the exploded view in
`dimensional-motion.md`.

**Write**
```
SHOT 2 — ASSEMBLE (2.5–5s), medium, 50mm. Camera locked. Three components travel
inward from just outside frame along straight paths and seat into the body in
sequence — first the base at 3s, then the collar at 4s, then the cap at 4.8s —
each stopping dead on contact with no bounce. Realtime physics, mechanically
precise. Each part keeps its exact shape and scale; no morphing, no melting.
```

---

### 19. Liquid Form

Pour, fill, meniscus. Physical honesty is what sells it.

**Write**
```
SHOT 3 — POUR (5–8s), macro, 100mm. Camera locked. A clean stream enters from the
top of frame and fills the vessel across 3 seconds at realtime speed. Surface
tension holds at the meniscus, one bright caustic forms on the surface beneath,
and the level rises at a constant rate. No splashing beyond two small droplets.
No slow-motion.
```

---

### 20. Dust Disturbance

A tiny consequence that makes a locked frame feel physically real.

**Write**
```
...as the object seats, a fine ring of dust lifts 2 centimeters off the surface
and settles again within one second, catching the rim light. Realtime speed,
minimal — a few dozen particles, not a cloud.
```

---

### 21. Fabric Fall

Reveal by removing a covering. Classic, and dependent on weight reading correctly.

**Write**
```
SHOT 1 — DROP (0–3s), medium, 50mm. Camera locked. A dark cloth covering the
object slides off downward under its own weight in one continuous motion at
realtime speed, clearing frame at 2s and revealing the object already lit and
composed. The cloth has weight — it falls, it does not float or billow.
```

---

## Group 5 — Frame-Level Grammar

### 22. Match Cut On A Curve

The move that makes an assembled sequence read as one piece.

**Write**
```
...SHOT 2 ends on the object's chamfer arcing from lower-left to upper-right.
Match cut on the same curve into SHOT 3, which opens on the identical arc
described by a different element in a new framing — same line, same screen
position, same direction of travel.
```

---

### 23. Cut On The Highlight

A cut so smooth it barely registers as one.

**Write**
```
...SHOT 1 ends the instant the travelling specular reaches the right edge of the
mark. Hard cut into SHOT 2, which opens with a specular already at the left edge
of the new framing, travelling in the same direction.
```

---

### 24. Held Landing / End Card

How elegant sequences finish.

**Write**
```
SHOT 4 — LANDING (6–8s), medium, 85mm. The camera arrives and stops dead. The
object sits composed on the lower third, fully lit for the first time in the
piece, mark razor sharp. The frame holds absolutely still for the final second.
No text, no logo overlay, no fade — a held image.
```

---

## Recipe Selection Table

| User says | Reach for |
|---|---|
| "reveal it dramatically" | 1 Shadow Retreat, 2 Silhouette Bloom |
| "make it look premium / expensive" | 11 Glacial Push-In + 3 Travelling Specular |
| "have it emerge from darkness" | 2 Silhouette Bloom, 6 Shadow Wipe |
| "start blurry then sharp" | 7 Blur-In Reveal |
| "focus on the details" | 8 Rack-Focus Handoff, 3 Travelling Specular, macro dive in `dimensional-motion.md` |
| "show the whole thing at the end" | 12 Slow Pull-Reveal, 24 Held Landing |
| "make it feel monumental" | 14 Low-Angle Hero Rise, 13 Crane Down |
| "unbox / open it" | 17 Precision Settle, 21 Fabric Fall |
| "show how it's made / what's inside" | 18 Unfold, exploded view in `dimensional-motion.md` |
| "punchy, high energy" | 16 Whip-Pan Accent, 15 Dolly-Zoom, tighter beats |
| "moody, cinematic, film-like" | 4 Slat Crawl, 2 Silhouette Bloom, 21:9 aspect |
| "the logo should animate" | `logo-and-mark-motion.md` |
| "make it float / spin in the air" | `dimensional-motion.md` |

## Combining Recipes

Two or three per generation, maximum, and never two camera moves in one beat. A
proven three-beat elegant structure:

1. **Blur-In** or **Silhouette Bloom** — arrival out of nothing (0–3s)
2. **Travelling Specular** or **Shadow Retreat** — the information beat (3–5.5s)
3. **Held Landing** after a **Glacial Push-In** — resolution (5.5–8s)

Joined by a **Shadow Wipe** and a **Cut On The Highlight**. That is a complete,
elegant, eight-second reveal built from four named recipes and nothing else.
