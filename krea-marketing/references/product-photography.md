# Product Photography

Use this reference for editorial product photography in marketing work: packshots, hero frames, still lifes, launch and campaign imagery, PDP and marketplace crops, social and paid-social stills, editorial product features, gifting and bundle shots, and product restyling or re-lighting from a supplied reference image.

## Use this reference when

Shooting or generating photography of a physical product: packshots, hero frames, still lifes, launch and campaign imagery, PDP and marketplace crops, social and paid-social stills, editorial product features, gifting and bundle shots. Covers beauty, skincare, fragrance, haircare, body care, supplements, beverage, food, homeware, accessories, small hardware. Also covers restyling, reshooting, or re-lighting a product the user supplies as a reference image.

Do not use this reference for: typographic posters and ad layouts, packaging artwork and label design itself (`../workflows/product-packaging-design.md`), garments worn on bodies, or non-product abstract imagery.

## Core direction

This is a **photography** brief, not a graphic-design system. The output is a photograph of a real, specific, credibly designed object sitting in real light on a real surface. Everything below exists to keep the frame physical, chromatic, and dramatically lit.

**The user's request always outranks this skill's defaults.** Before naming any decision below, check what the user already said — a color, a mood word ("moody", "playful", "clinical", "cozy", "summery"), a season, a material, a specific setting (kitchen counter, gym bag, bathroom shelf, a reference image, a competitor's ad), a brand's existing palette, or an aspect ratio. Anything the user names is a constraint this skill must satisfy, not a preference it can override because a different choice fits the doctrine better:

- A **named or implied color or mood** selects the palette strategy and the actual hue — translate it into the closest entry in [Color](#color) rather than substituting whichever hue reads best on its own (e.g. "moody and dark" → Drained warm film or Chiaroscuro shaft, not a bright saturated field; "playful and summery" → Deep sky cobalt or Lavender under Open-sky contre-jour, not Oxblood).
- A **named setting or environment** selects or overrides the staging mode — a real place the user describes outranks a default studio field.
- A **reference image or described shot** should be matched as closely as this skill's vocabulary allows — its light, palette, and staging, not the nearest worked example below.
- Only fall back to this skill's own defaults for any axis (lighting register, palette, staging, props) the user left unspecified. Never silently drop a user-specified detail to fit a cleaner recipe.

With that constraint applied, make four decisions **explicitly, in writing, before you draft a prompt**:

1. **Lighting register** — pick exactly one of the seven in [Light and drama](#light-and-drama). Name it.
2. **Palette strategy** — pick exactly one of the six in [Color](#color). Name the actual hue.
3. **Staging mode** — pick exactly one of the six in [Object positions and staging](#object-positions-and-staging). Name it.
4. **Finish** — clean digital, or film-grained. All-or-nothing, decided up front.

Then write the prompt using the ordering template in [Prompt construction](#prompt-construction). Never blend two lighting registers, never blend two palette strategies, and never hedge in the middle of a decision. Half-committed is the single most common failure.

**The product is a specific object, not an abstract module.** Give it real proportions, a real closure mechanism, real material thickness, a real label with a real (invented) name set in a real typeface. Do not generate anonymous cylinders, rounded-rectangle blobs, or "a generic bottle". Vagueness in the prompt is what produces the flat, weird, empty images this skill exists to prevent.

## The look in one paragraph

Editorial commercial photography with the confidence of a small independent brand's launch campaign: a fully committed saturated backdrop or a genuinely real environment, one hard light source low or raking, long knife-edged shadows treated as part of the composition, color that is either fully saturated or deliberately drained with nothing in between, glass and liquid and cotton and skin doing the material work, hands entering the frame to hold, pour, lift and grip, props chosen with deadpan wit rather than decorative taste, packaging rendered legibly and specifically, and the whole thing finished either perfectly clean or with honest film grain over the entire frame. It should look like it was photographed on a table by a person with one light and strong opinions — not rendered in a studio simulator.

---

## Color

Color is the loudest variable in this aesthetic and the one most often botched. Read this whole section.

### Saturation policy

Saturation is **bimodal**. Pick one and hold it frame-wide:

- **Fully committed** — the dominant field is a real, high-chroma, paint-or-paper color at roughly 60–95% of the reference gamut. It reads as an intentional brand color, not a tint. This is the default for anything shot against a backdrop.
- **Deliberately drained** — overall saturation pushed low with a warm cast, in the register of expired film or tungsten room light. Dusty, putty, olive, tarnished. Not grey: still warm, still colored, just quiet.

**Never the middle.** A "tastefully desaturated" mid-chroma frame is the signature of default AI product photography and is banned. If you catch yourself writing "muted pastel", "soft neutral tones", or "subtle color palette", stop and re-commit to one of the two poles.

### The six palette strategies

Pick one. The parenthetical hex values are anchors for your own calibration — write the **words** into the prompt, not the hex codes, which image models handle poorly.

**1. Saturated seamless field** — the workhorse. One flat, unbroken, high-chroma paper or painted backdrop occupying 55–90% of the frame; the product sits against or on it. No gradient wash, no vignette, no horizon line, no second color in the field. At most a faint falloff where the light rolls away, plus the shadow the product actually casts.

Named field hues that belong to this aesthetic:

| Field hue | Character | Pairs with |
| --- | --- | --- |
| Brick terracotta (`#a8503f`) | Warm, earthed, skin-flattering | Skin, matching terracotta packaging, cream type |
| Scarlet / crimson (`#c8202a`) | Loud, graphic, confrontational | Black velvet, white poplin, warm wood, chrome |
| Oxblood / deep red (`#7d1f22`) | Dense, dramatic, low-key | Brass, amber glass, near-black shadow |
| Mustard ochre (`#c9a14a`) | Sour, deadpan, mid-century | Raw pine, deep red glass, steel |
| Cerulean / workwear blue (`#3f7fa8`) | Cool, clinical, structural | Frosted glass, black-and-white labels, steel |
| Deep sky cobalt (`#1b4f9c`) | Open-air, joyful, backlit | Teal glass, cream labels, sunlit skin |
| Lavender (`#a58fd0`) | Playful, dairy-adjacent, mottled | Cream cartons, ribbed clear glass, milk |
| Sage grey-green (`#a8b2a4`) | Quiet, cool, archival | Kraft paper, smoky glass, film grain |
| Bone / pale cool grey (`#e4e4e2`) | High-key, product-forward | A single long grey shadow, tiny navy-and-gold marks |

The backdrop may be seamless paper, a painted wall, or a mottled hand-sponged wall — mottling is permitted only as low-frequency painterly unevenness in a single hue, never as a texture pattern.

**2. Chromatic loop — product matches ground.** Lock one hue across the backdrop, the surface, and the packaging so the frame is effectively monochrome in color. Separate the product from the field using **value and specularity only**: gloss against matte, a chrome collar, a hard shadow edge, a silhouette. This is the most sophisticated move in the set and the most reliably striking. Red-on-red and blue-on-blue are the proven pairs. Hands crossing a matching field are permitted and encouraged.

**3. Complementary collision.** One committed field hue, plus exactly one opposing hue introduced as either a gelled light spill on one third of the frame, or a single object. Weight them unequally — roughly 80/20. Proven collisions: scarlet field with a hard teal-cyan light spill on the right; deep red glass on mustard ochre; cream product against cerulean; teal-green glass against cobalt sky; red-and-white check against nude packaging.

**4. Warm daylight neutral.** The neutral mode, and the one most at risk of collapsing into the banned stone aesthetic. Its neutrals come from **textile, paper, skin, and sand — never from a stone slab**: oat and sand plaster wall, cream linen gauze, cotton canvas, unbleached kraft, uncoated label stock, pale rippled beach sand, warm hand and forearm skin. The single warm accent is always **material, never paint**: amber or cognac liquid inside glass, tortoiseshell acetate, brushed brass, raw pine. Backlight the amber so it glows and throws a warm caustic onto the surface.

**5. Drained warm film.** Dusty putty linen, olive-green stems, tarnished silver, brown bottle glass, oxidised brass, warm beige wall, dim rosé in a glass. Low saturation, warm cast, deep but not black shadows, visible grain. Reads as a domestic evening tabletop shot on expired film. Nothing in it is bright.

**6. High-key white and black.** Zero chroma except skin. White waffle terry, white cotton canvas, white poplin, white HDPE, matte soft-touch black plastic, black glass, black type. Skin is the only warm element and does all the color work. Bright, flat, tactile, intimate.

### Warm, cool, and shadow color

- Shadow color stays inside the family of the light and the field. A terracotta field throws a deeper terracotta-brown shadow. A lavender field throws a violet shadow. A cerulean field throws a navy shadow. **Never fill a shadow with neutral grey or an unrelated blue.**
- Where warm and cool coexist, weight them 80/20 and let one be structural (the field) and the other incidental (a light spill, one object, one reflection).
- Amber, cognac, honey, and gold appear as **liquid or resin or metal**, lit from behind. They never appear as a background color and never as a "premium gold" grade.
- Skin is a color. Include real skin tone variation across multiple hands in one frame where hands are used; it is both truer and chromatically richer than a single hand.

### Color bans

- No mid-chroma "tasteful" desaturation. No dusty-pink-and-sage bathroom palette.
- No neutral grey backgrounds as a default rest state, and no white seamless sweep.
- No gold-on-black luxury grade. No rose-gold. No holographic or iridescent gradient.
- No digital neon or screen primaries (`#FF0000`, `#00FF00`). Field hues are pigment colors, mixed and slightly dirty.
- No two competing saturated fields in one frame. One field, one optional 20% counter-hue.
- No gradient background of any kind, including subtle radial "studio" falloff behind the product.

---

## Contrast and tonality

- Contrast is **high by default**. The reference register runs a 4:1 to 16:1 key-to-shadow ratio under hard light. Fill is minimal or absent; if a fill exists it is a bounce off the field itself, not a second lamp.
- **Blown highlights are permitted and often correct.** Direct sun on white cotton, on a glossy cap, on wet glass may clip to pure white in small areas. Do not roll every highlight off in the name of safety.
- **Genuinely black shadows are permitted and often correct.** Under direct sun or hard flash, the unlit side and the cast shadow may fall to near-black with no detail recovery. A frame may carry a large true-black region — an unlit corner, dark water, a velvet table, a room falling away behind a shaft of light.
- Where the register is soft and high-key instead, compress the whole frame into the upper third of the tonal range with no true black anywhere and only faint contact shadows. That is a different, equally committed choice.
- Value structure per frame is one of three, chosen deliberately:
  - **Three-pole** — near-white pole, saturated mid-field, near-black anchor. Most common.
  - **Two-pole split** — a knife-edge boundary carves the frame into a lit half and a dark half, with almost nothing in between.
  - **Compressed high-key** — everything in the top third of the range, no true black, separation by texture and faint shadow.
- Earn the focal read from **value contrast against the field**, not from centering or size: a white bottle on a black rockpool, a bright label inside a dark wedge of shade, a chrome collar against matte red.
- No HDR tone-mapping, no shadow-lifting, no clarity or structure sliders, no local-contrast halos. Contrast comes from the lighting decision, not from a grade.

---

## Light and drama

The most important section. Light is where this aesthetic lives, and "dramatic" here means *one hard source doing something specific*, not stacked effects.

### The drama doctrine

- **Exactly one dominant source per frame.** Every shadow, highlight, caustic and gradient in the frame agrees with its single incident angle. Two disagreeing shadow directions is the clearest tell of a fake image.
- **The source is hard unless the register says otherwise.** Hard means a small effective source: bare sun, an unmodified flash, a bare bulb, a window edge — producing crisp shadow edges you could trace.
- **The cast shadow is a compositional object, not a by-product.** Design it: its direction, its length, its edge quality, where it exits the frame. It should be as large as or larger than the object throwing it, and it should run on a different axis from the object so the frame carries two overlaid compositions.
- **Drama comes from one physical mechanism**, chosen per frame: a raking shadow, a knife-edge light boundary, a caustic through glass or water, a backlit translucent liquid, a two-pole chiaroscuro split, a hard flash shadow on a colored wall. Pick one. Never stack them, and never simulate any of them with a filter.
- **Light-direction default:** from the upper-left or upper-right at 25–45° above horizontal and 20–60° off the lens axis, so the shadow travels diagonally across the surface toward the opposite lower corner. Straight-on frontal light and pure top-down light are both deliberate, less common choices.
- Where a dappled foliage shadow is used, it falls across a corner or the lower third as a secondary broken pattern, always subordinate to the primary hard shadow, and never across the label.

### The seven lighting registers

Pick one. Each specifies angle, quality, ratio, shadow behavior, and what it is for.

**A — Hard low raking sun.** A single hard source 15–30° above the horizon, 40–70° off axis. Long shadows, 1.5–3× the height of the objects, travelling diagonally across the surface and often exiting the frame. Ratio 8:1. Shadow edges crisp near the object's contact point and very slightly softening along their length. Warm color temperature (4000–5000K), slightly golden. Best for: hero packshots, flat-lays on sand or plaster, lineups on a shelf or in shallow water. This register is what makes a plain object monumental.

**B — Direct overhead noon sun.** A hard source 60–85° overhead, slightly off axis. Short, dense, hard-edged shadows pooling tight to each object; blown highlights on white and glossy surfaces; unlit areas dropping to true black. Ratio 16:1 or beyond. Often combined with a dappled foliage gobo. Best for: overhead flat-lays on sand, in water, or into an open bag; anything that should feel like an actual hot afternoon.

**C — Hard flash on a colored seamless.** A single small unmodified flash near the lens axis or 20–40° to one side. A crisp, slightly rimmed shadow thrown onto the backdrop just behind and beside the product; flat frontal modelling on the product itself; specular pops on gloss and chrome. Ratio 6:1. Slightly cool-neutral (5500K). Best for: saturated-field studio frames, deadpan prop set-ups, playful FMCG and beverage, macro cosmetics. This is the register with the most graphic snap.

**D — Soft flat daylight.** A large window or overcast sky, near-frontal, minimally directional. Near-shadowless: only faint contact shadows and gentle wraparound modelling. Ratio 2:1. High-key, compressed tonality, no true black. Best for: intimate close crops of a product held in hands, objects on rumpled bedding, tactile textile-heavy frames, clean FMCG lineups. This is the only register where the product may be softly lit — use it when touch, not drama, is the subject.

**E — Chiaroscuro shaft.** A single hard shaft entering from one side, low, catching the product and a wedge of the surface while the rest of the room falls to near-black. Ratio 16:1 or beyond. The lit wedge is itself a hard-edged geometric shape and part of the composition. Warm (3200–4000K). Best for: wine, spirits, fragrance, evening tabletop still lifes, anything that should feel like late light through a doorway.

**F — Open-sky contre-jour.** The product held or raised against open sky with the sun behind or beside it. Translucent bodies and liquids glow; opaque parts fall toward silhouette; edges catch a hot rim; slight halation and lens flare bloom are acceptable **only** as a genuine optical artifact of shooting into the light. Ratio 12:1 against the sky. Best for: bottles held aloft, beverages, anything glass, anything joyful.

**G — Found practical light.** The light that actually exists in the location: a fridge's interior lamp, an office ceiling grid, a bathroom window, a shop's fluorescents, a car interior. Color-cast, uneven, unflattering, real. Ratio varies. Best for: product-in-context frames, reportage-flavoured lifestyle, editorial features where the product is incidental to a scene.

### Optical effects: permitted and banned

Permitted, when physically caused by the chosen register:

- Caustics: light refracted through amber or colored glass throwing a warm patch onto the surface; sun through moving water rippling gold across a submerged rock.
- Halation and a soft bloom around a hot highlight, in register F only.
- Real lens flare shooting into the sun, in register F only.
- Reflected color bounce: a red field throwing red light onto the underside of a white object.
- Refraction and distortion of what is behind a glass body or a liquid.
- Fingers and a glass's contents visibly distorting and magnifying behind the glass.
- Condensation, water beads, running water, spills, and drips — physically placed, following gravity.

Banned outright:

- Rim light on a black background. Chrome-ring kicker highlights. Twin symmetric strip highlights on a bottle.
- Softbox-plus-fill-plus-hair-light three-point studio setups. Any lighting that reads as "product studio".
- Any glow, bloom, haze, fog, dry ice, god-ray, or volumetric beam not caused by register F.
- Applied vignettes, filter grades, "cinematic teal-orange" LUTs, lens-blur backgrounds.
- Frozen water-crown splashes, floating ingredient explosions, levitating products with an airbrushed reflection.
- Any second shadow disagreeing with the first.

---

## Materials

Material contrast is the second engine of this aesthetic, equal to color. Combine **two to four** distinct surface behaviors per frame so the single light source performs differently across the scene: one thing that absorbs it, one that transmits it, one that reflects it.

### The material vocabulary

Use these by name in prompts. Specificity here is what produces tactile output.

**Glass** — clear soda-lime with visible seams and a thick base; frosted or satin-etched; smoked grey; amber and cognac apothecary glass; teal-green bottle glass; deep red translucent flacon glass; ribbed or fluted drinking glass; cut crystal.

**Liquid** — whole milk, opaque and heavy; still or pouring in a smooth rope; wine, rosé, amber cordial; olive oil; clear serum with a visible meniscus; running water over a surface; standing water 5–10mm deep with concentric ripples; condensation.

**Metal** — brushed brass with directional grain; polished stainless with soft distorted reflections; a chrome collar or engraved ring; anodized bronze or copper caps; a plain aluminum screw cap; a silver serving tray.

**Plastic** — matte soft-touch black; nude, blush, or bone injection-molded with a satin finish; white HDPE; a molded pump head with a visible seam and hinge.

**Textile** — white waffle-weave terry; a rumpled cotton bedsheet; heavy cotton canvas tote; loose cream linen gauze; putty linen tablecloth; black velvet, light-absorbing to near-zero; crisp white poplin shirting with pressed sleeve creases; red-and-white terry check; a chunky lurex knit.

**Paper and card** — crumpled kraft or tissue wrapping with sharp creases; uncoated label stock; matte seamless backdrop paper; loose stacked documents.

**Wood** — a raw pine offcut with visible end-grain and saw marks; a live-edge log round with bark and growth rings; polished mahogany reflecting a warm shaft; wood shavings and curls.

**Found mineral and ground** — wet river rock with a golden mineral surface; pale beach sand, rippled and rake-marked; a rough cream plaster wall with chips and patches. These are **landscape and architecture**, encountered in place. They are never a slab, tile, riser, or prop cut to size.

**Skin** — hands and forearms across a range of skin tones, with visible knuckles, tendons, veins, nail shape, cuticles, small scars and tattoos, and the pressure-pale patches where fingers grip.

**Found environment** — a fridge interior with wire shelves and molded plastic; glass shelving with visible edge-green; a white wire crate; office carpet; a bathroom counter; a desk underside.

### Surface honesty

- Keep every physical imperfection: fingerprints on glass, dust, water trails, a lint fibre on velvet, a slightly crooked label, a chipped plaster patch, a spill, a saw mark. Do not retouch toward generic smoothness.
- Imperfection must be **physically motivated**. Do not add fake distress, fake paper texture overlays, or artificial wear to an object that would not have it.
- The focal product usually carries the *least* texture; the surface and surround carry the most. Refinement reads as refinement only against roughness.
- Gloss budget: one to two genuinely glossy or mirror-finish elements per frame. Everything else matte to satin. Glossy-everything is a collapse.
- Reflections are soft, slightly distorted, lower in contrast than their source, and often broken by ripple or texture. Never a crisp ray-traced mirror double.

### Banned materials — read this twice

**Marble is banned. Travertine, onyx, quartz, terrazzo, granite, and every other polished stone slab is banned.** So is any stone or concrete pedestal, plinth, cube, step, cylinder, or riser; any floating acrylic or glass riser; any arch-shaped stone niche. If a mineral appears it is a wet river rock in a rockpool, a plaster wall in a room, or sand on a beach — encountered where it lives, never cut into a prop and never used as a surface for the product to sit on.

Also banned: white seamless sweep with a soft gradient; silk or satin drape swooshes; the spa cliché of an orchid plus folded towel plus stacked river stones; gold foil on black; brushed-gold everything; dry ice; glitter; abstract flowing chrome blobs; iridescent film; generic "luxury texture" backgrounds; a product standing on its own reflection in a void.

If a prompt draft contains the word "marble", "travertine", "pedestal", "plinth", or "podium", delete it and choose a real surface from the vocabulary above.

---

## Object positions and staging

Where things sit, and how they touch. Answer all of these before writing the prompt: what surface, what height, what angle, what shadow direction, what enters from an edge.

### The six staging modes

**1. Found-riser frontal.** Eye-level or slightly above, product standing on a found object that acts as a plinth without being one: a raw pine offcut, a live-edge log round, an upturned crate, a stack of books, a glass shelf, a wire basket, a step of the actual furniture. The riser is visibly a real thing with its own material story. Product sits off-center, 40–60% across, its base 55–75% down the frame, with the field open above it. Shadow travels across the riser and onto the field behind.

**2. Overhead flat-lay, off-axis.** Camera straight down, 90°, but the **arrangement is off-axis**: nothing parallel to the frame edge, objects at 10–35° to each other, at least one object cropped by an edge, at least one textile or drape entering from a corner. Objects rest in a single flat layer and *touch or nearly touch* — they never float in even isolation. Circular forms foreshorten to true circles; use their shadows to build the diagonal the arrangement lacks.

**3. In hands.** See the hands rules below. The product is held, lifted, gripped, poured, or passed. Camera close, often cropping the hands at the wrist or forearm.

**4. In a real environment.** The product placed where it would actually be: in a fridge among other bottles, in an open beach bag on a towel, on a wet rock in a stream, on a bathroom counter, on a bed, on a restaurant table. The environment is rendered with its own real clutter and its own practical light (register G, or hard sun entering it).

**5. Lineup and family.** Three to eight units of a range arranged as **repetition with variation**: differing heights, two or three of the same SKU at different depths, one turned slightly off-parallel, one cropped by an edge. Arrange as a loose non-equilateral cluster or as tiered rows on shelves. Never a symmetric row of evenly spaced identical units, never mirrored pairs.

**6. Dense field.** Fill the frame edge to edge with repeating units until repetition reads as texture — a stocked fridge, a packed crate, a full shelf run — organized into color blocks, with a hand entering to remove one. Depth comes from the shelving armature, not from blur.

### Placement geometry

- **Off-center by default.** The primary object's axis sits 35–48% or 52–65% across the frame. Dead center is permitted only as strict, exact single-axis centering, and then all the dynamism must come from the cast shadow.
- **Compose on a diagonal.** Align the primary axis with the light direction, or set the object orthogonal and let the shadow supply the diagonal, or cross two diagonals near mid-frame. Never a flat orthogonal grid with no diagonal anywhere.
- **Three objects make a non-equilateral triangle**, one dominant, one mid (often partly cropped or partly occluded), one small peripheral. Vary all three distances between them.
- **Overlap is mandatory in multi-object frames.** At least one object must partially occlude another. Nothing floats in its own clearance.
- **Shadow direction points away from the camera at roughly 4 or 8 o'clock** in flat-lays, so the shadow reads as depth rather than as a shape lying flat on the label side.
- **Crop with conviction.** Either cut at least one form at a frame edge so mass is implied beyond it, or hold generous even clearance on all four sides. Never a polite catalogue margin that keeps everything whole with a modest border.
- **One empty zone stays empty.** Preserve at least one quadrant or third carrying nothing but field, tone, texture, or shadow. Do not fill it with a duplicate or a decorative prop.
- **One deliberate irregularity per frame:** a lean off vertical, a drape spilling past a boundary at exactly one point, a shaving that fell off the round, a cord trailing out of frame, a bottle laid on its side among standing ones, a knocked-over cap. Precise everywhere else.
- Frame tilt is 0° by default; a 5–15° camera tilt is the permitted activation move for a cluster or a hand-held reportage frame. No heavy dutch angle.
- Viewpoints in the register: eye-level frontal; gentle 15–30° oblique above; true 90° overhead; low angle from below against sky or ceiling. Never a floating three-quarter hero at 45° with an invisible ground plane.

### Hands

Hands are a signature device here, not an exception — roughly half of the reference register uses them. They provide scale, warmth, color, and narrative in one move.

- Hands **do a specific action**: grip a bottle around its neck, lift a stick out of a bag, press flat on a surface, pour in a smooth rope, hold a glass to receive it, reach in to take one from a row, raise two bottles overhead, hold a bottle to the ear.
- Crop at the wrist or mid-forearm. Faces are optional and rare; when a face appears (register G, editorial) it is a directed portrait with real posture, not a smiling stock model.
- **Multiple hands from multiple people, with visibly different skin tones, is a strong and proven configuration** — for example four forearms rising from the bottom edge of a matching field, hands overlapping and gripping each other as they pass the product upward.
- Render hands honestly: correct anatomy and finger count, visible tendons and knuckles, nails with real cuticles and shape, pressure-blanching where fingers press, small tattoos and marks. Hands are frequently the hardest element to generate — inspect them in every output and regenerate if they are wrong.
- Nails may be manicured or bare; polish color counts against the palette budget.
- No praying hands, no open-palm presentation gesture, no fingertip-balancing, no hand floating disembodied against a void with a perfect gradient.

### Props

- Props are chosen for **deadpan wit or genuine use**, never for decorative filling. The proven register: three nails standing in a pine offcut next to a fragrance; two knives stabbed upright into a log round with a hand pressed flat between them; a perfume bottle held to the ear like a telephone; a bar of soap and wired earbuds on a silver tray; scattered wood shavings; a comb standing in a beaker.
- Ingredient props are permitted only when they are **the actual ingredient**, present as a real physical object, not as a styled garnish ring. One or two, placed asymmetrically, at least one partly occluded.
- Total prop count: zero to five. A frame with one hero and no props at all is a valid and strong choice.
- Banned props: scattered rose petals; a folded towel; stacked river stones; a single orchid stem; loose coffee beans in a fan; cinnamon sticks tied with twine; a floating dropper mid-air; glitter; confetti; abstract plaster geometric shapes.

---

## Camera, frame, and finish

- **Aspect ratio:** 2:3 or 4:5 vertical is the default and covers most of the register. 1:1 for a centered single hero or a marketplace crop. 3:2 or 16:9 landscape for wide set-piece tableaux with a person. Choose deliberately; do not default to square.
- **Focal length and perspective:** 50–85mm equivalent for hero and lineup frames, giving mild compression and honest proportions. 35mm for reportage and environment frames. 100mm macro for cosmetic detail. Avoid wide-angle distortion on packaging — a barrel-distorted bottle reads as fake instantly.
- **Depth of field:** deep and sharp is the default; the product, its label, and its immediate surface are all in focus. Shallow focus is permitted in exactly two cases: a true macro frame where the edges of a very close subject naturally fall away, and a reportage environment frame at 35mm where the background softens honestly. Never a blurred gradient "bokeh backdrop" behind a studio product.
- **Sharpness:** label type must be legibly rendered and correctly kerned. Print-crisp edges on packaging; soft edges only where a real optic would soften.
- **Finish is all-or-nothing.** Either perfectly clean digital with no grain anywhere, or one continuous fine-to-medium film grain over 100% of the frame including shadows and highlights. Never partial, never a decorative grain overlay on one element, never grain as a "vintage" wash. When grain is on, the whole frame may also carry a slight film color shift and a touch of halation on hot highlights — that is a coherent stock, not a filter.
- No borders, no white frames, no simulated film sprockets, no date stamps, no watermarks, no UI chrome.

---

## Product, label, and type rendering

The packaging in these frames is *designed*, and rendering it credibly is half the job.

- Give the product a real construction: wall thickness, a molded seam, a shoulder radius, a screw thread, a pump collar, a hinge, a crimped ferrule, a debossed logo. Objects without construction logic read as toys.
- Give the label a real substrate: uncoated paper with a visible cut edge, a clear pressure-sensitive film, a screen print directly on glass, a debossed emboss, a foil block. Show its edge, and show it slightly imperfectly applied.
- **Invent the brand.** Never place a real brand's name, wordmark, or trade dress on a generated product unless the user supplied that brand's own assets and asked for it. Invented names should be short, plausible, and typographically confident.
- Label typography: one type family, two tiers — a product name at display scale and a small block of subordinate detail at a quarter of it or less — set flat, high-contrast, generously letter-spaced where uppercase. Micro-copy reads as a texture band rather than as reading matter. Ingredient lists, volumes, and certification marks are permitted as small, believable, non-specific type.
- Type on the label is **flat**: no gradients, no bevel, no drop shadow, no transparency. It curves with the surface it sits on and dims where the surface turns away from the light.
- Do not add floating headline text, price flashes, badges, or lockups into the photograph. This skill produces photographs; layout belongs to `static-ads` and `poster-design`.
- If the user supplies a product image, the packaging in the output must match it exactly — color, proportion, closure, label layout, and type. Composite the real product into the new light rather than reinventing it.

---

## Prompt construction

Write one dense paragraph, comma-separated, in this order. Every clause is a decision you already made above.

1. **Shot type and staging mode** — "vertical eye-level packshot", "overhead flat-lay", "close two-hand crop".
2. **Subject with real specificity** — form, size, closure, material, label construction, invented name.
3. **Surface and riser** — the actual named material it sits on or in.
4. **Backdrop** — named field hue and substrate, or the named real environment.
5. **Lighting register** — named source, angle in degrees, quality, color temperature.
6. **Shadow behavior** — direction, length relative to the object, edge quality, where it exits frame.
7. **Palette** — the named hues in order of area.
8. **Contrast and tonality** — ratio, whether highlights clip, whether shadows go black.
9. **Materials present** — two to four named surface behaviors.
10. **Secondary objects and hands** — what they are and exactly what they are doing.
11. **Placement geometry** — off-center percentage, diagonal, overlap, what is cropped, which zone stays empty.
12. **Camera** — focal length, aspect ratio, depth of field.
13. **Finish** — clean, or grain plus optional halation.
14. **Negative clauses** — the specific defaults to suppress for this frame.

Keep the vocabulary physical throughout. Delete every mood adjective — "premium", "elevated", "clean", "luxurious", "aesthetic", "minimalist", "high-end" — and replace it with the physical fact that would produce it.

### Worked example

> Vertical eye-level packshot of a 100ml squared fragrance flacon in deep translucent oxblood glass with a brushed brass lower third, a chrome collar debossed with small letterspaced caps reading MERIDIAN FIELD, and a black anodized cap, standing on a raw pine offcut with visible end-grain and three steel nails driven in beside it, against a flat mustard-ochre seamless paper backdrop, single hard low sun from the right at 20° above horizon and 60° off axis at 4500K, throwing one dense red-brown shadow twice the bottle's height diagonally left across the pine and up the ochre field before exiting the left edge, palette of mustard ochre field then raw pine pink-tan then oxblood glass then brass, 8:1 ratio with the shadow falling to near-black and a small clipped specular on the chrome collar, materials are transmissive colored glass, brushed metal with directional grain, sawn softwood end-grain and matte paper, bottle axis at 44% across with its base 70% down frame, nails clustered low left as the one irregularity, upper third of the ochre field left completely empty, 85mm, 2:3, deep focus throughout, fine film grain over the whole frame with slight halation on the collar highlight, no marble, no pedestal, no gradient background, no second shadow, no rim light.

---

## Prompt library

Twelve tested frame recipes for when the user has no specific vibe or setting in mind. Fill the `[bracketed slots]` with the user's product and range. When the user's request is generic, use a recipe verbatim as a starting point, adjusting the named product only, and keep every lighting, color, and staging clause intact. When the user specified a color, mood, or setting, a recipe is a **structural template only**: keep its staging mechanics (placement geometry, crop, hands, prop count) but restage its light and palette to match what the user actually asked for — do not port over the recipe's own field hue or mood over the user's request.

### Long-shadow bone packshot

Square eye-level packshot of a single tall [primary product] in frosted pearl-white glass with a rounded cap and a small letterspaced serif wordmark plus a tiny navy-and-gold circular emblem, floating on a flat bone-pale cool grey seamless with no visible contact surface, one hard sun-like source from the upper left at 35° above horizon and 45° off axis, casting one long soft-edged mid-grey shadow at 40° to the lower right, roughly 1.6× the bottle's height, palette of pale cool grey field then pearl ivory glass then a single navy and gold emblem accent, three-pole value structure with the shadow as the darkest mass and no true black, materials are satin-etched glass, a faint clear liquid meniscus visible at the base, and matte paper, bottle exactly centered on a single vertical axis with more air above than below, whole upper third empty, 85mm, 1:1, deep focus, perfectly clean digital finish with no grain, no marble, no pedestal, no reflection, no gradient, no second light.

### Raking-sun sand flat-lay

Vertical overhead flat-lay of [two or three products from the range] — an amber apothecary jar with a white cap, an amber dropper bottle, a nude satin-finish squeeze tube — lying at 20–30° to each other on a sand-colored rough plaster surface, hard low afternoon sun from the upper left at 25° above horizon, cutting a knife-edge diagonal boundary that drops the entire upper right of the frame into deep warm umber shade, each object throwing a crisp shadow 1.5× its length to the lower right and the amber glass refracting a warm orange caustic patch onto the plaster beside it, cream loose linen gauze entering from the right edge in soft folds, broken dappled foliage shadow across the lower left corner, palette of sand then cream then cognac amber then deep umber shadow, 8:1 ratio with genuinely dark shade and no fill, materials are rough plaster, transmissive amber glass, satin plastic and loose woven linen, objects clustered slightly below and left of center with the tube cropped by no edge and the gauze cropped by the right edge, lower right quadrant left as bare lit plaster, 50mm, 2:3, deep focus, fine film grain across the whole frame, no marble, no travertine, no stone slab, no pedestal, no white sweep.

### Chromatic-loop four-hand raise

Vertical studio frame of four bare forearms of four visibly different skin tones rising from the bottom edge against a flat brick-terracotta seamless, hands overlapping and gripping one another in a vertical chain, the topmost hand holding a [primary product] as a tall rectangular pump bottle molded in the exact same brick terracotta as the backdrop with small cream serif and sans type and a matching terracotta pump head, soft-hard directional light from the upper left with gentle wraparound modelling, one faint shadow on the field to the right of the bottle, palette locked to a single terracotta hue across field and product with skin tones as the only variation, product separated from the ground by value and a satin sheen only, 4:1 ratio with no true black, materials are matte injection-molded plastic, warm skin with visible tendons and pressure-blanched fingertips, and matte paper, the arm chain rising slightly right of center on a diagonal, left third of the field left empty, 85mm, 2:3, deep focus, clean digital finish, no marble, no gradient, no rim light, no second color.

### Shallow-water bronze lineup

Vertical frontal frame of [five or six products from the range] — bronze anodized screw-top jars and frosted pump bottles with bronze caps — standing in 8mm of still water on a dark reflective surface, concentric ripples spreading from the nearest jar, in front of a rough cream plaster wall with visible chips and patches, one hard side light from the left at 30° above horizon throwing a soft-edged dark grey silhouette of one bottle onto the plaster wall behind, each unit doubled in the water as a soft broken reflection, palette of cream plaster then bronze then frosted white then warm grey shadow, three-pole structure with the wall highlight near-white and the water near-black, materials are anodized metal, frosted glass, standing water and rough plaster, units arranged in two staggered depths as a loose non-equilateral cluster with two jars cropped by the left and right edges, upper left of the wall left empty except the cast silhouette, 70mm, 4:5, deep focus, clean digital finish, no marble, no pedestal, no gradient, no splash crown.

### High-key towel hand crop

Vertical extreme close crop of one hand with small fine-line tattoos gripping a matte soft-touch black pump bottle and a frosted bone-white pump bottle side by side, both with black pump heads and flat black grotesque labels carrying a product name and small circled category codes, cradled in a heap of white waffle-weave terry towelling that fills the entire frame, soft flat overcast daylight near-frontal, near-shadowless with only faint contact shadows in the towel folds and gentle wraparound on the bottles, palette of white and black with warm skin as the only chroma, compressed high-key tonality with a small clipped highlight on the towel ridges and no true black, materials are matte soft-touch plastic, satin frosted plastic, waffle terry cotton and skin, bottles on a shallow diagonal across the upper half with the hand entering from the left and cropped at the wrist, all four edges cropped through the towel, 50mm, 4:5, deep focus, clean digital finish, no marble, no gradient, no studio sweep, no rim light.

### Kraft-nest grain still life

Vertical overhead flat-lay of a single [primary product] as a rectangular flacon in smoky grey glass with a rough dark stone-textured cap, a small white uncoated paper label with a serif brand name and a letterspaced sub-line, nested in loosely crumpled unbleached kraft tissue paper with sharp creases, on a flat pale sage grey-green paper backdrop, one medium-hard source from the upper left at 40°, throwing a soft-edged grey-green shadow to the lower right about half the flacon's length, palette of sage grey-green then kraft tan then smoky grey glass then warm liquid amber inside, drained low saturation with a warm cast, compressed mid-band tonality with no pure white and no pure black, materials are crumpled tissue paper, smoky transmissive glass, uncoated label stock and matte paper, the paper nest occupying the middle 60% of the frame with the flacon centered inside it and one paper corner reaching toward the lower left, all four margins left as bare sage field, 50mm, 4:5, deep focus, heavy uniform medium-coarse film grain over the entire frame like a scanned 35mm negative, no marble, no pedestal, no gradient, no clean digital finish.

### Cerulean glass-shelf structure

Vertical frontal frame of [six to eight products from the range] arranged across three horizontal glass shelves with visible green edges, against a flat saturated cerulean seamless, black-and-white packaging throughout — matte white squeeze tubes with black caps and small black grotesque type, a tall cylindrical bottle of blue-tinted liquid, a black dropper bottle, a dark glass jar — plus a black comb standing upright in a clear glass beaker, one hard source from above and slightly left throwing short tight shadows onto each shelf, palette of cerulean field then white then black with the blue liquids reading as a darker note of the field hue, three-pole structure with clipped white on the tubes and near-black in the caps, materials are transmissive tinted glass, matte white plastic, plate glass shelving and matte paper, products distributed unevenly across the three tiers with the top shelf weighted right, the middle shelf weighted center-left, and one lone tube on the bottom shelf cropped by the bottom edge, upper left of the field left empty, 85mm, 4:5, deep focus, clean digital finish, no marble, no pedestal, no gradient, no rim light, no symmetric row.

### Noon-sun bag reach

Vertical close overhead crop of two hands lifting a nude blush satin-finish [primary product] deodorant stick out of an open white heavy cotton canvas tote, the tote also holding a bone-white pump bottle and a translucent pink soap bar in printed film, all resting on a red-and-white checkerboard terry towel inside the bag, hard direct overhead noon sun from the upper right at 75°, blown white highlights on the canvas, crisp black shadows tight to each object, the entire upper right corner falling to true black in shade, palette of white canvas then nude blush then saturated scarlet check then black shadow, 16:1 ratio with clipped whites and crushed blacks both permitted, materials are heavy cotton canvas, satin plastic, terry check towelling, printed film and skin, the stick held at 20° off vertical slightly left of center with one hand entering from the top left cropped at the wrist and the other from the bottom center cropped at the forearm, lower left corner left as plain lit canvas, 35mm, 4:5, deep focus, clean digital finish, no marble, no gradient, no studio light, no soft shadow.

### Rockpool contre-sun overhead

Vertical overhead frame of [two products from the range] — a tall bone-white cylindrical bottle with a pump and a smaller white dropper bottle, both with tiny letterspaced sans type — lying on a wet golden-brown mineral rock in a dark rockpool, clear water running over the bottles and pooling around them, the corners of the frame falling to near-black open water, hard high sun raking the water so caustics ripple gold and white across the submerged rock, palette of near-black water then golden ochre wet rock then pure white bottles, 16:1 ratio with clipped white highlights on the water and true black in the pool, materials are running water, wet mineral rock, matte white plastic and clear glass, the two bottles crossing at 30° to each other slightly below center with the larger one aligned to the rock's long axis, upper left third left as dark open water, 35mm, 4:5, deep focus, clean digital finish, no marble, no studio rock prop, no pedestal, no frozen splash crown, no gradient.

### Mustard deadpan riser

Vertical frontal frame of a single [primary product] as a squared flacon of deep translucent red liquid with a brushed brass lower half, a chrome collar carrying small debossed letterspaced caps, and a black cap, standing on a rough-sawn pine construction offcut with visible end-grain, three steel nails driven part-way into the pine beside it, against a flat mustard-ochre seamless, one hard low source from the right at 20° above horizon, throwing a heavy dark red-brown shadow diagonally left across the pine and continuing up the ochre field, palette of mustard ochre then raw pine pink-tan then deep red glass then brass then black, 8:1 ratio with the shadow near-black and one clipped specular on the collar, materials are transmissive colored glass, brushed brass, chrome, sawn softwood end-grain and matte paper, bottle axis at 46% across with the pine block cropped by both the left and right edges and the bottle base 62% down frame, upper left of the ochre field left empty, 100mm, 4:5, deep focus, fine film grain over the whole frame, no marble, no pedestal, no plinth, no gradient, no rim light.

### Scarlet macro with teal spill

Vertical macro frame of a single [primary product] as a glossy oxblood lacquered octagonal lipstick case with a chrome band debossed with small caps, standing on a saturated scarlet lacquer surface against a matching scarlet ground, a large deep-red anthurium leaf with visible veining entering from the left edge, and a single smeared dab of the dark red bullet on the surface at the lower right, one hard source from the upper left plus a hard teal-cyan gel spill washing the right third of the frame as the only cool note, palette locked to scarlet and oxblood across 80% of the frame with teal-cyan at 20%, high 12:1 contrast with deep near-black reflections inside the gloss and clipped speculars on the chrome, materials are high-gloss lacquer, polished chrome, waxy leaf surface and soft pigment paste, case axis at 52% across running the full height and cropped by the top edge, leaf cropped by the left edge, the smeared dab as the single irregularity, edges of the frame falling softly out of focus as a natural consequence of the macro distance, 100mm macro, 4:5, clean digital finish, no marble, no pedestal, no gradient background, no glitter, no water droplets.

### Chiaroscuro tabletop shaft

Vertical frame of [two products from the range] as two clear glass bottles with cork-and-foil tops and glowing scarlet and cream paper labels bearing a heavy condensed wordmark and a single-line drawing, standing on a polished mahogany table, one hard low shaft entering from the left at 15° above horizon and cutting a hard-edged bright wedge across the tabletop while the background falls to near-black, the bottles backlit so the liquid glows amber-green and each throws a long dark shadow to the right along the wood grain, palette of deep red-brown mahogany then glowing amber-green glass then scarlet and cream labels then near-black surround, 16:1 ratio with true black in the background and a clipped highlight where the shaft meets the polished wood, materials are polished hardwood, clear transmissive glass, cork, uncoated label paper and warm liquid, bottles offset right of center at slightly different depths with the nearer one 8° off parallel, the entire upper left quadrant left as black room, 85mm, 4:5, deep focus, fine film grain over the whole frame with slight halation where the shaft clips, no marble, no pedestal, no fill light, no gradient, no rim light.

---

## Model and input choice

- **When the user supplies a photo of a real product, use it as an input image.** Product photography without the actual product is a different, weaker job. Route through an editing-capable model so the packaging, color, and label survive intact, and reserve text-to-image for concepting and mood exploration.
- **Nano Banana Pro** is the default when the product must be rendered exactly or the label type must be legible. It is the strongest at faithful subject reproduction and text.
- Aspect ratio must be set explicitly on the generation, matching the ratio the recipe specifies.
- If the user wants an exact stylistic match to a supplied reference frame, prefer an elaborate prompt describing that frame's light, palette, and staging over a style-transfer strength; a single style reference at default strength is acceptable, but never stack multiple style references.
- Generate a small spread rather than one frame, varying only the lighting register or the field hue across the set so the differences are legible and choosable.

---

## Avoid

Each item is a known collapse path, ordered by how often it ruins a frame:

1. **Marble, travertine, onyx, quartz, terrazzo, or any polished stone slab, tile, pedestal, plinth, podium, riser, step, or arch.** The single most common failure of this brief. Mineral appears only as a wet river rock, a plaster wall, or beach sand, encountered in place.
2. **Anonymous abstract objects** — unlabelled cylinders, blobby rounded rectangles, "a generic bottle". Products have construction, closures, labels, and invented names.
3. **White or grey seamless sweep with a centered floating product and an airbrushed reflection.** The ground is a committed hue, a real textile, a found riser, or a real place.
4. **Mid-chroma tasteful desaturation.** Saturation is fully committed or deliberately drained; never in between.
5. **Three-point studio lighting, rim light on black, chrome-ring kickers, twin symmetric strip highlights.** One hard source, one designed shadow.
6. **A soft generic ambient shadow pooled under every object, or fill light lifting the key shadow.** Shadows are hard and dark, or absent by regime.
7. **Two disagreeing shadow directions**, or a shadow whose angle contradicts the stated light.
8. **Stacked digital mood effects** — glow, bloom, haze, dry ice, god-rays, applied vignette, teal-orange LUT, HDR tone-mapping, lens blur backdrop.
9. **Gradient backgrounds of any kind**, including a subtle radial falloff behind the product.
10. **Frozen splash crowns, levitating products, exploding ingredients, floating droppers.** Liquid obeys gravity and sits, pours, pools, or runs.
11. **Spa and luxury clichés** — orchid stem, folded towel, stacked river stones, rose petals, coffee-bean fan, cinnamon and twine, gold foil on black, brushed gold everything, glitter.
12. **Symmetric side-by-side product pairing, evenly spaced identical rows, mirrored duplicates, grid or radial snapping.** Repetition carries variation.
13. **Timid crops** that keep every object whole inside a modest even border. Crop through something, or hold real clearance.
14. **Everything glossy**, or everything matte. Two to four distinct material behaviors per frame.
15. **Bokeh as the default depth cue.** Deep focus, except in true macro or honest 35mm reportage.
16. **Real brand names, wordmarks, or trade dress** on a generated product the user does not own.
17. **Floating headline text, price flashes, badges, or ad layout** inside the photograph.
18. **Mood adjectives standing in for decisions** — premium, elevated, clean, luxurious, aesthetic, minimalist, high-end. Every one of these is a physical fact you have not yet specified.
19. **Retouching away spills, fingerprints, dust, tool marks, and crooked labels** in pursuit of generic polish.
20. **Malformed hands** — extra fingers, fused knuckles, impossible grips. Check every hand in every output.

---

## Final check

Verify every line before returning an image.

1. Lighting register named, and exactly one source; every shadow, highlight and caustic agrees with its angle.
2. The cast shadow was designed — direction, length, edge quality, exit point — and is doing compositional work.
3. Palette strategy named; saturation is fully committed or deliberately drained, never mid-chroma.
4. Shadow color sits inside the family of the field and the light; no grey or unrelated blue fill.
5. Contrast is high with real black and, where the register calls for it, clipped white — or fully compressed high-key with no black at all. Not a timid middle.
6. No marble, travertine, stone slab, pedestal, plinth, podium, or riser cut to size anywhere in the frame.
7. Two to four distinct named material behaviors present; one to two glossy elements at most; the focal product is less textured than its surround.
8. Physical imperfection is visible and physically motivated.
9. Staging mode named; the product sits on a real named surface, not in a void.
10. Composition carries a diagonal; the primary axis is off-center or exactly centered with the shadow supplying the movement; at least one overlap in multi-object frames.
11. At least one form cropped by an edge, or real clearance on all four sides — not a catalogue margin.
12. One quadrant or third left genuinely empty; exactly one deliberate irregularity present.
13. Hands, if present, are doing a specific action, cropped at wrist or forearm, anatomically correct, with real skin detail.
14. Props are witty or functional, counted, and none are on the banned list.
15. Product has real construction and a real label substrate; label type is legible, flat, two-tier, and carries an invented name.
16. Aspect ratio, focal length, and depth of field were chosen deliberately and match the recipe.
17. Finish is uniformly clean or uniformly grained across 100% of the frame.
18. No mood adjective survived into the final prompt in place of a physical decision.
