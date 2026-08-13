# Cut Architecture — Maximal Cinema In Eight Seconds

The default answer to "animate this" is a staged cut sequence: four beats, each at a
different scale, angle and lighting state, ending on the first and only full view of
the subject. One continuous move across the whole duration is the failure this file
prevents — it is what the model returns when the prompt did not commit to anything.

## The Standard Build

| Beat | Length | Size | What it does |
|---|---|---|---|
| 1 | 1–1.8s | ECU / macro | A detail nobody looks at: a chamfer, a weave, one letter's edge. Hard raking key. |
| 2 | 1–1.8s | ECU, different axis | Second detail, camera on another side. Key flips direction. |
| 3 | 1–1.5s | CU, angled | Third detail, hardest light of the piece — top-left rake or underlit. |
| 4 | 2–2.5s | Full frame, locked | The whole subject, fully lit, composed, dead still. The payoff. |

Every beat needs a time range, shot size, lens, one camera move, one physical event,
and a named transition out. A beat missing any of the six renders as a dissolve.

## The Four Rules

1. **Change scale and angle together.** Jump at least a full size class (ECU → MS,
   not ECU → CU) *and* move the camera to a different side or height. Two adjacent
   beats at the same size read as one shot with a hiccup, whatever the transition says.
2. **Relight every beat.** Name the direction each time — top-left rake at 20°, then
   rear rim with the front face in shadow, then underlit, then broad key on the
   landing. This is the cheapest way to make four cuts read as four shots.
3. **One physical event per beat.** A new angle where nothing happens is dead air: a
   specular crossing an engraving, dust lifting, focus snapping to the mark.
4. **The payoff appears once, at the end.** Never open on the whole subject, and
   never cut back to a detail after revealing it — that reads as a loop and invites
   the model to actually loop. The one exception is a web product loop, which
   alternates on purpose and is *supposed* to loop — `../references/product-beauty-macro.md`.

## Recurring Structures

| Structure | Use for | Shape |
|---|---|---|
| Staccato detail chain | Products, hardware, packaging, anything with material worth showing | Three macro beats, different surface and key each, then a pull to the whole |
| Blur-out reveal | Marks, single objects, when one move is genuinely wanted | One continuous pull from macro to full frame while focus resolves left to right, subject snapping sharp exactly as it becomes whole |
| Angle slam | Sculptural objects, bottles, hardware | Three ~1s beats, same size, three camera positions around the subject, no movement inside any beat, then a pull out |
| Sequential ignition | Wordmarks, keyboards, modular assemblies | Elements light or lift in turn, then the whole holds — see `../references/logo-and-mark-motion.md` |

The blur-out reveal in prompt terms:

```
Motion split: the object is locked. The camera pulls back 40cm over 6 seconds at a
constant rate while the focus plane travels from 5cm in front of the object to the
object's face; the left third resolves first, sharpness sweeping right across the
frame at a constant rate, the whole object razor sharp and fully composed at 6s.
```

## Beat Density Versus What The Model Delivers

Seedance commits to roughly **three to four strongly distinct beats per generation**.
A fifth usually merges into the fourth.

- **Four fully staged beats is the reliable maximum.** Put `no long static holds,
  keep cutting` in the constraints tail.
- **The payoff appears once.** Reveal the whole subject on the final beat and stop.
  Cutting back to a detail after the reveal and then showing the whole thing again
  reads as a loop, and it invites the model to actually loop.
- **The single-move exception.** One continuous 6–8s move is legitimate for an
  architectural interior, a landscape, or a brand that has explicitly asked for
  restraint. Name it out loud as a choice. For objects, products and marks the
  default is the cut sequence.
- **Buy only the seconds you have staged.** Unstaged time gets filled with a replay
  of an earlier beat, usually degraded. Three beats is a 4–5s clip, not a 6s one.
- **For five or more beats, or true ~1s staccato**, stop fighting one generation. The
  duration floor is 4s, so generate each angle as its own clip and trim it to the
  1–1.5s core, then assemble per `../references/edit-qa-retakes.md`.

```bash
ffmpeg -y -ss 1.2 -i beat-01-raw.mp4 -t 1.2 -c:v libx264 -pix_fmt yuv420p -an beat-01.mp4
```

Pick the trim window from a contact sheet — the usable second is rarely the first,
because the model spends the opening frames settling.

## Verify

A maximal piece that came back as one drift, or that resolved early and replayed, is
invisible if you only watch it once and sampled frames will not catch it. Contact
sheet plus scene detection, every time — see step 8 of `../workflows/cinematic-shot.md`.

## What Maximal Is Not

Not shaky, not whip-panning between beats, not speed-ramped: the beats are short but
the motion inside each is quantified and realtime. Not busy frames — each beat is
still mostly darkness with one lit subject, because the density lives in the cutting.
Not random: macro → macro → macro → whole, or an equally deliberate order. And not an
excuse to skip the locks, since fast cutting makes identity drift more likely, not less.
