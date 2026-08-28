# Black-box command evidence

`capture.py` records one subprocess invocation and its exact stdout, stderr,
exit status, timestamp, goal, expectation and documentation references. It
requires only Python's standard library. It does not discover APIs, enforce
the source-access boundary, or constitute a complete acceptance runner.
Follow root `AGENTS.md`; the operator is responsible for selecting allowed
commands. Exit status alone is not an acceptance verdict.

Example for an already-created, isolated container, substituting a new run ID:

```sh
python3 acceptance/capture.py \
  --run-dir artifacts/RUN-ID/phase_b \
  --id B-001 --phase B \
  --goal 'Install the documented external package' \
  --expected 'A published wheel installs successfully' \
  --documentation https://github.com/CU-ESIIL/cubedynamics \
  -- docker exec CONTAINER python -m pip install --only-binary=cubedynamics cubedynamics
```

Use a specified published version (`cubedynamics==VERSION`) or a supplied wheel
when available. Never use a Git URL, editable install, source distribution,
checkout, or fixture. The wheel-only restriction prevents building CubeDynamics
from source; it is an intentional addition to the public installation command.

The recorder refuses existing operation IDs and any run directory beneath a
`FROZEN.json` marker. `--timeout` bounds the host subprocess; for Docker commands,
also use a container-side timeout when needed, because terminating a Docker
client may not terminate the process in the container.

For the first run, the coordinator started a standard Python 3.11 Linux image
with no mounts, dropped capabilities and a 2 GiB memory limit. Actual image
digest and runtime details are in `artifacts/2026-08-28-black-box/environment/`.
No upstream source repository is needed or allowed. Exploration must precede
systematic coverage, and each new run must use new evidence paths and a clean
tester context. Python version, release artifact, and exploration seed are run
inputs; there is not yet an automated end-to-end release acceptance CLI.

## Freeze and verify

After finishing a phase, create a SHA-256 manifest. It preserves a verifiable
snapshot, not filesystem write protection. Do not edit frozen files; put later
interpretations in separate reports or a new run.

```sh
python3 acceptance/freeze.py \
  --scope artifacts/RUN-ID/phase_a \
  --include reports/naive_session.md \
  --manifest artifacts/RUN-ID/phase_a/FROZEN.json
python3 acceptance/freeze.py \
  --manifest artifacts/RUN-ID/phase_a/FROZEN.json --verify
```

Freeze the entire evidence directory plus the final naive-user report before
writing a proposed issue list. For later runs, give reports a run-specific
directory too, so old manifests continue to verify.
