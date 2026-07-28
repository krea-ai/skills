# Reveal Sequence

## Trigger

Use for a **multi-beat cinematic reveal film**: a product launch film, a brand
reveal, a hardware or hero-object piece, an architectural film, a CGI showcase — 8 to
30 seconds of elegant, deliberate, textless motion where one subject is disclosed
across several beats.

Not this workflow:

- one shot only → `workflows/cinematic-shot.md`
- a paid social ad, UGC, or performance creative → the `krea-marketing` skill (the ad
  framing, hooks, captions and formats live there)
- narrative animation with characters and story → `workflows/series-from-scratch.md`
- designed typography, kinetic type, end cards → generate textless footage here,
  compose type in post per the `krea-marketing` skill's `workflows/launch-teaser.md`

## Two Construction Paths — Choose Deliberately

### Path A — One Generation, Multi-Beat

One Seedance job carrying 3 or 4 fully staged beats with real cuts inside it.

**Choose when** total runtime is ≤ 15s, all beats live in one world, and no beat
needs a guaranteed exact frame.

**Advantages** the world, light and grade are automatically consistent; the cuts are
free; one job, one cost, one QA pass.

**Constraints** Seedance commits to about **three strongly distinct beats** on its
own. Four land only when every beat is fully staged and no beat runs long. Cap beats
at ~2.5s and put `no long static holds, keep cutting` in the constraints tail.

### Path B — Chained Shots, Assembled

Several separate Seedance jobs, each one shot, normalized and concatenated locally.

**Choose when** runtime exceeds 15s, beats live in different worlds or lighting
states, a specific shot needs its own start/end frames, or individual shots need
independent retakes without regenerating the piece.

**Advantages** surgical retakes; no beat budget; per-shot best-of-N.

**Costs** you own continuity — world, light, grade and scale must be enforced by
prompt discipline across jobs, plus a normalize-and-assemble pass.

**Default: try Path A first** for anything ≤ 15s. It is cheaper, faster, and its
consistency is hard to match by hand. Fall back to Path B when a beat fails
repeatedly or the runtime demands it.

## Recipe

### 1. Lock the subject still

Everything downstream inherits it. Read the source with vision. The start image is
the quality ceiling for the entire film — a soft mark or a bad crop poisons every
beat. Fix it before planning beats.

### 2. Write the beat sheet before any prompt

A reveal has a shape, not a list. Use the tempo grammar from
`references/cinematic-craft.md`:

| Beat | Length | Job |
|---|---|---|
| 1 — Held opener | 2.5–3s | Darkness, scale, near-stillness. Earns the rest. |
| 2 — First information | 2–2.5s | One fact: a detail, an angle, a material. |
| 3 — Second information | 2–2.5s | A different fact. Often the mechanism or the mark. |
| 4 — Accent (optional) | 1–1.5s | The fast one. Contrast makes the slow beats read as deliberate. |
| 5 — Landing | 2–3s | Composed, still, fully lit, resolved. |

For each beat write: shot size, lens, the one camera move, the one physical event,
and the named transition out. Pull the moves from
`references/reveal-recipes.md` and `references/dimensional-motion.md`.

**Show the beat sheet to the user before generating.** It is cheap to change here
and expensive to change after.

### 3. Resolve Seedance

Per `references/seedance-routing.md`: MCP check → list models → get schema →
fetch the prompting guide.

### 4. Cost preflight

Price the run before submitting. Show: path A or B, beat count, seconds, blocking runs
on `-fast`, delivery runs on `seedance-2`, best-of-N for the hero beat, and the retry
budget. Wait for the go-ahead.

### 5. Write the prompt(s)

All nine blocks, per `references/seedance-prompt-architecture.md`.

Path A specifics:

- one world block governing every beat
- each beat: time range + shot size + lens + one move + one event + named transition
- no beat over ~2.5s; no long final hold
- `no long static holds, keep cutting` in the constraints tail
- one motion split covering the whole piece

Path B specifics — restate in **every** job:

- the same world block, verbatim
- the same light block, verbatim
- the same grade and lens family
- the same subject lock
- the same negatives

Verbatim repetition across jobs is what makes separate generations cut together.

### 6. Block cheap, judge, then commit

Generate the whole piece on `seedance-2-fast` first — the full Path A prompt, or the
two most load-bearing shots of Path B. Judge:

- Do the beats read as distinct, or did the back half coast on one lazy move?
- Did the cuts cut? Prove it:

```bash
ffmpeg -i sequence-raw.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```

An empty list on a multi-beat prompt means the cuts morphed. Fix by fully staging
each beat, not by shouting HARD CUT.

- Contact sheet across the full duration:

```bash
ffmpeg -i sequence-raw.mp4 -vf "fps=2,scale=320:-1,tile=6x5" -frames:v 1 contact.png
```

Read it with vision. Check: one world throughout, subject locked, marks intact in the
**last** frames, no flare, no drift into blue.

### 7. Retake per beat

One change per retake. Path A: adjust the one failing beat's staging and re-run with
the seed pinned. Path B: regenerate the single failing shot and leave the rest locked.

If a Path A beat fails three times, lift it out and produce it as a Path B shot,
then assemble.

### 8. Deliver

Re-run the approved prompt on `bytedance/seedance-2`, best-of-2 for the hero beat.
Upscale if the live schema exposes it and delivery needs it.

Path B assembly — normalize before concatenating or the cut will hitch. Commands in
`references/edit-qa-retakes.md`.

Strip per-clip generated audio unless the plan keeps it, and lay one designed bed
under the whole piece.

### 9. Final QA before handoff

- [ ] One world, one light logic, one grade across every beat
- [ ] Subject never rotates, drifts or changes scale unless a beat named it
- [ ] Realtime physics — nothing came back speed-ramped
- [ ] Every mark and printed line intact in every last frame
- [ ] Cuts verified by scene detection, not by eye
- [ ] No god rays, flare, bloom or blue cast anywhere
- [ ] No on-screen text, captions or invented graphics
- [ ] The film **lands** — the final frame is composed and still, not drifting

## Banned

- Do not plan a reveal as one long continuous camera move over 15 seconds. That is a
  screensaver, not a film.
- Do not end a multi-beat prompt with a long hold — the model front-loads and coasts.
- Do not let beat 3 relocate to a different world.
- Do not vary the world or light wording between Path B jobs.
- Do not burn captions or type into these deliverables; the format reads cheap with
  them and clean typography belongs in post.
- Do not call scene detection optional. Eyeballing cuts is how morphs ship.
- Do not name a brand as an imitation target. Describe the look in craft terms.
