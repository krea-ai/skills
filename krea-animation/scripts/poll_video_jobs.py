#!/usr/bin/env python3
"""Prepare Krea MCP job status checks and optionally download completed raw clips."""

from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path

from _common import project_root


def read_jobs(path: Path) -> list[tuple[str, str]]:
    jobs: list[tuple[str, str]] = []
    if not path.exists():
        return jobs
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1] and parts[1] != "FAILED":
            jobs.append((parts[0], parts[1]))
    return jobs


def download(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as response:
        out.write_bytes(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    parser.add_argument("--download", action="store_true", help="Download completed raw clips")
    parser.add_argument("--results-jsonl", help="Optional JSONL file of MCP get_job responses to merge")
    args = parser.parse_args()

    root = project_root(args.project)
    jobs_path = root / "04_generation/jobs/jobs.tsv"
    results_path = root / "04_generation/jobs/results.tsv"
    checks_path = root / "04_generation/jobs/mcp-status-checks.jsonl"
    raw_dir = root / "05_edit/shots_raw"
    pending = read_jobs(jobs_path)
    if not pending:
        raise SystemExit(f"No jobs found at {jobs_path}")

    checks_path.write_text(
        "\n".join(
            f'{{"shot_id": "{shot_id}", "tool": "get_job", "jobId": "{job_id}"}}'
            for shot_id, job_id in pending
        )
        + "\n",
        encoding="utf-8",
    )

    results: list[str] = []
    if args.results_jsonl:
        import json

        responses = Path(args.results_jsonl).read_text(encoding="utf-8").splitlines()
        for line in responses:
            if not line.strip():
                continue
            data = json.loads(line)
            shot_id = str(data.get("shot_id", ""))
            status = str(data.get("status", "unknown"))
            result = data.get("result") if isinstance(data.get("result"), dict) else {}
            urls = result.get("urls") if isinstance(result.get("urls"), list) else data.get("urls")
            url = urls[0] if isinstance(urls, list) and urls else ""
            if status == "completed":
                if args.download and url:
                    out = raw_dir / f"shot-{shot_id}-raw.mp4"
                    if not out.exists():
                        download(url, out)
                results.append(f"{shot_id}\tcompleted\t{url}")
            elif status in {"failed", "cancelled"}:
                results.append(f"{shot_id}\t{status}\t")
        results_path.write_text("\n".join(results) + ("\n" if results else ""), encoding="utf-8")

    with results_path.open("a", encoding="utf-8") as handle:
        for shot_id, job_id in pending:
            handle.write(f"{shot_id}\tpending\t{job_id}\n")
    print(f"Wrote MCP status checks: {checks_path}")
    print(f"Wrote {results_path}")


if __name__ == "__main__":
    main()
