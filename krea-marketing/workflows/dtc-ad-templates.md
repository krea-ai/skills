# DTC Ad Templates

## Trigger

User wants a set of on-brand **static ad stills** from one product photo: "DTC ad
templates", "ad format library", "give me N on-brand ad layouts", "a static ad set from
this product", "one product photo into many ads". This produces N separate finished stills,
one per format. If the user wants a single composed sheet/grid, use `key-visual-sheet.md`
instead; if they want a multi-format campaign across video + static, start at
`full-ad-campaign.md` and route here for the static set.

## Clarify

Ask once, in a single batched message. Skip whatever the user already gave.

- **Product reference image** (required) — a clean photo of the product to keep faithful.
- **Brand**: brand name + how the wordmark should read.
- **Product**: one-line descriptor + category (and size/variant if relevant).
- **Proof you can stand behind**: 3–5 supported claims/benefits, and — only if real — a
  customer quote, a press/outlet name, a rating, or an offer/code.
- **Brand look**: palette, one accent, preferred staging surface.
- **Aspect**: default `4:5`; offer `1:1`, `3:4`, `9:16`.
- **Scope**: the core set (default) or a named subset of format ids from
  `../references/dtc-ad-formats.md`.
- **Output folder**: default `./dtc-ads/` in the user's project.

If the brief is already tight, skip Clarify and proceed.

## Recipe

Hard prescription. Follow in order.

1. **Cost-preflight** (mandatory — `../../krea-generate/references/cost-preflight.md`). This
   is a batch (one image per selected format). Restate the brief in one line (brand,
   product, aspect, format count), show `N formats × per-image ≈ total CU` and a rough
   wall-clock, and wait for go.
2. Verify Krea MCP tools are available. Resolve a text-capable
   model from the marketing image set in `../SKILL.md` **live** from `list_models`.
   Prefer `openai/gpt-image-2` when confirmed available (strong in-image text); otherwise
   use live Nano Banana 2 if available, then Nano Banana Pro.
3. Read the product reference with vision: shape, materials, label, colour, proportions,
   hardware/trim, texture, and any visible logo/pin/embroidery — so you can judge fidelity
   later. Do not substitute PDP copy, alt text, or filenames for visual facts.
4. **Upload the reference once** through Krea MCP; capture the asset URL and reuse it for every format through the schema-declared image-reference field.
5. Load `../references/dtc-ad-formats.md`. Select formats (core set, or the user's subset).
   **Drop** any format whose `required` fields the brief can't honestly supply — do not
   invent quotes, press names, ratings, certifications, or pricing.
6. Fill each chosen template's `{{placeholders}}` from the brief, append the universal tail,
   and resolve `{{aspect_px}}` and `{{orientation}}` from the aspect map (use the
   gpt-image-2 ÷16 column when that model is selected). For real product references,
   keep `{{product}}` category-level; prompt the format, scene, light, copy, and placement,
   not product color/material/garment descriptors.
7. **Generate one image per format** — submit every selected format's job first (async),
   then poll them all, so the batch's wall-clock is roughly one job's time rather than N×.
   Model-aware hard requirements:
   - `openai/gpt-image-2`: pass explicit width/height in **multiples of 16** when the MCP schema supports them, and run **async**; capture the returned job id, poll with MCP `get_job`, then download `result.urls[0]`.
   - Nano Banana 2 / Nano Banana Pro (schema permitting): pass the live schema's
     aspect or size fields; synchronous calls are fine only when the model completes inside the MCP timeout cap.
   - Retry transient `502`/`524`/empty-job-id with backoff. Skip a format whose file already
     exists (resumable).
8. **Blocking Vision-QA gate for each output against its structural device** (`../../krea-generate/references/vision-qa.md`).
   One line per image: does the device hold? `comparison-diptych` = exactly one hairline
   rule, no VS badge; `spec-leader-lines` = leader lines to small-caps labels; `ugc-two-panel`
   = two visibly separate panels (photo + card); `before-after` = distinct BEFORE/AFTER; hero
   = single light + near-black falloff + no props. Also check product identity and that text
   is legible and correctly spelled. Reject Recolored logo, Prompt-text override, wrong
   product identity, and unsupported claims. Regenerate failures (move one lever); leave
   the passes. Do not present the batch as finished or on-brand before this gate is recorded.
9. **Deliver images only**, named by format id into the output folder (e.g.
   `./dtc-ads/comparison-diptych.png`), with a short QA note per image and any unsupported
   copy removed. Offer one-lever variants on request.

### MCP path

Use the available Krea MCP tools to list models and inspect the selected model
schema to confirm the image-input field and size/aspect params, then call image generation
with the schema-verified prompt, reference, and dimensions; poll slow jobs with the available
job-status tool.

## Banned

- Do not invent claims, quotes, press names, ratings, certifications, or pricing. Drop the
  format instead.
- Do not build product prompts from PDP copy alone or use product descriptors when a
  reference image exists.
- Do not skip the structural-device QA — a pretty image that isn't the format is a miss.
- Do not run `openai/gpt-image-2` synchronously when it is slow, and do not use non-divisible-by-16 dimensions.
- Do not pad to the whole library when the brief only supports a few formats.
- Do not write generated images into the skill's own directory; deliver them into the
  user's project output folder.

## Cost & time

- One image per selected format; core set ≈ 16 images. Per-image CU is model-dependent;
  submitting all jobs async and then polling keeps the batch's
  wall-clock near a single job's time (minutes), even for the full set.
- Regenerations from QA add a few images. No video, no upscale here.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Empty job_id / 502 / 524 on submit | transient origin/proxy error | Retry with backoff; keep async for slow models |
| `gpt-image-2` dimension error | width/height not multiples of 16 | Use the ÷16 column of the aspect map |
| Image is pretty but off-type | structural device didn't render | Regenerate that format; restate the device literally, move one lever |
| Product identity wrong | weak or partial reference, or model drift | Re-upload a cleaner reference; restate "true to the reference" |
| Recolored logo | product reference became a tinted graphic/logo-like mark | Retake with photo-first settings, cleaner ref, and scene-only prompt |
| Prompt-text override | output follows prompt product words instead of the reference | Remove product descriptors; keep format, scene, light, copy, and placement |
| Garbled or misspelled text | model text limits | Prefer `openai/gpt-image-2`; shorten copy; regenerate |
| A format looks empty/generic | brief lacked its `required` field | Drop it, or supply the missing quote/press/offer and re-run |
