# Product Beauty Macro — Minimalist Close-Up Motion For Web

For the piece that loops on a product page, a brand's landing hero, or a
skincare/cosmetics PDP: a single product, shot impossibly close, in a coloured field
pulled from its own palette, where the only thing that ever enters frame is the
product, its named ingredient, or the substance the product is made of.

This is the **beauty register**. `../references/cinematic-craft.md` stages an object against
darkness and `../references/luxury-showcase.md` stages it against an opposing surface; this
one dissolves it *into* a monochrome envelope and goes close enough that the packaging
becomes landscape. Two colours in the whole piece, one light, one material.

Two modes — a slow held macro and a fast uneven cut chain — and **which one is a question
for the user, asked before anything is written.**

Restraint applies to the *frame*, never to whether anything happens. The characteristic
failure is **prettiness with nothing looked at**: a bottle standing in a pink void while a
highlight crawls over it, which is what importing this skill's subject locks wholesale
gets you. Commit to a specific square centimetre, then make something in it act.

## When This Register

| The brief says | Register |
|---|---|
| Product page hero, PDP loop, website background, "for our site" | **This file** |
| Skincare, serum, cream, cleanser, fragrance, cosmetics, supplement, candle | **This file** |
| "Minimal", "clean", "soft", "editorial", "elegant but light", "airy" | **This file** |
| Watch, jewellery, leather, hardware, sculptural design object | `../references/luxury-showcase.md` |
| Launch film, teaser, title-sequence energy, "dramatic", "cinematic reveal" | `../references/cinematic-craft.md` |
| Paid social, hooks, captions, performance creative | the `krea-marketing` skill |

A product can legitimately want both — a fragrance bottle is a beauty product and a
luxury object. Ask which surface it lives on. A page hero wants this file. A campaign
film wants the other.

## Ask First — Minimal Or Maximal

The fork changes the beat count, duration, shot list, generation count and cost. **Ask
before building anything** — the modes share no structure, so a wrong guess wastes the
whole run. Put it in their terms:

> Two directions for this, and they're genuinely different films:
>
> **Slow and minimal** — two or three very close shots, long holds, one thing happening:
> the product tips and settles, or a droplet detaches, or it turns thirty degrees in the
> air. One surface, one material, nothing else. Reads quiet, expensive, confident; the
> kind of thing that sits behind type on a page without competing with it.
>
> **Fast and maximal** — eight or ten cuts in fifteen seconds: the formula pouring at
> macro, the label cropped hard, the product tumbling in air or several copies of it
> turning at once, its texture as an abstract field. Reads editorial and alive, and it
> holds attention on its own.
>
> Which one? (Minimal is one or two generations; maximal is three or four and costs
> proportionally more.)

| | Minimal | Maximal |
|---|---|---|
| Duration | 5–8s | 7s for the one-generation entry point, 10–15s assembled |
| Beats | 1–3 | 4–5 per generation, 8–11 across the assembled piece |
| Detected cuts | 0–2 | **beats − 1** — a 5-beat take scene-detects as 4 |
| Beat length | 2.5–4s, or one continuous take | 0.4–2.4s, uneven |
| The subject | One square centimetre of the product, held | The product, its label, its matter, alternating |
| What carries it | Light, focus, texture, the falloff | The cutting |
| Whole product on screen | Only at the end, or never | Beat two, and again at the end |
| Generations | 1 | 1 for MAX 1, 2 for MAX 3, 3–4 for a full 12–15s piece |
| Cadence section | `## Minimal Cadence` below | `## Maximal Cadence` below |

**MAX 2 sits outside this table** — one continuous 6s take, one beat, zero cuts, and it
serves the minimal mode too. Take its numbers from the shape.

`beats − 1` matters because scene detection sees only transitions, and the cut-count gate
in `## Verify` counts detected cuts. A four-beat take returning three is correct.

Everything between here and the cadence sections — the tonal envelope, the light
doctrine, the substance rule, label framing — is **shared by both modes**. Only the
cadence and the shapes differ.

If the user does not answer, or answers "whatever you think": default to **minimal**
for a page hero or a background loop, and **maximal** for a PDP or a launch page where
the piece is the content rather than the backdrop. State the default you took.

### If They Ask To Experiment

**Only when the user explicitly asks for options, experimentation, or a maximalist
version, and has signalled they have time and budget for it.** Never the default — it is
several times the cost and the wait.

Then make three, not one, and make them genuinely different:

1. **Quantity** — several copies in air, per `### MAX 2`.
2. **Minimal** — one held macro, per `### MIN 1`.
3. **Maximal with nature** — the surface ground and an active substance event.

For the third, generate the environment first: consult `../../krea-marketing/references/product-photography.md` for the lighting register, make a still of the product on the real material — wet stone,
a water film, the formula pooled — approve it, then animate that as the `start_image`. A
reference of an actual lit material beats asking a video model to invent one around a
plain packshot, every time. Cost it out loud first: one extra image generation per
variant on top of three video takes.

## What The Page Imposes

Four constraints come from the medium, not from taste, and they are the reason this
register diverges from the house default at all:

1. **It plays muted.** No audio design. State silence explicitly.
2. **It often loops.** Usually 6–15 seconds, cut back to the head, forever. Not
   always — a piece with an authored ending is legitimate — but decide early, because
   looping constrains the last beat and the grade. See `## Loop Discipline`.
3. **The page supplies the type.** The footage is textless; the only words in frame
   are the ones physically printed on the product.
4. **The visitor must know what is being sold immediately.** This is the big one, and
   it overrides a hard rule.

### The One House Rule This Register Relaxes

**Maximal mode only** — in minimal mode the product is never shown whole, or only in the
last second, which is what the house rule wants anyway.

`../references/cut-architecture.md` withholds the whole subject until the last beat. That
suits a reveal film, whose viewer has committed to watching. A page hero has no such
contract: a visitor who cannot identify the product in the first second and a half
bounces. So the structure **alternates** instead of building:

```
substance or detail macro → the whole product → detail → substance → the whole product
```

Beat one is still macro — the opening is still an intimacy, never an establishing
shot. But the whole product lands on beat two, and it returns at the end. The piece
reads as a circuit rather than an arrival, which is exactly what a loop needs.

Say this out loud in the prompt so the model does not fight it:

```
Structure: alternating. The complete product is fully visible in the second beat and
again in the final beat; the beats between are extreme details and material. This is
intentional and not a reveal — do not withhold the product, and do not treat the
final beat as a first disclosure.
```

Everything else in `cut-architecture.md` stands: change scale, angle and light on
every cut, one move and one event per beat, quantify everything, no long holds.

## Where To Point The Camera

Macro is not an excuse to shoot the nearest interesting-looking edge. On a skincare
product the interesting-looking edge is the cap, and the cap is not the product.

**Shoot, in this order:**

1. **The formula** — through the glass, at the meniscus, pooled, dispensed, mid-pour.
2. **The body of the bottle or tube** — the part the formula reads through or the copy is
   printed on. This is the product's shape and the thing a customer recognises.
3. **The printed face** — the wordmark, the claim line, the foil. Cropped hard.
4. **The product on skin** — cream drawn across the back of a hand, a drop landing on a
   forearm, sheer where it spreads. The strongest beat available and the most skipped.
5. **The named ingredient** — formed out of the formula, unfurling behind the product,
   or its own texture at macro. Derived from the label, never generic.
6. **The matter alone** — a swatch, a comb, a spread, filling frame.

