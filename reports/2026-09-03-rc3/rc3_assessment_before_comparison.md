# CubeDynamics 0.1.0rc3 Outside-User Acceptance Report

## Executive verdict

**FIX BEFORE HUMAN OUTSIDE TEST**

CubeDynamics 0.1.0rc3 is installable and substantially usable as a public
black-box package. The exact PyPI release installed without intervention,
import completed, the prominent real PRISM example worked, gridMET VPD worked,
eleven realistic questions were attempted, event and temporal-support concepts
were unusually inspectable, plotting worked across requested object shapes, and
Boolean NetCDF export succeeded.

It is not ready for broader human outside testing because four major
user-facing problems remain: a declared rasterio backend cannot import in a
clean supported-style Linux environment; Boolean condition units conflict with
source measurement units; reduction outputs retain stale temporal/dimension
attrs; and strict temporal-support comparison rejects same-provider PRISM
temperature/precipitation whose declared observation intervals are identical.
Several multi-input and exported results also lose enough provenance that the
central scientific-inspectability claim is only partly met.

Question outcome after explicit, evidence-preserving follow-ups: **11 attempted,
9 successfully answered, 2 partially answered, 0 unresolved failures**.

Issue count: **0 blocker, 4 major, 3 moderate, 1 minor**.

This document contains the rc3-only assessment made before opening the previous
rc1 report. The requested comparison is intentionally deferred until this rc3
evidence and verdict are frozen.

## Environment

- Test date: 2026-09-03, America/Denver; evidence timestamps are UTC.
- Host runtime: Docker Desktop 4.63.0, Engine 29.2.1, Apple Silicon host.
- Guest: Debian GNU/Linux 13.6 (`trixie`), Linux 6.12.72, `aarch64`.
- Image: official `python:3.11-slim`, image ID
  `sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6`.
- Isolation: no bind mounts, no inherited `PYTHONPATH`, bridge network, all
  Linux capabilities dropped, `no-new-privileges`, 2 GiB memory, 512 PID limit.
- Python: 3.11.16; pip: 24.0.
- Exact command: `python -m pip install cubedynamics==0.1.0rc3`.
- Installed artifact: public
  `cubedynamics-0.1.0rc3-py3-none-any.whl` from PyPI.

Relevant installed versions:

| Package | Version |
| --- | --- |
| cubedynamics | 0.1.0rc3 |
| numpy | 1.26.4 |
| xarray | 2026.7.0 |
| pandas | 2.3.3 |
| dask | 2026.8.0 |
| rasterio | 1.4.4 |
| rioxarray | 0.19.0 |
| h5netcdf | 1.8.1 |
| h5py | 3.16.0 |
| matplotlib | 3.11.1 |
| plotly | 7.0.0 |
| cubo | 2026.2.0 |
| pystac-client | 0.9.0 |
| planetary-computer | 1.0.0 |
| scipy | 1.17.1 |
| geopandas | 1.1.4 |
| shapely | 2.1.2 |
| pyproj | 3.7.2 |

Evidence: `artifacts/2026-09-03-rc3/environment/`.

## Installation and first import

Installation succeeded on the first attempt. pip resolved all declared Python
requirements, installed the exact rc3 wheel, and `pip check` returned “No
broken requirements found.” Both distribution metadata and
`cubedynamics.__version__` reported `0.1.0rc3`; import resolved from ordinary
`site-packages`.

The first import exited successfully but was not clean:

```text
RuntimeWarning: Engine 'rasterio' loading failed:
libexpat.so.1: cannot open shared object file: No such file or directory
```

Every new Python process repeated the warning. A focused `import rasterio`
failed with the same missing library. No system package was installed and no
package recovery was attempted because PRISM/gridMET, events, plotting, and
export remained testable. The observed state is therefore: CubeDynamics import
works, but an installed declared backend does not.

Evidence: `ENV-003.json` through `ENV-007.json` and
`phase_b/regression_outputs/regression_results.json`.

## Phase A: naive-user experience

