# Project Preferences

Krea's model lineup changes fast and what's "best" depends on the project (architecture studio vs. boutique creative vs. enterprise marketing all want different defaults). To avoid hardcoding choices in this skill, projects can override defaults via a preferences file.

## Where preferences live

The skill checks, in this order:

1. `KREA_PREFERENCES.md` at the repository root
2. A `## Krea preferences` H2 section inside the repo's `CLAUDE.md`
3. A `## Krea preferences` H2 section inside the user-level `~/.claude/CLAUDE.md`

The first match wins.

If none exist, the skill uses the archetype defaults in `model-catalog.md`.

## Format

Free-form markdown with bullet points. The skill reads it as guidance, not as a structured config. Examples:

```markdown
## Krea preferences

- Default to `flux-1-dev` for fast image drafts
- For final image work, prefer `nano-banana-pro` over `gpt-image`
- Use `seedance-2.0` for any cinematic / multi-shot video
- For face animation, prefer Kling over Veo (Kling handles faces better in our tests)
- Always check `topaz-standard-enhance` first for upscaling before reaching for generative variants
- Stick to 16:9 aspect ratio unless the brief explicitly calls for vertical
```

## What the skill does with preferences

1. When picking an archetype's candidate model, **honor explicit pins** in the preferences file. ("Default to X for Y" — use X for Y.)
2. When the user gives a brief that the preferences don't cover, fall back to the archetype default in `model-catalog.md`.
3. When the preferences and the user's explicit instruction conflict, the user wins. ("Use gpt-image for this one" overrides "prefer nano-banana-pro for final".)

## Updating preferences

A common pattern: one or two "champions" in a studio or org maintain the preferences file as new models ship. The skill doesn't auto-update it — that's intentional. The champion knows the team's taste; the skill doesn't.

If you (the agent) repeatedly notice the user picking the same model for the same intent, you can offer once: *"I notice you keep choosing X for this kind of brief. Want me to pin that in `KREA_PREFERENCES.md`?"* — then stop and wait for an answer. Don't write the file unprompted.

## When NOT to write preferences

- Don't write a preferences file just to record what a one-off generation used.
- Don't pin a model the user has only tried once.
- Don't store user-specific secrets, API keys, or personal data here. Preferences are committed to the repo.
