"""Capture one black-box command without overwriting an existing operation.

This is an evidence recorder, not an automatic API inventory or full test suite.
The operator must keep commands inside the repository's public-surface boundary.
"""

import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--phase", choices=["environment", "A", "B"], required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--documentation", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command is required after --")
    if args.id != Path(args.id).name or args.id in {".", ".."}:
        parser.error("id must be a filename, not a path")
    if args.timeout <= 0:
        parser.error("timeout must be positive")
    if any((parent / "FROZEN.json").exists()
           for parent in (args.run_dir, *args.run_dir.parents)):
        parser.error("this run directory is frozen; use a new run directory")
    args.run_dir.mkdir(parents=True, exist_ok=True)
    output = args.run_dir / f"{args.id}.json"
    # Exclusive creation protects previous attempts even if this process fails.
    with output.open("x") as stream:
        start = time.monotonic()
        record = {
            "id": args.id,
            "phase": args.phase,
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "goal": args.goal,
            "documentation_consulted": args.documentation,
            "command": command,
            "expected_behavior": args.expected,
        }
        try:
            result = subprocess.run(command, capture_output=True, text=True,
                                    timeout=args.timeout, check=False)
            record.update(returncode=result.returncode, stdout=result.stdout,
                          stderr=result.stderr, status="succeeded" if result.returncode == 0 else "failed")
        except subprocess.TimeoutExpired as exc:
            def as_text(value):
                return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
            record.update(returncode=None, stdout=as_text(exc.stdout), stderr=as_text(exc.stderr),
                          status="timed_out", error=str(exc))
        except OSError as exc:
            record.update(returncode=None, stdout="", stderr="", status="failed", error=str(exc))
        record["runtime_seconds"] = round(time.monotonic() - start, 6)
        record["interpretation"] = "Exit status only; scientific/acceptance interpretation belongs in the report."
        json.dump(record, stream, indent=2)
        stream.write("\n")
    print(json.dumps(record, indent=2))
    return 0 if record["status"] == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