The chronological narrative and raw Phase A evidence were SHA-256 frozen before
the public grammar inventory or systematic questions were constructed. See
`reports/2026-09-03-rc3/naive_session.md` and
`artifacts/2026-09-03-rc3/phase_a/FROZEN.json`.

The high-level experience was positive:

- The search-discovered first PRISM request—21 years of daily precipitation at
  a point—returned a real `(7671, 3, 3)` cube in about 30 seconds with units,
  provider, requested range, daily frequency, streaming service, and
  `is_synthetic=0`.
- `data.list_sources()` and `data.describe()` were excellent discovery tools.
  They exposed eight scientific nouns, source flavors, native variables, units,
  coverage, resolution, access mode, limitations, revision/health, and physical
  observation support before data retrieval.
- A real PRISM temperature mean produced readable `semantic_state`, an ordered
  immutable trace, `explain()`, and `validate()` output.
- Both order-sensitive pipelines were expressible and correctly explained as
  prevalence versus a condition on an aggregate.
- A 3-D real-data plot saved as a standalone HTML viewer, and a real temporal
  mean exported and reopened as NetCDF.

The main naive-user frictions were the repeated rasterio warning, a noisy public
namespace, mixed-generation documentation, conflicting plotting return
descriptions, and stale xarray attrs after reduction despite a correct live Pipe
state.

## Phase B: scientific questions

### Q1. What was temperature over a small region during a short period?

- **Data:** Real PRISM daily maximum temperature, Boulder-area 3×3 cells,
  2024-07-01 through 2024-07-31.
- **Workflow:** `pipe(temperature) | v.mean(over=("time", "y", "x"), keep_dim=False)`.
- **Result:** 30.9505 °C regional-period mean.
- **Outcome:** **Worked; scientifically interpretable.** The trace retained the
  reduction dimensions and source state, and the current state correctly became
  a scalar summary in `degC`.
- **Problem:** Unwrapped reduction attrs still described the original temporal
  dimensions/support.

### Q2. Where was it unusually warm within the selected data?

- **Data:** The same real PRISM cube.
- **Workflow:** `v.quantile_state(quantile=0.8, direction="above")`.
- **Result:** 63 true cell-days; each cell was true for 7/31 days. Cell-specific
  thresholds ranged from 31.3485 to 35.6768 °C.
- **Outcome:** **Worked; scientifically interpretable.** The output explicitly
  said the reference population was all 31 selected observations, pooled over
  time independently at each remaining coordinate.
- **Problem:** The Boolean `state` variable inherited `units="degC"` even though
  live semantic units were Boolean.

### Q3. Where was it both hot and dry?

- **Data:** Real PRISM maximum temperature and precipitation on the same 3×3
  grid and dates.
- **Workflow:** temperature >30 °C, precipitation <1 mm, then `v.overlap`.
- **Result:** Strict support mode failed; explicit label mode returned 151
  co-labelled hot-and-dry cell-days and prominently marked support unverified.
- **Outcome:** **Partially answered.** The explicit label-policy result is
  technically clear, but it cannot be called physical same-interval overlap.
- **Problem:** Both PRISM variables declared the same labels, day-ending
  convention, UTC, and `-12h/+12h` intervals. The package nevertheless called
  support “different,” apparently because their descriptive resolution strings
  were `daily` and `daily total`. Strict overlap rejected a scientifically valid
  same-interval case. The output also retained mainly the left temperature
  provenance and a misleading Dataset-level `units="degC"` for a Boolean
  compound condition.

### Q4. Does changing operation order change scientific meaning?

- **Data:** Real PRISM maximum temperature, July 2024.
- **Workflow:** threshold→mean versus mean→threshold at 30 °C.
- **Result:** Threshold→mean returned per-cell occurrence proportions from
  0.3226 to 0.7742. Mean→threshold returned a Boolean map with 8 of 9 cells true.
- **Outcome:** **Worked; highly interpretable.** Units were `proportion` versus
  `boolean`, trace order was exact, and both paths produced accurate
  `ORDER_CHANGES_MEANING` notes.
- **Problem:** Correct meaning was clearest in the live Pipe, not the stale
  unwrapped attrs.

