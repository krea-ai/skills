#!/usr/bin/env bash
# Minimal frontmatter validator for packaged SKILL.md files.
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "usage: $0 path/to/SKILL.md [...]" >&2
  exit 2
fi

fail=0

for file in "$@"; do
  if [ ! -f "$file" ]; then
    echo "::error file=$file::Skill file not found"
    fail=1
    continue
  fi

  if [ "$(sed -n '1p' "$file")" != "---" ]; then
    echo "::error file=$file,line=1::Missing opening frontmatter marker"
    fail=1
    continue
  fi

  frontmatter="$(awk 'NR > 1 && $0 == "---" { exit } NR > 1 { print }' "$file")"

  check_field() {
    local field="$1"
    local pattern="$2"
    if ! printf '%s\n' "$frontmatter" | grep -qE "$pattern"; then
      echo "::error file=$file::Missing or invalid frontmatter field: $field"
      fail=1
    fi
  }

  check_field version '^version:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+[[:space:]]*$'
  check_field name '^name:[[:space:]]*[A-Za-z0-9_-]+[[:space:]]*$'
  check_field description '^description:[[:space:]]*.+$'
  check_field license '^license:[[:space:]]*[A-Za-z0-9._-]+[[:space:]]*$'
done

exit "$fail"
