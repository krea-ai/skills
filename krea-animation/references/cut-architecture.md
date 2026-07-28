# Cut Architecture — Maximal Cinema In Eight Seconds

The default answer to "animate this" is **not** one move. It is a staged cut
sequence: four or more beats, each at a different scale, angle and lighting state,
ending on the first full view of the subject.

A single continuous move across the whole duration — a drift, a pan, a highlight
travelling over a static frame — is the failure mode this file exists to prevent.
It is the shot the model gives you when the prompt did not ask for anything.

## The Standard Eight-Second Build

Five beats. Macro in, whole subject out.

| Beat | Length | Size | What it does |
|---|---|---|---|
| 1 | 1.2–1.8s | ECU / macro | A detail nobody looks at: a chamfer, a weave, one letter's edge. Hard raking key. |
| 2 | 1.2–1.8s | ECU from a different axis | A second detail, camera moved to another side. Key flips direction. |
| 3 | 1–1.5s | CU, angled | Third detail with the most aggressive light of the piece — hard top-left rake, or underlit. |
| 4 | 1–1.5s | MS, pulling | The pull begins. Subject readable but not yet whole. |
| 5 | 2–2.5s | Full frame, locked | The whole subject, fully lit, composed, dead still. The payoff. |

Each beat gets its own line in the SHOTS block with a time range, a shot size, a
lens, one camera move, one physical event, and a named transition out. A beat
without all six renders as a dissolve.

## The Three Rules That Make Cuts Read

### 1. Change scale AND angle on every cut

Two adjacent beats at the same size read as one continuous shot with a hiccup,
whatever the transition says. Jump at least one full size class (ECU → MS, not
ECU → CU) *and* move the camera to a different side or height.

```
SHOT 2 — EDGE (1.4–2.8s), extreme close-up, 100mm macro, camera on the opposite
side of the object from SHOT 1 and 30cm lower. HARD CUT in.
```

### 2. Relight every beat

The cheapest way to make four beats read as four shots instead of one is to move
the key. Name the direction every time.

- Beat 1: hard key raking from top-left at 20°, everything else black
- Beat 2: rim only, source directly behind the subject, front face in shadow
- Beat 3: underlit, hard source below the object throwing shadow up the back wall
- Beat 4: broad soft top light as the pull begins
- Beat 5: full key plus rim, subject completely legible

### 3. Give every beat one physical event

A cut to a new angle where nothing happens is still dead air. Each beat needs one
thing to occur inside it: a specular crossing an engraving, dust lifting, a
reflection sweeping, focus snapping from foreground to the mark, a shadow clearing.

## Recurring Structures

### Staccato detail chain

Four to five macro beats around one object, each ~1.2s, each a different surface
and light direction, then a pull to the whole. The default for products, hardware,
packaging, and anything with material worth showing.

### Blur-out reveal

The whole piece is one continuous pull from macro to full frame, but the *focus*
carries the reveal: the frame opens as unreadable bokeh and resolves left to right
as the camera pulls, the subject snapping sharp exactly as it becomes whole. One
move, but it is not a drift — the frame changes completely from first to last.

```
Motion split: the object is locked. The camera pulls back 40cm over 6 seconds at a
constant rate while the focus plane travels from 5cm in front of the object to the
object's face; the left third resolves first, sharpness sweeping right across the
frame at a constant rate, the whole object razor sharp and fully composed at 6s.
```

### Angle slam

Three beats, ~1s each, same shot size, three completely different camera positions
around the subject — front, hard side, low three-quarter — each with its own key,
cut hard, no camera movement inside any beat. Then a fourth beat that pulls out.
Reads as expensive because the cuts do all the work.

### Sequential element ignition

For subjects made of parts — letterforms, keys, modules, buttons. Each element
lights, lifts or resolves in turn, then the whole assembly holds. See
`references/logo-and-mark-motion.md` for the version that survives text.

## Beat Density Versus What The Model Will Actually Do

Seedance commits to roughly **three to four strongly distinct beats per
generation**. Ask for five and the fifth usually merges into the fourth.

So:

- **4 beats in one 8s generation** is the reliable maximum. Stage every one fully
  and put `no long static holds, keep cutting` in the constraints tail.
- **For 5+ beats, or for true ~1s staccato**, do not fight one generation. The
  duration floor is 4s, so generate each angle as its own 4s clip and trim it to
  the 1–1.5s core you want, then assemble. Trimming is free and exact.

```bash
# Trim each generated clip to its usable core, then concatenate.
ffmpeg -y -ss 1.2 -i beat-01-raw.mp4 -t 1.2 -c:v libx264 -pix_fmt yuv420p -an beat-01.mp4
printf "file '%s'\n" beat-*.mp4 > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy sequence.mp4
```

Pick the trim window by eye from a contact sheet — the usable second is rarely the
first second, because the model spends the opening frames settling.

## Verify The Cuts Landed

A maximal piece that came back as one drifting shot is the single most common
failure here, and it is invisible if you only watch it once. Prove it:

```bash
ffmpeg -i sequence-raw.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```

Fewer detected cuts than staged beats means the beats were under-staged. Fix by
giving each beat a distinct size, angle, key and event — not by writing HARD CUT
in capitals again.

## What Maximal Is Not

- Not shaky, not whip-panning between every beat, not speed-ramped. The beats are
  short; the motion inside each beat is still quantified and realtime.
- Not busy frames. Each individual beat is still mostly darkness with one lit
  subject — the density is in the *cutting*, not in the clutter.
- Not random. The order is macro → macro → macro → pull → whole, or an equally
  deliberate structure. A shuffled set of angles reads as a contact sheet.
- Not an excuse to skip the locks. Fast cutting makes identity drift *more* likely,
  so the subject lock and text lock matter more here, not less.
