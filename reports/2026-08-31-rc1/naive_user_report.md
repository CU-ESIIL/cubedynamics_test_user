# CubeDynamics 0.1.0rc1 outside-user acceptance report

## 1. Executive summary

The public release installed from PyPI, but did not import in the supplied clean `python:3.11-slim` Linux environment because `libexpat.so.1` was unavailable. A scientifically competent tester eventually recovered by downloading and unpacking Debian's runtime library locally and setting `LD_LIBRARY_PATH`; that is specialist environment work, not a credible first-use path. After recovery, one bounded real PRISM precipitation analysis, pipe reduction, semantic explanation, validation, trace inspection, xarray unwrapping, computation, and Matplotlib plot succeeded.

This run does not establish broad API reliability. The bounded naive session completed, but exhaustive systematic execution, ten original questions, randomized combinations, and a novice-error matrix were not completed. Those are recorded as zero rather than implied by documentation discovery.

## 2. Environment and artifact tested

- Artifact: public PyPI `cubedynamics==0.1.0rc1`
- OS: Debian GNU/Linux 13.6 (trixie), aarch64, clean container with no mounts or `PYTHONPATH`
- Python: 3.11.16; pip: 24.0
- Image: `python:3.11-slim@sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6`
- Installed version: `0.1.0rc1`
- Observed origin: `/usr/local/lib/python3.11/site-packages/cubedynamics/__init__.py` (recorded, not opened)

## 3. Installation experience

PyPI resolution and installation succeeded. The verbose log is at `artifacts/2026-08-31-rc1/phase_a/install_pip_verbose.log`. The first import failed with `ImportError: libexpat.so.1: cannot open shared object file`. `pip check` nevertheless reported no broken Python requirements. Normal `apt-get install libexpat1` recovery failed under the intentionally restricted container; local package unpacking plus `LD_LIBRARY_PATH` made import succeed. This is **BLOCKER** severity for a clean outside-user test.

## 4. First 30 minutes

The chronological session is frozen in `phase_a/naive_session.jsonl` and narrated in `reports/2026-08-31-rc1/naive_session.md`. The tester independently used PyPI, public docs, public names/signatures/docstrings, and observed behavior. It encountered installation/import friction, an older/newer API presentation mismatch, an unsupported default monthly PRISM request, a successful five-day daily PRISM retrieval, a failed NetCDF export caused by boolean attributes, then a successful real-data mean/semantic-inspection/plot workflow.

## 5–12. Product understanding, grammar, data and inspection

CubeDynamics appeared to be a noun-and-verb grammar over environmental xarray objects. Public catalog discovery and signatures were understandable after import. The successful expression retained five daily observations while averaging spatial dimensions. `explain()`, `validate()`, semantic state, trace, `unwrap()`, xarray computation, units, provider metadata, and a static plot were useful and mutually consistent. Source choice and API generation were harder to reconcile across dated public pages.

## 13. Scientific-question experiments

One original practical question was completed: *What was mean daily precipitation over a small Boulder-area PRISM grid for 1–5 January 2024?* It passed after environment and request-frequency recovery. Result values and semantic evidence are in `raw/A31-017.txt`; plot: `phase_a/prism_boulder_mean_daily_ppt.png`. Nine additional original questions were not attempted.

## 14–17. Randomization, errors, documentation, trust

Randomized cases: **0**. Deliberate novice-error suite: **0**. Naturally occurring errors were highly informative: missing system library, unsupported monthly PRISM behavior, and NetCDF serialization failure. Once the final daily workflow succeeded, units, dimensions, time ordering, provider and trace supported scientific trust. Exhaustive noun/source/verb coverage and cross-source trust were not established.

## 18. Major failures

1. **BLOCKER — clean import fails.** Reproduce with `python -m pip install cubedynamics==0.1.0rc1` then `python -c 'import cubedynamics'` in the recorded image. Expected: import. Observed: missing `libexpat.so.1`. Evidence: A31-003–A31-011.
2. **MAJOR — first PRISM path is not copy-and-run.** The initially discovered monthly/default request failed; a daily retry worked. Evidence: A31-012–A31-014.
3. **MAJOR — ordinary NetCDF export fails.** The retrieved public result could not serialize because boolean attributes were rejected. Evidence: A31-014.

## 19–22. Friction, surprises, use decision and priorities

The successful grammar/inspection experience was the positive surprise. Environment recovery dominated first use, and API/documentation age differences slowed discovery. Before another human outside test: make the PyPI artifact import in the clean supported environment; ensure the first public example uses supported request semantics; make ordinary returned xarray objects export cleanly; then rerun full noun/source/verb, ten-question, randomized and novice-error coverage.

## 23. Acceptance verdict

The release can perform a meaningful real environmental analysis after substantial specialist recovery, but clean first use is blocked and broad acceptance coverage remains unproven.

**FIX BEFORE HUMAN OUTSIDE TEST**
