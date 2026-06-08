# Marketplace Cards

Use this reference when the user asks for marketplace listing images, secondary product images, product cards, infographics, lifestyle listing shots, or A+ style content modules.

## Scopes

| Scope | Creates |
|---|---|
| `main` | One compliant lead marketplace image |
| `product_images` | Main image plus secondary product/detail/lifestyle images |
| `aplus` | Main image plus A+ style product-detail modules |
| `full_set` | Main image, secondary images, and A+ modules |

## Assets

Use these asset labels when planning a custom subset:

- `main_image`
- `infographic`
- `multi_angle`
- `detail_shot`
- `lifestyle`
- `whats_in_box`
- `aplus_hero_banner`
- `aplus_pain_points`
- `aplus_features`
- `aplus_ingredients`
- `aplus_efficacy`
- `aplus_how_to_use`
- `aplus_endorsement`

## Workflow

1. Ask for product image/URL, marketplace/category, scope, brand context, and required claims.
2. Prefer real product references. If only text exists, proceed only when product details are specific.
3. Create the main image first unless the user already has an approved main image.
4. Generate secondary/A+ modules from the approved main image and product references.
5. QA for product fidelity, unsupported claims, marketplace-safe composition, and text legibility.

## Compliance Guardrails

- Do not invent claims, certifications, medical benefits, endorsements, ratings, or comparative promises.
- Do not create fake badges, marketplace logos, or review-star systems unless the user supplied exact permitted assets.
- Call out that exact marketplace compliance still requires human/platform review.
- Keep module copy factual and user-supplied. If the user has no copy, generate visual modules without factual claims.

## Krea Pattern

Use `product-photo-hero.md` for the main image, `product-photo-lifestyle.md` for lifestyle/detail shots, and `../../krea-generate/workflows/image-text-poster.md` only when text-heavy infographics are required.
