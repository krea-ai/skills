#!/usr/bin/env bash
# Check relative references/workflows markdown targets inside Krea skill docs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0
pattern='((\.\./)+)?([A-Za-z0-9_-]+/)?(references|workflows)/[A-Za-z0-9_./-]+\.md'

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
done < <(rg -n "$pattern" \
  krea-generate/SKILL.md krea-generate/workflows krea-generate/references \
  krea-marketing/SKILL.md krea-marketing/workflows krea-marketing/references \
  krea-animation/SKILL.md krea-animation/workflows krea-animation/references \
  krea-build/SKILL.md krea-build/references)

exit "$fail"