### Q5. Can two variables be compared while retaining their identities?

- **Data:** The aligned PRISM temperature and precipitation arrays.
- **Workflow:** Build an ordinary xarray Dataset with named variables, then
  `pipe(dataset) | v.mean(over="time", keep_dim=False)`.
- **Result:** Both variable names and their units (`degC`, `mm`) survived and
  means were computed.
- **Outcome:** **Partially answered.** xarray variable identity survived, but the
  Pipe described only “Dataset”/“mean of values,” with no CRS, units, source
  flavor, provider, or provenance. Validation emitted CHECKs for all four.
- **Problem:** There was no documented public multi-noun constructor that
  preserved two source records in Pipe semantic state; `verbs.combine` exposed
  by `dir()` is a module, not a callable.

### Q6. Can hot events be identified through time?

- **Data:** The Q2 upper-quantile condition.
- **Workflow:** `v.detect_events(min_duration=1, max_gap=0)`.
- **Result:** 27 local-cell events with 1–4 day durations. The public catalog
  included start/end, duration, peak, mean, integral, spatial identity,
  sequence, and time since the previous event.
- **Outcome:** **Worked; scientifically interpretable.** EventResult explicitly
  stated that each row is one contiguous event instance at one grid cell and is
  not a count of independent regional episodes.
- **Problem:** An exploratory `.cube` guess failed; the public attribute is
  `.dataset`. This was preserved as a novice error, not treated as a defect.

### Q7. Can local-cell events be distinguished from regional episodes?

- **Data:** The 27 local events from Q6.
- **Workflow:** `v.consolidate_events(spatial_relation="neighbors", max_gap="1D")`.
- **Result:** 3 regional episodes. The result changed `event_scope` to
  `regional_episode` and row meaning to one consolidated regional
  spatiotemporal episode; it retained source event IDs, participating-cell
  counts, duration, severity, and centroid.
- **Outcome:** **Worked; scientifically interpretable.** This was one of the
  strongest public API results.

### Q8. Can event frequency, duration, and intensity be summarized?

- **Data:** Both local and regional EventResults.
- **Workflow:** `v.event_metrics(period="month")`; intensity inspected from the
  public event catalog's integral field.
- **Result:** Local metrics: 27 events, mean duration 2.333 days, maximum 4.
  Regional metrics: 3 episodes, mean duration 2.667 days, maximum 5. Local-event
  mean integral was 2.5766 and maximum 6.1506 in the condition's magnitude
  units integrated over observations.
- **Outcome:** **Worked; scientifically interpretable.** Metric output explicitly
  said whether counts represented local instances or regional episodes.
- **Problem:** The configured `event_metrics` defaults do not include intensity;
  the catalog makes it available but the result requires a second summarizing
  step and careful unit interpretation.

### Q9. Can event timing or synchrony be compared among locations?

- **Data:** Q6 local events.
- **Workflow:** `v.timing_synchrony(event_anchor="start", match_tolerance="4D",
  timescale="3D", spatial_mode="neighbors")`.
- **Result:** A Dataset with timing synchrony, matched counts, mean/absolute
  lag, and unmatched counts. Mean timing synchrony was 0.9790 with 3 matched
  events on average.
- **Outcome:** **Worked.** The method and event-anchor semantics were inspectable.
- **Problem:** The relationship result lost CRS, units, and source provenance;
  validation marked each as CHECK and temporal support was unverified.

### Q10. Can a lagged relationship be investigated without implying causality?

- **Data:** PRISM hot and dry condition cubes.
- **Workflow:** `v.sync_with(..., synchrony="occurrence", lags=("-2D", "0D",
  "+2D"))`.
- **Result:** Coupling scores, joint-event counts, valid-sample counts, and best
  lag for each cell.
- **Outcome:** **Worked; appropriately non-causal.** Attributes and explanation
  stated that +k compares left(t) with right(t+k), that the right-hand condition
  occurs later, and that observation support is neither shifted nor harmonized.
- **Problem:** The result correctly warned that supports differ, but again lost
  CRS, units, and source provenance.

### Q11. Can equal labels be distinguished from equal observation support?

