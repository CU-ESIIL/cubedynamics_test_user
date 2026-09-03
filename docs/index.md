# CubeDynamics, from a new user's perspective

Can a scientist discover, understand, and use CubeDynamics using only what an ordinary package user can see?

`cubedynamics_test_user` is an independent workspace for answering that question. We treat CubeDynamics as an external installed package and record the experience of trying environmental analyses through its public documentation and user-facing functions.

[Testing workflow](examples.md){ .md-button .md-button--primary }
[Evidence and prompt log](evidence.md){ .md-button }

!!! warning "Public surface only"
    During naive-user testing, do not inspect, clone, or mount the CubeDynamics source repository, or read its tests, agent instructions, developer files, or installed implementation. Use public documentation, the README, ordinary public-package introspection, and observed behavior. If those are insufficient, record a finding.

<div class="grid cards" markdown>

- **Discover**

    ---

    Begin as a new user. Follow public documentation, form scientific questions, and preserve the first attempts without a preloaded API checklist.

- **Exercise**

    ---

    After freezing the exploratory session, inventory the public surface and test documented usage, composition, extensions, and plausible mistakes.

- **Record**

    ---

    Keep requests, decisions, exact attempts, results, errors, and recovery steps traceable. Confusion and unsuccessful attempts are evidence too.

</div>

## Current status

**CubeDynamics 0.1.0rc3 black-box test completed.** The exact PyPI release imported without recovery, real PRISM and gridMET data worked, and 11 scientific questions produced 9 complete and 2 partial answers. Plotting, Boolean NetCDF export, operation order, local/regional events, and temporal-support checks ran. Four major runtime and scientific-metadata issues remain. Primary verdict: **FIX BEFORE HUMAN OUTSIDE TEST**.

Read the [final rc3 report](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/reports/2026-09-03-rc3/naive_user_report.md). The frozen rc1 and 2026-08-28 runs remain historical evidence; the [project notes](project.md) distinguish all three.

## Where the rules and history live

The repository is the source of truth; this website is its rendered documentation.

- [AGENTS.md — operating rules and the naive-user boundary](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/AGENTS.md)
- [PROMPT_LOG.md — what agents were asked to do and what they actually did](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/PROMPT_LOG.md)
- [Repository](https://github.com/CU-ESIIL/cubedynamics_test_user)
