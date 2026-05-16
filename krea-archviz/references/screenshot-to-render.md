# 3D Screenshot → Photoreal Render

The most common archviz workflow at firms like Henning Larsen: user has a Sketchup / Rhino / Revit / Blender screenshot and wants it transformed into a photoreal render at a specific time of day, mood, or style.

## The workflow

```
1. Receive the screenshot from the user (attached file, URL, or pasted image)
2. Read it with vision — Claude's built-in Read on the local file
3. Identify: scene type, implied lighting, visible materials, missing elements
4. Confirm the brief one-line with the user if anything is genuinely ambiguous
5. Upload the screenshot via upload_asset (after checking ≥1024px on long side)
6. Pick the model (image-to-image high-fidelity archetype, see ../../krea-ai/references/model-catalog.md)
7. get_model_schema(model=<id>) — confirm the imageUrl/imageUrls field name
8. Submit generate_image with sync=true, timeoutSeconds=60
9. Download result, Read with vision, verify against the brief
10. Deliver URL + one-line model rationale (only if asked) + suggest variants
```

## Reading the screenshot

Before generating, the agent should be able to answer:

- **Scene type**: exterior facade / interior room / urban context / landscape / detail close-up
- **Camera angle**: eye-level / aerial / worm's eye / oblique
- **Implied time of day**: from any shadows, color cast, or lighting in the 3D scene
- **Visible materials**: glass, concrete, wood, metal, fabric, stone, etc.
- **Missing elements that will need to be inferred**: people, vegetation, sky, ground texture

This is where Claude's vision is doing real work — a generic prompt produces generic output. A vision-grounded prompt is sharper.

## Prompt structure

```
[scene type], [target style/medium],
[time of day],
[lighting quality],
[material details that need preservation or change],
[atmosphere / mood],
[any specific elements to add — people, vegetation, vehicles, etc.]
```

The five slots are the minimum. For a hero render, also add camera language (lens, focal length, depth of field).

## Five worked examples

### Example 1: Modern villa exterior, golden hour

**Source**: Sketchup screenshot of a modernist villa, clean massing, glass + concrete + wood cladding, daytime daylight rendering with no shadows.

**Prompt**:
> Photoreal exterior render of a modernist single-family villa, golden hour, warm low-angle sun casting long shadows across the entrance courtyard, exposed board-formed concrete facade with visible texture, large floor-to-ceiling glazing with subtle reflections of the sky, slatted oak cladding warm in the late light, mature olive tree casting dappled shadow, clean entrance walkway, distant rolling hills softened by atmospheric haze, shot on 35mm, shallow depth of field on the foreground planting, architectural photography style

### Example 2: Office interior, midday daylight

**Source**: Rhino screenshot of an office floor, ceiling grid visible, desks and chairs blocked in.

**Prompt**:
> Photoreal interior render of a contemporary corporate office floor, midday natural daylight pouring through floor-to-ceiling windows along the long facade, polished concrete floor with subtle sheen, exposed coffered ceiling with linear LED downlighting, oak veneer desks with task lighting, ergonomic mesh task chairs, scattered occupants working but blurred to suggest activity without distraction, plants in the breakout corner, neutral palette, soft contact shadows, shot on 35mm, eye-level, deep depth of field, editorial architectural photography

### Example 3: Brutalist facade study, overcast evening

**Source**: Revit screenshot of a museum facade, harsh diagonal sun in the render.

**Prompt**:
> Photoreal exterior detail of a brutalist museum facade, overcast late afternoon, diffuse soft daylight that removes harsh shadows and reveals texture, board-formed concrete with deep relief and visible aggregate, weathering streaks suggesting age, narrow vertical bronze-framed slot windows with warm interior light beginning to register against the cooling sky, light rain on the paving, atmospheric mist softening the background, shot on 50mm at eye level, documentary architectural photography

### Example 4: Restaurant interior, twilight glow

**Source**: Sketchup screenshot of a restaurant dining room, daytime lighting.

**Prompt**:
> Photoreal interior render of an intimate restaurant dining room at twilight, warm pendant lights low over each table casting pools of amber light, soft ambient glow from indirect coves on the textured plaster walls, dark stained oak floor, leather banquette seating in oxblood, brushed brass detailing on the bar, candles on the tables creating warm reflections in the wine glasses, blurred patrons suggesting atmosphere, deep window views showing the blue hour outside, shot on 35mm at eye level, intimate editorial photography, shallow depth of field

### Example 5: Urban tower at night with neon context

**Source**: Sketchup screenshot of a tower, daytime daylight rendering, blank urban surroundings.

**Prompt**:
> Photoreal exterior render of a slender urban tower at night, dense surrounding cityscape lit with characteristic mixed neon and tungsten signage, wet streets reflecting colored light, the tower's curtain wall illuminated from within in soft white, balconies showing scattered occupied apartments, low fog drifting between buildings, distant skyline blurred and atmospheric, shot on 50mm slightly elevated angle, cinematic urban photography, late-night documentary feel

## Iteration loop

After the first render:

1. Deliver the URL.
2. `Read` the result with vision, verify it matches the brief.
3. If it broadly works, ask: "Generate 3 variants — variant in time of day / lighting / material? Or refine this one further?"
4. If it doesn't match the brief, name the specific failure ("the facade material reads as smooth concrete instead of board-formed") and offer to retry with a refined prompt + the previous output as an additional reference for what to preserve.

## Common failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Output ignores reference, looks generic | Reference image too small (< 512px on long side) | Re-upload at higher resolution, or use a different model that accepts smaller references |
| Wrong material (concrete reads as plaster, etc.) | Material descriptor too vague in prompt | Use specific descriptors from `materials.md` — "board-formed concrete with visible aggregate" not "concrete" |
| Lighting doesn't match brief | Time-of-day language too generic | Use specific recipes from `lighting.md` — "golden hour, warm low-angle sun, long shadows" not "evening" |
| Image is photoreal but composition is off | Model defaulted to text-to-image, ignoring reference | Confirm via `get_model_schema` that the model accepts image input; try a different image-to-image archetype |
| Result is "stylized" when user wants photoreal | Wrong archetype picked | Re-route via `../../krea-ai/references/model-catalog.md` — "high-fidelity image" archetype, not "stylized" |
| Lighting is right but materials lost detail | Model produced over-strong stylization | Try a different model with weaker stylization, or include `imageUrl` as a stronger reference (some models support strength flags) |

## Cost guidance

For archviz workflows, default behavior should be:

- **Moodboard exploration / draft**: 1K resolution, cheap fast model
- **Client-facing iteration**: 2K resolution, high-fidelity model
- **Final hero / print**: 4K resolution, premium model

Confirm 4K renders before submitting. They're typically 3-5x the cost of 1K.
