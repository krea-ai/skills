#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$REPO_ROOT/clawhub"

rm -rf "$OUT"
mkdir -p "$OUT/scripts"

cp "$REPO_ROOT"/scripts/*.py "$OUT/scripts/"

sed 's|uv run scripts/|uv run ~/.codex/skills/krea/scripts/|g' \
    "$REPO_ROOT/SKILL.md" > "$OUT/SKILL.md"

echo "Built clawhub/ bundle at $OUT"
echo "Upload this folder to clawhub.ai/upload"
