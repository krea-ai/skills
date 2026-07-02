# UGC Ad Scripts

Use this when writing the spoken script and overlay text for a scripted UGC ad (`../workflows/ugc-video-ad.md`). The script is the cheapest artifact in the pipeline; iterate here, not on video jobs.

## Pacing Law: 2-4 Words Per Second

Natural talking-head delivery sits between 2 words/second (slow, deliberate) and 4 words/second (conversational). Outside this window the model either pads with dead air and filler or races the line and breaks lip-sync realism. Validate by word count before any video submit.

| Spoken duration | Min words | Max words |
|---|---|---|
| 5s | 10 | 20 |
| 10s | 20 | 40 |
| 15s | 30 | 60 |
| 30s | 60 | 120 |

- Count the words, divide by seconds, confirm 2-4 wps. If a line does not fit its shot, lengthen the shot rather than compressing the line.
- Scripts longer than one job's max duration chunk into takes at sentence boundaries; every take must independently obey 2-4 wps.
- Do not deliver a "15-second ad" script of 90 words and hope the model copes.

## Script Skeleton

Every UGC ad script follows: **hook -> context -> reveal/result -> social proof or emotion -> CTA**. The hook owns the first 1-3 seconds; the CTA owns the final beat. Everything else is compression.

## Hook Families

Five brand-agnostic spoken-script families. Fill placeholders with confirmed product facts and supported claims only.

### 1. Deception / high stakes

- [hook] "Help, I used [PRODUCT] for [HIGH-STAKES SITUATION] and [SURPRISING POSITIVE OUTCOME]."
- [context] "All I gave it was [ONE BASIC INPUT]."
- [reveal] "It gave me [POLISHED RESULT] that looks like [EXPENSIVE ALTERNATIVE]."
- [proof] "[SOMEONE WHO MATTERS] reacted with [POSITIVE REACTION]."
- [twist] "Nobody knew. Nobody asked."
- [cta] "[PRODUCT NAME]. [WHERE TO GET IT]."

### 2. Identity dream

- [hook] "I never had [DESIRED THING] until [PRODUCT]."
- [context] "I don't [HAVE THE PRIVILEGED ACCESS]. I tried this instead."
- [reveal] "[PRODUCT] gave me [RESULT]."
- [emotion] one short human beat - "I just sat with it for a minute."
- [cta] "[PRODUCT NAME]. [WHERE]."

### 3. Social problem

- [hook] "The reason I [SPECIFIC PROBLEM] was [UNEXPECTED CAUSE] and I didn't know it."
- [context] "I tried [USUAL FIXES]. Nothing worked."
- [discovery] "Then I found [PRODUCT]."
- [result] "[SPECIFIC SUPPORTED RESULT]."
- [cta] "[PRODUCT NAME]. [WHERE]."

### 4. Genuine shock

- [hook] "I gave [PRODUCT] [ONE HUMBLE INPUT] and it made me [STRONG EMOTION]."
- [reveal] "This is not [WHAT IT LOOKS LIKE]. It started as [HUMBLE INPUT]."
- [proof] "I showed [PERSON] and they asked [BELIEF-BREAKING QUESTION]."
- [cta] "[PRODUCT NAME]. [WHERE]. Go."

### 5. Which is real

- [hook] "Which of these is [PRODUCT OUTPUT] and which is real?"
- [setup] "I showed these to [N] people and [N-1] guessed wrong."
- [context] "All it took was [ONE INPUT] into [PRODUCT]."
- [invitation] "Comment your guess."
- [cta] "[PRODUCT NAME]. [WHERE]."

These map onto the Video Hook Families in `marketing-creative-anatomy.md` (quiet confession, product proof, pattern interrupt); pick the family there first, then the concrete script here.

## Overlay Text Hooks

For the caption-sticker or burned text hook in the opening frames:

- "When [relatable situation]..."
- "POV: [emotional scenario]"
- "[Statistic] of people [relatable behavior]"
- "Nobody talks about [hidden truth]"
- "I wish someone told me [lesson]"
- "[Age/role] and still [relatable struggle]"
- A blunt question: "Why is nobody talking about this?"
- Before/after framing

Rules: 3-7 words per line, max 3 lines, high contrast rendering. Lowercase is fine and often reads more native. Relatable beats clever.

## CTA Patterns

- Spoken CTA is one short sentence: name + where. "[PRODUCT]. On the App Store." / "[PRODUCT] dot com."
- Visual CTA card owns the last beat (see `video-ad-post.md`); do not stack a polished end card on a UGC piece unless asked.
- One CTA per ad. A hook, a proof, and a single ask.

## Compliance

- No personal-attribute phrasing: never address the viewer's own condition or traits ("your acne", "your PCOS", "your debt"). Speak from the creator's first person instead ("my skin", "I was broke"). Meta rejects personal-attribute callouts.
- No invented claims, pricing, certifications, or performance promises - same claims rules as the rest of this skill. If the user hasn't supported a claim, cut it from the script.
- Product facts in the script come from the confirmed visual/claims brief, not PDP copy.

## Demo / B-Roll Placement

For narrated-demo and cutaway structures:

| Material | Why | Placement |
|---|---|---|
| Money shot (the jaw-drop result/reveal) | The "aha" frame | Second demo slot, after context is set |
| UI / gallery / range | Shows breadth, sets up the input | First demo slot |
| Input moment (upload, scan, pour, apply) | Frames "this is all it takes" | Early |
| Result animation (loading -> reveal) | Builds anticipation | Mid, pairs with shock-family scripts |

Avoid: loading screens longer than ~2s, settings/login screens, placeholder data, landscape-only demo sources for a 9:16 ad. App or software demos must use real screen recordings - never generate product UI with a model; hallucinated UI is a compliance and trust failure.

For batches, collect at least 4 visually distinct demo clips and rotate them across variants.