**Do not build a beat on** the cap, the collar, the pump head, knurling, threading, the
crimp, or the hinge. That is the hardware instinct from
`../references/luxury-showcase.md`, where machined metal *is* the product. Here it says
nothing: nobody buys a serum for its collar. Hardware can sit in frame as part of a wider
shot; it cannot be what a cut is about.

The test: could this frame be any brand's bottle with the label removed? If yes, it is a
hardware shot — move to the formula or the printed face.

## Motion: The Product Is Allowed To Act

Read this before the envelope and the light, because it is the section that decides
whether the piece looks like anything.

The rest of this skill locks the subject hard — *nothing wobbles*, the suspension lock.
That is right for a watch. Imported here it produces the register's deadening failure:
**a product standing dead still in a coloured void while a specular crawls over it, every
beat, every piece** — after which the only lever left for variety is more dramatic light.

In this register the product **may move, and usually should.** The lock is one option, not
the default.

| Motion | Prompt language |
|---|---|
| Turn in place | `the product rotates in place about its own vertical axis exactly 40 degrees over 1.6 seconds at a constant rate, dead level, no bobbing, no drift` |
| Tip and settle | `the product tips 12 degrees toward camera-left over 0.5 seconds, reaches the tilt, and settles back to upright over 0.4 seconds with one small overshoot and no wobble after; realtime gravity` |
| Rise and hold | `the product lifts 8 centimetres straight up across 1.2 seconds at a constant rate, dead level, no rotation, then stops dead and holds; its contact shadow softens and spreads as it rises` |
| Fall into frame and land | `the product enters from above frame, falls 15 centimetres under realtime gravity, decelerates over the last 3 centimetres and settles upright with one small bounce; no slow-motion, no floating` |
| Tumble in air | `the product tumbles slowly about a single horizontal axis, one full revolution across 4 seconds at a constant rate, holding its position in space — it does not also drift, rise or fall` |
| Roll and stop | `the cylindrical product rolls 10 centimetres to camera-right across the surface over 1.4 seconds at a constant realtime rate, decelerates, and stops with the label facing camera` |
| Two copies passing | `two copies cross at different depths, the near one travelling left to right and the far one right to left, both at the same constant rate; they never touch and never swap depth` |
| Cluster in air | see `### MAX 2` — several copies, each turning in place |

Three rules keep this from becoming the flailing that `../references/cinematic-craft.md`
also bans:

1. **One motion per beat**, quantified — degrees or distance, duration, constant rate,
   realtime physics. Unquantified "rotating slowly" is the floaty look the lock existed
   to prevent.
2. **It completes or settles inside its beat.** Still in progress at the cut is fine only
   for the blur whip.
3. **The camera holds still when the product moves.** Both at once is the lurch.

### The Rule That Prevents The Monoculture

> **At least one beat in every maximal piece has the product or its own matter
> physically moving.** Not the light. Not the camera. The thing itself.

Locked in every beat with only the specular travelling is a failed piece here however
good the light is, and it is the most likely thing to come back. Restage the weakest
locked beat.

Minimal mode is not exempt, it just needs less: one small motion in the whole piece — a
tip and settle, a droplet detaching, one copy turning 30 degrees. Minimal means few
elements and long holds, not an inert product.

## The Tonal Envelope

The single most recognisable trait of this register: **the background is one colour,
derived from the product, and nothing else is ever in frame.** No set, no surface, no
props, no horizon. The product exists inside a field of tinted light.

This inverts the tension principle in `../references/luxury-showcase.md` on purpose: rather
than pairing the object against an opposing surface, the envelope removes every colour
that is not the product's, so the eye can only read form, finish and texture.

Three legitimate field strategies. Pick one; never blend two.

| Strategy | Field | Use when |
|---|---|---|
| **Tone-on-tone** | The product's own dominant hue, desaturated to roughly a quarter and lifted one to two stops — a nude tube in a warm blush field, a sand-coloured jar in bone | Opaque packaging with subtle colour. The safest and most editorial. |
| **Muted complement** | The formula's complement, desaturated hard — a dusty mauve-rose field behind a gold or amber oil | The formula is visible through glass. The liquid becomes the only saturated thing in frame. |
| **High-key bone** | Near-white, soft, one thin contact shadow | Tinted or translucent glass. Transmission needs a bright ground or the glass reads as grey plastic. |

The rules that hold across all three:

- **One hue in the entire piece.** The product's own colours are the exception; the
  world gets exactly one.
- **Saturation cap.** The field never exceeds about a quarter saturation. The product is
  the only saturated element in frame, along with its named ingredient — a green frond in
  a mauve field is the product's colour, not a second world colour.
- **Gradient, not flat.** A flat colour reads as a chroma key. A soft gradient — one
  corner a stop brighter than the opposite — reads as a lit space.
- **No horizon, no seam, no vignette, no second colour.** Seedance adds all four.

```
Consistent world across all beats: an infinite seamless field of dusty mauve-rose,
lit as a soft gradient one stop brighter at upper camera-left and falling to a
deeper mauve at lower camera-right. No horizon line, no floor seam, no wall, no
table, no surface edge, no props, no set dressing, no vignette. The field is the
only environment and it never changes hue between beats. Palette: mauve-rose at
low saturation throughout, plus the warm amber of the formula and the rose-gold of
the collar — no other colour anywhere in frame.
```

Suppress the dark-register defaults explicitly, or the model reaches for charcoal the
moment you ask for drama:

```
NO charcoal or black void, NO dark studio background, NO true blacks, NO low-key
grade, NO teal or blue cast, NO second background colour, NO gradient sweep across
the field.
```

### Three Grounds

The infinite field above is one option, not the only one. Used for every beat of every
piece it is what makes this register feel airless — a product floating in nothing,
forever. **Pick a ground per piece:**

| Ground | What it is | Use when |
|---|---|---|
| **The field** | No surface at all; the product suspended in tinted light | The product is in the air, tumbling or clustered. The default for MAX 2 and for anything levitating. |
| **One surface** | A single tone-matched material plane the product sits on, fills the lower third, or reflects in | The product stands, tips, rolls or settles. Gravity needs somewhere to land. |
| **Its own matter** | The dispensed product itself as the ground — a pool, a swatch, a spread seen nearly edge-on | Formula products. The strongest of the three and the most specific to this register. |

For the surface ground, one material only, tone-matched, and no props on it:

```
The product sits on a single unbroken plane of honed travertine in the same warm blush
as the field, filling the lower third of frame, its own soft reflection visible in the
stone. The plane has one straight edge running horizontally and nothing else is on it —
no props, no second object, no set dressing, no visible room beyond, no wall, no
horizon line above the plane.
```

Materials that hold up at macro and stay inside the palette: honed travertine or
limestone, raw plaster, unglazed ceramic, brushed aluminium, a linen fold, a thin film
of water on glass, wet glass, a mirror. One of them. A surface earns its place by
letting the product **do** something — tip, roll, settle, cast a shadow that moves —
and if the product is locked anyway, drop the surface and use the field.

The banned list is unchanged for everything that isn't the ground: still no props, no
second object, no room, no window, no plant, no towel, no marble-with-gold-veining.

## Light: Soft-Dramatic, Not Low-Key

"Dramatic lighting" in this register does not mean the 95%-darkness ratio from
`cinematic-craft.md`. It means **one large raking source and a deep, soft, coloured
shadow** — the drama is in the falloff and the direction, not in the absence of light.

