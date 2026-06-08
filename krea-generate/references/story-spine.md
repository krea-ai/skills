# Story spine — the gate before the storyboard

A logline is not a story. "A swordswoman fights an ink-dragon" is a logline. The story is what the character *wants*, what's in their *way*, what they *do*, what *turns*, and how the world is *different at the end*. If those five things aren't written down before any keyframe is composed, you will produce 60 seconds of pretty footage that the viewer cannot follow.

This reference exists because the 2026-05-21 Inkfall delivery had a logline, a 6-scene storyboard, and 24 fps of polished animation — and the user's verdict was "the story makes no sense." That outcome was structural, not a render quality issue.

## The spine (write all five before storyboarding)

In `CONCEPT.md`, add a `## Story spine` section with exactly these fields. One sentence each. If you can't write a sentence, you don't have a story.

1. **PROTAGONIST** — name + one defining trait. Not a description; a trait that the story will *test*. ("Mira, an apprentice who's never struck a real blow.")
2. **WANT** — what does the protagonist actively want *in this 60 seconds*? It must be concrete and visible. Not "happiness" — "deliver this letter," "finish the brushstroke," "serve one last bowl perfectly." ("Mira wants to protect her master.")
3. **OBSTACLE** — what specifically blocks them? Concrete antagonist or condition. ("The ink-dragon is faster and her only weapon is paper.")
4. **STAKES** — what does the protagonist lose if they fail? Must be visible/personal, not abstract. ("If she fails, her master dies and the temple burns.")
5. **TURN** — the decisive choice or revelation around the midpoint that flips the trajectory. Not the climax — the *reason* the climax becomes possible. ("She realizes the cranes aren't a weapon — they're her brush, and her brush is what answers the ink.")
6. **NEW NORMAL** — how is the world different at the end vs. the start? One concrete visible thing. ("The scroll is whole again, but with one extra crane painted in its corner — her signature.")

## Why all six matter (the 60-second test)

Cover one of these and discard it and watch what breaks:

- Drop **WANT**: the protagonist becomes reactive. Every shot is them responding to spectacle. Viewer disengages by 15s.
- Drop **OBSTACLE**: no tension. The climax has no weight because there was no risk.
- Drop **STAKES**: even with conflict, viewer doesn't care. "Cool fight" with no emotional read.
- Drop **TURN**: the climax is just *more of the same*. Final shot has no payoff because nothing flipped.
- Drop **NEW NORMAL**: the ending feels arbitrary — why end *here* and not anywhere else?

## Dialogue is part of the spine

Most narrative skill failures so far have been silent films — the workflow generated `STORYBOARD.md` with an empty dialogue field for every scene. That's a default, not a choice. If you choose silent, justify it in `CONCEPT.md` under a `## Dialogue posture` line ("This piece is silent because the protagonist literally cannot speak — the bell-tones carry her voice").

Otherwise, write the dialogue *first*, before the keyframes. Two reasons:

1. The dialogue often dictates camera grammar — a two-shot vs. shot/reverse-shot, OTS vs. profile, when to cut to listener.
2. Dialogue length determines shot duration. "Just once more, Nana" is ~1.5s of audio; the shot holding it needs to be ~2s with breathing room before/after. Storyboarding scene durations *without* writing the lines first produces shots that are either too short to fit the line or too long and dead.

Write each line verbatim in the original language. Translate only if the user needs subtitles.

## The "logline only" trap

If the user gave you only a logline ("anime about a samurai apprentice"), do NOT proceed to storyboard. Run the concept development step in `../../krea-animation/workflows/series-from-scratch.md` first — propose 3 distinct concepts and let the user pick. Each pitch should already imply a spine in one sentence: *"Mira (apprentice who's never struck) wants to protect her dying master from an ink-dragon she accidentally summoned (obstacle she caused herself raises stakes); the cranes aren't her weapon, they're her signature (turn from soldier to artist); she signs the scroll instead of striking (new normal)."* That sentence is more useful than ten descriptive paragraphs.

## The taste gate (write this last, before storyboarding)

After writing the spine, write one sentence answering: **"What does the audience *feel* in the last 5 seconds?"** Specific feeling, not "moved." Examples:

- "Tired warmth — like the smell of dinner after a long walk home."
- "Quiet pride at recognizing a small private gesture (the painted crane in the corner)."
- "Held breath releasing — relief that the world is bigger than the threat."

If you can't write that sentence, your story doesn't have a destination yet. Don't render keyframes against a story that doesn't know where it's going.

## Approval gate

The user approves the **spine** (six fields + dialogue posture + final-five-seconds feeling) **before** the storyboard is written. This is the single cheapest course-correction point in the pipeline. Once shots are listed and stills are composed, the structural decision is already locked in pixels.

If the user says "looks fine, proceed," push once: "Quick check — what's the protagonist's *want*? Confirming we both see the same story." If they can articulate it back, proceed. If they say "I don't know, you decide," you have a brief that will produce another Inkfall.

## Comprehensibility gate (the 5-year-old test)

A story whose spine is locked in your head but invisible on screen is a *failed* story. The user verdict on the 2026-05-22 LAST BOWL piece was "I see a random robot, random things, I don't understand anything" — even though CONCEPT.md, STORYBOARD.md, and SHOTLIST.md were all internally coherent. The story was in the documents, not in the pixels.

Before approving CONCEPT.md, the bible writer must answer all four of these in one sentence each. If you can't, the story is not yet comprehensible.

1. **5-second premise**: Within the first 5 seconds, what visible element tells the audience the premise? Examples: a sign that reads "FINAL SERVICE"; a clock showing 23:59; a character running with something fragile; a "MISSING" poster. *If no such element exists in the opening 5s, add a TITLE CARD (one shot, 2-3s, white text on the opening image: "The Last Bowl" / "Tokyo, the night the rain stopped" / etc.). Title cards are not a failure mode; they are how cinema solves this exact problem.*

2. **5-year-old retelling**: A 5-year-old watches the 60s with no context and no dialogue. Can they retell the story in one sentence? *"The old man's robot makes a special bowl and then they say goodbye"* is fine. *"There was a robot and an old man and a bowl"* is the failure mode. If the answer is the latter, the premise is too internal — replace it with one that has VISIBLE STAKES.

3. **Visible stakes**: What in the frame tells the audience what the protagonist would LOSE if they fail? Examples: rain washing away a letter; a customer's smile fading; a candle about to burn out. Stakes the audience cannot see are stakes the audience cannot feel.

4. **Climax legibility**: The TURN beat must be visually unmistakable. A subtle "the robot looks at him for the first time" is invisible if the camera doesn't punch into the eye, hold for a beat, and let the audience SEE the change. If your climax requires the audience to remember a setup beat from 30 seconds earlier, you have ~5% retention — write a more visible climax or punch the setup harder.

If you can't answer all four crisply, **scrap the concept and choose a different story**, even one less artistically interesting. A simple legible story beats a sophisticated illegible one at every length under 5 minutes.

### Premise-first concept patterns that pass the comprehensibility gate

When the bible writer is unsure, default to one of these high-comprehension structures:

- **Goal-and-obstacle**: protagonist visibly wants X, obstacle visibly blocks X, protagonist visibly overcomes (or fails). *Delivery boy races hot bowl through rain before it cools.*
- **Quiet-and-magic**: ordinary scene → magical intervention → ordinary scene restored at a new beat. *Lantern goes out → firefly relights it → girl walks home glowing.*
- **Lost-and-found**: protagonist loses something visible → searches → finds (or makes peace). *Child loses balloon, chases, balloon escapes, child laughs.*
- **Promise-and-payoff**: visible promise made at start → visible payoff at end. *Old woman waters dying tree all 60s; final shot the tree blooms.*

Each of these passes the 5-year-old test trivially because the visible action **IS** the story.

## Iteration after a failed verdict

If the previous attempt scored low, the bible writer's first job is to read the prior CONCEPT.md and the judge's critique, identify the comprehensibility failure (it is almost always comprehensibility), and pick a new concept that fixes it. Do NOT iterate on the same story by adding more keyframes — that produces the same failure at higher cost. Iterate by CHOOSING A MORE LEGIBLE STORY.
