# Marketplace Cards

## Trigger

User asks for marketplace listing images, main product card, secondary product images, product infographics, lifestyle listing shots, A+ style content, marketplace image set, or sales-ready marketplace visuals.

## Clarify

Ask once, skipping what the user already gave:

- **Product reference**: image, URL, or existing Krea asset.
- **Marketplace/category**: Amazon-style, Shopify marketplace, app store, retail PDP, or other.
- **Scope**: `main`, `product_images`, `aplus`, `full_set`, or custom asset list.
- **Required copy/claims**: exact user-supplied facts only.
- **Brand context**: palette, tone, visual style, competitors to avoid.

## Recipe

1. Load `../references/marketplace-cards.md`.
2. Read product references with vision and extract only visible/product-supplied facts. If the source is a URL/PDP, use page copy only for claims/copy; do not substitute PDP text, alt text, or filenames for visual product truth.
3. Use `product-photo-hero.md` to create or validate the main image first.
4. For secondary images, use `product-photo-lifestyle.md`; for text modules, use `../SKILL.md` model guidance and a text-capable image model.
5. Generate one module type first, then batch remaining modules after visual direction is approved.
6. **Blocking QA gate**: inspect every image before delivery for product fidelity, text legibility, unsupported claims, marketplace-safe composition, Recolored logo, and Prompt-text override; use the definitions in `../references/marketplace-cards.md`. Record pass/fail; do not present a full set as ready or on-brand before this gate.
7. Deliver labeled URLs/paths by scope.

## Banned

- Do not invent ratings, claims, badges, certifications, endorsements, or guarantees.
- Do not build faithful product prompts from PDP copy alone.
- Do not use marketplace logos unless the user supplied permitted assets.
- Do not generate A+ modules before the main image is product-accurate.
- Do not claim platform compliance is guaranteed; say human/platform review is still required.

## Output

```text
Marketplace set ready:
- Main image: <url/path>
- Secondary detail: <url/path>
- Lifestyle: <url/path>
- A+ module: <url/path>
QA: <one line>
```
