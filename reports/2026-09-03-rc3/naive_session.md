# CubeDynamics 0.1.0rc3 Phase A naive-user session

## Scope and tester context

This is the chronological Phase A record for the exact public PyPI release
`cubedynamics==0.1.0rc3`. The package was treated as an external black box. No
upstream or installed implementation source, tests, fixtures, developer files,
disassembly, editable install, or package patch was used.

The repository prompt log had to be read before the run and disclosed the
previous rc1 verdict plus four high-level finding summaries. The rc1 report and
evidence were not opened. That unavoidable exposure means this is a controlled
new-user exploration rather than a claim of perfect psychological blinding.
The exploration nevertheless followed only rc3 public materials in the order
recorded below; no rc1 comparison was made before this freeze.

Session date: 2026-09-03 (America/Denver). Raw records use UTC timestamps.

## Chronology

### 1. Clean install and first import

I began in a fresh official `python:3.11-slim` container with no host mount and
no `PYTHONPATH`. The guest was Linux 6.12.72 on `aarch64`, Python 3.11.16, and
pip 24.0. The exact command was:

```text
python -m pip install cubedynamics==0.1.0rc3
```

Installation completed without intervention and installed the public
`cubedynamics-0.1.0rc3-py3-none-any.whl`. `pip check` reported no broken Python
requirements. Both `importlib.metadata.version("cubedynamics")` and
`cubedynamics.__version__` reported `0.1.0rc3`; the import resolved from normal
`site-packages`.

The first `import cubedynamics` returned exit status 0, but emitted:

```text
RuntimeWarning: Engine 'rasterio' loading failed:
libexpat.so.1: cannot open shared object file: No such file or directory
```

The same warning appeared on every subsequent fresh Python process. I made no
recovery attempt in Phase A because import and the chosen PRISM workflows still
ran; the missing runtime library remains genuine first-use evidence.

Evidence: `environment/ENV-001.json` through `environment/ENV-007.json`.

### 2. What the public site said CubeDynamics is

A normal web search led first to the public Getting Started page. It described
CubeDynamics as a grammar above environmental data sources: a consistent way to
compute on environmental streams, with `pipe(cube) | verb() | verb()` as the
central form. The homepage emphasized that it is not storage, a catalog, a file
format, or an observation archive. The newer semantic-grammar material added a
clearer claim: an immutable trace and current semantic state should make both
operation order and scientific meaning inspectable.

The core terms became understandable after visiting multiple pages:

- A **noun** is the scientific thing entering an analysis, such as temperature,
  precipitation, or VPD.
- A **source flavor** identifies the actual data product/provider behind a
  noun, such as PRISM or gridMET; common nouns do not imply interchangeability.
- A **verb** is a configured callable that transforms the current object.
- A **pipe** carries the object and applies verbs exactly left to right.

This model is compelling and concise once the newer Learn/Documents material is
found. The search-discovered Getting Started and legacy API pages, however,
look older than the newer reference pages: they have different navigation,
2026-03-28 footers versus 2026-08-27, different plotting return descriptions,
and older `dim=` examples alongside newer `over=` examples. Getting Started
also promotes installing the latest GitHub `main`, which is inappropriate for
an exact-release acceptance path.

Public pages consulted in this order:

1. <https://cu-esiil.github.io/cubedynamics/quickstart/>
2. <https://cu-esiil.github.io/cubedynamics/>
3. <https://cu-esiil.github.io/cubedynamics/data/>
4. <https://cu-esiil.github.io/cubedynamics/documentation/>
5. <https://cu-esiil.github.io/cubedynamics/reference/verbs/>
6. <https://cu-esiil.github.io/cubedynamics/reference/pipe/>
7. <https://cu-esiil.github.io/cubedynamics/concepts/semantic_grammar/>
8. <https://cu-esiil.github.io/cubedynamics/viz/cube_viewer/>

### 3. The most obvious first cube

