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
    warn = s.get("warnings", 0)
    total = s.get("variants", passed + fail + review + error)
    ok = (args.outcome == "success") if args.outcome else (fail == 0 and error == 0)
    header = f"{'✅' if ok else '❌'} Hero evals — {passed}/{total} passed"

    # Per-case one-liners for quick triage.
    # Group results under each case's short title; one "what went right/wrong" line
    # per variant, so the report reads as named tests rather than bare ids.
    icons = {"PASS": "✅", "FAIL": "❌", "MANUAL_REVIEW": "🟡", "ERROR": "💥"}
    groups = []
    for c in s.get("results", []):
        key = c.get("case") or c.get("id")
        if not groups or groups[-1]["key"] != key:
            groups.append({"key": key, "title": c.get("title") or key, "rows": []})
        groups[-1]["rows"].append(c)

    # One section block per case → Slack shows clear spacing between each eval point.
    # `lines` keeps a flat, blank-line-separated copy for the no-webhook plain-text fallback.
    case_blocks, lines = [], []
    for g in groups:
        vs = [r.get("verdict", "") for r in g["rows"]]
        npass = sum(1 for x in vs if x == "PASS")
        gicon = "✅" if npass == len(vs) else ("💥" if "ERROR" in vs else "❌")
        glines = [f"{gicon}  *{g['title']}*  ({npass}/{len(vs)})"]
        for r in g["rows"]:
            ic = icons.get(r.get("verdict"), "•")
            tag = str(r.get("variant", "")).strip()
            label = f"`{tag}`  " if tag else ""
            reason = (r.get("reason") or "").strip().replace("\n", " ")
            glines.append(f"{ic}  {label}{reason[:1500]}" if reason
                          else f"{ic}  {label}{r.get('verdict')}")
            for w in (r.get("warnings") or []):
                w = str(w).strip().replace("\n", " ")
                if w:
                    glines.append(f"⚠️ {w[:300]}")
            fix = " · ".join(x.strip() for x in (r.get("fix") or "").splitlines() if x.strip())
            if fix:
                glines.append(f"💡 *Suggested fix:* {fix[:1500]}")
        case_blocks.append({"type": "section",
                            "text": {"type": "mrkdwn", "text": "\n".join(glines)[:2900]}})
        lines += glines + [""]  # trailing blank line spaces each case apart in plain text

    ctx = [f"model `{s.get('model', '?')}`"]
    if args.trigger:
        ctx.append(f"trigger `{args.trigger}`")
    if args.reason:
        ctx.append(args.reason)
    context_line = " · ".join(ctx)

    # Rich block layout for a clean card, with a plain-text fallback.
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": header[:150], "emoji": True}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*Passed:* {passed}/{total}"},
            {"type": "mrkdwn", "text": f"*Failed:* {fail}"},
            {"type": "mrkdwn", "text": f"*Warnings:* {warn}"},
            {"type": "mrkdwn", "text": f"*Review:* {review}"},
            {"type": "mrkdwn", "text": f"*Errors:* {error}"},
        ]},
        {"type": "divider"},
    ]
    blocks += case_blocks
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
