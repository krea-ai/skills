#!/usr/bin/env bash
# Check relative references/workflows markdown targets inside Krea skill docs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0
pattern='((\.\./)+)?([A-Za-z0-9_-]+/)?(references|workflows)/[A-Za-z0-9_./-]+\.md'

targets=()
for root in krea-generate krea-marketing krea-animation wip; do
  if [ -e "$root" ]; then
    while IFS= read -r file; do
      targets+=("$file")
    done < <(find "$root" -type f -name '*.md' | sort)
  fi
done

# Every skill root a link may be written against. Docs address sibling files
# either file-relatively (`../references/x.md`) or from their own skill root
# (`references/x.md`) — the latter is what hosted runtimes that key skill files
# by manifest path require, so both forms have to resolve. Cross-skill mentions
# name the owning skill in prose, so a bare `references/…` may belong to any
# skill root, not just the current one.
skill_roots=()
for root in krea-generate krea-marketing krea-animation; do
  [ -d "$root" ] && skill_roots+=("$root")
done
if [ -d wip ]; then
  while IFS= read -r dir; do
    skill_roots+=("$dir")
  done < <(find wip -mindepth 1 -maxdepth 1 -type d | sort)
fi

if [ "${#targets[@]}" -eq 0 ]; then
  echo "No markdown docs found"
  exit 0
fi

while IFS=: read -r file line text; do
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    target="$(dirname "$file")/$ref"
    found=0
    [ -e "$target" ] && found=1
    if [ "$found" -eq 0 ]; then
      for skill_root in "${skill_roots[@]}"; do
        if [ -e "$skill_root/$ref" ]; then
          found=1
          break
        fi
      done
    fi
    if [ "$found" -eq 0 ]; then
      echo "::error file=$file,line=$line::Missing doc reference: $ref (not found relative to $(dirname "$file") or any skill root)"
      fail=1
    fi
  done < <(printf '%s\n' "$text" | grep -oE "$pattern")
done < <(grep -HnE "$pattern" "${targets[@]}")

exit "$fail"
