# CubeDynamics 0.1.0rc1 naive outside-user session

## Scope and boundary

I approached CubeDynamics as an environmental scientist encountering an unfamiliar public Python package. I used only the public PyPI release, the public CubeDynamics website and landing-page material, public package metadata, public names/signatures/docstrings, and observed behavior. I did not inspect CubeDynamics implementation files, source, tests, fixtures, developer material, or earlier acceptance evidence. Tracebacks are preserved as observations and were not followed into package files.

The bounded session ran from 2026-08-31 19:45:14 UTC through 19:53:59 UTC. It contains 17 chronological operations (`A31-001` through `A31-017`) and 63.55 seconds of recorded command runtime. The machine-level elapsed interval was 8 minutes 44 seconds.

## Environment and artifact

- Container: `cubedynamics-rc1-naive-20260831`, initially empty `/work`, no mounts
- OS: Debian GNU/Linux 13 (trixie), `aarch64`
- Python: 3.11.16
- Install command: `python -m pip install --disable-pip-version-check --verbose cubedynamics==0.1.0rc1`
- Public artifact selected by pip: `cubedynamics-0.1.0rc1-py3-none-any.whl`
- PyPI wheel SHA-256 reported before install: `785b0ef217c7af1c3d869ddc7c0ce6b91abbcbff280160038c46216b698641c0`
- Imported package version: `0.1.0rc1`
- Installed distribution version: `0.1.0rc1`
- Observed import path: `/usr/local/lib/python3.11/site-packages/cubedynamics/__init__.py`
- `pip check`: no broken Python requirements

The exact verbose pip transcript is `artifacts/2026-08-31-rc1/phase_a/install_pip_verbose.log`; it records all selected dependency versions and the root-user warning.

## What I initially understood

PyPI describes CubeDynamics as a composable grammar for streaming spatiotemporal cubes. The public Getting Started page presents a simple pattern: load environmental data, wrap it with `pipe(...)`, then apply verbs such as `mean`, `anomaly`, and `plot`. A newer public Library page organizes available data by scientific nouns: temperature, precipitation, humidity, radiation, VPD, wind, surface reflectance, and vegetation index.

My working interpretation after discovery was that CubeDynamics is an xarray-adjacent analysis layer that combines environmental data access with readable, inspectable pipelines. It does not replace xarray; it adds source-aware loaders, a pipe grammar, semantic state/trace, validation, and suggestions.

## Chronological experience

### Public discovery and installation (`A31-001`–`A31-003`)

The clean environment contained no CubeDynamics distribution. PyPI was clear and useful: `0.1.0rc1` was publicly available as a wheel and sdist and claimed Python 3.9 or newer. Installing the exact candidate succeeded in 44.7 seconds.

The dependency footprint felt large for a small grammar package. The default install brought in Rasterio, Rioxarray, GeoPandas, Plotly, Matplotlib, SciPy, Dask, STAC packages, Planetary Computer tooling, Cubo, and IPython, among others. That may be defensible for an integrated environmental package, but it increases the chance of platform-specific installation trouble.

### First import failure and specialist recovery (`A31-004`–`A31-011`)

The first `import cubedynamics` failed:

```text
ImportError: libexpat.so.1: cannot open shared object file: No such file or directory
```

The import reached Rasterio through the eagerly imported CubeDynamics data/Sentinel-2/Cubo surface. `pip check` nevertheless reported no broken requirements. This meant the public Python install had succeeded while the package remained unusable in this minimal Debian container.

My ordinary first recovery was `apt-get update; apt-get install -y libexpat1`. It failed because this supplied container forbade the user/group transitions apt attempted. I then confirmed that no shared `libexpat.so` existed, even though the Python standard library's `pyexpat` module worked.

Two further recovery wrong turns are preserved: my first package-pool parsing command had a quoting SyntaxError, and the next assumed `curl`, which the minimal image did not provide. I finally used Python `urllib` to identify the Debian 13 arm64 runtime package, downloaded it from the public Debian pool, and unpacked it only under `/work`. With

```text
LD_LIBRARY_PATH=/work/local-expat/usr/lib/aarch64-linux-gnu
```

the import succeeded and both version sources reported `0.1.0rc1`.

This recovery did not inspect or modify CubeDynamics, but it required Linux ABI, Debian package-pool, and dynamic-linker knowledge. I would not expect a typical notebook or environmental-science user to diagnose this from the installation page. The workaround also had to be carried into every later Python process.

### The public first-cube example failed as written (`A31-012`–`A31-013`)

I copied the Getting Started PRISM precipitation example using Boulder coordinates and its documented dates/variable. It failed immediately. The underlying message said real PRISM streaming currently supports `freq='D'`; the final exception said that streaming failed and synthetic fallback was disabled.

Public signature/docstring inspection clarified the mismatch:

```text
time_res: str = 'ME'
freq: str | None = None
```

but the same docstring states that real streaming currently supports daily data. Therefore the first example's omitted frequency selects a default that the real backend cannot implement. The page does mention daily frequency later under common pitfalls, but the advertised first-cube example itself does not apply it.

This was confusing because the final error emphasizes synthetic fallback, while the real fix is to request daily frequency. I reduced the retry from the example's 21-year interval to five days and explicitly set `freq="D"`.

### Real PRISM retrieval succeeded, then ordinary export failed (`A31-014`)

The daily retry successfully returned and computed a real PRISM precipitation cube for January 1–5, 2024 near Boulder:

- Dimensions/shape: `(time, y, x)`, `(5, 3, 3)`
- Units: `mm`
- Source: `prism_streaming`
- Provider: PRISM Climate Group
- Service/protocol: NCSCO THREDDS NetCDF Subset Service / NcSS
- Synthetic: `False`
- Missing fraction: `0.0`
- Observed range in the subset: `0.0` to about `0.1992 mm`

The object was Dask-backed before computation, matching the streaming/lazy claim.

I then tried the natural xarray operation `loaded.to_netcdf(...)`. That failed because the returned cube includes the boolean attribute `is_synthetic=False`, which `h5netcdf` does not accept as a valid NetCDF attribute dtype by default:

```text
h5netcdf.utils.CompatibilityError: boolean dtypes are not a supported NetCDF feature
```

The partial file `prism_boulder_ppt_2024-01-01_05.nc` is retained only as failed-output evidence and must not be treated as a valid analysis product. I did not try CubeDynamics' own `to_netcdf` helper before the session was bounded, so I cannot say whether it handles this attribute.

### Current catalog and one useful pipeline (`A31-015`–`A31-017`)

The newer scientific-noun catalog was discoverable without downloading data. `data.list_sources()` reported eight nouns, while `data.sources("temperature")` returned `('gridmet', 'prism')`. `data.describe("temperature", source="prism")` provided useful coverage, units, backend, resolution, limitations, QA profile, revision, and endpoint metadata.

The public `data` namespace was noisier than expected: alongside the scientific nouns it exposed certification, revision, serving-history, schema, and QA names that read more like maintainer infrastructure. A scientist can still find the noun functions, but the namespace does not feel minimal.

For the final analysis I loaded the same real five-day PRISM cube and ran:

```python
result = pipe(cube) | v.mean(over=("y", "x"), keep_dim=False)
series = result.unwrap().compute()
```

This succeeded. The daily spatial means were:

```text
[0.0, 0.0, 0.0, 0.0498555563, 0.0225999989] mm
```

`explain()` clearly described the starting precipitation field and spatial averaging step. `validate()` reported ready, ordered time, millimeter units, and source provenance. `semantic_trace` recorded the input/output semantic states and verb parameters. `suggest()` returned no suggestions. The static time-series plot is `artifacts/2026-08-31-rc1/phase_a/prism_boulder_mean_daily_ppt.png`.

One small semantic inconsistency caught my eye: the final semantic state had `source_provider='PRISM Climate Group'` and provenance true, but `source_flavor=None`, even though the cube's `source` attribute was `prism_streaming`. I did not investigate further under the black-box boundary.

## Overall assessment

The core concept became understandable, and a real, non-synthetic PRISM cube successfully flowed through a useful CubeDynamics reduction with readable semantic explanation and validation. The strongest part of the experience was the inspectable pipe after data were available.

This is not a clean-install acceptance pass for the supplied minimal Debian/Python environment. A successful public pip install was followed by a hard import failure, and recovery required specialist system knowledge. The public first-cube example also failed as written because its default frequency is incompatible with the real PRISM backend. After correcting both issues, real retrieval and pipe analysis worked. Ordinary xarray NetCDF export then exposed a boolean-attribute interoperability problem.

A concise outside-user verdict is **conditional core success after substantial recovery; clean first-use experience failed**.

## Documentation observations

- PyPI accurately identified the public version, Python floor, links, and artifacts.
- The Getting Started page was easy to follow but its first PRISM example was not runnable as written against the shipped real backend.
- The quickstart and newer Library pages appeared to represent different generations of the public interface: provider-specific `load_prism_cube` versus scientific nouns such as `data.precipitation`.
- Public signatures and docstrings were substantially more helpful than the failed quickstart for diagnosing frequency, pipe exit via `unwrap()`, and verb behavior.
- No installation material I consulted prepared me for the missing `libexpat.so.1` import failure.

## Not attempted in this bounded session

- gridMET, Sentinel-2, vegetation index, VPD, wind, humidity, or radiation retrievals
- Source-to-source comparison or unit harmonization
- Long ranges, large AOIs, explicit `VirtualCube` tiling, or memory-scaling claims
- `v.anomaly`, `v.variance`, rolling, correlation, event/state, tube, fire, or custom verbs
- The interactive `v.plot` cube viewer, map viewers, notebook rendering, or HTML export
- Synthetic fallback behavior
- The CubeDynamics `to_netcdf` helper as a recovery from native xarray export failure
- Source QA/certification behavior beyond catalog description
- Optional extras, other Python versions, x86_64, macOS, Windows, HPC, or notebook installations
- Full systematic public-surface inventory or performance benchmarking

No claims about these areas are supported by this session.

## Evidence index

- `artifacts/2026-08-31-rc1/phase_a/naive_session.jsonl`: 17 complete chronological operation records with timestamps, exact commands, expectations, raw actual output, interpreted outcomes, confusion, recovery/learning, exit codes, and runtimes
- `artifacts/2026-08-31-rc1/phase_a/raw/A31-001.txt` through `A31-017.txt`: per-operation raw combined stdout/stderr
- `artifacts/2026-08-31-rc1/phase_a/install_pip_verbose.log`: exact verbose installation transcript
- `artifacts/2026-08-31-rc1/phase_a/prism_boulder_mean_daily_ppt.png`: successful final static plot
- `artifacts/2026-08-31-rc1/phase_a/prism_boulder_ppt_2024-01-01_05.nc`: incomplete failed export evidence; not a valid result