The distinction that matters: the shadow side falls to a **deeper version of the field
hue**, never to true black. Black on the shadow side is what makes a beauty frame look
like a car advert.

```
Light: one large soft source, a 1.5-metre diffused panel high at camera-left raking
across the product at about 30 degrees, close enough that falloff across the frame is
visible. The shadow side of the product retains detail and resolves into a deeper,
warmer version of the field hue — never to black, never crushed. One thin hard
specular runs the length of the glass edge nearest the source. A soft, coloured
contact shadow sits under the product, its edge diffuse.

NO god rays, NO visible beams, NO lens flare, NO bloom, NO haze glow, NO rim light
from behind, NO second source, NO hard black shadow, NO clipped highlights.
```

Three light events that belong to this register specifically:

| Event | Prompt phrasing |
|---|---|
| Field breathe | `over 2 seconds the field brightens by two thirds of a stop at upper-left and settles, at a constant rate; the product's exposure does not change` |
| Coloured shadow travel | `the soft contact shadow lengthens 3 centimetres to camera-right over 1.5 seconds at a constant rate as the source drifts; its edge stays diffuse and it stays mauve, never black` |
| The closing stop-down | `on the final beat the field darkens by one and a half stops over 2 seconds at a constant rate while the product's own exposure holds exactly; the hue does not change, only the level` |

The closing stop-down is the cheapest way to make a page loop feel authored — the
piece ends richer and heavier than it began. **It is incompatible with a seamless
loop**, since the last frame no longer matches the first. Choose one, and say which.

## The Substance Rule

The "drop of nature" that makes these pieces feel alive is almost never generic nature.
It is matter with a reason to be there — the product's own formula, or the thing the
product is made of.

> Whatever substance is in frame is one the product contains, produces, is made of, or
> would physically touch in use.

That tie is what separates this register from stock beauty footage. Petals on a retinol
serum are set dressing; a frond of the marine botanical the oil is actually made from,
forming out of the oil itself, is the product.

### Derive The Matter From The Product

Read the label first. A product is *about* something — marine botanicals, oat, fig,
fermentation, cold-pressed oil, clay — and the non-product beats are made of that story.
Invent them from it.

A marine body oil suggests something that grows in water: a frond forming out of the oil
and unfurling behind the bottle, the weighted drift of something suspended in seawater.
An oat cleanser suggests clouding, settling, milkiness. A clay mask suggests cracking,
dust, dry breaking. A fermented essence suggests slow bubbling and a lit haze inside the
liquid.

The tables below are starting points, not a list to work through — if the product
suggests something better, do that instead. What is fixed is not the subject. It is
these six:

- **Semantic tie.** Whatever is in frame is what the product is actually made of.
  Unrelated decoration is the stock-footage tell.
- **One instance.** A frond, not a bed of them. At three it is set dressing.
- **Behind or beside, never in front.** The product's silhouette stays unbroken and
  sharp; the matter sits at a softer depth in the same field.
- **Same field, same light.** One scene, lit by the same source — never a cutout pasted
  into the frame.
- **Realtime, and the beat length enforces it.** Fast events get 0.5–0.9s; slower ones
  get a quantified rate. Buying two seconds for a splash is how you get a slow-motion
  splash whatever the prompt says.
- **Its colour counts as the product's.** A green frond in a mauve field is correct, not
  a second world colour.

### Active — the matter does something

Reach for an active beat first; the passive traces below are texture, not events, and a
piece built only from them has nothing happening in it. Six physics families, one
example each:

| Event | Prompt phrasing |
|---|---|
| Dispensed | `a ribbon of white cream extrudes from the nozzle over 1.5 seconds at a constant realtime rate and folds over on itself once, holding a soft peak; it does not drip, run, string, or overflow` |
| Poured | `a thin steady stream of the amber oil pours from the bottle mouth for 1.2 seconds at a constant realtime rate and gathers into a shallow pool below; the stream stays unbroken` |
| Detaching | `a single droplet of serum gathers at the dropper tip over 0.8 seconds, detaches, falls 6 centimetres under realtime gravity and lands on the surface below, spreading to a 1-centimetre disc` |
| Impact | `the bottle drops the last 4 centimetres into a shallow pool and the impact throws a tight, asymmetric splash 6 centimetres outward; the whole event begins and completes inside 0.6 seconds at realtime speed under normal gravity — no held crown, no symmetrical coronet, no frozen droplets` |
| Crossing frame | `a sheet of water is thrown across frame from camera-left, passes behind the product and clears frame entirely within 0.7 seconds at realtime speed; the product stays dry, sharp and locked, and no droplet hangs in the air after it has passed` |
| On skin | `the cream is drawn across the skin in one pass over 1.4 seconds at a constant rate, going from opaque white to sheer as it spreads; visible pores at macro, subsurface warmth at the edges, never plastic` |

### Passive — traces that live on the product

| Substance | Prompt phrasing |
|---|---|
| The formula behind glass | `extreme macro through the glass into the amber oil: dozens of small round bubbles suspended at different depths, drifting upward at realtime speed, surface tension intact, the nearest sharp and the rest falling to bokeh` |
| Condensation | `fine condensation beads across the glass, each holding a tiny specular; two beads merge and run 8 millimetres down the bottle over 1 second at realtime speed, leaving a clear track through which the formula reads` |
| The meniscus | `the liquid line sits across the lower third, its meniscus curving up against the glass, one caustic focused on the surface below it` |
| The matter as a texture field | `extreme macro filling frame with the cream itself, combed into even parallel ridges; the camera tracks laterally 3 centimetres across the ridges over 2 seconds at a constant rate, the raking source catching each crest` |

### Banned — mechanisms, not subjects

```
no slow-motion, no speed ramping, no dreamy float, no held or symmetrical droplet crown,
no frozen mid-air droplets, no featureless spheres or blobs of liquid or metal, no
floating balls of any kind, no silk or fabric drifting through frame, no glitter, no
sparkles, no floating particles, no soap bubbles in the air, no steam, no smoke, no ink
blooms or dye plumes that are not the formula itself, no submerging, no set dressing with
no tie to the product — no scattered or falling petals, no beds or piles of plant matter,
no sliced fruit unless the fruit is the named ingredient
```

Every entry is either a *mechanism* that reads cheap whatever the subject, or decoration
with no reason to be in frame. Splashes, pours, botanicals, clouding and cracking are
deliberately **not** here — they are the agent's call under the six constraints above.
What makes a splash look like stock is slow motion, not the splash.

### The Cap

**Up to two substance events in a maximal piece, one in a minimal one.** A third is
where restraint turns into a stock-footage reel. A derived-ingredient beat counts as one
of the two.

At most one of the two may be a *passive* trace — condensation, suspended bubbles, a
meniscus. Those are texture rather than events and they can run for the whole piece, but
two passive traces and no active one is a piece where nothing happens.

For the matter section of an assembled maximal piece, a **chain of two active events
plus one texture field** across three beats is legitimate and is the strongest thing in
this register: the ribbon extrudes, the spatula drags it, the camera traverses the
furrow. Three beats, one material, escalating. That counts as its two events.

Physics, every time: `realtime speed, surface tension intact, no slow-motion, no
speed ramping, no dreamy float`. Liquid slowed down is the most common way this
register turns into stock footage. See the liquid and skin rows in
`../references/cinematic-craft.md`.

## Framing The Label

The most confident device in these pieces, and the most likely to break: **the printed
type cropped hard by the frame edge**, letters larger than the frame, running at a
rake across the composition.

