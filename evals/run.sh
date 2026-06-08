#!/usr/bin/env bash
# krea-skills evals — runs scenarios from evals/scenarios.md through `claude -p`
# headless mode, grades with regex.
#
# Usage:
#   ./evals/run.sh                # v1: regex + MANUAL_REVIEW for ambiguous
#   ./evals/run.sh --judge        # v2: re-pipe MANUAL_REVIEW through claude-as-judge (disabled)
#   ./evals/run.sh --only 1,5,12  # run only those scenarios (by number)
#   ./evals/run.sh --limit 3      # run first N scenarios only
#
# Outputs land in runs/<timestamp>/ at the repo root. .gitignored.
#
# Exit code 0 if all PASS, 1 if any FAIL, 2 if there are MANUAL_REVIEW cases and no --judge.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCENARIOS_FILE="$SKILL_DIR/evals/scenarios.md"

# ─── Load .env.local if present ─────────────────────────────
if [ -f "$SKILL_DIR/.env.local" ]; then
  # shellcheck disable=SC1091
  set -a
  . "$SKILL_DIR/.env.local"
  set +a
fi

# ─── Output dir: runs/<timestamp>/ ──────────────────────────
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
OUT_DIR="${EVAL_OUT_DIR:-$SKILL_DIR/runs/$TIMESTAMP}"
mkdir -p "$OUT_DIR"

# ─── Flags ──────────────────────────────────────────────────
JUDGE_MODE=0
ONLY=""
LIMIT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --judge)
      JUDGE_MODE=1
      shift
      ;;
    --only)
      shift
      ONLY="$1"
      shift
      ;;
    --limit)
      shift
      LIMIT="$1"
      shift
      ;;
    --help|-h)
      sed -n '2,13p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 2
      ;;
  esac
done

# ─── Prerequisites ──────────────────────────────────────────
if ! command -v claude >/dev/null 2>&1; then
  echo "ERROR: claude CLI not on PATH. Install Claude Code first." >&2
  exit 2
fi

if [ ! -f "$SCENARIOS_FILE" ]; then
  echo "ERROR: scenarios file missing at $SCENARIOS_FILE" >&2
  exit 2
fi

echo "==> Eval run starting"
echo "    Output dir: $OUT_DIR"
echo "    Scenarios:  $SCENARIOS_FILE"
[ -n "$ONLY" ]    && echo "    Only:       $ONLY"
[ "$LIMIT" -gt 0 ] && echo "    Limit:      $LIMIT"
echo ""

# ─── Parse scenarios ────────────────────────────────────────
awk '
  /^## Format spec/ {
    if (in_scenario) { printf "---\n" }
    exit
  }
  /^### [0-9]+\./ {
    if (in_scenario) { printf "---\n" }
    in_scenario = 1
    title = $0; sub(/^### /, "", title)
    num = title; sub(/\..*$/, "", num)
    print "NUMBER=" num
    print "TITLE=" title
    next
  }
  in_scenario && /\*\*Category\*\*:/ {
    cat = $0; sub(/.*\*\*Category\*\*: */, "", cat)
    print "CATEGORY=" cat
    next
  }
  in_scenario && /\*\*User input\*\*:/ {
    inp = $0; sub(/.*\*\*User input\*\*: */, "", inp)
    gsub(/^"|"$/, "", inp)
    print "INPUT=" inp
    next
  }
  in_scenario && /\*\*Expected\*\*:/ {
    expected_line = $0; sub(/.*\*\*Expected\*\*: */, "", expected_line)
    print "EXPECTED=" expected_line
    next
  }
  in_scenario && /\*\*Pass regex\*\*:/ {
    pr = $0; sub(/.*\*\*Pass regex\*\*: */, "", pr)
    gsub(/^`|`$/, "", pr)
    print "PASS_REGEX=" pr
    next
  }
  in_scenario && /\*\*Fail regex\*\*:/ {
    fr = $0; sub(/.*\*\*Fail regex\*\*: */, "", fr)
    gsub(/^`|`$/, "", fr)
    print "FAIL_REGEX=" fr
    next
  }
  END { if (in_scenario) printf "---\n" }
' "$SCENARIOS_FILE" > "$OUT_DIR/parsed-scenarios.txt"

# ─── Run each scenario ──────────────────────────────────────
TOTAL=0
PASS=0
FAIL=0
REVIEW=0
ERRORED=0
RAN=0

# Filter for --only
should_run() {
  local n="$1"
  if [ -n "$ONLY" ]; then
    echo ",$ONLY," | grep -q ",$n,"
    return $?
  fi
  return 0
}

# Split parsed-scenarios.txt into individual scenario files, one per '---'-separated block.
SCENARIO_IDX=0
CURRENT_FILE=""
while IFS= read -r line; do
  if [ "$line" = "---" ]; then
    CURRENT_FILE=""
    continue
  fi
  if [ -z "$CURRENT_FILE" ]; then
    SCENARIO_IDX=$((SCENARIO_IDX + 1))
    CURRENT_FILE=$(printf "%s/scenario-%03d" "$OUT_DIR" "$SCENARIO_IDX")
    : > "$CURRENT_FILE"
  fi
  printf "%s\n" "$line" >> "$CURRENT_FILE"
done < "$OUT_DIR/parsed-scenarios.txt"