I copied the first PRISM example from Getting Started exactly: a point at
40.0, -105.25, daily precipitation from 2000-01-01 through 2020-12-31. Despite
the long period, it returned real data in about 30 seconds as a `(7671, 3, 3)`
DataArray with `time`, `y`, and `x`. Attributes reported millimetres, total
precipitation, the PRISM Climate Group, NcSS streaming, daily frequency, the
requested dates, and `is_synthetic=0`.

This was unexpectedly good: the default, network-backed first-use path worked
without shrinking the request, credentials, a hidden fixture, or synthetic
fallback. The persistent rasterio warning made the success look less clean than
it was.

Evidence: `phase_a/A-001.json`.

### 4. Discovering nouns, sources, and verbs

Normal `dir()` inspection exposed the advertised root `pipe`, `data`, and
`verbs` namespaces. It also exposed a very large and mixed root surface,
including compatibility names, plotting internals, fire-specific functions,
runtime types, and modules. The `verbs` namespace included the expected basic
statistics plus state, event, regional-consolidation, synchrony, overlap,
plotting, and export operations. This is powerful but initially noisy.

The documented `data.list_sources()` and `data.describe()` calls were much more
successful as scientific discovery tools. They clearly reported eight nouns,
implemented source flavors, native variables, units, coverage, resolution,
backend, limitations, revision state, live health, and—unusually helpfully—the
observation-support convention. For example, PRISM temperature is daily
`degC`, labelled day-ending with support `-12h` to `+12h`, whereas gridMET VPD
is daily `kPa`, labelled calendar-day-starting with support `+7h` to `+31h`.

The records also reported `live_health='STALE'` while
`revision_status='VALIDATED'`. That distinction is scientifically useful but
needs interpretation: validation of a serving revision is not current endpoint
health.

Evidence: `phase_a/A-002.json` and `phase_a/A-003.json`.

### 5. A noun-first pipeline and inspectability

Following the newer noun API, I requested three days of real PRISM maximum
temperature near Boulder and computed:

```python
analysis = pipe(cube) | v.mean(over="time", keep_dim=False)
```

The request returned a named `temperature` DataArray with explicit product,
provider, source variable, units, CRS, spatial/temporal query, resolution,
support convention, revision, access, normalization, and QA metadata. The mean
returned a spatial DataArray and the pipe correctly described it as a
non-temporal summary in degrees Celsius. `semantic_state`, `semantic_trace`,
`explain()`, and `validate()` were readable and mutually consistent. The trace
retained the input and output state plus the exact mean parameters.

The underlying result attributes were less truthful than the semantic state.
They still claimed `semantic_temporal=1`,
`semantic_dimensions='["time", "y", "x"]'`, daily temporal resolution/support,
and the source cube's `min=-10.4361` and `max=27.6489`, even though `time` was
removed and the values had been averaged. A scientist inspecting the unwrapped
or exported xarray object without the live Pipe could mistake stale metadata
for the current object's properties.

Evidence: `phase_a/A-004.json`.

### 6. Learning exact calls

The newer purpose-organized verb reference was the easiest place to understand
what is actually implemented. Allowed signature/docstring inspection then
resolved ambiguities for `mean`, `variance`, `threshold_state`, `overlap`,
`detect_events`, `consolidate_events`, `event_metrics`, synchrony, plotting,
NetCDF export, and temporal support. The docstrings were substantially more
precise than the older API pages, particularly about condition means, temporal
alignment policy, lag direction, and plot dispatch.

Evidence: `phase_a/A-005.json`.

### 7. Plotting

Using real three-dimensional PRISM temperature, the pipe-style plot returned a
`CubePlot`, and `save()` produced a 42,771-byte standalone HTML viewer. The
operation printed useful preparation progress. This matched the newer verb
docstring. It did not match the older verb page's statement that plotting
returns the incoming cube and attaches a viewer, which would lead a user to
expect `unwrap()` to return data rather than a viewer.