It works because it assumes the viewer already knows the brand. It breaks because a mark
filling the frame at macro is the easiest thing for a video model to re-letter.

Requirements, all of them:

1. **The three-place text lock** from `../references/logo-and-mark-motion.md` —
   references block, motion split, constraints tail. Non-negotiable.
2. **Name which words are in frame** and state that the crop is intentional. Without
   this, Seedance "helpfully" pulls back to fit the whole label, or invents the
   missing letters at the frame edge.
3. **Tilt the product, not the horizon.** A rotated camera reads as a mistake; a
   product lying at a rake in a level frame reads as styling.
4. **Never crop mid-glyph on a letter that is also mid-motion.** Crop between
   characters, or on a character that stays put.

```
SHOT 3 — LABEL RAKE (3.2–5.0s), extreme close-up, 100mm macro, camera above and to
the right of the product's face. HARD CUT in. The product lies at a 35-degree rake
across frame, its printed face filling the whole frame; only the words FORMULE and
ANTI-AGE are within the crop, and both are cut by the frame edge at the right — this
crop is deliberate, hold it exactly, do not pull back to fit the full label and do
not add or complete any letter beyond the frame. Camera pushes in 4 centimetres over
1.8 seconds at a constant rate. Every letterform, stroke weight, counter and kerning
pair stays pixel-exact to @Image1 — never re-lettered, never warped, never re-spaced.
```

Include a foil, deboss or varnish note if the packaging has one — it is the reason to
be at macro at all: `the gold foil of the wordmark catches the raking source and
reads as metal against the matte substrate, the specular travelling along the
letterforms as the camera moves`.

## Maximal Cadence: Fast, Uneven, Never Metronomic

The timing is what most people get wrong. These pieces are **not** four even beats.
Across a 14–15 second piece the shape is roughly:

| Property | Value |
|---|---|
| Cuts | 8–11 across 14–15 seconds |
| Interval range | 0.4s to 2.4s |
| Mean interval | ~1.5s |
| Where the short beats go | Front-loaded: one or two staccato sub-second beats early, often two attitudes of the whole product back to back |
| Where the long beats go | The abstract ones — a texture field, a mist, a substance macro holds 2.0–2.4s because it takes the eye a moment to work out what it is looking at |
| The last beat | 1.5–2.0s, the whole product, camera stopped |

**Alternate what the beat is *about*** — product, ingredient, matter — not only its
scale. Intercut product beats of 1.5-2s with 1-1.5s ingredient or texture cutaways inside
one consistent scene. A chain of macros that are all the bottle reads as one long look at
a bottle however hard it cuts. A splash or impact beat is 0.5-0.9s and belongs in the
staccato slot, never in a long hold.

**The irregularity is the craft.** Even intervals read as a slideshow with transitions;
uneven intervals read as edited. Write the time ranges out and make them uneven on
purpose — 1.4, 0.6, 0.5, 1.9, 2.3, 1.2, 1.8 is a rhythm; 1.5 × 8 is a metronome.

Seedance commits to three or four strongly distinct beats per generation
(`../references/cut-architecture.md`). A 14-second piece at this cut density is therefore
**assembled**, not generated: three or four generations of three beats each, trimmed
to their usable cores and cut together. Plan it that way from the start, and keep the
world block byte-identical across every generation so the field matches at the seams.

```bash
ffmpeg -y -ss 1.4 -i beat-04-raw.mp4 -t 0.6 -c:v libx264 -pix_fmt yuv420p -an beat-04.mp4
```

### The Off-Axis Punch

The other timing signature: the camera never arrives square. Each cut lands on a
noticeably different product attitude, and the move inside the beat is a short push
that is **off the product's face by 10 to 25 degrees**, stopping dead.

```
Camera sits 20 degrees off the product's printed face and 15 centimetres above its
centre line. One push of 5 centimetres over 1.1 seconds at a constant rate, holding
the off-axis relationship throughout — the camera does not straighten, does not
orbit, does not correct toward square. It stops dead and holds for the final third of
the beat.
```

The rule that makes a chain of these read as deliberate: **change the product's
attitude, not just the camera's position.** Between two adjacent beats the product
should differ by at least 20 degrees of tilt or roll. Two beats at the same attitude
under a new light still read as one shot.

Banned in this register: the dead-on symmetric push, and the product centred upright
in frame anywhere except the final landing.

### The Blur Whip

A ~0.6–0.9 second beat where **the product itself** swings through frame under heavy
motion blur, between two static beats. It hides a cut, it resets the eye, and it is
the only fast movement permitted here.

```
SHOT 5 — WHIP (7.6–8.4s), close, 50mm. The product swings through frame from lower-
left to upper-right across 0.8 seconds at a constant realtime rate, heavily motion-
blurred by its own speed — the blur comes from the movement, not from a filter or a
zoom. The field stays in place behind it. No camera move. Cut out of this beat while
the product is still travelling.
```

Never two of these in one piece, and never one at the loop seam.

## Minimal Cadence: Long Holds, One Thing Changing

The minimal mode is the harder of the two to get right, and it is the one that most
often gets asked for — "clean", "simple", "just the product, nice and slow". It is two
or three very close shots, 2.5–4 seconds each, or a single continuous take across the
whole duration. Nought to two cuts in the entire piece.

| Property | Value |
|---|---|
| Duration | 5–8s |
| Cuts | 0, 1 or 2 |
| Beat length | 2.5–4s, or one 6–8s continuous take |
| Camera move | One per beat, tiny: a 2–4cm push, or a 2–3cm lateral traverse, or locked |
| The event | Optical or luminous — focus resolving, a specular travelling, a shadow lengthening, the field stopping down. Never mechanical. |
| The frame | One square centimetre of the product. Never the whole thing except possibly at the very end. |
| Tail | The move stops dead with 0.5–1s of held stillness left |

This mode sits directly on top of hard rule 3 — *cut, don't drift* — and it is the one
place in this skill where a slow continuous shot is the right answer rather than the
primary failure. That permission is conditional. It holds only if the shot passes all
five tests below.

### What Makes Slow Legitimate

The difference between minimalism and the timid drift the skill bans is not duration.
It is whether anything is actually being looked at, and whether anything actually
changes. Five tests, all required:

1. **The frame is a detail, not the product.** One boundary between two materials, and
   it never widens. If the whole product is legible in the opening frame this is the
   failure mode, not the minimal mode.
2. **Something changes state across the duration.** Freeze the first and last frames: if
   they differ only in scale, the shot failed.
3. **The move is quantified, constant, and stops.** Distance, duration, `at a constant
   rate`, dead stop before the end. Unquantified slowness comes back speed-ramped.
