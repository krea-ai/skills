---
version: 0.1.0
name: krea-archviz
description: "Architectural visualization workflows with Krea — turn 3D screenshots from Sketchup, Rhino, Revit, or Blender into photoreal renders; compose interior or exterior scenes from multiple reference images; explore materials, lighting, and time-of-day variants. Use when the user asks for a render, an architectural visualization, an interior or exterior, a facade study, a moodboard for a building or space, or wants to apply a different style to a 3D model output. NOT for product photography (use krea-marketing) or generic image generation (use krea-ai)."
license: MIT
---

# Krea Archviz — Architectural Visualization

A vertical skill for architects, interior designers, and archviz professionals. Built on top of `krea-ai`'s MCP-first generation, with vertical-specific workflows for the most common archviz tasks.

If you're handling a generic image request (cyberpunk cat, anime character, ad creative), stay in `krea-ai`. Hand off here when the user's brief is clearly architectural.

## Bootstrap

Requires the Krea CLI (`npm install -g @krea-ai/cli && krea auth login`) by default, with Krea MCP (`mcp__krea-public-api__*` tools) as the fallback if the CLI is unavailable. See `../krea-ai/SKILL.md` Bootstrap section for full detection + install flow, and `../krea-ai/references/cli-or-mcp.md` for the parallel operation table. This skill inherits all UX rules from `../krea-ai/SKILL.md`.

## When to use this skill

- "Render this Sketchup screenshot in golden hour, photoreal"
- "Make my Revit model look photoreal, interior, midday daylight"
- "Take the chair from this image, put it in this room, in this style" (multi-reference composition)
- "Generate moodboard images for a modernist beach house"
- "Swap the concrete facade to brushed copper, keep everything else"
- "Show this lobby at dawn, golden hour, twilight, and neon night"

## When NOT to use this skill

- Product hero shots, commercial ads, social-media creative → `krea-marketing`
- Developer integration / app-building patterns → `krea-build`
- Generic image gen with no architectural intent → stay in `krea-ai`

## The four core archviz workflows

Each has a dedicated reference doc. The summary below is for routing; load the reference for the actual prompt templates and decision details.

### 1. 3D screenshot → photoreal render

The most common archviz task. User has a Sketchup / Rhino / Revit / Blender output and wants a photoreal version.

- `Read` the screenshot with vision first to identify scene type, implied lighting, visible materials
- Upload via `mcp__krea-public-api__upload_asset` (file ≥ 1024px on long side for good anchoring)
- Pick a high-fidelity image-to-image archetype from `../krea-ai/references/model-catalog.md`
- Prompt structure: `[scene type] + [target style] + [time of day] + [lighting quality] + [material details] + [atmosphere]`
- Iterate: first variant for approval, then 2-3 more with adjustments

See `references/screenshot-to-render.md` for the full workflow + 5 worked examples.

### 2. Multi-image composition

"Take element X from image A, put it in environment B, in the style of image C." Hard for the legacy Krea image/edit tool; well-suited to agent orchestration.

- Read each reference with vision; build an explicit decomposition (subject / environment / style)
- Upload all references
- Pick a multi-reference model (check schema via `mcp__krea-public-api__get_model_schema` — needs `imageUrls` array, not single `imageUrl`)
- Prompt structure: explicit per-reference role descriptions

See `references/composition.md` for the pattern, common failure modes, and how to recover.

### 3. Time-of-day / mood variants

User has a render that's working and wants 4–8 variants across times of day, weather, or moods.

- Take the working render as the reference
- Pick the same model used to produce it (consistency)
- Use `references/lighting.md` recipes to build the prompts
- Submit variants in parallel where the MCP allows; otherwise sequentially with same seed

### 4. Material / surface swap

"Same building, but the facade is brushed copper instead of concrete." Image-to-image edit where most of the composition is preserved.

- Reference image of the source
- Pick an edit-capable image-to-image archetype from `../krea-ai/references/model-catalog.md` (verify via `get_model_schema` that the model supports preservation-style edits, not just text-to-image replacement)
- Prompt: focus on what *changes*, not what stays. "swap concrete facade to brushed oxidized copper, keep all other surfaces and lighting unchanged"
- Reference `references/materials.md` for descriptor vocabulary

## Workflow shape (common to all 4)

```
1. Read user attachments with vision (Claude's Read tool, not upload_asset)
2. Identify the workflow above that fits the brief
3. Resolve the model archetype via ../krea-ai/references/model-catalog.md
4. get_model_schema(model=<id>) — confirm input field names and required params
5. upload_asset(...) for any local references
6. generate_image(...) with sync=true (archviz is image-only by default)
7. Download the output, Read it with vision, verify it matches the brief
8. Deliver URL + one-line summary
```

For animated walkthroughs, fly-throughs, or any video output, hand off to `../krea-ai/references/video-production.md` for the polling pattern.

## UX rules (extends krea-ai)

Inherits all UX rules from `../krea-ai/SKILL.md`. Additions specific to archviz:

- **Aspect ratio defaults by intent.**
  - Exterior hero → 16:9
  - Interior → 3:2 or 4:3 (16:9 often crops too aggressively at typical ceiling heights)
  - Panoramic / portfolio cover → 2:1 or 21:9
  - Square moodboard tile → 1:1
  - See `references/aspect-ratios.md` for full table
- **Always confirm the first variant before generating siblings.** Arc-viz briefs are detailed and rendering 6 wrong variants is expensive. One first, then iterate.
- **Resolution rules of thumb.** 1K for exploration / moodboards. 2K for client presentation. 4K only when the brief explicitly calls for hero or print output — cost scales hard.
- **Read user references at full vision before picking a model.** A Sketchup wireframe and a Revit photoreal preview need different image-to-image strengths. Vision-first lets you pick correctly the first time.

## Reference docs

Load on demand:

- `references/screenshot-to-render.md` — the canonical workflow with 5 worked examples
- `references/materials.md` — descriptor vocabulary for 15+ common materials
- `references/lighting.md` — 8 lighting recipes (golden hour exterior, midday interior, overcast facade, twilight, night neon, etc.)
- `references/composition.md` — multi-image composition patterns and failure modes
- `references/aspect-ratios.md` — archviz format conventions

## Model selection (defer to krea-ai)

This skill does NOT maintain its own model catalog. Always resolve concrete model IDs via:

```
list_models()                        → returns all currently-supported models
get_model_schema(model=<id>)         → returns the exact input shape for one model
```

Use `../krea-ai/references/model-catalog.md` for the intent → archetype mapping. The archetypes most relevant to archviz:

- **High-fidelity image (photoreal, hero shots)** — for final renders
- **Image-to-image / face reference** — for screenshot → render (subset of high-fidelity)
- **Stylized / illustrated** — when the user wants painted, watercolor, or hand-drawn looks instead of photoreal

If the user explicitly names a model ("use nano-banana-pro for this"), honor it — skip the archetype routing.

## Project preferences

Honor `KREA_PREFERENCES.md` per `../krea-ai/references/preferences.md`. Useful overrides for archviz teams:

```markdown
## Krea preferences

- Default to 3:2 aspect for interiors, 16:9 for exteriors
- Skip cost confirmation under 100 CU
- For final hero shots, prefer nano-banana-pro
- For moodboard exploration, use flux-1-dev
- Brand style ID: style_xyz123 (apply with strength 0.8 to all client renders)
```

A "champion" in the studio maintains this file as defaults evolve.