Two initial `docker cp` attempts could not read the saved file directly from
the container's tmpfs even though the file existed; copying it to the container
root filesystem first allowed preservation. This is a test-harness/container
artifact, not attributed to CubeDynamics.

Evidence: `phase_a/A-006.json` through `phase_a/A-010.json` and
`phase_a/naive_temperature_viewer.html`.

### 8. NetCDF export

The documented pipeable export worked on a real PRISM temporal mean. It wrote a
17,346-byte NetCDF file, returned the original DataArray in the pipe, and could
be reopened with xarray. Units, source, product, query, revision, and summary
operation survived on the data variable. Dataset-level attributes were empty,
which is normal for a serialized DataArray, but the stale temporal, dimension,
min, and max attributes described above also survived exactly. Export therefore
preserved metadata successfully but did not make all of it scientifically true.

Evidence: `phase_a/A-011.json`, `phase_a/A-012.json`, and
`phase_a/naive_prism_mean.nc`.

### 9. Operation order

Both requested orders were directly expressible on ten days of real PRISM
maximum temperature:

```python
pipe(cube) | v.threshold_state(threshold=5, direction="above") | v.mean(over="time")
pipe(cube) | v.mean(over="time") | v.threshold_state(threshold=5, direction="above")
```

The first returned a proportion summary: the fraction of daily observations
above 5 °C. The second returned a Boolean condition: whether the temporal mean
was above 5 °C. Their states, units (`proportion` versus `boolean`), exact trace
order, explanations, validation reports, and purpose-specific
`ORDER_CHANGES_MEANING` notes were excellent. This was the clearest successful
demonstration of the central scientific claim in Phase A.

The second condition Dataset still inherited stale source-array metadata such
as the original temporal dimensions and min/max, even while live semantic state
correctly described a non-temporal condition.

Evidence: `phase_a/A-013.json`.

## What was immediately obvious

- Installation spelling and the `pipe(cube) | v.operation()` shape.
- The first PRISM example and how to inspect xarray dimensions/attributes.
- The high-level purpose: concise ordered computation over environmental cubes.
- `data.list_sources()` and `data.describe()` once the newer Library page was
  found.

## What required searching

- The noun/source distinction; Getting Started still leads with a
  provider-specific loader.
- The newer semantic state/trace contract and order notes.
- Exact state, event, temporal-support, synchrony, output, and plotting calls.
- Whether a plotting pipe unwraps to data or a viewer, because public pages
  disagree.

## Confusion, dead ends, and assumptions

- Public documentation appears to mix at least two generations of site
  structure and API explanation.
- The root and verbs namespaces are discoverable but crowded; purpose-organized
  documentation is much easier than raw `dir()`.
- The import warning says a registered backend failed, but does not say which
  CubeDynamics capabilities remain safe or how a PyPI user should obtain the
  missing system library.
- The semantic state is more truthful after reduction than the underlying
  xarray attrs; which one is authoritative is not obvious after export.
- The source records' VALIDATED revision plus STALE live health are responsible
  distinctions, but a new user needs to know that neither alone certifies their
  requested values.

## Unexpectedly good experiences

- The long default PRISM request worked from a clean public install.
- Noun/source descriptions included unusually rich product, unit, support,
  revision, QA, and access information before download.
- Real-data loaders explicitly refused silent source interchangeability and
  retained bounded-query provenance.
- Operation-order explanations were concise, accurate, and visible in both the
  trace and validation output.
- HTML plotting and metadata-safe NetCDF export both worked without package
  modification.

## Phase A freeze conclusion

By the end of naive exploration I could explain the noun/source/verb/pipe
grammar, acquire real data, build and inspect a pipeline, plot, export, identify
source units and support, discover operations, and distinguish two operation
orders. The core experience was scientifically promising and substantially
usable. It was not clean: the missing rasterio runtime warning, mixed-generation
documentation, and stale transformed/exported attrs all weaken outside-user
confidence and require systematic follow-up.

No Phase B inventory, rc1 comparison, maintainer triage, or package fix was
performed before this record was closed.
