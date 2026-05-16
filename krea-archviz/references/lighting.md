# Lighting Recipes for Archviz Prompts

Lighting is the single biggest factor in whether an archviz render reads as photoreal or generic. Each recipe below is a prompt fragment you can splice into the full structure from `screenshot-to-render.md`.

## Exterior lighting

### Golden hour exterior

> Golden hour, warm low-angle sun casting long directional shadows, sky transitioning from warm orange at the horizon to deeper blue overhead, surfaces facing the sun glowing in amber light while shadowed planes hold cooler tones, atmospheric haze in the middle distance softening edges

**Use for**: hero shots of residential, hospitality, retail. Single-family villas, beach houses, anything where "warmth" and "lifestyle" sell.

**Common failures**: model produces a flat warm wash instead of directional shadows. Fix: add "long directional shadows from a low sun" explicitly.

### Midday daylight exterior

> Midday natural daylight, soft overhead sun position with shorter shadows directly beneath overhangs, sky bright blue with scattered cumulus, surfaces reading their true daytime color without warm or cool cast, sharp contact shadows beneath canopies, sense of openness and visibility

**Use for**: documentation renders, public buildings, civic context shots.

**Common failures**: looks washed out. Fix: add "scattered cumulus clouds for sky interest" + a specific material that holds detail well (textured concrete, stone) in the foreground.

### Overcast diffuse exterior

> Overcast diffuse daylight, even soft sky illumination without directional shadows, surfaces revealing their full texture without contrast, muted cool color palette, light rain on the paving creating subtle reflections, atmospheric mist softening the middle distance

**Use for**: brutalist, textural, monumental architecture where you want material detail without harsh shadows. Northern European context.

**Common failures**: dull. Fix: add wet paving / rain detail to give the image moisture and life.

### Twilight / blue hour exterior

> Blue hour, deep cobalt sky with the last warm horizon glow, interior lights beginning to register warmly against the cooler exterior, surfaces holding ambient cool tones while warm interior light pools at openings, atmospheric and contemplative mood

**Use for**: when you want both architecture and interior life visible. Hospitality, retail at opening hours, cultural buildings before evening events.

**Common failures**: too dark. Fix: emphasize "warm interior light visible through openings" so the building reads as occupied and alive.

### Night exterior with context

> Night, dark sky with subtle city light pollution glow, building illuminated by carefully placed accent lighting on key materials and architectural elements, warm interior light spilling from openings, wet streets reflecting colored urban lighting, scattered atmospheric mist between buildings

**Use for**: urban towers, civic projects in nighttime use, retail flagships.

**Common failures**: building feels disconnected from context. Fix: anchor with "dense surrounding cityscape with mixed neon and tungsten signage" or specific local cues.

## Interior lighting

### Midday natural daylight interior

> Midday natural daylight pouring through large openings, soft sky-color cast on the surfaces facing the windows, deeper neutral tones in areas further from the glazing, sharp contact shadows beneath furniture, sense of openness and bright airiness

**Use for**: residential daytime shots, office spaces, retail. The default interior look.

**Common failures**: looks like a stock photo. Fix: add atmospheric specifics — "dust motes visible in the light shafts" / "soft window reflections on the polished floor".

### Warm interior, evening artificial

> Evening artificial interior lighting, warm 2700K pendants and accent fixtures creating pools of light, soft ambient glow from indirect coves washing the walls, dark areas held in shadow rather than fill-lit, candles or table lamps adding warm point sources, intimate residential or hospitality atmosphere

**Use for**: restaurants, hotel lobbies, residential evening, premium retail.

**Common failures**: overlit, no shadow areas. Fix: explicitly call out "dark areas held in shadow" to prevent the model from filling everything in.

### Museum / gallery lighting

> Museum lighting, precise accent lighting on the exhibits and architectural features, soft ambient wash on walls, neutral 3500-4000K color temperature for accurate color rendering, polished concrete or wood floor with subtle reflections of the lighting, hushed contemplative atmosphere

**Use for**: cultural, gallery, hospitality lobby with art, premium retail with curated product display.

**Common failures**: light feels uniform / generic. Fix: name specific accent positions ("pinspot on the central sculpture, wall wash on the long blank wall behind").

### Retail showroom lighting

> Bright retail showroom lighting, multiple fixture layers, 3000-3500K warm-neutral temperature, accent lighting on hero products, soft wash on the floor, glossy material reflections amplifying the brightness, energizing commercial atmosphere

**Use for**: flagship retail, showrooms, automotive displays.

**Common failures**: feels like a photo studio. Fix: add architectural lighting context — "linear LED coves at the ceiling perimeter, recessed downlights on a regular grid".

## Mixed conditions

### Architectural model photography

> Studio architectural photography lighting, single soft directional key from above and slightly behind the model, secondary fill from the front at lower intensity, neutral grey seamless background, sharp shadows revealing the model's massing, scale figures placed for context

**Use for**: physical model photography simulation, design competition boards.

### Cinematic / dramatic mood

> Cinematic dramatic lighting, single strong directional key light raking across the space, deep contrasted shadows, fog or atmosphere visible in the light shafts, saturated color from a specific light source (warm tungsten, cool sodium, colored neon), high contrast film-grade look

**Use for**: marketing imagery, brand shots, anything that needs emotional impact over documentary accuracy.

**Common failures**: model produces flat film-look instead of dramatic. Fix: name the lighting setup explicitly ("single strong directional key from camera-right, no fill").

## Picking from this list

When the user gives you the brief, identify two anchors:

1. **Time of day or condition** — pick from above
2. **Mood** — overlay one or two emotional descriptors ("intimate", "monumental", "energizing", "contemplative")

Then splice into the prompt template from `screenshot-to-render.md`.

If the user provides a reference image of the lighting they want, prefer image-to-image with the lighting reference as `imageUrl` rather than describing it in words — vision-anchored is sharper than vocabulary-anchored.
