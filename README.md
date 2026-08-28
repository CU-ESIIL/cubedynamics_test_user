# CubeDynamics naive-user testing

`CU-ESIIL/cubedynamics_test_user` is an independent acceptance-testing workspace for **CubeDynamics as an external installed package**. It asks what happens when a competent environmental scientist who has never developed CubeDynamics tries to discover, install, understand, and use it.

This repository holds the tester's instructions, work, and evidence. It does not contain or develop CubeDynamics itself.

## Start here

1. Read [AGENTS.md](AGENTS.md) for the test boundary and operating rules.
2. Read [PROMPT_LOG.md](PROMPT_LOG.md), then add an entry for your task before substantive work.
3. Follow the [testing workflow](docs/examples.md) and [evidence policy](docs/evidence.md).
4. Record what you actually tried, including confusion, failures, and recovery attempts.

## The naive-user boundary

Use only CubeDynamics' public documentation, public README, normal installed-package introspection, and observed behavior. Do not inspect, clone, mount, or read `CU-ESIIL/cubedynamics` source, tests, agent instructions, prompt logs, fixtures, or developer files. Do not inspect installed implementation files, install editable, or patch the package to make a test pass.

If a user cannot proceed without implementation knowledge, that is a finding to record. The full policy in [AGENTS.md](AGENTS.md) applies to both testing phases and all tools or delegated agents.

## Two distinct testing phases

- **A — Naive exploratory user:** discover the package through public material and pursue scientific questions without a preloaded API checklist. Preserve and freeze the chronological experience.
- **B — Systematic public-surface coverage:** inventory the documented API, build a coverage matrix, and exercise valid usage, composition, extensions, and plausible mistakes. Keep the same source boundary.

Freeze the black-box report before any separately authorized maintainer triage. Do not fix CubeDynamics or submit upstream issues as part of naive testing.

## Current state

The repository has been adapted from a research website template. Agent policy, prompt logging, and the testing protocol are documented. **No CubeDynamics artifact has been installed or tested in this setup task; no acceptance verdict or coverage results exist yet.**

The [supplied acceptance-run protocol](prompts/2026-08-28-acceptance-protocol.txt) is preserved as a future-run brief, not an executed test. A clean Linux environment, a selected external release artifact, and a fresh exploratory tester context are still needed. There is no acceptance CLI, container definition, or automated package test suite yet.

## Repository map

| Path | Role |
| --- | --- |
| `AGENTS.md` | Agent rules and the naive-user boundary |
| `PROMPT_LOG.md` | Requests, attempted actions, actual outcomes, and decisions |
| `prompts/` | Saved long-form task briefs |
| `docs/` | Project documentation and website source |
| `mkdocs.yml` | Website identity, navigation, and build configuration |
| `requirements.txt` | Website dependencies, not a CubeDynamics test environment |
| `.github/workflows/` | Website deployment and inherited manual template workflows |

Future `acceptance/`, `artifacts/`, and `reports/` directories should be created when they contain real harness code or evidence. See the [project notes](docs/project.md) for workflow limitations and template history.

## Website

The website is a rendered view of this repository, built with MkDocs Material. Its configured GitHub Pages address is [cu-esiil.github.io/cubedynamics_test_user](https://cu-esiil.github.io/cubedynamics_test_user/).

To preview locally:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Open [the local preview](http://127.0.0.1:8000/). To run the same strict build used by the Pages workflow:

```sh
mkdocs build --strict --clean --site-dir dist
```

The existing workflow deploys on pushes to `main` or a manual dispatch, provided GitHub Pages is enabled with **Settings → Pages → Source: GitHub Actions**. Local edits alone do not publish the site.
