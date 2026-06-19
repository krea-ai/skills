# Krea Codex Plugin Package

This directory contains Codex-specific packaging inputs for the Krea plugin.

Build the zip from the repository root:

```bash
python3 codex-plugin/build.py
```

The build script copies the canonical skill directories into a self-contained
plugin root, applies `plugin-overrides.json`, copies `codex-plugin/.mcp.json`,
and writes `codex-plugin/dist/krea-codex-plugin.zip`.

Place real Krea assets in `codex-plugin/assets/` and reference them from
`plugin-overrides.json`. The build fails if a referenced asset is missing.
