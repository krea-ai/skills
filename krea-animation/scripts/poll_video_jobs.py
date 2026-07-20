#!/usr/bin/env python3
"""Prepare Krea job status checks and optionally download completed raw clips."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

from _common import project_root, result_url


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


def response_job_id(data: dict[str, object]) -> str:
    for key in ("jobId", "job_id", "id"):
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    job = data.get("job")
    if isinstance(job, dict):
        value = job.get("id")
        if isinstance(value, str) and value:
            return value
    return ""


def status_rows(
    pending: list[tuple[str, str]], results_jsonl: str | None, raw_dir: Path, should_download: bool
) -> list[str]:
    rows_by_shot: dict[str, str] = {}
    shot_by_job = {job_id: shot_id for shot_id, job_id in pending}
    if results_jsonl:
        responses = Path(results_jsonl).read_text(encoding="utf-8").splitlines()
        for line in responses:
            if not line.strip():
                continue
            data = json.loads(line)
            shot_id = str(data.get("shot_id") or data.get("shotId") or "").strip()
            response_job = response_job_id(data)
            if not shot_id:
                shot_id = shot_by_job.get(response_job, "")
            if not shot_id:
                continue
            status = str(data.get("status", "unknown")).lower()
            if status == "completed":
                url = result_url(data)
                if not url:
                    rows_by_shot[shot_id] = f"{shot_id}\tfailed\tcompleted without result URL"
                    continue
                if should_download:
                    out = raw_dir / f"shot-{shot_id}-raw.mp4"
                    if not out.exists():
                        download(url, out)
                rows_by_shot[shot_id] = f"{shot_id}\tcompleted\t{url}"
            elif status in {"failed", "cancelled", "canceled"}:
                rows_by_shot[shot_id] = f"{shot_id}\t{status}\t"
            else:
                job_id = response_job or next((job for item_shot, job in pending if item_shot == shot_id), "")
                rows_by_shot[shot_id] = f"{shot_id}\tpending\t{job_id}"

    rows: list[str] = []
    for shot_id, job_id in pending:
        rows.append(rows_by_shot.get(shot_id, f"{shot_id}\tpending\t{job_id}"))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory")
    parser.add_argument("--download", action="store_true", help="Download completed raw clips")
    parser.add_argument("--results-jsonl", help="Optional JSONL file of job responses to merge")
    args = parser.parse_args()

    root = project_root(args.project)
    jobs_path = root / "04_generation/jobs/jobs.tsv"
    results_path = root / "04_generation/jobs/results.tsv"
    checks_path = root / "04_generation/jobs/status-checks.jsonl"
    raw_dir = root / "05_edit/shots_raw"
    pending = read_jobs(jobs_path)
    if not pending:
        raise SystemExit(f"No jobs found at {jobs_path}")

    checks_path.write_text(
        "\n".join(
            json.dumps({"shot_id": shot_id, "tool": "get_job", "jobId": job_id}, sort_keys=True)
            for shot_id, job_id in pending
        )
        + "\n",
        encoding="utf-8",
    )

    results = status_rows(pending, args.results_jsonl, raw_dir, args.download)
    results_path.write_text("\n".join(results) + "\n", encoding="utf-8")
    print(f"Wrote status checks: {checks_path}")
    print(f"Wrote {results_path}")


if __name__ == "__main__":
    main()
