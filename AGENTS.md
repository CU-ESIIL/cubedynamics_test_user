# AGENTS.md

## Repository Purpose
- `cubedynamics_test_user` is an independent naive-user acceptance-testing environment for CubeDynamics, not a development copy of the package.
- Act as a scientifically competent new user: discover capabilities through public material, attempt environmental analyses, and preserve confusion, failures, and recovery attempts as evidence.
- The default phase is naive-user testing. Establishing policies or documentation does not constitute a completed acceptance run.

## Naive-User Boundary
`cubedynamics_test_user` may inspect and modify this repository, but during the naive-user phase it must not inspect, clone, mount, or read the source code, tests, AGENTS.md, or developer files from `CU-ESIIL/cubedynamics`. CubeDynamics must be treated as an external installed package and understood only through its public documentation, README, package introspection, and observed behavior.

- This boundary applies to both exploratory testing and systematic public-surface coverage, including any delegated agents, containers, tools, and external searches.
- Allowed: this repository; an installed release or supplied built wheel; the public CubeDynamics website, README, and normal repository landing information; ordinary scientific Python tools; and public data services with appropriate rights.
- Allowed introspection is limited to public names, `help()`, public docstrings, `dir()`, `inspect.signature()`, installed distribution metadata, and checking the import path. Do not use these to explore private implementation details.
- Forbidden: reading package implementation files (including installed files or wheel contents), `inspect.getsource()` or equivalent source/disassembly inspection, upstream tests, fixtures, `AGENTS.md`, `PROMPT_LOG.md`, developer-only documentation, local checkouts, editable installs, or source searches to diagnose errors. Do not patch the installed package or modify CubeDynamics.
- Record tracebacks as observed evidence, but do not follow their paths into package source. If public material is insufficient, record a documentation gap or blocker rather than crossing the boundary.
- Do not import prior development knowledge, internal test answers, or known-good private examples into the naive-user experiment. If such information is encountered accidentally, stop that exploration, record the exposure, and use a fresh tester context before claiming unprimed discovery.
- Run exploratory discovery before building the systematic inventory. Freeze the chronological exploratory evidence before systematic testing; freeze the complete black-box report before any maintainer triage. Add corrections separately rather than rewriting the original experience.
- Maintainer triage is a separate phase requiring explicit user authorization to change this boundary after evidence is frozen. An attached future-run protocol does not itself authorize source inspection. Do not submit upstream issues, create pull requests, or fix CubeDynamics without separate authorization.

## Prompt and Action Log
- Maintain the root `PROMPT_LOG.md` for every agent task, including documentation-only work and unsuccessful attempts. Read it after this file before starting work.
- Add a dated entry with a stable ID before substantive changes. Record the agent/role, phase, the user's request (verbatim when short, otherwise a faithful summary and a repository-relative reference to a saved prompt), constraints, and intended work.
- Update that entry with what was actually attempted and changed, decisions and reasons, commands/checks and their outcomes, failures, limitations, evidence/output paths, and final status. Distinguish planned, attempted, completed, blocked, and not-run work.
- For acceptance runs, also record the package artifact/version, environment, evidence paths, and verdict, or explicitly state that no verdict is supported. Reference large transcripts and raw evidence instead of embedding them in this log.
- Keep entries chronological. Complete the current entry as work proceeds; preserve closed entries and append later corrections. Never rewrite failures as successes or invent missing history.
- Exclude credentials, tokens, private data, and restricted content from prompts and logs; mark necessary redactions. Log delegated tasks and their actual outcomes under the parent task ID.

## Core Operating Contract
- Treat this repository as the source of truth.
- Treat the website as a rendered view of repository state.
- Prefer small, additive, traceable edits.
- Keep documentation synchronized with code and project structure.
- Keep the repository minimalist by default.

## Default Workflow
- Inspect repository structure before editing.
- Make the smallest diff that solves the request.
- Update related docs when behavior, workflows, or outputs change.
- Update changelog, dev log, or equivalent history files for meaningful changes.
- Preserve existing structure and historical context.
- Do not perform destructive rewrites unless explicitly requested.

## Documentation and Website Policy
- Treat `docs/` as project-level documentation and website source.
- Update docs whenever code, workflows, or outputs change.
- Amend existing docs when possible; do not replace whole files without need.
- Preserve navigation, readability, and consistency in website changes.
- Keep default website behavior clean and minimal unless the user asks for more expressive design.

## Testing Policy
- Assume `tests/` may exist before a full testing framework is defined.
- Do not invent domain-specific tests when expected behavior is unclear.
- Add the smallest meaningful tests when behavior is known.
- Prefer early-stage checks such as smoke tests, import tests, CLI tests, schema checks, or example-based checks.
- If tests are deferred, document the gap; do not imply coverage that does not exist.

## Package and Structure Separation Policy
- Keep website structure and package structure clearly separated.
- Do not automatically repurpose `docs/` for package-native docs or build artifacts.
- For Python packaging requests, prefer standard Python layout, typically `src/`.
- For R packaging requests, follow standard R conventions (`R/`, `man/`, `DESCRIPTION`, `NAMESPACE`, optional `vignettes/`).
- For other ecosystems, follow ecosystem conventions.
- If structural conflicts arise, choose a durable long-term structure and document the decision.

## Data Discovery and Data Use Policy
- Prefer open and FAIR data when possible.
- Prefer streaming or lazy-access workflows over bulk downloads when feasible.
- Use standards-based discovery systems (for example STAC) when relevant.
- When relevant, consider streaming-friendly tooling such as xarray, zarr, GDAL, rasterio, pystac-client, stackstac, gdalcubes, terra, stars, cubo, or equivalent tools.
- When introducing data, document source, access method, format, license, and citation requirements.
- Do not silently ingest external data into the project.

## Data Sovereignty and Intellectual Property Policy
- Consider licensing, copyright, privacy, Indigenous data sovereignty, and related restrictions for all data and content.
- If rights or permissions are unclear, document uncertainty and avoid assuming open reuse.

## Design and Usability Policy
- Keep the website simple, readable, and easy to extend by default.
- When design improvements are requested, prioritize system-level improvements (layout, spacing, typography, hierarchy, navigation, consistency).
- Do not use scattered one-off styling hacks.
- If direct site inspection is possible, verify readability, navigation, link integrity, and that docs still reflect repository state.

## Decision Logging
- Reflect meaningful structural, architectural, documentation, data-source, or design decisions in changelog, dev log, roadmap, or equivalent history files when appropriate.