4. **One named light event with a start and an end position.** Not "the light plays across
   the surface" — `the specular begins at the left edge of the first letterform and
   travels 2 centimetres to its right edge across 3 seconds`.
5. **The texture is the content.** There must be a material worth 4 seconds at macro:
   a foil wordmark against a matte substrate, the formula behind glass, frost on a cold
   bottle, the ridge of a cream comb, the meniscus. A flat printed panel cannot carry
   this mode — go maximal, or find a better centimetre.

Fail any one and the result is a still frame with a slow zoom on it. The cure is never
a longer duration or another adjective; it is a closer frame and one committed event.

**These five govern the held-macro shapes — MIN 1, MIN 2, MIN 3.** The suspended
cluster (MAX 2) is also a zero-cut take and deliberately fails tests 1 and 5: it is a
medium of whole products, not a macro of one detail. It earns the permission on a
different argument — every copy is in continuous motion at a different depth, so no
region of the frame is ever static, and there is no unstaged time for the model to
fill. That is the only other configuration in this register where zero cuts is
sanctioned. A locked medium shot of a *single* product satisfies neither argument and
is the drift failure with extra steps.

### Seedance Inserts Cuts You Did Not Ask For

The trap specific to this mode: an under-staged single take gets *filled*. Seedance
invents a cut, a second angle, or a drift to the whole product to occupy time the
prompt did not spend. Forbid it explicitly, in the format block and again in the tail:

```
Format: one single continuous take, no cuts, no scene changes, no angle changes, no
second shot — the camera never cuts and the framing never jumps.
```

```
Constraints (reassert): a single continuous take from first frame to last. No cuts, no
additional beats, no second angle, no jump in framing, no reframe to the whole
product, no dissolve, no fade. Nothing enters frame that is not already in it.
```

And buy only what you staged. A 6-second take with 4 seconds of staged move gets 2
seconds of invention on the tail. Either stage the tail as an explicit hold — `the
camera stops dead at 4s and holds absolutely still for the final 2 seconds, nothing
moving in frame` — or buy 4 seconds.

### Where The Closing Stop-Down Earns Its Place

With no cutting to shape the piece, the grade is what gives it a beginning and an end.

**All three MIN prompts below use it, so none of them loop** — a continuous take has no
cut to hide a seam, and a piece ending darker than it began flashes on every repeat. Since
minimal is often asked for *because* it suits a looping background, use the cyclic variant
below rather than shipping a shape that cannot do the job.

### The Cyclic Minimal Loop

For a minimal piece that must loop, drop the stop-down and make the single event
**cyclic** — it has to end where it started. Camera locked; the event travels out and
returns within the duration:

```
Motion split: the product is locked absolutely and the camera does not move at any
point. One specular is the only thing that changes. Realtime speed, no slow-motion, no
speed ramping.

SHOT 1 — CYCLE (0–6s), extreme macro, 100mm macro, camera locked and absolutely still.
The frame holds the boundary between the matte substrate and the gold foil. One thin
hard specular travels along the raised foil from the left edge of the first letterform
to the right edge of the second across 3 seconds at a constant rate, then travels back
along exactly the same path over the following 3 seconds at the same constant rate,
arriving at its starting position at 6.0s. The field level and hue are identical at 0s
and 6s — no darkening, no brightening, no fade in, no fade out. Nothing else in frame
changes.
```

This also settles two of the five tests for the looping case:

- **Test 2** (something changes state) is satisfied by the outbound half. The change
  must simply be cyclic rather than terminal — the frame at 6s matches the frame at 0s,
  but the frames between do not.
- **Test 3** (the move stops dead) becomes *the move returns* — a cyclic event does not
  need a held tail, because the arrival back at the start position is the resolution.

The other three tests apply unchanged. Out-and-back specular is the most reliable cyclic
event, a field breathing up and settling back the second. Anything that consumes the
product — a droplet detaching, a ribbon extruding — cannot be cyclic; put it in a
non-looping piece.

## Canonical Minimal Shapes

**MIN 1 is a complete prompt. MIN 2 and MIN 3 are shot blocks only** — drop them into
MIN 1's surrounding structure, which supplies the format, references, world, motion
split, light, audio and constraints blocks they omit. Hard rule 7 makes all of those
mandatory on any shot over 4 seconds, and both of these are 6–7 second shots.

Two of the surrounding blocks are not optional decoration for this mode:

- **MIN 2 needs the no-cuts format line and the reassert tail** from `### Seedance
  Inserts Cuts You Did Not Ask For` above. A single locked 6-second take with no cut
  declaration is precisely the under-staged prompt that comes back with an invented cut
  in it — the more so because this is the shape with the least happening.
- **MIN 3 needs the tail, with `no additional beats` in it.** "Two beats is two beats"
  is a lock the model only obeys if the prompt says it.

### MIN 1 — The Single Surface Hold

One continuous take. Extreme macro on the boundary between two materials, one
travelling specular, no cuts. The most confident thing in this whole register, and the
cheapest — one generation.

```
Format: One single continuous take, macro material study of a beauty product, 6
seconds, 9:16, soft high-contrast beauty grade, no on-screen text, silent. No cuts, no
scene changes, no second angle.

References: @Image1 as the first frame and the hero product — the nude tube with the
gold foil wordmark. Every letterform, stroke weight, counter and kerning pair stays
pixel-exact as shown: do not re-letter, re-draw, re-space, warp or substitute any
glyph, do not add a tagline.

World: an infinite seamless field of warm blush, a soft gradient one stop brighter at
upper camera-left. No horizon, no floor seam, no surface edge, no props, no set
dressing. Palette: low-saturation warm blush, plus the gold of the foil — no other
colour in frame at any point.

Motion split: the product is locked absolutely — it does not rotate, tilt, bob, drift
or change scale at any point. The camera makes one small quantified move. The only
other thing that changes is the position of the specular and the level of the field.
Realtime speed, no slow-motion, no speed ramping.

SHOT 1 — FOIL EDGE (0–6s), extreme macro, 100mm macro, camera 20 degrees off the
product's face and slightly below its centre line. The frame holds the boundary
between the matte nude substrate and the gold foil of the wordmark, filling the frame
edge to edge; two letterforms are within the crop and both are cut by the frame edge —
this crop is deliberate, do not pull back, do not complete any letter beyond the
frame. The camera tracks laterally 2.5 centimetres to camera-right across the first
4.5 seconds at a perfectly constant rate, dead level and parallel to the surface, then
stops dead and holds absolutely still for the final 1.5 seconds. As it travels, one
thin hard specular runs along the raised foil, beginning at the left edge of the first
letterform and reaching the right edge of the second at 4.5s — the matte substrate
beside it stays free of specular and reads as powder. Over the last 2 seconds the
field darkens one and a quarter stops at a constant rate while the product's own
exposure holds exactly; the hue does not change.

Light: one large soft diffused panel high at camera-left raking across the surface at
about 25 degrees, close enough that the foil reads as metal against the matte and the
falloff across the frame is visible. The shadow side resolves into a deeper warm blush,
never to black, never crushed. NO god rays, NO beams, NO flare, NO bloom, NO rim
light, NO second source, NO black shadow, NO clipped highlights.

Transitions: none. This is one continuous take.

Audio: silent.

