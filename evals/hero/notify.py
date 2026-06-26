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
    ap.add_argument("--repo", default="", help="owner/name, for linking case files (e.g. krea-ai/skills)")
    ap.add_argument("--ref", default="", help="git ref/sha the eval ran against, for case-file links")
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
    header = f"{'✅' if ok else '❌'} Hero evals — {passed}/{total} variants passed"

    # Group results by eval (case). Within a group the content is ordered for readability:
    # one verdict line per variant first, then ALL warnings pooled, then the fix(es) last
    # (the bottommost item) — each warning/fix tagged with its variant so it stays traceable.
    icons = {"PASS": "✅", "FAIL": "❌", "MANUAL_REVIEW": "🟡", "ERROR": "💥"}
    groups = []
    for c in s.get("results", []):
        key = c.get("case") or c.get("id")
        if not groups or groups[-1]["key"] != key:
            groups.append({"key": key, "title": c.get("title") or key,
                           "file": c.get("file", ""), "rows": []})
        groups[-1]["rows"].append(c)

    # The eval title links to its case file (where the prompts + rubric actually live) when we
    # know the repo + ref; otherwise it falls back to plain bold (e.g. local runs).
    blob_base = (f"https://github.com/{args.repo}/blob/{args.ref}/evals/hero/cases"
                 if args.repo and args.ref else "")

    # One section block per eval, each preceded by a divider for clear visual separation.
    # `lines` keeps a flat copy for the no-webhook plain-text fallback.
    case_blocks, lines = [], []
    for g in groups:
        vs = [r.get("verdict", "") for r in g["rows"]]
        npass = sum(1 for x in vs if x == "PASS")
        gicon = "✅" if npass == len(vs) else ("💥" if "ERROR" in vs else "❌")
        title_md = (f"<{blob_base}/{g['file']}|{g['title']}>"
                    if (blob_base and g.get("file")) else f"*{g['title']}*")

        verdicts, warns, fixes = [], [], []
        for r in g["rows"]:
            ic = icons.get(r.get("verdict"), "•")
            tag = str(r.get("variant", "")).strip()
            tagmd = f"`{tag}` " if tag else ""
            reason = (r.get("reason") or "").strip().replace("\n", " ")
            verdicts.append(f"{ic}  {tagmd}{reason[:600]}" if reason
                            else f"{ic}  {tagmd}{r.get('verdict')}")
            for w in (r.get("warnings") or []):
                w = str(w).strip().replace("\n", " ")
                if w:
                    warns.append(f"⚠️ {tagmd}{w[:300]}")
            fix = " · ".join(x.strip() for x in (r.get("fix") or "").splitlines() if x.strip())
            if fix:
                fixes.append(f"💡 {tagmd}*fix:* {fix[:900]}")

        parts = [f"{gicon}  {title_md}  ({npass}/{len(vs)} variants passed)", *verdicts]
        if warns:
            parts += ["", *warns]   # blank line separates warnings from the verdict lines
        if fixes:
            parts += ["", *fixes]   # fix(es) always last
        case_blocks.append({"type": "divider"})
        case_blocks.append({"type": "section",
                            "text": {"type": "mrkdwn", "text": "\n".join(parts)[:2900]}})
        lines += parts + [""]

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
            {"type": "mrkdwn", "text": f"*Evals:* {len(groups)}"},
            {"type": "mrkdwn", "text": f"*Variants:* {total} (2-3 prompt phrasings per eval)"},
            {"type": "mrkdwn", "text": f"*✅ Passed:* {passed} variants"},
            {"type": "mrkdwn", "text": f"*❌ Failed:* {fail} variants"},
            {"type": "mrkdwn", "text": f"*⚠️ Warnings:* {warn}"},
            {"type": "mrkdwn", "text": f"*Review / Errors:* {review} / {error}"},
        ]},
    ]
    blocks += case_blocks  # each eval group brings its own leading divider
    if context_line:
        blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": context_line[:1000]}]})
    if args.run_url:
        blocks.append({"type": "actions", "elements": [
            {"type": "button", "text": {"type": "plain_text", "text": "View CI run"},
             "url": args.run_url}]})

    text_fallback = f"Hero evals: {passed}/{total} passed, {fail} failed, {error} errors"

    webhook = os.environ.get("NOTIFY_WEBHOOK_URL")
    if not webhook:
        counts = f"{len(groups)} evals · {total} variants · {passed} pass · {fail} fail · {warn} warn"
        print("notify: NOTIFY_WEBHOOK_URL unset; summary below:\n"
              f"{header}\n{counts}\n{context_line}\n" + "\n".join(lines))
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
