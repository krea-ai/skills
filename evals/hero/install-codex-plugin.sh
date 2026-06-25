#!/usr/bin/env bash
# Install the Krea plugin into the local Codex from this repo so `codex exec` loads
# the Krea skills (not just the MCP tools). Uses a bearer-token MCP variant because
# the shipped .codex-plugin/.mcp.json is OAuth, which can't authenticate headlessly.
#
# The Krea MCP needs KREA_API_KEY in the environment at run time (resolved when codex
# connects to the MCP, not at install). Used by the eval CI and for local runs.
#
# Usage: evals/hero/install-codex-plugin.sh [WORKDIR]
# Requires: codex CLI, python3.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK="${1:-$(mktemp -d)}"
MP="$WORK/krea-mp"
rm -rf "$MP"
mkdir -p "$MP/.agents/plugins" "$MP/plugins"

# 1) Build the self-contained plugin root (skills + manifest + assets).
python3 "$REPO_ROOT/.codex-plugin/build.py" --staging-dir "$MP/plugins/krea" --no-zip

# 2) Replace the shipped OAuth MCP config with a bearer-token variant (headless-friendly).
cat > "$MP/plugins/krea/.mcp.json" <<'JSON'
{
  "mcpServers": {
    "krea": {
      "type": "http",
      "url": "https://api.krea.ai/mcp",
      "bearer_token_env_var": "KREA_API_KEY"
    }
  }
}
JSON

# 3) Minimal local marketplace manifest pointing at the built plugin.
cat > "$MP/.agents/plugins/marketplace.json" <<'JSON'
{
  "name": "krea-local",
  "interface": { "displayName": "Krea (local eval)" },
  "plugins": [
    {
      "name": "krea",
      "source": { "source": "local", "path": "./plugins/krea" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Creativity"
    }
  ]
}
JSON

# 4) Register the marketplace and install the plugin (idempotent).
codex plugin remove krea@krea-local >/dev/null 2>&1 || true
codex plugin marketplace remove krea-local >/dev/null 2>&1 || true
codex plugin marketplace add "$MP"
codex plugin add krea@krea-local

echo "Installed krea@krea-local (marketplace root: $MP)"
