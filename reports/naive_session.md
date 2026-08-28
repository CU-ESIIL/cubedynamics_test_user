# Naive environmental-scientist session

**Date:** 2026-08-28. **Parent task:** TASK-002. **Role:** fresh-context exploratory tester. **Status:** blocked at package installation; ready for evidence freeze.

## What I tried to do

I approached CubeDynamics as an environmental scientist interested in a small Boulder-area temperature analysis. I began with its public README, followed the website's Learn and Library links, and attempted the advertised package installation. I did not read the acceptance coordinator's detailed protocol, an API checklist, earlier findings, or other agents' evidence. Local `AGENTS.md` and `PROMPT_LOG.md` were read as required.

The public description made the basic idea understandable: obtain environmental observations, compose operations with a pipe, and inspect the result. I wanted to request a few days of PRISM maximum temperature, calculate its temporal mean, and then try the quickstart's anomaly and spatial mean. These were intended analyses, **not executed operations**.

## Chronological experience

| Operations | Attempt and observation |
|---|---|
| A-001–A-002 | Read local rules, then the [public README](https://github.com/CU-ESIIL/cubedynamics). It advertises `python -m pip install cubedynamics`. Its first offline example instead needs a file under the upstream tests directory, unavailable within this experiment's boundary. |
| A-003–A-005 | Opened [Home](https://cu-esiil.github.io/cubedynamics/), [Learn](https://cu-esiil.github.io/cubedynamics/learn/), and [Library](https://cu-esiil.github.io/cubedynamics/library/). Learn also requires a clone, editable installation, and test fixture. I chose the live-data route in principle. Web lookup of release metadata failed; direct PyPI metadata retrieval reached HTTP 404 after an initial sandbox DNS denial. |
| A-006 | Read only normal [GitHub release metadata](https://api.github.com/repos/CU-ESIIL/cubedynamics/releases). The two prereleases, `0.0.1` / `alpha` and `build` / `1.1.0`, had no attached assets. These labels do not establish an installed version. |
| A-007–A-008 | Attempted the documented pip installation in clean Linux, adding the required wheel-only restriction. The sandbox first denied the Docker socket. The approved retry failed: no matching CubeDynamics distribution. |
| A-009–A-010 | Followed installation help. The web tool returned a stale quickstart, so I fetched current published HTML directly. Current [Quickstart](https://cu-esiil.github.io/cubedynamics/quickstart/) still recommends PyPI. Current [Installation](https://cu-esiil.github.io/cubedynamics/getting_started/install/) explains that PyPI is not released yet and recommends installing from GitHub main. That recovery is outside the permitted black-box boundary. |
| A-011 | Stopped without a package. No scientific runs were manufactured to fill the evidence gap. |

## Actual installation attempt

```sh
docker exec cubedynamics-naive-20260828 python -m pip install --only-binary=cubedynamics cubedynamics
```

Approved retry output:

```text
ERROR: Could not find a version that satisfies the requirement cubedynamics (from versions: none)
ERROR: No matching distribution found for cubedynamics
```

The retry exited 1 after approximately 1.05 seconds. The full output, including pip's unrelated update notice, is preserved in `artifacts/2026-08-28-black-box/phase_a/install_approved_retry.json`.

**Environment supplied by coordinator:** isolated Linux container `cubedynamics-naive-20260828`, Python 3.11 base image `python:3.11-slim@sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6`, working directory `/work`, no mounts. The coordinator owns the full environment record. **Package artifact, installed version, and installed import path:** all null; installation did not succeed.

## What is and is not supported by this evidence

The observable user problem is an unavailable advertised packaged-install path. The installation page explains the situation, but the README/quickstart send a new user into a failed pip install, and the offline learning path requires a source checkout. This is an installation and documentation usability blocker, not evidence that cube mathematics or data loaders are defective.

No CubeDynamics import, public introspection, data download, cube creation, transformation, statistical analysis, export, visualization, or scientific check ran. No remote environmental observations were ingested. Consequently there are no scientific outputs, and no runtime capability verdict is supported. The source-install alternative was not attempted; no package source, tests, fixtures, implementation, developer documentation, archives, or wheel contents were inspected.

No private implementation knowledge was encountered. Root filenames and developer links visible on the permitted README/landing page were not followed. The stale quickstart returned by the web tool is recorded as a retrieval limitation; the current page was checked before drawing conclusions.

## Evidence

- Chronological record: `artifacts/2026-08-28-black-box/phase_a/naive_session.jsonl` (A-001–A-011). Early timestamps are explicitly approximate; direct-fetch completion uses a measured UTC timestamp.
- Installation output: `install_attempt.json` and `install_approved_retry.json` under the same directory.
- Public README, installation and quickstart snapshots, HTTP headers, release metadata, and web retrieval results: `phase_a/public_docs/`.
- Snapshot sizes and SHA-256 hashes: `phase_a/public_doc_snapshot_manifest.json`.

**Outcome:** exploratory discovery and installation recovery were attempted; scientific exploration was blocked before execution. An externally built wheel or published distribution is needed to continue under the existing boundary. This report does not authorize source inspection or maintainer triage.
