#!/usr/bin/env bash
# Check relative references/workflows markdown targets inside krea-ai docs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0
pattern='(\.\./)?(references|workflows)/[A-Za-z0-9_./-]+\.md'

while IFS=: read -r file line text; do
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    case "$ref" in
      ../*) target="$(dirname "$file")/$ref" ;;
      *) target="$(dirname "$file")/$ref" ;;
    esac
    if [ ! -e "$target" ]; then
      echo "::error file=$file,line=$line::Missing doc reference: $ref -> $target"
      fail=1
    fi
  done < <(printf '%s\n' "$text" | rg -No "$pattern")
done < <(rg -n "$pattern" krea-ai/SKILL.md krea-ai/workflows krea-ai/references)

exit "$fail"
