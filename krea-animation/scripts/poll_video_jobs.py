#!/usr/bin/env python3
"""Poll Krea video jobs and optionally download completed raw clips."""

from __future__ import annotations

import argparse
import time
import urllib.request
from pathlib import Path

from _common import command_exists, result_url, run_json, project_root


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
    parser.add_argument("--interval", type=int, default=20, help="Polling interval in seconds")
    parser.add_argument("--max-iterations", type=int, default=120)
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    args = parser.parse_args()

    if not command_exists("krea"):
        raise SystemExit("krea CLI not found")

    root = project_root(args.project)
    jobs_path = root / "04_generation/jobs/jobs.tsv"
    results_path = root / "04_generation/jobs/results.tsv"
    raw_dir = root / "05_edit/shots_raw"
    pending = read_jobs(jobs_path)
    if not pending:
        raise SystemExit(f"No jobs found at {jobs_path}")

    results: list[str] = []
    for iteration in range(1, args.max_iterations + 1):
        print(f"poll {iteration}: {len(pending)} pending")
        next_pending: list[tuple[str, str]] = []
        for shot_id, job_id in pending:
            data = run_json(["krea", "jobs", "show", job_id, "--json"])
            status = data.get("status", "unknown")
            url = result_url(data)
            if status == "completed":
                if args.download and url:
                    out = raw_dir / f"shot-{shot_id}-raw.mp4"
                    if not out.exists():
                        download(url, out)
                results.append(f"{shot_id}\tcompleted\t{url}")
                print(f"  {shot_id} completed")
            elif status in {"failed", "cancelled"}:
                results.append(f"{shot_id}\t{status}\t")
                print(f"  {shot_id} {status}")
            else:
                next_pending.append((shot_id, job_id))
        results_path.write_text("\n".join(results) + ("\n" if results else ""), encoding="utf-8")
        pending = next_pending
        if not pending or args.once:
            break
        time.sleep(args.interval)

    if pending:
        with results_path.open("a", encoding="utf-8") as handle:
            for shot_id, job_id in pending:
                handle.write(f"{shot_id}\tpending\t{job_id}\n")
    print(f"Wrote {results_path}")


if __name__ == "__main__":
    main()