Constraints: a single continuous take from first frame to last — no cuts, no
additional beats, no second angle, no jump in framing, no reframe to the whole
product, no dissolve, no fade. The wordmark is pixel-exact to @Image1, never
re-lettered, never warped; no additional text, no tagline, no captions, no watermark.
One environment: the blush field, unchanged in hue. No charcoal or black void, no dark
studio, no true blacks, no low-key grade, no teal or blue cast. No water, no splashes,
no petals, no leaves, no particles, no glitter, no sparkles, no steam. No light
streaks, no shine sweeps beyond the single specular named above, no bars or bands
crossing frame, no gradient sweeps, no rings or ripples. No slow-motion, no speed
ramping, no camera shake, no handheld feel, no searching or hunting adjustments.
```

### MIN 2 — The Focus Resolve

Locked camera; the entire duration is one focus travel from full bokeh to razor-sharp
on a single detail. The most reliable minimal shape there is, because the event is
unmistakable and Seedance handles rack focus well.

```
SHOT 1 — RESOLVE (0–6s), extreme macro, 100mm macro, camera locked and absolutely
still for the entire take. The frame opens as complete soft bokeh with no readable
form — only a warm blush field and one diffuse gold smear. Over 4.5 seconds the focus
plane travels backward at a constant rate until the meniscus of the amber formula inside
the bottle is razor sharp, the liquid line and its caustic legible, the surround falling
away to bokeh. The camera does not move at any point — no push, no drift, no reframe.
Focus arrives at 4.5s and holds
absolutely still for the final 1.5 seconds. Over the last 2 seconds the field darkens
one stop at a constant rate while the sharp detail's exposure holds.
```

Pair it with a field breathe if it needs one more thing happening: `over the same 4.5
seconds the field brightens two thirds of a stop at upper-left, at a constant rate`.

### MIN 3 — The Two-Beat Pair

The minimum that still cuts: two long beats, one hard cut, two different surfaces of
the same product, the key direction flipping between them. Use when one surface cannot
hold 6 seconds but the brief still wants quiet.

```
SHOT 1 — GLASS (0–3.4s), extreme macro, 100mm macro, camera above and left. Locked.
The frame holds the shoulder of the bottle where the glass turns away from the source;
fine condensation beads sit across it, each holding a tiny specular. Two beads merge
and run 8 millimetres down the glass over 1.6 seconds at realtime speed, leaving a
clear track. Nothing else moves. HARD CUT out.

SHOT 2 — SKIN (3.4–7s), extreme macro, 100mm macro, camera below and right, key flipped
to camera-right. HARD CUT in. The frame holds the back of a hand; a bead of the serum
is drawn across it in one pass over 2.2 seconds at a constant realtime rate, going from
a raised drop to a sheer film as it spreads. Visible pores at macro, subsurface warmth
at the edges, never plastic. Camera locked. Over the last 1.5 seconds the field darkens
one stop while the skin's exposure holds.
```

Two beats is two beats — do not let it become three. If the piece needs a third
surface, the brief is maximal and the user should be asked again.

### Also Available In Minimal

**MAX 2 — Suspended Cluster Drift**, in its looping version, serves this mode
unchanged — locked camera, seven copies, one full turn, zero cuts. Take it as written;
do not de-tune it. Dropping the copy count below five makes it sparse rather than
minimal, and it is already the low-energy option.

It earns its zero cuts on a different argument from the shapes above — see the end of
`### What Makes Slow Legitimate`.

## Canonical Maximal Shapes

### MAX 1 — Tonal Macro Chain

The default for a bottle, jar or tube with a printed face. Substance macro, the product
tipping, a droplet detaching, a label crop, back to the whole.

Five beats in **one generation** at 7 seconds — the entry point, not the full 12–15s
shape. For that, chain two more takes and assemble.

Spread **1.7 / 0.9 / 0.7 / 1.7 / 2.0**: staccato pair early, longest holds at the back.
Do not flatten it toward equal beats. Two of the five have something physically moving
and only two are the whole product — keep that ratio; three locked whole-product beats is
how this shape decays into the monoculture.

Five beats is one over the budget in `../references/cut-architecture.md`, and the 0.9/0.7s
pair is where a merge will happen. Scene-detect for four cuts; if you get three, buy
SHOT 2 and SHOT 3 as their own 4-second take and assemble.

**This take does not loop**, and the format line says so. It ends on the closing
stop-down, which leaves the tail a stop and a half under the head — an authored ending,
and the thing that makes the piece feel finished rather than cut off. To make it loop
instead: hold the field level flat across the landing and keep the hue constant. The
droplet is one-way but it already sits mid-piece, which is where irreversible events
belong. Head and tail composition do **not** have to
match here, because the seam of a cut piece is itself a hard cut — see `## Loop
Discipline`, which separates that case from a continuous take. What you cannot do is
claim both the stop-down and the loop in one format line; the model resolves that
contradiction on its own and usually drops the one you cared about.

```
Format: Cinematic beauty product piece for a web hero, 7 seconds, 9:16, soft
high-contrast beauty grade, no on-screen text, silent. This take does not loop — it
ends on a graded landing.

References: @Image1 as the first frame and the hero product — the clear glass spray
serum with amber oil and rose-gold collar. Every printed line, letterform, stroke
weight and kerning pair is fixed exactly as shown: do not re-letter, re-draw,
re-space, warp or substitute any glyph, do not add a tagline, do not translate the
label.

Consistent world across all beats: a field of dusty mauve-rose, lit as a soft gradient
one stop brighter at upper camera-left, falling to deeper mauve at lower camera-right.
The product stands on a single unbroken plane of honed travertine in the same mauve,
filling the lower third, with its own soft reflection in the stone. Nothing else is on
the plane and nothing is visible beyond it — no props, no second object, no wall, no
room, no horizon above the plane. Palette: low-saturation mauve-rose throughout, plus
the amber of the oil and the rose-gold of the collar — no other colour in frame, in any
beat.

Structure: alternating, not a reveal. The complete product is fully visible in beat 2
and again in beat 5. This is intentional — do not withhold it.

Motion split: the product moves only where a beat names it — the tip and settle in SHOT
2 — and is otherwise locked, with no bobbing, drifting, rotating or scale change. The
oil's bubbles, the condensation and the falling droplet move at realtime physical speed
with surface tension and gravity intact. The camera is locked in every beat; where the
product or its matter moves, the camera does not. Nothing is speed-ramped, nothing is
slow-motion.

SHOT 1 — INSIDE THE OIL (0–1.7s), extreme macro, 100mm macro. Camera locked, framed
through the glass into the amber oil: small round bubbles suspended at several
depths, the nearest sharp, the rest falling to bokeh, drifting upward at realtime
speed. No product silhouette is readable yet. HARD CUT out.

SHOT 2 — WHOLE, AND IT MOVES (1.7–2.6s), medium, 85mm. HARD CUT in. The complete bottle
stands at a 10-degree rake on the travertine plane, off-centre to camera-left, fine
condensation across the glass. Camera locked. The bottle tips 12 degrees further toward
camera-left over 0.5 seconds, reaches the tilt, and settles back to its 10-degree rake
over 0.4 seconds with one small overshoot and no wobble after; realtime gravity. Its
contact shadow shifts with it. HARD CUT out.

SHOT 3 — DETACH (2.6–3.3s), extreme macro, 100mm macro, camera at the level of the pump
mouth and 25 degrees off it. HARD CUT in. A single droplet of the amber serum gathers at
the mouth, detaches, falls 6 centimetres under realtime gravity and lands on the plane
below, spreading to a 1-centimetre disc. Camera locked. No slow-motion, no crown, no
splash. HARD CUT out.

SHOT 4 — LABEL RAKE (3.3–5.0s), extreme close-up, 100mm macro, camera above and
right. HARD CUT in. The bottle lies at a 40-degree rake, its printed face filling
frame; only FORMULE and ANTI-AGE are within the crop and both are cut by the right
frame edge — this crop is deliberate, do not pull back to fit the label, do not
complete any letter beyond the frame. Camera locked. One thin hard specular travels
along the letterforms from the left of FORMULE to the right of ANTI-AGE across 1.6
seconds at a constant rate. HARD CUT out.

SHOT 5 — LANDING (5.0–7.0s), medium close, 85mm. HARD CUT in. The complete bottle
upright and composed on the lower third, camera stopped dead and absolutely still for
the full 2 seconds. Across those 2 seconds the field darkens one and a half stops
at a constant rate while the bottle's own exposure holds exactly; the hue does not
change.

Light: one large soft diffused panel high at camera-left raking at 30 degrees. The
shadow side of the bottle keeps detail and resolves to a deeper mauve, never black. A
thin hard specular runs the glass edge nearest the source; a soft mauve contact
shadow sits beneath. NO god rays, NO beams, NO flare, NO bloom, NO rim light from
behind, NO second source, NO black shadow.

Transitions: hard cuts only, on the beat boundaries above. No dissolves, no fades, no
wipes, no whip transitions, no morphs.

Audio: silent. No music, no room tone, no sound design.

Constraints: the label is pixel-exact to @Image1 — same letterforms, weights,
spacing, proportions; never re-lettered, never warped, never substituted; no
additional text, no tagline, no captions, no watermark, no URL. One environment only:
the mauve field, unchanged in hue across every beat. No charcoal or black void, no
dark studio, no true blacks, no low-key grade, no teal or blue cast. No water
splashes, no petals, no flowers, no silk, no leaves, no floating particles, no
glitter, no sparkles, no steam, no smoke. No light streaks, no shine sweeps beyond the
two speculars named above, no glints, no bars or bands crossing frame, no gradient
sweeps, no lens flare, no bokeh particles, no rings or ripples around the product. No
slow-motion, no speed ramping. No long static holds before the final beat — keep
cutting.
```

