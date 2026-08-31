#!/usr/bin/env bash
# Check relative references/workflows markdown targets inside Krea skill docs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0
pattern='((\.\./)+)?([A-Za-z0-9_-]+/)?(references|workflows)/[A-Za-z0-9_./-]+\.md'

targets=()
for root in krea-generate krea-marketing krea-motion product-packaging-design wip; do
  if [ -e "$root" ]; then
    while IFS= read -r file; do
      targets+=("$file")
    done < <(find "$root" -type f -name '*.md' | sort)
  fi
done

if [ "${#targets[@]}" -eq 0 ]; then
  echo "No markdown docs found"
  exit 0
fi

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
  done < <(printf '%s\n' "$text" | grep -oE "$pattern")
done < <(grep -HnE "$pattern" "${targets[@]}")

exit "$fail"