- **Data:** Real PRISM temperature and gridMET VPD, identical date labels for
  2024-07-01 through 2024-07-10; gridMET spatially aligned to PRISM with the
  public nearest-grid verb.
- **Workflow:** `compare_temporal_support`, `observation_intervals`, strict
  overlap, then explicit label overlap.
- **Result:** Labels were exact but support different. PRISM's first interval was
  2024-06-30 12:00 to 2024-07-01 12:00 UTC; gridMET's was 2024-07-01 07:00 to
  2024-07-02 07:00 UTC. Strict mode rejected the overlap. Label mode returned 4
  co-labelled cell-days and recorded the caveat without changing timestamps or
  values.
- **Outcome:** **Worked; exceptionally interpretable.** This directly met the
  requested temporal-support safeguard.

Primary structured evidence:
`phase_b/outputs/scientific_questions.json` and
`phase_b/outputs/followups.json`. Raw command records preserve the initial Q3
and Q10 failures before follow-up.

## RC3 regression results

| Area | Result | Evidence | Severity |
| --- | --- | --- | --- |
| Installation/import | Install and CubeDynamics import passed; rasterio backend warned and direct import failed for missing `libexpat.so.1` | `ENV-003`–`ENV-006`, `B-011` | Major |
| First-use data | The exact prominent 21-year daily PRISM example returned real data in ~30 s | `A-001` | Pass |
| Export | Real mean and Boolean condition exports wrote and reopened; Boolean became flagged int8. Stale/conflicting attrs survived and trace did not | `A-011`, `A-012`, `B-011`, `hot_condition.nc` | Major |
| Operation order | Both orders ran and exposed different units, meanings, traces, and order notes | `A-013`, `B-005/Q04` | Pass |
| Units | Mean `degC`, variance `degC^2`, prevalence `proportion` were correct; Boolean `state` was labeled `degC`, threshold had no unit, overlap Dataset said `degC` | `B-011` | Major |
| Metadata/state | Live state was truthful; reduced/unwrapped/exported attrs retained removed `time` and temporal support; multi-input outputs lost context | `A-004`, `A-011`, `B-005/Q05`, `B-011` | Major |
| Plotting | 3-D DataArray, condition Dataset, Boolean DataArray, selected multi-variable Dataset, and 2-D aggregate all rendered; ambiguous Dataset produced a useful error | `A-006`, `B-011`, HTML artifacts | Pass |
| Temporal support | Excellent PRISM/gridMET distinction and strict safeguard; false strict mismatch for same-interval PRISM temperature/precipitation | `B-005/Q11`, `B-008` | Major |
| Events | Local events, explicit regional consolidation, metrics, and timing synchrony ran with clear scope | `B-003`, `B-005/Q06`–`Q09` | Pass |
| Provenance/inspectability | Live pipes were strong; multi-input/relationship/exported outputs lost sources, CRS, units, or trace | `B-005/Q05/Q09`, `B-008/Q10`, `B-011` | Moderate |

## Scientific inspectability assessment

### Upward: can the expression communicate the question?

Usually yes. `pipe(noun) | verb() | verb()` reads clearly, and named operations
such as `quantile_state`, `detect_events`, `consolidate_events`,
`timing_synchrony`, and `sync_with` express scientific intent better than an
equivalent sequence of low-level array operations. Threshold→mean versus
mean→threshold is exemplary: both expressions are concise and the package
explicitly narrates why they mean different things.

### Downward: can the result recover important choices?

While the live Pipe remains available, mostly yes for single-source workflows:
the trace records exact order and parameters, and state reports kind,
dimensions, shape, units, CRS, temporal/spatial status, source flavor,
provenance presence, support convention, event scope, quantile population, and
lag semantics. Source nouns retain product, native variable, query, revision,
endpoint, backend, QA profile, and retrieval information.

The claim weakens at three compression boundaries:

1. **Transformation to plain xarray:** current Pipe state says a mean is
   non-temporal, but attrs still say temporal with `time,y,x` dimensions and
   daily support.
