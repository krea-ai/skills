---
name: krea-2-moodboards
description: Krea 2 image-generation reference covering live schema checks, moodboard discovery, and moodboard/style-reference use.
---

# Krea 2 Image Reference

Load this file only after live discovery resolves a `krea/krea-2/*` image model, or when the user explicitly asks for K2, Krea 2 Turbo, Krea 2 moodboards, style references, or Krea 2 LoRAs.

## Prompting Stance

You are an expert Krea 2 image prompt engineer. Convert the user's intent into a concrete still-image prompt where the prompt controls subject, scene, composition, camera, lighting, and constraints, while moodboards, style references, and LoRAs carry taste, palette, texture, and art direction.

This is a model-specific operating reference, not a generic model preference. Always verify the live catalog and selected model schema before submitting.

## Live Schema Check

Observed live Krea 2 image IDs on 2026-06-11 included:

- `krea/krea-2/large`
- `krea/krea-2/medium`
- `krea/krea-2/medium-turbo`

Do not assume those IDs still exist. Confirm with live `list_models` through Krea MCP, then inspect the chosen model schema.

The Krea 2 schemas observed on 2026-06-11 exposed these important fields:

| Field | Meaning |
|---|---|
| `prompt` | Subject, composition, camera, lighting, and concrete content. |
| `aspect_ratio` | One of the live enum values, such as `1:1`, `16:9`, or `9:16`. |
| `resolution` | Live enum; observed value was `1K`. |
| `creativity` | Prompt expansion mode. Observed enum: `raw`, `low`, `medium`, `high`. |
| `intensity` | K2 Intensity slider, observed integer range `-100` to `100`. |
| `complexity` | K2 Complexity slider, observed integer range `-100` to `100`. |
| `image_style_references` | Array of `{url, strength}` style-reference images, observed `maxItems: 10`. |
| `styles` | Array of `{id, strength}` style/LoRA controls. |
| `moodboards` | Array of `{id, strength}` moodboards, observed `maxItems: 1`, `id` as UUID, strength range `0` to `1`, default `0.23`. |

Use only fields present in the live schema. If a field is absent, do not approximate it with an invented input key.

## Moodboard Discovery

### Preset gallery (public)

Krea exposes the preset moodboard gallery at:

```text
GET https://www.krea.ai/api/preset-moodboards?limit=72&seed=<uuid>&search=<query>&cursor=<nextCursor>
```

Verified live on 2026-06-11: this endpoint answered without authentication and reported `total: 3549` preset boards. This is the default discovery path; the agent can search it directly.

| Param | Meaning |
|---|---|
| `limit` | Page size; `72` mirrors the web gallery. |
| `seed` | Any UUID. Stabilizes the shuffled gallery order; keep the same seed across pages of one browse session. |
| `search` | Keyword filter over the gallery, for example `search=neo`. Search by aesthetic keywords instead of paging blindly. |
| `cursor` | Pagination cursor; pass the previous response's `nextCursor`. |

Observed response shape: `{datasetName, items, nextCursor, total}`. Each item exposed `id` (the moodboard UUID used for generation), `name`/`styleName`, `styleDescription`, `styleKeywords`, `imageCount`/`totalImages`, `isStaffPick`, and `previewImages`/`images` as `{id, url, width, height}` with Krea-hosted asset URLs. Inspect the live response before relying on field names.

Preset discovery recipe:

1. Search the gallery with 1-3 aesthetic keywords from the user's brief.
2. Shortlist by `styleName`, `styleDescription`, and `styleKeywords`; prefer `isStaffPick` boards on ties.
3. Vision-check one or two `previewImages` per candidate. If the brief is loose, show the user 2-3 labeled candidates with one-line captions before generating.
4. Use the chosen item's `id` as the K2 moodboard UUID.

### Personal moodboards (authenticated)

The user's own boards live at:

```text
GET https://www.krea.ai/api/moodboards
```

This endpoint is authenticated web-app state. In an unauthenticated request on 2026-06-11 it returned HTTP `401` with:

```json
{"message":"Unauthorized"}
```

Treat this as separate from MCP auth unless the current Krea tooling explicitly documents otherwise. The ability to generate with a moodboard ID once the K2 schema exposes `moodboards` does not by itself prove that `www.krea.ai/api/moodboards` is accessible without a logged-in web session.

Safe discovery rules for personal boards:

- Use the authenticated browser/UI or a user-provided JSON sample to find moodboard IDs.
- Do not scrape local browser cookie stores or print private account payloads.
- Inspect the live response shape before relying on field names. Look for fields such as the moodboard UUID, display name/title, preview/cover assets, source images, tags, keywords, avoids, or analysis metadata, but the exact names must come from the authenticated response.
- Confirm the board is analyzed before trying to use it for generation. Krea's public article says analysis builds and saves the taste profile, keywords, and avoids used by later generations.
- Prefer a stable moodboard UUID over a display name when submitting generation jobs.

## Using Moodboards With K2

Krea's public Krea 2 material describes moodboards as a Krea 2 feature for larger style/concept sets than ordinary style references. Public pages also describe Krea 2 Turbo as compatible with style references, moodboards, and LoRAs, and describe Moodboard Gallery with many moodboards plus Random and Auto selection modes.

Treat Random and Auto as gallery/UI selection modes unless the live generation schema exposes explicit fields for them.

Generation path:

1. Resolve the Krea 2 model with live `list_models`.
2. Inspect the selected model schema.
3. Resolve the moodboard UUID: search the public preset gallery first; use the authenticated moodboard endpoint, the Krea UI, or the user for personal boards.
4. Submit `moodboards: [{ "id": "<uuid>", "strength": <0-1> }]` only when the live schema exposes that shape.
5. Keep `prompt` focused on subject, composition, scene, camera, lighting, and deliverable constraints. Let the moodboard carry style, taste, color, texture, and concept direction.

Strength guidance, unless the user says otherwise:

- `0.15` to `0.3`: light style guidance while preserving prompt literalness.
- `0.3` to `0.6`: visible moodboard influence for art direction.
- `0.6` to `1.0`: strong moodboard pull; use carefully because it can override subject and composition.

If the live schema exposes only `image_style_references`, not `moodboards`, use Krea-hosted image URLs from the moodboard as style references: the preset gallery's `previewImages`/`images` URLs qualify, as do authenticated-response assets. Do not pass arbitrary external image URLs; normalize them through `../media-inputs.md`.

If no moodboard or style-reference field exists in the live schema, do not fake the moodboard in the prompt. Either proceed prompt-only after telling the user the current schema lacks moodboard input, or ask the user to choose a Krea 2 surface that supports moodboards.

## Prompt And QA Notes

- Moodboards control taste; prompts control what is in the frame. Keep both explicit.
- If the moodboard analysis includes keywords or avoids, fold them into the prompt or negative constraints only when they match the user's brief.
- Watch for over-transfer: the output copying a moodboard subject, layout, or object when only style was intended.
- For product or identity-sensitive work, compare the generated image against the user-provided subject reference after generation. Retake if style pressure changes the product, face, logo, packaging, or required text.

## Public Source Pointers

- `https://www.krea.ai/index/moodboards-krea-2`
- `https://www.krea.ai/index/moodboard-gallery-krea-2-random-auto`
- `https://www.krea.ai/index/krea-2-turbo`