for f in "$OUT_DIR"/scenario-*; do
  [ ! -s "$f" ] && continue
  NUM=$(grep -m1 '^NUMBER=' "$f" 2>/dev/null | sed 's/^NUMBER=//')
  TITLE=$(grep -m1 '^TITLE=' "$f" 2>/dev/null | sed 's/^TITLE=//')
  INPUT=$(grep -m1 '^INPUT=' "$f" 2>/dev/null | sed 's/^INPUT=//')
  CATEGORY=$(grep -m1 '^CATEGORY=' "$f" 2>/dev/null | sed 's/^CATEGORY=//')
  PASS_REGEX=$(grep -m1 '^PASS_REGEX=' "$f" 2>/dev/null | sed 's/^PASS_REGEX=//')
  FAIL_REGEX=$(grep -m1 '^FAIL_REGEX=' "$f" 2>/dev/null | sed 's/^FAIL_REGEX=//')

  [ -z "$TITLE" ] && continue
  [ -z "$INPUT" ] && continue

  TOTAL=$((TOTAL + 1))

  # --only filter
  if [ -n "$ONLY" ] && ! should_run "$NUM"; then
    continue
  fi

  # --limit filter
  if [ "$LIMIT" -gt 0 ] && [ "$RAN" -ge "$LIMIT" ]; then
    continue
  fi

  RAN=$((RAN + 1))
  # Slug: zero-padded number + lowercased title (alphanum + hyphen only)
  SAFE_TITLE=$(echo "$TITLE" | sed -E 's/^[0-9]+\. *//' | tr '[:upper:]' '[:lower:]' | tr -c '[:alnum:]\n' '-' | sed -E 's/-+/-/g; s/^-//; s/-$//' | head -c 60)
  SCENARIO_NUM=$(printf "%02d" "$NUM")
  SCENARIO_DIR="$OUT_DIR/${SCENARIO_NUM}-${SAFE_TITLE}"
  mkdir -p "$SCENARIO_DIR"

  RESPONSE_FILE="$SCENARIO_DIR/response.txt"
  META_FILE="$SCENARIO_DIR/meta.json"
  STDERR_FILE="$SCENARIO_DIR/stderr.txt"

  START=$(date +%s)
  printf "[%2d/%s] %s … " "$NUM" "$CATEGORY" "$TITLE"

  # Run scenario through claude -p (headless, text output), from the scenario dir
  # so any files the agent downloads land here.
  if ! ( cd "$SCENARIO_DIR" && echo "$INPUT" | claude -p --output-format text ) > "$RESPONSE_FILE" 2>"$STDERR_FILE"; then
    ERRORED=$((ERRORED + 1))
    echo "ERROR (claude invocation failed) — see $STDERR_FILE"
    cat <<EOF > "$META_FILE"
{"number": "$NUM", "title": "$TITLE", "verdict": "ERROR", "category": "$CATEGORY", "duration_s": $(( $(date +%s) - START ))}
EOF
    continue
  fi

  END=$(date +%s)
  DURATION=$((END - START))

  # Grade
  if [ -n "$FAIL_REGEX" ] && grep -qE "$FAIL_REGEX" "$RESPONSE_FILE" 2>/dev/null; then
    VERDICT="FAIL"
    FAIL=$((FAIL + 1))
  elif [ -n "$PASS_REGEX" ] && grep -qE "$PASS_REGEX" "$RESPONSE_FILE" 2>/dev/null; then
    VERDICT="PASS"
    PASS=$((PASS + 1))
  else
    VERDICT="MANUAL_REVIEW"
    REVIEW=$((REVIEW + 1))
  fi

  printf "%s (%ds)\n" "$VERDICT" "$DURATION"

  # Escape input + regexes for JSON safely (avoid subscripting a print() return)
  python3 - "$NUM" "$TITLE" "$CATEGORY" "$INPUT" "$VERDICT" "$DURATION" "$PASS_REGEX" "$FAIL_REGEX" <<'PYEOF' > "$META_FILE"
import json, sys
num, title, category, inp, verdict, duration, pr, fr = sys.argv[1:9]
print(json.dumps({
  "number": num,
  "title": title,
  "category": category,
  "input": inp,
  "verdict": verdict,
  "duration_s": int(duration),
  "pass_regex": pr,
  "fail_regex": fr,
}, indent=2))
PYEOF
done

# Clean up parsed scenario files (keep only responses + meta)
rm -f "$OUT_DIR"/scenario-* "$OUT_DIR"/parsed-scenarios.txt 2>/dev/null || true

# ─── v2 judge mode (wired but disabled in v1) ────────────────
if [ "$JUDGE_MODE" -eq 1 ]; then
  echo ""
  echo "v2 judge mode is wired but disabled in v1."
  echo "When enabled, MANUAL_REVIEW responses (count: $REVIEW) would be re-piped through"
  echo "  claude -p with a judge prompt to auto-grade them."
fi

# ─── Summary ────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════"
echo "  Run:         $TIMESTAMP"
echo "  Scenarios:   $TOTAL parsed, $RAN ran"
echo "  PASS:        $PASS"
echo "  FAIL:        $FAIL"
echo "  REVIEW:      $REVIEW"
echo "  ERROR:       $ERRORED"
echo "════════════════════════════════════════════"
echo ""
echo "Outputs:     $OUT_DIR/"

# Write a JSON summary
cat <<EOF > "$OUT_DIR/summary.json"
{
  "timestamp": "$TIMESTAMP",
  "scenarios_parsed": $TOTAL,
  "scenarios_ran": $RAN,
  "pass": $PASS,
  "fail": $FAIL,
  "manual_review": $REVIEW,
  "error": $ERRORED,
  "out_dir": "$OUT_DIR"
}
EOF

# Append to runs/history.jsonl
mkdir -p "$SKILL_DIR/runs"
cat "$OUT_DIR/summary.json" | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin)))' >> "$SKILL_DIR/runs/history.jsonl"

if [ "$FAIL" -gt 0 ]; then exit 1; fi
if [ "$REVIEW" -gt 0 ] && [ "$JUDGE_MODE" -eq 0 ]; then exit 2; fi
exit 0
