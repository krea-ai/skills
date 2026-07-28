# Luxury Showcase — Environment, Material, Palette

For objects that should read as *desirable*, not merely well lit: design pieces,
hardware, jewellery, fragrance, watches, leather goods, tools with sculptural form.

The default void — charcoal seamless, one key, nothing else — is honest but anonymous.
It says "product photograph." A luxury piece reads expensive when it sits somewhere
that has been *designed*, on a surface chosen to argue with it. This file is about
that choice. Structure, beats and cuts stay as they are in
`references/cut-architecture.md`.

## The Tension Principle

Pick a surface and a setting that are the **opposite material** to the object. The
friction is the point; matching materials read as a catalogue.

| Object | Put it on / in | Why it works |
|---|---|---|
| Machined metal, chrome, polished steel | Aged tan leather, raw linen, oiled walnut | Warmth and grain against something cold and exact |
| Glass, crystal, clear resin | Raw concrete, unfinished plaster, dark brick | Fragility staged against mass |
| Soft goods, leather, textile | Glass with slim metal legs, polished stone | The object is the only warm thing in a cold room |
| Matte ceramic, stone, clay | Brushed steel, mirror-polished black | Hand-made against machine-made |
| Warm-toned jewellery or gold | Deep oxblood or cognac leather, dark velvet | Saturated colour field the metal can sit inside |

Two settings that carry an enormous amount on their own, both worth naming in the
world block:

- **A slim glass table with thin brushed-metal legs**, low angle, the object sitting
  on the glass with its own reflection under it and the room falling away behind.
- **A pared-back apartment with raw structural materials** — board-formed concrete, an
  exposed brick return, tall shutters, one shaft of daylight — with the object left on
  a surface as though someone set it down.

## Place It, Don't Present It

Centered on a plinth reads as a display. Set down at an angle, off-centre, near the
edge of the surface, next to nothing else, reads as owned.

```
The object rests on the glass at a slight angle, off-centre in frame, close to the
near edge of the table; nothing else is on the surface. No plinth, no podium, no
riser, no pedestal, no display stand.
```

## Palette And The Single Accent

One dominant neutral field, one accent occupying **under five percent** of frame.
Almost always warm against cool: a thin amber specular along a chrome edge, a cognac
leather ground under a steel object, one warm bounce in an otherwise neutral room.

Say the accent explicitly and cap it, or the model spreads it across everything.

```
Palette: cool graphite and near-black throughout, with a single warm amber accent
confined to the specular on the top edge. No warm cast anywhere else in frame.
```

## Environment Grade As A Build

The strongest device in this register, and it costs no extra beats: **transform the
environment while the object stays fixed.** Open high-key with the object on a bright,
almost blown-out white field, and let the world fall away to true black as the camera
moves in — so the final frame is the same object in a completely different world.

```
Motion split: the object is locked and never moves. Over the first 1.5 seconds the
environment transitions continuously from a bright near-white field to true black —
the background falls away, the fill drops out, and the object retains only a hard
specular along its top edge. The transition is continuous and even, not a cut, not a
fade to black: the object stays fully visible and correctly exposed throughout.
```

This is the one case where showing the whole object early is correct: the object is
not the reveal, the *transformation* is. The final beat still lands on the full object
composed and still.

## Named Aesthetics Without Naming Houses

Users will reference luxury houses. Never put a brand into the prompt as an imitation
target — it is banned in the hard rules and it degrades output. Translate to craft:

| They say | Write |
|---|---|
| "like Hermès" | saddle-stitched tan leather, brushed palladium hardware, warm neutral ground, no logo in frame |
| "like a Swiss watch brand" | brushed and polished steel contrast, applied indices, deep sunburst dial, macro at 100mm |
| "like a Danish furniture brand" | oiled oak, soft daylight from one tall window, matte off-white walls, no hard specular |
| "like a luxury car interior" | perforated leather, knurled metal dial, stitched seams, low warm key |
| "quiet luxury" | no logo in frame, no gloss, matte surfaces, one soft source, muted greige palette |

## Building The Environment Shot

The environment is usually not in the source still. Do not ask the video model to
invent it around an existing product photo — it warps the product. Instead:

1. Generate the product **in** the environment as a still first, with the `krea-generate`
   skill, and gate it with vision.
2. Approve that still with the user.
3. Animate the approved still as the `start_image`.

## Banned Here

- Plinths, podiums, risers, pedestals, display stands, turntable platforms.
- Rose petals, water splashes, silk swirling through frame, floating particles.
- Marble slabs with gold veining as a default backdrop; it is the stock luxury cliché.
- More than one accent colour, or an accent occupying more than a corner of the frame.
- A logo or brand name anywhere in frame unless it is physically on the product.
- Everything on the cheap list in `references/cinematic-craft.md`.