### MAX 2 — Suspended Cluster Drift

Five to nine copies of **the same product** turning slowly at different depths in a
high-key field. One continuous shot, no cuts, 5–7 seconds.

It comes in two versions and they are not interchangeable, because a loop requires the
last frame to match the first:

- **Looping** — camera **locked**, every copy completing a **full 360°** over the
  duration. Head and tail are identical, so the seam is invisible. There is no parallax
  in this version; the depth reads from scale, occlusion and the focus falloff instead,
  and the interest comes from seven copies presenting different faces at once. Use this
  for a page background.
- **Non-looping** — camera tracks laterally through the cluster, copies turning a
  quarter turn. Richer, and the version to reach for when the clip plays once. It
  cannot loop: the frame ends 12cm from where it started and every copy ends 90° off
  its start attitude.

The prompt below is the looping version. To get the other, swap the locked camera for
the lateral track, drop the full turn back to a quarter, and remove every loop clause.

Alongside the minimal mode, this is the one shape in this skill where a single
continuous take with no cuts is the correct answer — the density lives in the cluster
rather than in the edit, and because every copy is turning at every moment there is no
unstaged time for the model to fill with an invented cut.

**Reach for this family more often than feels natural.** It is the one shape here where
the product is unambiguously *doing* something, and it is the antidote to a page of
pieces that are all a locked bottle under a moving specular. If the last thing you made
for this product was a locked macro chain, make this next.

Three variants. The prompt below is the first; the other two are worth having in hand:

| Variant | Shape |
|---|---|
| **Cluster turn** (below) | Seven copies, locked camera, one full 360° each, zero cuts, loops |
| **Attitude cuts** | A cut piece: three or four ~1.2s beats, each on a *different* copy at a different attitude and depth, hard cuts between them, the cluster visible behind each. Fast, editorial, does not loop. |
| **Single tumble** | One copy only, tumbling one full revolution about a horizontal axis across 5 seconds, locked camera, macro enough that the label passes through frame twice. The cheapest way to get real product motion into a piece. |

The locks come from the mid-air choreography section of
`../references/dimensional-motion.md`, with one divergence: those are three or four
*different* objects, and this is many copies of *one*. That changes two things — the
copies may overlap and occlude freely, and the count can go past four, because
identical objects read as a pattern rather than as soup.

```
Format: Single continuous shot, beauty product cluster suspended in air, 6 seconds,
9:16, high-key clean grade, no on-screen text, silent, seamlessly loopable.

References: @Image1 as the hero product — the translucent green-glass bottle with the
pale grey cap. Every printed line on the label stays exactly as shown; do not
re-letter, warp or substitute any glyph, and do not add text.

World: an infinite seamless near-white bone field, soft and shadowless except for
faint diffuse contact shadows. No horizon, no floor seam, no surface, no props.
Palette: bone white plus the pale green of the glass and the grey of the cap — no
other colour.

Motion split: seven identical copies of the product are suspended in mid-air at seven
different depths, spread across the frame, none centred. Each holds its own fixed
position in space — none rises, falls, drifts laterally or changes scale. Each rotates
in place about its own vertical axis at the same constant rate, all in the same
direction, completing exactly one full 360-degree turn across the 6 seconds so that
every copy ends at precisely the attitude it started in. They may overlap and occlude
one another and are always correctly occluded by depth; they never interpenetrate. The
camera does not move at all. Realtime speed, no slow-motion, no speed ramping, no
bobbing, no floating drift.

SHOT 1 — CLUSTER TURN (0–6s), medium, 50mm. The camera is locked and absolutely still
for the entire take — no track, no push, no drift, no reframe. The seven copies turn
in place at a constant rate through one full revolution. The nearest copy is sharp and
its label legible; copies further back fall progressively to soft bokeh. As each copy
turns, its faint contact shadow shifts with it, staying diffuse, and returns to its
starting shape as the copy completes its turn. Nothing else happens.

Light: broad soft overhead diffusion filling the field evenly, plus one slightly
stronger soft source at camera-left giving each bottle a gentle gradient across its
body and a thin bright edge where the glass turns away. The green glass transmits —
the field is visible through each bottle, tinted. NO hard shadows, NO black, NO
specular hotspots, NO flare, NO bloom, NO caustic patterns on a floor, because there
is no floor.

Audio: silent.

Constraints: seven copies of the same product, identical to @Image1, all labels
pixel-exact — no variant packaging, no different colours, no other product. One
environment: the bone field, unchanged. No charcoal, no dark background, no gradient
sweep. No water, no splashes, no petals, no leaves, no particles, no glitter, no
bubbles in the air. No light streaks, no bars, no rings, no ripples. No cuts, no scene
changes, no second angle — this is one continuous shot. The first and last frames are
identical in composition, attitude, scale, field level and hue so the clip loops
seamlessly: the camera never moves, every copy completes a whole turn, and there is no
grade change, no darkening, no fade in and no fade out.
```

Practical notes:

- **Seven is a good count.** Five reads sparse, twelve reads like a warehouse.
- **One copy is the hero** — nearest, sharpest, label legible. Without that
  designation every copy comes back equally soft and the piece has no subject.
- **The shadows are the tell.** `its faint contact shadow shifts with it, staying
  diffuse` is what stops the cluster reading as a flat collage.
- **Never a push.** In the non-looping version the move is a lateral track, which is
  what produces the parallax through the cluster; pushing in instead makes the front
  copy dominate and flattens the depth. In the looping version there is no camera move
  at all, and the depth comes from scale, occlusion and focus falloff.
- **The full turn is what buys the loop**, and it is worth restating in the tail. Given
  "a quarter turn" plus "loops seamlessly" the model resolves the contradiction itself,
  and the usual casualty is the turn — the copies go nearly static and the piece
  becomes the pretty-but-empty failure this register opens by warning about.

### MAX 3 — Extrude And Texture

For a tube, pump or dropper — anything that dispenses. The product's own matter is the
protagonist and the packaging is the supporting cast.

The build, six beats: label crop → **the whole product at a rake** → the extrude →
blur whip → the matter as an abstract texture field → the whole product again, graded
down. Beat two is the whole product, not the nozzle — this register identifies the
product early, and a build that saves it for the end contradicts the alternating
structure the prompt itself asserts. The strong optional beat is the product held above
its own dispensed pool, the frame divided hard and horizontally — packaging in the
upper two-thirds, a field of the actual cream across the lower third, seen nearly
edge-on.

