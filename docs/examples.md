# Testing workflow

This is the coordinator's workflow for acceptance runs. Completed evidence and reports are run-specific; the current rc3 result is linked from [Project notes](project.md). The recorder and freeze utilities exist, while scientific run scripts remain release-specific rather than a universal test runner.

## 1. Establish the boundary and environment

Read this repository's [AGENTS.md](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/AGENTS.md) and [PROMPT_LOG.md](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/PROMPT_LOG.md). Add the task entry before substantive work.

Select a specified CubeDynamics release candidate, a supplied built wheel, or another legitimate external install artifact. Do not guess a release version or substitute a source checkout. If no suitable artifact is available, record the blocker and ask for one.

Use a clean Linux container beginning with Python, pip, and ordinary shell utilities. Neither a CubeDynamics source checkout nor repository-local fixtures may be copied or mounted into it. Do not install editable or patch the installed package.

Record the image and digest where available, OS, architecture, Python and pip versions, artifact identity, package version, exact install command, warnings/errors, and installed import path. Verify imports resolve to the installed environment rather than a checkout. Website dependencies in this repository are not a test-environment specification.

## 2. Phase A — Naive exploratory user

Start with a fresh tester context where possible. Give it this repository's boundary and logging rules, the external installation details, and only this scientific goal:

> You are an environmental scientist who has discovered CubeDynamics. Figure out what it does and try to use it for environmental analysis. Explore what you can do with it. Use its public documentation when you need help. Try increasingly ambitious analyses. Keep going when reasonable, and record everything that happens.

Do not preload the tester with a public API inventory, internal architecture, known limitations, expected answers, previous development history, or the later systematic checklist. Reading the full acceptance brief in a coordinating context is not an unprimed exploratory session.

Let the tester choose documentation, infer terminology, formulate scientific questions, and progress beyond the first working example. Record its starting point, expectations, exact attempts, results, confusion, errors, recovery, and dead ends in chronological order.

Normal public introspection includes `help()`, public docstrings and signatures, public names, distribution metadata, and import-path checks. Reading implementation files or using `inspect.getsource()` is outside the boundary, even for an installed package.

## 3. Freeze the exploratory experience

Preserve the raw chronological session and a human-readable account before moving on. Record a freeze identifier in the prompt log. Do not rewrite wrong guesses after learning the correct usage; later explanations are separate annotations.

See [evidence and prompt log](evidence.md) for planned artifact paths and required records.

## 4. Phase B — Systematic public-surface coverage

Only after Phase A is frozen, inventory the public functionality using public documentation, the README, and allowed package introspection. Record where each item was discovered. Build a coverage matrix before systematic execution, distinguishing documented support from experimental, unavailable, or undiscovered functionality.

Use the actual public vocabulary you discover. Exercise valid calls, meaningful compositions and operation order, visualization, provenance, lazy/eager behavior where documented, user-supplied inputs and extensions, and plausible novice mistakes. Prefer small, scientifically meaningful inputs over an indiscriminate Cartesian product.

Give each documented public operation a valid attempt where feasible. Record blocked and not-attempted items honestly. Assess whether errors are early, safe, clear, and actionable without source access. Keep source identity, units, dimensions, coordinates, and scientific interpretation visible in the evidence.

The broader [acceptance-run protocol](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/prompts/2026-08-28-acceptance-protocol.txt) defines the intended depth, including original scientific questions, custom inputs and operations, and reproducible exploratory combinations. No package API names or successful results are assumed here.

## 5. Report, freeze, and review

Report actual coverage, what worked, confusion, breakages, documentation gaps, scientific ambiguities, and limitations. Link every finding to reproducible evidence. If testing is incomplete, say so; do not manufacture a readiness verdict.

Freeze the final black-box report and evidence before maintainer triage. Source-based diagnosis requires separate explicit authorization after the freeze. Do not fix CubeDynamics, submit issues, or open pull requests during naive testing. Any proposed issue plan remains a draft for review.

## Current implementation boundary

`acceptance/capture.py` records commands and `acceptance/freeze.py` creates and verifies SHA-256 manifests. Release-specific scientific scripts may be retained for reproduction, but they do not replace chronological Phase A or establish a universal acceptance suite. The [current project state](project.md) lists completed runs.
