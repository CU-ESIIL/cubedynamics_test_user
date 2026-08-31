#!/usr/bin/env python3
"""Run one black-box acceptance-test operation and preserve raw evidence."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import time


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("op_id")
    parser.add_argument("--action", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--docs", default="")
    parser.add_argument("--confusion", default="")
    parser.add_argument("command")
    args = parser.parse_args()

    root = pathlib.Path("/work/session")
    raw_dir = root / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc)
    begin = time.monotonic()
    proc = subprocess.run(
        ["/bin/sh", "-lc", args.command],
        cwd="/work",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    elapsed = time.monotonic() - begin
    ended = dt.datetime.now(dt.timezone.utc)
    raw_path = raw_dir / f"{args.op_id}.txt"
    raw_path.write_text(proc.stdout, encoding="utf-8")
    record = {
        "operation_id": args.op_id,
        "phase": "Phase A naive-user exploration",
        "started_utc": started.isoformat(),
        "ended_utc": ended.isoformat(),
        "runtime_seconds": round(elapsed, 6),
        "action": args.action,
        "expected": args.expected,
        "command": args.command,
        "documentation_consulted": [item for item in args.docs.split("|") if item],
        "actual": proc.stdout,
        "exit_code": proc.returncode,
        "warnings_errors_tracebacks": proc.stdout if proc.returncode else "See actual output; non-fatal warnings retained verbatim.",
        "confusion": args.confusion,
        "recovery_or_learning": "To be interpreted in the chronological narrative and subsequent operation.",
        "raw_evidence": f"raw/{args.op_id}.txt",
    }
    with (root / "naive_session.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(proc.stdout, end="")
    print(f"\n[{args.op_id}] exit={proc.returncode} runtime={elapsed:.3f}s raw={raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
