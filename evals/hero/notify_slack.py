#!/usr/bin/env python3
"""Post a hero-eval run summary to Slack. Stdlib only.

Reads SLACK_WEBHOOK_URL from the environment. If it is unset, prints the summary
and exits 0 (never fails the CI job over a missing webhook).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True, help="path to the run summary.json")
    ap.add_argument("--run-url", default="", help="link to the CI run / artifacts")
    ap.add_argument("--trigger", default="", help="what triggered the run")
    ap.add_argument("--reason", default="", help="dispatch reason (client_payload)")
    ap.add_argument("--outcome", default="", help="run step outcome (success/failure)")
    args = ap.parse_args()

    try:
        s = json.loads(open(args.summary).read())
    except (OSError, json.JSONDecodeError) as e:
        print(f"notify_slack: cannot read summary ({e}); skipping.", file=sys.stderr)
        return 0

    passed = s.get("pass", 0)
    fail = s.get("fail", 0)
    review = s.get("manual_review", 0)
    error = s.get("error", 0)
    total = s.get("variants", passed + fail + review + error)
    ok = (args.outcome == "success") if args.outcome else (fail == 0 and error == 0)
    status = ":white_check_mark: PASS" if ok else ":x: FAIL"

    header = f"Hero evals {status} — {passed}/{total} passed"
    bits = [f"{fail} fail", f"{review} review", f"{error} error",
            f"model `{s.get('model', '?')}`"]
    if args.trigger:
        bits.append(f"trigger `{args.trigger}`")
    if args.reason:
        bits.append(f"_{args.reason}_")
    line2 = " · ".join(bits)

    # Per-case one-liners for quick triage.
    rows = []
    for c in s.get("results", []):
        emoji = {"PASS": "✅", "FAIL": "❌", "MANUAL_REVIEW": "🟡", "ERROR": "💥"}.get(
            c.get("verdict"), "•")
        rows.append(f"{emoji} {c.get('id')} ({c.get('verdict')})")
    detail = "\n".join(rows)

    text = f"*{header}*\n{line2}"
    if args.run_url:
        text += f"\n<{args.run_url}|View run + transcripts>"
    if detail:
        text += f"\n```\n{detail}\n```"

    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        print("notify_slack: SLACK_WEBHOOK_URL unset; summary below:\n" + text)
        return 0

    payload = json.dumps({"text": text}).encode()
    req = urllib.request.Request(webhook, data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp.read()
    except urllib.error.URLError as e:
        print(f"notify_slack: post failed ({e}); not failing the job.", file=sys.stderr)
        return 0
    print("notify_slack: posted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
