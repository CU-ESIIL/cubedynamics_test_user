"""Create or verify a SHA-256 manifest for evidence and selected reports."""

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--scope", type=Path)
    parser.add_argument("--include", type=Path, action="append", default=[])
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    manifest_path = args.manifest.resolve()
    manifest_path.relative_to(root)
    if args.verify:
        manifest = json.loads(manifest_path.read_text())
        scope = root / manifest["scope"]
        files = {path.relative_to(root).as_posix() for path in scope.rglob("*")
                 if path.is_file() and path.resolve() != manifest_path}
        files.update(manifest["included_reports"])
        expected = manifest["sha256"]
        problems = sorted(files.symmetric_difference(expected))
        problems.extend(name for name, sha in expected.items()
                        if not (root / name).is_file() or digest(root / name) != sha)
        if problems:
            raise SystemExit("Freeze verification failed: " + ", ".join(problems))
        print(f"Verified {len(expected)} frozen files: {args.manifest}")
        return
    if not args.scope or not args.scope.is_dir():
        parser.error("--scope must be an existing directory")
    scope = args.scope.resolve()
    scope.relative_to(root)
    files = {path.resolve() for path in scope.rglob("*")
             if path.is_file() and path.resolve() != manifest_path}
    files.update(path.resolve() for path in args.include)
    manifest = {
        "frozen_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "method": "SHA-256 manifest; content is tamper-evident, not filesystem write-protected",
        "scope": scope.relative_to(root).as_posix(),
        "included_reports": [path.resolve().relative_to(root).as_posix() for path in args.include],
        "sha256": {path.relative_to(root).as_posix(): digest(path) for path in sorted(files)},
    }
    with manifest_path.open("x") as stream:
        json.dump(manifest, stream, indent=2)
        stream.write("\n")
    print(f"Froze {len(files)} files: {args.manifest}")


if __name__ == "__main__":
    main()
