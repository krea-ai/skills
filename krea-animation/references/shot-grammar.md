# Shot grammar — a scene is NOT a single clip

A 10-second scene in a movie or anime is **not** one continuous shot. It's typically 3–6 cuts: an establishing wide, a close-up on the character's face for emotional read, an insert on a hand/object, a reaction, then a final beat. One continuous 10-second take is music-video grammar; it reads as "pretty footage," not "story."

The failure mode this reference exists to prevent: planning a 60-second piece as six 10-second scenes and submitting six video jobs, one continuous clip per scene. That returns six camera moves over tableaux — no coverage, no rhythm.

## The rule

For every scene in the storyboard, write a shot-list entry that **explodes** the scene into 3–6 individual shots, each 2–3 seconds. Each shot is its own video generation job. The number of shots per scene is dictated by emotional/informational beats, not by clock time.

A useful working count for a 60s narrative is **20–30 shots total**, not 6.

## Shot vocabulary (use these names in the shot list)

| Name | Frame size | Purpose |
|---|---|---|
| EWS | extreme wide shot | establish location, dwarf the subject |
| WS | wide shot | full body + environment |
| MS | medium shot | waist up, conversation default |
| CU | close-up | face only, emotional read |
| ECU | extreme close-up | eyes, mouth, hand on hilt, single drop of sweat |
| OTS | over-the-shoulder | conversation, POV-adjacent |
| POV | point-of-view | what the character sees |
| INSERT | object close | the letter, the brush, the trigger, the bowl |
| MACRO | extreme object close | texture, single noodle, ink swirl |
| LOW | low angle (camera below eye line) | power, threat, hero entrance |
| HIGH | high angle (camera above eye line) | vulnerability, defeat, doll's-eye |
| DUTCH | tilted horizon | unease, breaking reality |
| TWO-SHOT | medium framing two subjects | relationship beat |
| RACK | rack-focus mid-shot | shift attention between fore/background |
| MATCH | match cut | shape/motion/sound carries one cut to the next |
| WHIP | whip pan | aggressive transition, same camera |

## Standard anime beat patterns (3-6 shots per ~10s scene)

### Entrance beat (5 shots)
1. WS — the door / threshold from inside
2. ECU — the doorknob turning OR the hand of the entering character
3. CU — the entering character's face seen through the gap
4. LOW WS — the character now framed in the doorway, full body
5. CU reaction — whoever is already in the room reacts

### Action beat (5 shots)
1. MS — subject sets stance
2. ECU — eyes narrow / weapon grip tightens
3. MACRO — feet pushing off ground / hilt sliding free
4. WS — the swing or leap, full body in frame
5. CU reaction — opponent or onlooker registers it

### Dialogue beat (4 shots)
1. TWO-SHOT — establish both speakers in the same frame
2. OTS over speaker A — listener (B) is the focus
3. OTS over speaker B — speaker (A) is the focus, reverse angle
4. CU — whoever has the last line, held a beat past the line

### Insert/object beat (3 shots)
1. WS or MS — subject doing the action
2. MACRO — the object itself (bowl, letter, screen, photograph)
3. CU — subject's face reading/seeing the object

### Resolution beat (4 shots)
1. CU — final small action (switch flipped, hand lowering)
2. MS — character's full body settling
3. WS — the wider environment now changed (lights off, dawn, snow)
4. EWS — pull out wide; world continues

Mix these. A 10-second SETUP scene might be: WS establish → CU character → INSERT prop → CU character react. A 10-second CLIMAX scene might be: ECU eyes → MACRO hilt → WS leap → CU opponent.

## Per-shot fields

For every shot:

- **id**: `S{scene}.{shot}` — e.g. `S3.2` is scene 3 shot 2
- **duration**: 2.0s, 2.5s, or 3.0s (anime cutting; never longer per shot unless deliberately held). Seedance's floor is 4s, so buy 4s and trim to this.
- **frame**: WS / MS / CU / etc. from the table above
- **action**: one sentence — what happens in this 2–3s, including camera move if any (push-in, dolly L→R, locked)
- **subject**: which character / object / environment
- **start_image**: which keyframe file (or "extracted from S{prev}.{prev_shot} last frame")
- **end_image**: which keyframe file (or "same as next shot start" or "none" if terminal)
- **dialogue**: verbatim line if any, in original language. Many shots have no dialogue — that's correct.
- **sfx/foley**: specific sound cue at this shot
- **continuity hook**: how this shot connects to the next — match cut (same shape / same motion / same sound) or hard cut (deliberate jolt) or J-cut (audio of next shot bleeds in over end of this one) or L-cut (audio of this shot bleeds into start of next)

## Match cuts — the anime move

The single best transition trick anime uses, and the one that distinguishes a real cut from a slapped-together concat:

- **Shape match**: end shot A on the silhouette of a brush stroke; cut to shot B on the silhouette of a dragon's spine — same curve.
- **Motion match**: end shot A on a sword swinging left-to-right; cut to shot B on a flock of cranes streaking left-to-right.
- **Sound match**: end shot A on the high taiko hit; start shot B on the *same* hit fading out.
- **Color match**: end shot A on a red glow; start shot B with the same red dominating frame.

Plan at least 2–3 match cuts per 60s narrative. They are what makes the assembled cut read as *one piece* instead of *footage stapled together*.

## Shot count budget

If a 60s narrative is 20–30 shots, price it before submission. Do not quote credit figures from this document — nothing in the toolset exposes price, so state shot count, seconds per shot, variant and resolution, and say plainly that 20–30 shots costs several times a six-clip plan. The right comparison is not "this costs more than before"; it's "the six-clip plan produced a slideshow.".

## What this is NOT

This is not coverage for live-action editing where you'd shoot every angle and decide in post. Each shot here is a deliberate, named, pre-planned generation — the cut is decided at shot-list time, not at edit time. If you can't justify why a shot is in the list before generating it, drop it.
