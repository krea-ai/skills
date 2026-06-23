# Model Selection Boundary

`krea-generate` is the generic Krea skill. It must discover models from the live Krea catalog instead of maintaining project-level model recommendations.

## Rule

For every generation task:

1. List live models through Krea MCP.
2. Choose candidates by matching the user's intent against live model category, name, description, and capabilities.
3. Inspect the chosen candidate's schema through the same surface.
4. Submit only with fields present in that live schema.

Do not read `KREA_PREFERENCES.md`, `CLAUDE.md`, user memory, or local project notes as generic model-selection overrides. Those files can describe the user's brief, style, or output constraints, but they do not replace live discovery.

## Explicit User Model Requests

If the user names a model for the current request, treat that as an instruction for this request only:

1. Look for that model in live `list_models`.
2. Confirm the schema supports the needed prompt, references, aspect, duration, resolution, or enhance fields.
3. If it fits, use it.
4. If it is unavailable or lacks required fields, explain the mismatch and select the nearest live alternative.

## Where Opinionated Model Preferences Belong

Domain skills may be opinionated when the domain needs it. For example, marketing image preferences belong in `../krea-marketing/SKILL.md`, not here. Animation-specific model playbooks belong in `references/models/` after a model has already been selected from live discovery.
