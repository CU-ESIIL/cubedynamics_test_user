# Project notes

## Purpose and current state

This repository is the tester's workspace for CubeDynamics. It contains project documentation, agent policy, prompt history, and a saved acceptance-run brief. It does not contain the CubeDynamics implementation.

As of the 2026-08-28 setup task, no CubeDynamics release artifact has been installed or tested here. There is no acceptance runner, Linux test container definition, package test suite, or generated acceptance evidence. Those are future work, not implied capabilities of this website.

## Repository and website

The root `AGENTS.md` defines operating rules. `PROMPT_LOG.md` records requests, actions, validation, and decisions. Long task briefs live in `prompts/`. Website content lives in `docs/`, with identity and navigation in `mkdocs.yml`.

`requirements.txt` installs website dependencies only. Keep future acceptance code and environments separate from the website, and keep both separate from the external CubeDynamics package. Create `acceptance/`, `artifacts/`, and `reports/` only when there is actual code or evidence to put there.

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