2. **Multiple inputs and relationship results:** variable names may survive,
   but Pipe state often becomes generic and loses both source records, CRS,
   units, and provenance.
3. **Serialization:** NetCDF preserves many attrs and safely encodes Boolean
   data, but not semantic trace/order. It also preserves conflicting units and
   stale semantic attrs.

Another scientist can recover a strong argument from the live notebook object.
They cannot reliably recover the complete argument from every unwrapped or
exported result without reading the notebook line by line.

## Documentation assessment

The newer Library, Documents, and semantic-grammar material is unusually good.
Purpose-grouped verbs, noun/source descriptions, temporal-support policy,
quantile population, event scope, and lag direction were precise enough to
support demanding black-box tests.

The website also appears to publish mixed generations. Search led to a Getting
Started and legacy API set with 2026-03-28 footers and older navigation, while
newer reference pages show 2026-08-27. The older plot page says the plotting
verb returns the incoming cube and attaches the viewer; rc3 and its current
docstring return a viewer. The older quickstart leads with a provider-specific
loader, promotes GitHub `main`, and does not surface the richer noun-first and
semantic APIs. This makes the excellent new contract harder to discover and
creates uncertainty over which pages match rc3.

## Bugs and user-facing findings

### Major 1 — Clean pip install leaves rasterio unusable

- **Expected:** Declared runtime dependencies installed for a supported-style
  clean environment import without backend-loader warnings.
- **Actual:** CubeDynamics import warns that rasterio cannot load; direct
  `import rasterio` raises `ImportError: libexpat.so.1`.
- **Reproduction:** Fresh official Python 3.11 slim container; exact pip command;
  import CubeDynamics or rasterio.
- **Scientific consequence:** Raster-backed source or I/O paths may fail even
  though pip reports a consistent environment; every session begins with a
  warning that undermines trust.
- **Classification:** Dependency/packaging-environment compatibility; **major**.

### Major 2 — Boolean condition and overlap units conflict

- **Expected:** Boolean state units are Boolean/dimensionless; magnitude and
  numeric threshold retain source units; no enclosing Boolean object claims
  `degC`.
- **Actual:** Threshold Dataset has `semantic_units=boolean` but `units=degC`;
  `state.attrs['units']='degC'`; threshold has no unit. Overlap retains
  Dataset-level `units=degC` while its state has no unit. NetCDF preserves the
  conflict.
- **Reproduction:** PRISM temperature → `threshold_state`; inspect Dataset and
  variables; overlap with another condition; export/reopen.
- **Scientific consequence:** Downstream software or scientists can treat a
  truth value as temperature or lose the units of the numerical threshold.
- **Classification:** Package metadata defect; **major**.

### Major 3 — Reductions keep stale temporal/dimension attrs

- **Expected:** An unwrapped or exported mean/variance with no time dimension
  should not claim `semantic_temporal=1`, `semantic_dimensions=[time,y,x]`, or
  current daily observation support.
- **Actual:** Live Pipe state is correct, but xarray attrs retain the removed
  dimension and temporal-support fields; the naive mean also retained ambiguous
  source `min`/`max` fields not describing the reduced values.
- **Reproduction:** Real PRISM temperature → mean or variance with
  `keep_dim=False`; inspect Pipe state versus result attrs; export/reopen.
- **Scientific consequence:** Meaning changes when the wrapper is discarded or
  the file is handed to another scientist.
- **Classification:** Package metadata defect; **major**.

### Major 4 — Strict support rejects equivalent PRISM intervals

- **Expected:** PRISM temperature and precipitation with identical coordinates,
  timezone, day-ending convention, and `-12h/+12h` support compare as equal
  physical intervals.
- **Actual:** The report says support is different and strict overlap raises.
  Public output shows the interval fields are identical; only their descriptive
  temporal-resolution labels differ (`daily` versus `daily total`).
- **Reproduction:** Load same dates/AOI from both PRISM nouns; call
  `compare_temporal_support` or strict `overlap`.
- **Scientific consequence:** A central compound hot/dry analysis is blocked or
  forced into a label-only mode that emits a false unequal-interval warning.
- **Classification:** Package temporal-semantics defect; **major**.

