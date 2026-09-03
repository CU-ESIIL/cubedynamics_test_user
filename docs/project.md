# Project notes

## Purpose and current state

This repository is the tester's workspace for CubeDynamics. It contains project documentation, agent policy, prompt history, and a saved acceptance-run brief. It does not contain the CubeDynamics implementation.

The 2026-09-03 `0.1.0rc3` run installed the exact public PyPI release in a clean source-free container, froze Phase A before systematic work, attempted 11 scientific questions, and separately froze the rc3-only verdict before reading the previous report. Nine questions were answered, two were partial, and none remained wholly failed after explicit follow-ups. Clean CubeDynamics import, real PRISM/gridMET access, plotting, events, and Boolean NetCDF export worked; four major runtime and scientific-metadata findings keep the verdict at **FIX BEFORE HUMAN OUTSIDE TEST**. Evidence lives under `artifacts/2026-09-03-rc3/` and the [final report is in the repository](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/reports/2026-09-03-rc3/naive_user_report.md).

The 2026-08-28 setup/pre-release evidence and separate 2026-08-31 `0.1.0rc1` run remain preserved. rc1 installed but required specialist recovery before import and completed only one original scientific question. It is used only in the rc3 report's post-freeze comparison.

## Repository and website

The root `AGENTS.md` defines operating rules. `PROMPT_LOG.md` records requests, actions, validation, and decisions. Long task briefs live in `prompts/`. Website content lives in `docs/`, with identity and navigation in `mkdocs.yml`.

`requirements.txt` installs website dependencies only. Acceptance scripts live in `acceptance/`, raw run-specific evidence and small products in `artifacts/`, and narratives/verdicts in `reports/`. Keep all three separate from the external CubeDynamics package.

For local preview, from the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Open [the local preview](http://127.0.0.1:8000/). The strict website check is:

```sh
mkdocs build --strict --clean --site-dir dist
```

Generated website output and `.venv/` are ignored by Git. A website build is not a CubeDynamics acceptance test.

## Publishing

The existing `.github/workflows/pages.yml` builds and deploys the site on pushes to `main` or manual dispatch. GitHub Pages must be enabled with **Settings → Pages → Source: GitHub Actions**. The configured address is [cu-esiil.github.io/cubedynamics_test_user](https://cu-esiil.github.io/cubedynamics_test_user/).

Local documentation edits do not publish anything. This setup task does not verify the remote Pages setting or claim a live deployment.

## Template history and retained workflows

This project began as the `basic_OASIS` research website template. Its MkDocs Material structure, ESIIL branding assets, and general repository policies are retained. The old `examples/` page route now holds the testing workflow, so the existing route remains usable. The site logo now returns to this project's home page.

Two inherited workflows remain manual and are **not acceptance-test infrastructure**:

- `.github/workflows/fetch-template.yml` merges the original template. Do not dispatch it for naive-user testing; future template updates need review to avoid overwriting project policy or content.
- `.github/workflows/build-and-push-jupyterlab-image.yml` targets `containers/jupyterlab/Dockerfile`, which does not currently exist. It also requires Docker Hub credentials. Do not treat it as a working test environment or dispatch it for this purpose.

## Decisions — 2026-08-28

- Make the naive-user boundary explicit, including installed source and source-revealing introspection.
- Track every agent task in one root prompt log rather than introducing separate overlapping history files.
- Preserve exploratory evidence before systematic testing; require separate authorization before implementation-based triage.
- Keep MkDocs and GitHub Pages; replace template copy and project URLs without migrating the site or changing deployment workflows.
- Keep raw theme templates out of public build output and repair inherited card indentation so the homepage reads correctly.
- Preserve the supplied long acceptance protocol for a later run, with no fabricated results or placeholder acceptance verdict.

See [the prompt log](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/PROMPT_LOG.md) for the actual work and validation behind these decisions.
