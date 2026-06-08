#!/usr/bin/env bash
# Compatibility wrapper. The installable implementation lives inside
# krea-generate/scripts so skill installers that copy only skill directories
# still include the update checker.
set -euo pipefail

REPO_ROOT="${SKILL_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
TARGET="$REPO_ROOT/krea-generate/scripts/update-check.sh"

[ -f "$TARGET" ] || exit 0

SKILL_DIR="$REPO_ROOT/krea-generate" exec bash "$TARGET" "$@"