### Moderate 1 — Multi-input/relationship results lose scientific context

- **Expected:** Results retain or explicitly represent both source identities,
  CRS, units, and provenance.
- **Actual:** Multi-variable mean state is generic with no provenance; timing
  and lagged relationship outputs lose source provenance, CRS, and units;
  compound overlap retains mainly left-source metadata.
- **Reproduction:** Q5, Q9, and Q10 workflows.
- **Scientific consequence:** A result cannot independently establish what two
  processes/products were compared.
- **Classification:** Package metadata/provenance limitation; **moderate**.

### Moderate 2 — NetCDF omits transformation trace

- **Expected:** A metadata-safe exported CubeDynamics result supports recovery
  of transformation order and parameters, or documentation clearly limits the
  export contract.
- **Actual:** Rich source/condition attrs survive, but no semantic trace is
  serialized.
- **Reproduction:** threshold → `to_netcdf`; reopen and inspect attrs.
- **Scientific consequence:** Another scientist cannot reconstruct authored
  order from the product alone.
- **Classification:** Package feature/documentation gap; **moderate**.

### Moderate 3 — Public documentation generations disagree

- **Expected:** One coherent release-facing path whose examples and return
  contracts match rc3.
- **Actual:** Older and newer navigation/pages coexist; plotting return behavior
  conflicts; GitHub `main` is promoted in Getting Started; richer noun and
  semantic APIs are not the most obvious path.
- **Reproduction:** Compare public Getting Started/legacy plot pages with newer
  Documents/verb reference and rc3 docstrings.
- **Scientific consequence:** Users can follow a plausible but outdated mental
  model or test unreleased code rather than the public artifact.
- **Classification:** Documentation defect; **moderate**.

### Minor 1 — Public namespace is noisy and exposes module-like verb names

- **Expected:** Raw public discovery either distinguishes callable verb factories
  or keeps internal/grouping modules out of the apparent operation list.
- **Actual:** `dir(cubedynamics.verbs)` exposes many mixed objects;
  `verbs.combine` is a module and `inspect.signature` on it raises TypeError.
- **Reproduction:** Allowed `dir()`/signature inspection.
- **Scientific consequence:** Small discoverability cost; purpose-organized docs
  recover well.
- **Classification:** API discoverability; **minor**.

## Recommended fixes before broader human testing

1. Make the clean supported installation either supply/document the required
   rasterio system runtime or isolate optional backend registration so standard
   imports are clean and unavailable capabilities are explicit.
2. Normalize units at Dataset and variable level for state/overlap outputs:
   Boolean state should be Boolean/dimensionless, magnitude and threshold should
   carry source units, and serialized files should retain that separation.
3. Remove or rewrite temporal/dimension/support attrs after reductions so plain
   xarray and exported results agree with live semantic state.
4. Compare physical observation intervals by their support-defining fields, not
   descriptive resolution wording; add a public regression case for same-date
   PRISM temperature plus precipitation.
5. Define a multi-source provenance model for Dataset, overlap, synchrony, and
   lagged relationship outputs; retain CRS and well-defined dimensionless units.
6. Serialize the semantic trace or publish a clear sidecar/contract explaining
   how exported results carry authored order.
7. Retire or redirect legacy public pages and make exact-release/noun-first
   workflows the dominant Getting Started path.

## What improved relative to previous outside-user evidence

Not evaluated in this pre-comparison assessment. The rc3 verdict and evidence
must be frozen before the earlier rc1 report is opened.

## Final verdict

**FIX BEFORE HUMAN OUTSIDE TEST**

The scientific grammar is no longer merely promising: real data access,
operation-order reasoning, event scope, regional consolidation, temporal
support, plotting, and export all demonstrated substantial value. The remaining
failures are concentrated exactly where the project's central claim is most
sensitive—truthful units, truthful transformed metadata, multi-source
provenance, and portability of meaning beyond a live Pipe. Fix those major
problems before asking broader human testers to trust scientific products.

No CubeDynamics source, tests, implementation, package files, upstream issue,
pull request, monkeypatch, or package modification was used or produced.