**Six beats is two generations, not one.** Seedance commits to three or four, so buy
beats 1–3 as one take and 4–6 as another, then trim and assemble per the cadence
section above. Keep the world block byte-identical across both or the field will not
match at the seam, and chain the second take from the last frame of the first if the
schema exposes it. Six beats in one buy is where the tail comes back as a degraded
replay of beat two.

**Every timecode below is relative to its own take, not to the finished piece.** Each
generation is a separate submit and its timeline starts at 0 — a prompt whose first beat
opens at 6.1s buys six seconds of nothing. Renumber when you split, and state the take's
own duration in its format line.

```
TAKE 1 / SHOT 3 — EXTRUDE (3.4–5.2s of a 5.2s take), extreme close-up, 100mm macro,
camera 25 degrees off the
nozzle axis and slightly below it. HARD CUT in. The tube enters frame from upper-right
at a 40-degree rake, nozzle at frame centre; the lower third of frame is a field of
the dispensed white cream seen nearly edge-on, its own soft shadow beneath it, the
division between the two hard and horizontal. A ribbon of cream extrudes from the
nozzle over 1.5 seconds at a constant realtime rate and folds over once, holding a
soft peak — it does not drip, run, string, or overflow. Camera locked. Surface
tension intact, realtime physics, no slow-motion.

TAKE 2 / SHOT 2 — MATTER (0.8–3.1s of a 5s take; beat 5 of the finished piece), extreme
macro, 100mm macro. HARD CUT in. The frame is
filled edge to edge with the cream itself, combed into even parallel ridges running
diagonally; no packaging is visible and there is no readable context. The camera
tracks laterally 3 centimetres across the ridges over 2.3 seconds at a constant rate,
dead level and parallel to the surface, the raking source catching each crest and
throwing a soft shadow into each trough. Nothing moves but the camera.
```

The texture beat is the longest hold in the piece — around 2.3 seconds — because the
viewer needs a beat to recognise what they are seeing. That recognition *is* the
event. Do not put a camera move and a substance event in it; the abstraction is
enough.

## Loop Discipline

Most page heroes loop. What a loop requires depends on whether the piece cuts, and
conflating the two cases is what produces a loop nobody can make work.

**Three rules for both cases:**

- **The seam is a hard cut, never a crossfade.** A crossfade at the seam is visible as
  a pulse on every repeat.
- **Field level and hue must match at the seam.** This is the one thing a cut cannot
  hide: a tail a stop darker than the head reads as a flash every time the clip
  repeats. It is also why **the closing stop-down is incompatible with looping** in
  either case. Pick the loop or pick the grade drop.
- **Irreversible events go in the middle.** A cream ribbon cannot un-extrude and a
  merged condensation bead cannot un-merge. Put anything one-way at the centre of the
  piece, never within a beat of either end.

**A continuous take** — MIN 1, MIN 2, MAX 2 — has no cut to hide anything, so head and
tail must match in **everything**: composition, product attitude, scale, focus, field
level and hue. That rules out any one-way move. The only motion that survives is
**cyclic**: a full 360° turn, a specular that travels out and returns, a field that
breathes up and settles back. A lateral track that stops cannot return to its head, and
a focus pull that arrives cannot un-arrive.

**A cut piece** — MAX 1, MAX 3 — loops across a hard cut, and a cut is *allowed* to
jump. Composition, scale, attitude and focus need not match at the seam: a macro of the
formula cutting back from a medium of the whole bottle is indistinguishable from every
other cut in the piece. Match field level and hue, keep one-way events away from both
ends, and the seam disappears.

**Verify the seam by concatenating the clip to itself** and watching the join, not by
comparing the first and last frames — for a cut piece those two frames are *supposed*
to differ.

```bash
printf "file '%s'\nfile '%s'\n" loop.mp4 loop.mp4 > /tmp/l.txt && \
ffmpeg -y -f concat -safe 0 -i /tmp/l.txt -c copy /tmp/loop-x2.mp4
```

## Aspect And Delivery

A page hero is almost never needed in one shape. Compose so the crops survive:

- **Keep the product inside the centre 60% of frame** on both axes. A 16:9 desktop
  hero, a 1:1 card and a 9:16 mobile block get cut from the same master only if
  nothing important lives near an edge — which is in direct tension with the label
  crop device, so use the rake on the beats you will not re-crop.
- **Generate vertical if mobile is the primary surface**, and re-frame outward for
  desktop rather than the reverse. Upscaling a crop of a horizontal master loses the
  macro detail that this register is entirely about.
- **Textless, always.** The page owns the type. If the user wants a headline or a
  price on it, that is composition in post — route per the type note in `SKILL.md`.
- **Silence is a delivery step, not a submit flag.** Seedance forces generated audio on
  every take whatever the prompt says. Keep `Audio: silent` — it stops the model staging
  beats around an imagined bed — then strip the track and hand back the stripped file:

  ```bash
  ffmpeg -y -i take-approved.mp4 -c:v copy -an hero-loop.mp4
  ```

## Verify

Beyond the standard contact sheet and scene detection in
`../workflows/cinematic-shot.md`, this register has five failure modes worth checking
explicitly on the last frame and across the sheet:

1. **Field creep** — a second colour has entered, or the hue has shifted between
   beats. Sample the field at the same frame position in every beat.
2. **Charcoal drift** — the shadow side has gone to true black, or the field has
   darkened toward a studio void. The register has collapsed into the other one.
3. **The monoculture** — the product is locked in every beat and the only thing moving
   is a specular or the camera. This is the most common failure in this register and the
   contact sheet shows it instantly: every cell is the same object in the same attitude
   under slightly different light. Restage the weakest beat as an action beat per
   `## Motion`.
4. **Label integrity at macro** — check every glyph in the cropped beats
   per-character, not at a glance. Macro is where re-lettering happens.
5. **Substance speed** — the liquid or cream event must read realtime. If it looks
   beautiful, it is probably slow-motion; the model adds it unasked.
6. **Cut count** — in maximal mode, an 8-beat plan that scene-detects as 3 is a failed
   generation, not a stylistic variant. See `../references/cut-architecture.md` on beat
   density. In minimal mode the test inverts: MIN 1, MIN 2 and MAX 2 declare a single
   continuous take, so zero detected cuts is the pass and **any** detected cut means
   Seedance invented one to fill unstaged time. Restage that take with the no-cuts
   clauses in both the format block and the tail.

## Banned Here

- Charcoal or black voids, dark studio backgrounds, true blacks on the shadow side,
  low-key grades — the whole dark register, which the model defaults to on the word
  "dramatic".
- Any surface, table, plinth, riser, podium, shelf or floor. There is only the field.
- Water splashes, pouring, submerging, petals, flowers, silk, sliced fruit, leaves as
  dressing, floating particles, glitter, sparkles, steam, smoke, ink blooms.
- More than one substance event, or any substance the product does not contain or
  produce.
- A second background colour, a gradient sweeping across the field, a vignette, or a
  horizon.
- Slow-motion on liquid, and pace adverbs standing in for a quantified move.
- The product dead-centre and upright anywhere but the final landing.
- Two blur whips, or a blur whip at the loop seam.
- On-screen text of any kind, including a tagline under the mark.
- Everything on the cheap list in `../references/cinematic-craft.md`.
