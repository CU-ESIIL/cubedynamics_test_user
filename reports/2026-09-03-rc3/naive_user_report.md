# CubeDynamics 0.1.0rc3 Outside-User Acceptance Report

## Executive verdict

**FIX BEFORE HUMAN OUTSIDE TEST**

The exact PyPI release installed and substantially worked: CubeDynamics import,
the most obvious real PRISM request, gridMET VPD, nine complete and two partial
scientific answers, order-sensitive semantics, local and regional events,
temporal-support safeguards, plotting, and Boolean NetCDF export all ran through
public interfaces.

Four major issues remain: rasterio is unusable after the clean pip install;
condition/compound units conflict; reduced xarray/export attrs retain removed
temporal meaning; and strict temporal comparison falsely rejects equivalent
PRISM temperature/precipitation intervals. The central inspectability claim is
strong for a live single-source Pipe but incomplete for unwrapped, multi-input,
relationship, and exported results.

## Complete rc3 assessment

The detailed rc3-only assessment was written and frozen before any rc1 report
was opened, preserving the required comparison boundary:

- [Detailed environment, installation, Phase A, eleven Phase B questions,
  regressions, inspectability, documentation, bugs, fixes, and verdict](rc3_assessment_before_comparison.md)
- [Chronological frozen Phase A narrative](naive_session.md)
- [Phase A freeze manifest](../../artifacts/2026-09-03-rc3/phase_a/FROZEN.json)
- [Environment freeze manifest](../../artifacts/2026-09-03-rc3/environment/FROZEN.json)
- [Phase B and pre-comparison assessment freeze manifest](../../artifacts/2026-09-03-rc3/phase_b/FROZEN.json)

That detailed report is incorporated into this final assessment by reference;
it is not rewritten after comparison.

## Outcome summary

| Measure | Result |
| --- | ---: |
| Installed version | 0.1.0rc3 |
| Scientific questions attempted | 11 |
| Successfully answered | 9 |
| Partially answered | 2 |
| Unresolved failed questions | 0 |
| Blockers | 0 |
| Major issues | 4 |
| Moderate issues | 3 |
| Minor issues | 1 |

The two partial questions were compound hot/dry overlap and multi-variable
comparison. Initial strict hot/dry and dependent lag attempts failed and remain
in the raw record; an explicit label-policy follow-up produced a scientifically
caveated compound result, while an independent follow-up completed the lagged
association. Multi-variable names and per-variable units survived, but the Pipe
lost source, CRS, units, and provenance at Dataset level.

## RC3 regression results

| Area | Result | Severity |
| --- | --- | --- |
| Installation/import | CubeDynamics imports, but rasterio warns and fails for missing `libexpat.so.1` | Major |
| First-use PRISM | Exact prominent 21-year daily request succeeded with real data | Pass |
| NetCDF/export | Mean and Boolean exports reopen; Boolean is flagged int8; conflicting/stale attrs and no trace remain | Major |
| Operation order | Both orders run and clearly distinguish prevalence from thresholding an aggregate | Pass |
| Units | Mean, variance, and prevalence are sensible; Boolean/overlap units conflict | Major |
| Metadata/state | Live state is truthful; transformed/exported attrs and multi-input context are not consistently truthful | Major |
| Plotting | Requested DataArray, Dataset, Boolean, selected multi-variable, and aggregate shapes rendered | Pass |
| Temporal support | PRISM/gridMET safeguard is excellent; same-interval PRISM variables are falsely rejected | Major |
| Events | Local events, regional episodes, metrics, and timing synchrony succeed with explicit scope | Pass |
| Provenance/inspectability | Strong in live single-source pipes; incomplete across combination, relationship, and serialization boundaries | Moderate |

## What improved relative to previous outside-user evidence

The comparison was performed only after the rc3 environment, both phases, and
rc3-only verdict were frozen. The runs used the same official Python 3.11 slim
image digest, Debian 13.6, `aarch64`, Python 3.11.16, and pip 24.0, so the clean
environment results are directly comparable.

1. **Clean CubeDynamics import improved from blocker to partial success.** rc1
   installation succeeded but `import cubedynamics` failed outright until a
   specialist manually unpacked a Debian library and set `LD_LIBRARY_PATH`.
   rc3 imports with no recovery. The underlying rasterio/libexpat problem is not
   fully resolved: rc3 emits a warning and direct rasterio import still fails,
   so this is a major issue rather than a clean pass.
2. **The obvious first-use PRISM path now works.** rc1's initially discovered
   default/monthly request failed and required a daily retry. rc3's public
   Getting Started daily PRISM request—covering 21 years—worked as copied, and
   the newer noun-first temperature path also worked.
3. **NetCDF export is functionally repaired.** rc1's ordinary export failed on
   Boolean attributes. rc3 exported both a real mean and a Boolean condition;
   the condition reopened with `state` encoded as int8 plus false/true flag
   metadata. Scientific metadata conflicts and missing trace remain separate
   rc3 findings.
4. **The public scientific grammar is materially more inspectable.** rc1
   established one real question and six grammar elements after environment
   recovery. rc3 attempted eleven questions and directly exercised nouns,
   source descriptions, conditions, quantiles, overlap, order, local events,
   regional consolidation, metrics, timing synchrony, lagged association,
   temporal intervals, plotting dispatch, and export.
5. **Event scope and temporal support are now demonstrably strong features.**
   rc3 explicitly distinguished 27 local-cell event instances from 3 regional
   episodes and separated equal date labels from unequal PRISM/gridMET physical
   observation windows. rc1 did not reach this coverage.

The stale transformed attrs, condition-unit conflicts, same-interval PRISM
support rejection, and multi-input provenance loss were not covered deeply
enough in rc1 to call them regressions. They are newly observed rc3 findings,
not evidence that rc3 became worse.

## Primary evidence

- [Structured eleven-question results](../../artifacts/2026-09-03-rc3/phase_b/outputs/scientific_questions.json)
- [Explicit compound/lag follow-ups](../../artifacts/2026-09-03-rc3/phase_b/outputs/followups.json)
- [Units, metadata, NetCDF, plotting, and runtime results](../../artifacts/2026-09-03-rc3/phase_b/regression_outputs/regression_results.json)
- [Exported Boolean condition](../../artifacts/2026-09-03-rc3/phase_b/regression_outputs/hot_condition.nc)
- [Real PRISM cube viewer](../../artifacts/2026-09-03-rc3/phase_b/regression_outputs/temperature_cube.html)
- [Frozen rc1 report used only for post-freeze comparison](../2026-08-31-rc1/naive_user_report.md)

## Final verdict

**FIX BEFORE HUMAN OUTSIDE TEST**

Compared with rc1, rc3 crosses an important threshold: a clean outside user can
now import CubeDynamics itself, retrieve real PRISM and gridMET data, express
advanced environmental questions, and obtain useful outputs without specialist
recovery or package modification. The release still should not be handed to
broader human testers as scientifically trustworthy until the four major
runtime, units, transformed-metadata, and temporal-support defects are fixed.

Testing stops here. No upstream source inspection, package modification,
maintainer triage, issue filing, or pull request was performed.
