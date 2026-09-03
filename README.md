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

CubeDynamics `0.1.0rc3` completed a strict public-PyPI black-box run on 2026-09-03. The package itself imported without recovery, real PRISM and gridMET access worked, and 11 scientific questions yielded 9 complete and 2 partial answers. Boolean NetCDF export and the requested plotting/event/order/temporal-support workflows ran. Four major runtime and scientific-metadata issues keep the verdict at **FIX BEFORE HUMAN OUTSIDE TEST**. See the [final rc3 report](reports/2026-09-03-rc3/naive_user_report.md), [pre-comparison detailed assessment](reports/2026-09-03-rc3/rc3_assessment_before_comparison.md), and [frozen Phase A narrative](reports/2026-09-03-rc3/naive_session.md).

The earlier 2026-08-31 rc1 and 2026-08-28 pre-release evidence remain preserved. The rc3 assessment was frozen before its explicit rc1 comparison, so earlier findings did not rewrite the new run.

## Repository map

| Path | Role |
| --- | --- |
| `AGENTS.md` | Agent rules and the naive-user boundary |
| `PROMPT_LOG.md` | Requests, attempted actions, actual outcomes, and decisions |
| `prompts/` | Saved long-form task briefs |
| `docs/` | Project documentation and website source |
| `mkdocs.yml` | Website identity, navigation, and build configuration |
| `requirements.txt` | Website dependencies, not a CubeDynamics test environment |
| `acceptance/` | Source-boundary-safe evidence recorder, freeze tool, and run scripts |
| `artifacts/` | Run-specific raw evidence, small outputs, metrics, and freeze manifests |
| `reports/` | Run-specific narratives and verdicts |
| `.github/workflows/` | Website deployment and inherited manual template workflows |

See the [project notes](docs/project.md) for workflow limitations and template history.

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
