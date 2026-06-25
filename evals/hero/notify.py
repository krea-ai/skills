#!/usr/bin/env python3
"""Post a hero-eval run summary to a webhook. Stdlib only.

Reads NOTIFY_WEBHOOK_URL from the environment. If it is unset, prints the summary
and exits 0 (never fails the CI job over a missing webhook).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def _section_chunks(lines: list, limit: int = 2800) -> list:
    """Pack per-case lines into mrkdwn section blocks under Slack's ~3000-char limit."""
    blocks, buf = [], ""
    for ln in lines:
        if buf and len(buf) + len(ln) + 1 > limit:
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": buf}})
            buf = ln
        else:
            buf = f"{buf}\n{ln}" if buf else ln
    if buf:
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": buf}})
    return blocks


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
        print(f"notify: cannot read summary ({e}); skipping.", file=sys.stderr)
        return 0

    passed = s.get("pass", 0)
    fail = s.get("fail", 0)
    review = s.get("manual_review", 0)
    error = s.get("error", 0)
    total = s.get("variants", passed + fail + review + error)
    ok = (args.outcome == "success") if args.outcome else (fail == 0 and error == 0)
    header = f"{'✅' if ok else '❌'} Hero evals — {passed}/{total} passed"

    # Per-case one-liners for quick triage.
    # Per-case line + the judge's one-line "what went right / wrong" summary.
    icons = {"PASS": "✅", "FAIL": "❌", "MANUAL_REVIEW": "🟡", "ERROR": "💥"}
    lines = []
    for c in s.get("results", []):
        v = c.get("verdict", "")
        line = f"{icons.get(v, '•')} `{c.get('id')}` — *{v}*"
        reason = (c.get("reason") or "").strip().replace("\n", " ")
        if reason:
            line += f"\n› {reason[:220]}"
        lines.append(line)

    ctx = [f"model `{s.get('model', '?')}`"]
    if args.trigger:
        ctx.append(f"trigger `{args.trigger}`")
    if args.reason:
        ctx.append(args.reason)
    context_line = " · ".join(ctx)

    # Slack Block Kit for a clean layout, with a plain-text fallback.
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": header[:150], "emoji": True}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*Passed:* {passed}/{total}"},
            {"type": "mrkdwn", "text": f"*Failed:* {fail}"},
            {"type": "mrkdwn", "text": f"*Review:* {review}"},
            {"type": "mrkdwn", "text": f"*Errors:* {error}"},
        ]},
    ]
    blocks += _section_chunks(lines)
    if context_line:
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": context_line[:1000]}]})
    if args.run_url:
        blocks.append({"type": "actions", "elements": [
            {"type": "button", "text": {"type": "plain_text", "text": "View CI run"},
             "url": args.run_url}]})

    text_fallback = f"Hero evals: {passed}/{total} passed, {fail} failed, {error} errors"

    webhook = os.environ.get("NOTIFY_WEBHOOK_URL")
    if not webhook:
        print("notify: NOTIFY_WEBHOOK_URL unset; summary below:\n"
              f"{header}\n{context_line}\n" + "\n".join(lines))
        return 0

    payload = json.dumps({"text": text_fallback, "blocks": blocks}).encode()
    req = urllib.request.Request(webhook, data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp.read()
    except urllib.error.URLError as e:
        print(f"notify: post failed ({e}); not failing the job.", file=sys.stderr)
        return 0
    print("notify: posted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
