# Evidence and prompt log

Record the experience as it happened. A wrong guess, confusing term, failed retrieval, or unsuccessful recovery can reveal more about usability than a clean example.

## Log every agent task

[PROMPT_LOG.md](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/PROMPT_LOG.md) is the canonical request-and-action history, including documentation work. [AGENTS.md](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/AGENTS.md) defines the policy.

Before substantive work, add a dated entry with a stable task ID, agent/role, phase, user request, constraints, and intended actions. During the task, update it with actual attempts, changes, decisions, validation, failures, limitations, and output paths. Close it with an honest status; append later corrections rather than rewriting closed entries.

For acceptance runs, also identify the package artifact/version, environment, evidence, and supported verdict. Keep long prompts and raw transcripts in separate files referenced by the log. Never include secrets or restricted data.

### Entry outline

```markdown
## YYYY-MM-DD — TASK-NNN — Short task title

- Agent / role:
- Phase:
- Request / saved prompt:
- Constraints:
- Intended work:
- Actual attempts and changes:
- Decisions and reasons:
- Checks and outcomes:
- Failures, limitations, and work not run:
- Evidence / output paths:
- Package artifact and environment (if tested):
- Status / verdict (if supported):
```

## Acceptance evidence

Assign an operation ID to each meaningful attempt. Separate what the tester expected from what actually happened and what they tried next. Record timestamps, documentation URLs and access dates, exact code and parameters, warnings, tracebacks, result types and dimensions, runtime, and recovery attempts. For systematic testing, also record the public API items and sources exercised, classification, and severity.

Use explicit states such as **not attempted**, **succeeded**, **failed**, or **blocked**. Missing credentials, unavailable data, and documentation gaps must remain visible; none counts as a successful test. Synthetic or local data must never stand in for a claimed successful live retrieval.

The following paths are conventions. Completed runs use dated, release-specific subdirectories so evidence is never overwritten; the rc3 run is under `artifacts/2026-09-03-rc3/` and `reports/2026-09-03-rc3/`.

| Planned path | Contents |
| --- | --- |
| `artifacts/environment.json` | Image/digest, OS, architecture, Python/pip/package versions, install command and import path |
| `artifacts/naive_session.jsonl` | Complete chronological exploratory attempts and outcomes |
| `reports/naive_session.md` | Human-readable account of that first experience |
| `artifacts/public_surface.json` | Public items discovered and where each was documented |
| `artifacts/coverage_matrix.csv` | Planned and actual systematic coverage, linked to operation IDs |
| `artifacts/operations.jsonl` | Systematic operation evidence and reproductions |
| `reports/naive_user_report.md` | Evidence-based findings, actual coverage, and readiness verdict |
| `reports/proposed_issues.md` | Deduplicated issue drafts for review; not submitted issues |

The [saved acceptance protocol](https://github.com/CU-ESIIL/cubedynamics_test_user/blob/main/prompts/2026-08-28-acceptance-protocol.txt) specifies the full future experiment. Its inventory and coverage instructions belong to the coordinator and Phase B; do not preload them into a fresh Phase A tester context.

## Freeze before learning more

Freeze Phase A before systematic coverage. Freeze the final black-box evidence and report before any separately authorized maintainer triage. Record the freeze time and an immutable identifier, such as a commit or checksums, in the prompt log. Preserve original files and add later interpretations separately.

Do not clean up misunderstandings after discovering the explanation. Do not declare release readiness from a partial run or from this documentation setup.

## Data and publication

Record external data source, access method, format, license, citation requirements, and relevant restrictions. Prefer small, lazy or streamed requests. Do not silently ingest data, assume open reuse, or publish credentials, private data, restricted content, or Indigenous data without appropriate authority. Mark redactions while retaining a safe reproduction where possible.
