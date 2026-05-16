# Multi-Image Composition

Nitsan's specific ask: *"take only the chair from image A, put it in the right side of the room of image B, and make them in the style of image C"*. The legacy Krea image / edit tools don't handle this well. An agent that orchestrates multi-reference generation does, if the chosen model supports multi-image input.

## When to use this workflow

- "Put this product in this scene"
- "I want this material on this building"
- "Apply this style to this room"
- "Use this character in this setting"
- Any brief with the pattern "X from A in B in style of C"

If the user only provides one reference, this is just image-to-image — handle it under `screenshot-to-render.md`.

## Workflow

```
1. Read EACH reference with vision (Claude's Read tool)
2. Build an explicit decomposition: which image is "subject", which is "environment",
   which is "style"? Confirm this with the user if the brief is ambiguous.
3. Verify all references are ≥1024px on the long side. If any are smaller, ask the
   user for a higher-resolution version — small refs anchor poorly.
4. Pick a multi-reference-capable model from ../../krea-ai/references/model-catalog.md
   (need imageUrls: array, not imageUrl: singular)
5. get_model_schema(model=<id>) — confirm the schema accepts an array
6. Upload all references via upload_asset
7. Submit generate_image with all upload URLs in imageUrls + an explicit prompt
   that names each reference's role
8. Read result with vision — multi-ref is where vision verification matters most
9. If wrong, iterate with the failure mode notes below
```

## Prompt structure for multi-image

Models don't reliably understand "reference 1 / reference 2 / reference 3" by index — they understand descriptive role labels. Always use descriptive anchors, not index labels.

> [overall scene description], featuring [the subject described — "the Eames lounge chair shown isolated"], placed within [the environment described — "the modernist living room with stone fireplace"], rendered in [the style described — "warm-toned 1970s film photography with grain"]

### Worked example: chair-in-room-in-style

References:
- Image A: photo of an Eames lounge chair, isolated on white background
- Image B: photo of a modernist living room with a fireplace
- Image C: warm-toned vintage 1970s photograph with film grain

**Prompt**:
> Interior scene of a modernist living room with a stone fireplace, featuring the isolated Eames lounge chair placed in the foreground angled toward the fireplace, the living room's composition and furnishings preserved, rendered in the warm-toned 1970s film photography style with subtle grain and warm color cast

## Common failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Result ignores subject (e.g. chair) | Subject reference too small or has too much background | Re-crop the subject closer to frame edges; re-upload at ≥1024px |
| Result ignores environment | Style reference dominated because it was visually striking | Reorder the prompt — describe environment first, then style |
| Result is a generic blend, no clear role | Prompt assigned roles by index, not by description | Use descriptive anchors: "the isolated chair", "the modernist living room", "the 1970s film style" |
| Style applied but composition is wrong | Model treated style ref as compositional ref too | Use simpler style references (texture / palette only), not fully-composed images |
| Result is photoreal when user wanted style C applied | Style ref isn't strong enough or model defaulted to base behavior | Make style descriptors more concrete: "warm-toned 1970s film with grain" not "vintage style" |
| Subject placed in wrong location | Model has weak spatial control | Add compositional cues: "in the foreground", "to the right of the central fireplace", "occupying the lower-right third" |

## Model selection

This workflow specifically needs models that accept **multiple reference images** (the schema's `imageUrls` field as an array, not a single `imageUrl`).

Don't hardcode — resolve via:

```
list_models()
get_model_schema(model=<candidate_id>)
# look for imageUrls: array in inputSchema.properties
```

If the model only accepts a single reference, true 3-image composition isn't possible with that model (pass 1 of any two-pass approach already needs both subject AND environment). Options in order of preference:

1. **Pick a different model.** Multi-reference models exist in the Krea lineup — check `../../krea-ai/references/model-catalog.md` for archetypes that declare `imageUrls` arrays in their schema.
2. **Pre-composite the subject into the environment outside of generation** (a quick image-edit step, or upload a hand-composited reference), then use that as the single image input for the style transfer pass.
3. **Describe one element in text.** If the subject is well-known and generic ("an Eames lounge chair"), describe it in the prompt and use only the environment + style references. Loses fidelity to a specific subject; only useful when the subject is iconic enough that text alone anchors it.

## Spatial control

Models vary in how well they respect spatial cues. Strongest to weakest:

1. **Models with explicit start-frame anchoring** — best for "subject occupies this region"
2. **Models with image-prompt influence** — decent
3. **Pure text-to-image with reference style** — weakest spatial control

For tightly composed scenes ("the chair must be on the right side of the room, not the left"), prefer the first category. If using a weaker model, expect 2-3 retries to get the placement right.

## Cost considerations

Multi-image generations are typically 1.5-2x the cost of single-reference. Confirm with the user before generating 4+ variants of a multi-reference composition — that's the cost of a small batch job.
