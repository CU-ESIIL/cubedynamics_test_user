# CubeDynamics

<p align="center">
  <img src="https://raw.githubusercontent.com/CU-ESIIL/cubedynamics/main/docs/assets/img/cubedynamics_logo.png" alt="CubeDynamics" width="520">
</p>

![Tests](https://github.com/CU-ESIIL/cubedynamics/actions/workflows/tests.yml/badge.svg) ![Docs](https://github.com/CU-ESIIL/cubedynamics/actions/workflows/pages.yml/badge.svg)

CubeDynamics is a composable grammar for spatiotemporal environmental cubes:
**nouns describe observations, verbs describe operations, and pipes make their
order explicit.** Its core is deliberately small: `pipe(cube) | verb() | verb()`.
It builds on xarray, NumPy, Dask, and geospatial tools rather than replacing them.

The checkout currently declares **version 0.1.0, alpha**, with Python **3.9+**
support. Development and documentation CI use Python 3.11; the offline test
matrix covers 3.9–3.12. These are repository metadata and CI targets, not a claim
that an installed PyPI release contains every change on `main`.

For the first public alpha release candidate, see the [0.1 support contract](docs/project/api_support_0_1.md),
[release-note draft](docs/project/release_0_1_0.md), and [non-publishing release checklist](RELEASING.md).
The candidate artifact targets `0.1.0`; it is not a published release or tag.

## Start here

The [website](https://cu-esiil.github.io/cubedynamics/) has five entry points:

- [Home](https://cu-esiil.github.io/cubedynamics/) — what the grammar is for.
- [Learn](https://cu-esiil.github.io/cubedynamics/learn/) — a progressive introduction.
- [Library](https://cu-esiil.github.io/cubedynamics/library/) — environmental nouns and source flavors.
- [Documents](https://cu-esiil.github.io/cubedynamics/documentation/) — operations, arguments, and return values.
- [Vignettes](https://cu-esiil.github.io/cubedynamics/vignettes/) — real-data analysis stories with runnable notebooks and figures.

[Developer documentation](https://cu-esiil.github.io/cubedynamics/developer/)
separates architecture, CI, source maintenance, and audits from user reference.

## Install

For the packaged release:

```bash
python -m pip install cubedynamics
```

For this checkout's code, real-data fixtures, and notebooks, clone the repository
and install from its root. The following uses the repository's Python 3.11
development target:

```bash
git clone https://github.com/CU-ESIIL/cubedynamics.git
cd cubedynamics
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows, activate with `.venv\Scripts\activate` instead. For an exact
reproduction, check out a recorded commit or release tag before installing.
`make install` and `make test` provide the existing local development shortcuts.

Optional extras in [pyproject.toml](pyproject.toml):

| Extra | Adds |
| --- | --- |
| `test` | Pytest and distribution-checking tools |
| `docs` | MkDocs, reference rendering, and notebook rendering |
| `vignettes` | Notebook execution and a Python kernel |
| `viz` | Optional Lexcube widget support; not required for the custom HTML cube viewer |
| `dev` | Test, docs, vignette, and Lexcube tooling |
| `browser` | Playwright and its pytest plugin, Python 3.10+; install Chromium separately |
| `roads` | Optional PyArrow reader for the bounded Overture roads candidate |

The former `climate_cube_math` namespace remains a deprecated compatibility
path. Use `cubedynamics` for new code.

## A short pipe, a visible result

Run this from the repository root after installation. It uses a small,
checksum-controlled **real PRISM extract**, not generated observations, and
requires no network request. The input contains January 1–30, 2024 daily
maximum temperatures near Boulder, Colorado, in degrees Celsius.

<!-- readme-example: offline -->
```python
import matplotlib.pyplot as plt
import xarray as xr
from cubedynamics import pipe, verbs as v

# Load only the small, reviewed fixture; the file closes after loading.
with xr.open_dataset(
    "tests/fixtures/real_data/prism_boulder_january_2024.nc", engine="scipy"
) as observations:
    cube = observations["tmax"].load()

# Average daily maximum temperature over these dates at each grid cell.
result = pipe(cube) | v.mean(over="time", keep_dim=False)
result.unwrap().plot(cmap="magma", cbar_kwargs={"label": "Temperature (°C)"})
plt.title("Boulder region · Mean daily maximum · January 1–30, 2024")
plt.show()
```

This describes the observed period, not a long-term climate normal. The
[fixture provenance](tests/fixtures/real_data/prism_boulder_january_2024.provenance.json)
records its source and checksum; [validation](https://cu-esiil.github.io/cubedynamics/validation/)
documents the checks.

Pipes also expose `explain()`, `suggest()`, `validate()`, `semantic_state`, and
`semantic_trace`. These inspect metadata and analytical order; they do not
certify the scientific question or independently validate source observations.
`|` invokes each stage when composed; Dask-backed stages can retain deferred
computation. `unwrap()` returns the current value, not a forced computation.

## Choose observations by scientific noun

The current catalog contains these implemented source flavors:

<!-- readme-catalog: start -->
| Noun | Source flavors |
| --- | --- |
| `temperature` | `gridmet`, `prism` |
| `precipitation` | `gridmet`, `prism` |
| `vpd` | `gridmet` |
| `wind` | `gridmet` |
| `humidity` | `gridmet` |
| `radiation` | `gridmet` |
| `surface_reflectance` | `sentinel2` |
| `vegetation_index` | `sentinel2` |
<!-- readme-catalog: end -->

Inspect support without downloading observations:

<!-- readme-example: discovery -->
```python
from cubedynamics import data

print(data.list_sources())
print(data.describe("temperature", "prism"))
```

For a live request, choose a source and statistic explicitly. This example
requires provider access and may fail if the remote service is unavailable:

<!-- readme-example: live -->
```python
import matplotlib.pyplot as plt
from cubedynamics import data, pipe, verbs as v

cube = data.temperature(
    source="prism", statistic="maximum",
    bbox=[-105.55, 39.85, -105.05, 40.15],
    start="2024-01-01", end="2024-01-03",
)
(pipe(cube) | v.mean(over="time", keep_dim=False)).unwrap().plot(cmap="magma")
plt.show()
```

The same noun does **not** make sources interchangeable. gridMET temperature
uses kelvin and provides maximum/minimum; PRISM uses degrees Celsius and also
provides a mean statistic. These climate sources cover the contiguous United
States. Sentinel-2 has different spatial, spectral, acquisition, and quality
constraints. Inspect units, CRS, coordinates, missingness, and source provenance
before combining observations; CubeDynamics does not silently harmonize them.

Noun loaders reject synthetic fallback. Provider-specific loaders remain
available for lower-level access. Landsat and FIRED integrations are additional
workflows, not extra registered noun flavors. `stream_global_climate_cube`
adapts an already-open xarray object; it is not a global-data downloader.

Lazy output is not proof of bounded remote access: PRISM uses daily THREDDS
NcSS subsets; gridMET can use OPeNDAP with an optional compatible engine, but
falls back to fetching annual HTTPS files. A long record can still be expensive.
Source QA separates a serving revision's scientific validity from live endpoint
health. See the [source reference](https://cu-esiil.github.io/cubedynamics/library/sources/).

## Built-in vocabulary and your own verbs

| Layer | Role |
| --- | --- |
| Core grammar | `pipe`, `Pipe`, callable stages, and semantic contracts |
| Shared vocabulary | Transformations, summaries, states/events, comparison, and alignment |
| Integrations | Source adapters, plotting/viewers, and output helpers |
| Project extensions | Synchrony, biological workflows, tubes, Fire VASE, and your own methods |

Project vocabularies currently ship in the same distribution for compatibility;
their scientific assumptions are not part of the minimal grammar contract.

A project-owned operation can be an ordinary callable factory. Continuing with
the **offline Celsius cube** above, ask what fraction of observed days exceeded
a chosen temperature. The threshold is an analytical choice, not a provider fact:

<!-- readme-example: custom -->
```python
def fraction_above(threshold):
    def _op(cube):
        # Count only observed days; missing values must not become cool days.
        observed = cube.notnull().sum("time")
        return ((cube > threshold).sum("time") / observed.where(observed > 0)).rename(
            "fraction_above"
        ).assign_attrs(units="1")
    return _op

warm_days = (pipe(cube) | fraction_above(10)).unwrap()
warm_days.plot(vmin=0, vmax=1, cbar_kwargs={"label": "Fraction of observed days"})
plt.title("Boulder region · Daily maximum above 10°C")
plt.show()
```

No registration or subclass is required. Start from the
[custom-verb scaffold](examples/custom_verb_project/README.md) and test direct
and piped use before presenting a method as reviewed.

[Browse operations by purpose](https://cu-esiil.github.io/cubedynamics/reference/verbs/)
or use the [full A–Z inventory](https://cu-esiil.github.io/cubedynamics/reference/verbs/a-z/).
Not every callable in `v` is a pipe-stage factory: `v.fire_plot`, for example,
is a direct visualization helper. `v.correlation_cube` and `v.fit_model` are
reserved placeholders, not implemented analysis operations. Compatibility
aliases are labeled separately in the reference. `v.month_filter` is a
supported stage; only its legacy `cubedynamics.ops` import warns.

`v.plot()` uses the custom HTML/CSS/JavaScript cube viewer. Fire plotting still
has a Plotly renderer; it has not been fully migrated to that viewer.
`FireEventDaily` and `FireHull` are the canonical fire object names;
`TimeHull` is retained for compatibility.

## Reproduce and validate

There are **twelve supported offline notebooks**: eight core lessons and three
real-data noun lessons (elevation, roads, streamflow) under
`docs/vignettes/` and the Working Lands analysis under `docs/decision_vignettes/`.
They cover arrays, tidy tables, Datasets, composition, transformations,
states/events, custom verbs, lazy computation, and a two-noun decision story.
Each has real-data provenance, executable code, and required static plots.
The runner checks those outputs without modifying notebook sources:

```bash
python scripts/run_vignettes.py
```

Use these checks from an installed development checkout:

```bash
python -m pytest -m "not integration and not online" -q
python scripts/run_validation.py --run-vignettes
python scripts/run_source_qa.py
python scripts/run_decision_qa.py
python scripts/build_reference_docs.py --check
python -m mkdocs build --strict
python scripts/check_site_links.py site
python scripts/check_repository_size.py --mode tracked
```

QA evidence is written under ignored `artifacts/`. Passing a bounded fixture
does not certify every product, location, period, or current provider endpoint.
Online checks and live-source certification are separate from offline tests.

For website changes, also run the opt-in browser suite (Python 3.10+):

```bash
python -m pip install -e ".[browser]"
python -m playwright install chromium
python -m pytest tests/browser -m browser --site-dir site --browser chromium \
  --tracing retain-on-failure --output artifacts/browser/playwright -q
```

It checks built-page links and anchors, decoded images, deferred embeds,
desktop/mobile journeys, and cube interaction. CI gates documentation and Pages
publication on browser failures; external-link availability is advisory.
See [CI and testing](docs/dev/ci_testing.md) for evidence and platform setup.

## Repository and contribution guide

The main noun library includes [elevation](docs/library/nouns/elevation.md),
[roads](docs/library/nouns/roads.md), and [streamflow](docs/library/nouns/streamflow.md),
with source-specific installed imports, complete references, and offline
real-data lessons. Their bounded QA status is documented separately from their
place in the grammar; `data.list_sources()` and production serving histories
are unchanged. Historical acquisition reports live in
[developer source engineering](docs/data/source_projects/index.md).

- `src/cubedynamics/` is the installed package; `code/cubedynamics/` is a legacy mirror.
- `docs/` holds the website, generated references, and supported notebooks.
- `tests/fixtures/real_data/` holds small observational fixtures and provenance.
- `scripts/` holds reference/notebook builders and QA runners.
- [paper/](paper/README.md) holds manuscript working material, including the
  supplied citation-map draft; draft markers are not completed references.

Large scientific products and runtime manifests belong outside Git. Use
[config/storage.example.yml](config/storage.example.yml) for local/object-store
paths. The size policy permits small reviewed fixtures under `tests/fixtures/`;
do not remove their NetCDF files merely because bulk NetCDF output is blocked.
Historical Fire VASE outputs still in Git require an explicit archival plan,
not automatic deletion. See [data policy](data/README.md) and the
[publication plan](docs/project/publication_plan.md).

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before changing
the package. Edit reference generators, not files marked generated. Keep the
five website entry points and distinguish implemented, compatibility, and
reserved APIs. See the [public API policy](docs/project/public_api.md).

## Citation and license

Use [CITATION.cff](CITATION.cff), recording the package version/commit and the
source products used. Its DOI field is not populated; manuscript citation
markers do not supply a release DOI. Release publishing is handled by
[publish.yml](.github/workflows/publish.yml) on `v*` tags or manual dispatch;
tagging/publishing and completing manuscript references are separate tasks.

CubeDynamics is distributed under the [MIT License](LICENSE).
