# Product Photoshoot Modes

Use this reference for brand/product stills. It adapts the useful Higgsfield mode taxonomy into Krea-native workflows; do not call external generator commands.

## Modes

| Mode | Use when the user wants |
|---|---|
| `studio_product` | Product on neutral, studio, catalog, plinth, white, or clean ecommerce background |
| `lifestyle_scene` | Product in a real environment: kitchen, desk, gym, bathroom, outdoors, cafe |
| `closeup_person` | Hands, partial face, applying/holding/using a beauty, food, fashion, or device product |
| `pinterest_pin` | Vertical 2:3 moodboard-native product pin |
| `hero_banner` | Wide website, email, landing-page, or campaign header |
| `social_carousel` | 3-10 related static slides for Instagram, LinkedIn, Facebook, or TikTok carousel |
| `ad_creative_pack` | Coordinated static ad variants across hooks, angles, and formats |
| `virtual_try_on` | Product worn or used by an AI-rendered model |
| `conceptual_product` | Surreal, CGI-style, floating, splash, sculptural, or impossible product visual |
| `restyle` | Existing product image with a new mood, season, setting, or aesthetic while preserving subject |

## Selection Rules

- Product + neutral / clean / white / catalog / Shopify -> `studio_product`.
- Product + environment / in use / everyday context -> `lifestyle_scene`.
- Hands, face crop, application, holding, demonstrating -> `closeup_person`.
- Pinterest / pin / moodboard -> `pinterest_pin`.
- Hero / banner / landing page / email header -> `hero_banner`.
- Carousel / swipe / multiple slides -> `social_carousel`.
- Paid social / Meta ads / static ad variants -> `ad_creative_pack`.
- Model wearing / try on / fashion lookbook -> `virtual_try_on`.
- Floating / splash / surreal / CGI / sculptural -> `conceptual_product`.
- Existing image + new aesthetic/season -> `restyle`.

Tie-break by output format first. Example: "hero banner showing serum being applied" is `hero_banner`, not `closeup_person`.

## Interview

Ask only missing fields, and keep questions labeled:

- Product reference or product URL.
- Count: `1`, `3`, `5`, or platform-specific.
- Use: Shopify, PDP, Instagram, Pinterest, paid ads, website hero, marketplace.
- Style/mood: clean studio, lifestyle, conceptual, with model, seasonal, brand-specific.
- Accuracy constraints: label, logo, color, material, claim/copy.

## Krea Generation Pattern

1. Read product references with vision before generating.
2. Upload local/non-Krea references to Krea.
3. Resolve a live image model with the needed reference fields.
4. Generate one candidate before batches unless the user approved variants.
5. Vision-check product identity, label, proportions, color, and use-case plausibility.
6. Only upscale/finalize user-approved winners.

## Banned

- Do not invent product claims, ingredients, certifications, prices, ratings, or guarantees.
- Do not let aesthetics override product identity.
- Do not generate people wearing or using products when the product detail is too weak for accuracy.
- Do not run a full ad batch before one product-accurate candidate passes QA.
