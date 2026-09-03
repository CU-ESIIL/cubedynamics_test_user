"""Focused public-interface regression checks for CubeDynamics 0.1.0rc3."""

from __future__ import annotations

import json
from pathlib import Path
import traceback

import matplotlib

matplotlib.use("Agg")
import numpy as np
import xarray as xr

import cubedynamics as cd
from cubedynamics import data, pipe, verbs as v


OUTPUT = Path("/rc3_regression")
OUTPUT.mkdir(exist_ok=True)
RESULTS = {}


def clean(value):
    if isinstance(value, dict):
        return {str(key): clean(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(item) for item in value]
    if isinstance(value, (np.integer, np.floating, np.bool_)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def run(name, function):
    print(f"\n===== {name} =====")
    try:
        detail = clean(function())
        RESULTS[name] = {"status": "worked", "detail": detail}
    except Exception as exc:
        RESULTS[name] = {
            "status": "failed",
            "exception": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }
    print(json.dumps(RESULTS[name], indent=2, sort_keys=True))


temperature = data.temperature(
    source="prism",
    statistic="maximum",
    bbox=[-105.30, 39.95, -105.20, 40.05],
    start="2024-07-01",
    end="2024-07-10",
)
precipitation = data.precipitation(
    source="prism",
    bbox=[-105.30, 39.95, -105.20, 40.05],
    start="2024-07-01",
    end="2024-07-10",
)


def units_and_metadata():
    mean_pipe = pipe(temperature) | v.mean(over="time", keep_dim=False)
    variance_pipe = pipe(temperature) | v.variance(over="time", keep_dim=False)
    threshold_pipe = pipe(temperature) | v.threshold_state(
        threshold=30.0, direction="above", name="hot"
    )
    dry_pipe = pipe(precipitation) | v.threshold_state(
        threshold=1.0, direction="below", name="dry"
    )
    overlap_pipe = pipe(threshold_pipe.unwrap()) | v.overlap(
        dry_pipe.unwrap(), name="hot_and_dry", temporal_alignment="labels"
    )

    mean = mean_pipe.unwrap().compute()
    variance = variance_pipe.unwrap().compute()
    threshold = threshold_pipe.unwrap().compute()
    overlap = overlap_pipe.unwrap().compute()

    return {
        "mean": {
            "dims": list(mean.dims),
            "units_attr": mean.attrs.get("units"),
            "semantic_units": mean_pipe.semantic_state.units,
            "actual_range": [float(mean.min()), float(mean.max())],
            "stored_source_range": [mean.attrs.get("min"), mean.attrs.get("max")],
            "semantic_dimensions_attr": mean.attrs.get("semantic_dimensions"),
            "semantic_temporal_attr": mean.attrs.get("semantic_temporal"),
            "live_state": mean_pipe.semantic_state.as_dict(),
        },
        "variance": {
            "dims": list(variance.dims),
            "units_attr": variance.attrs.get("units"),
            "semantic_units": variance_pipe.semantic_state.units,
            "actual_range": [float(variance.min()), float(variance.max())],
            "stored_source_range": [variance.attrs.get("min"), variance.attrs.get("max")],
            "attrs": dict(variance.attrs),
            "live_state": variance_pipe.semantic_state.as_dict(),
        },
        "threshold": {
            "dataset_units_attr": threshold.attrs.get("units"),
            "semantic_units_attr": threshold.attrs.get("semantic_units"),
            "live_semantic_units": threshold_pipe.semantic_state.units,
            "variable_units": {
                name: threshold[name].attrs.get("units") for name in threshold.data_vars
            },
            "dtypes": {name: str(threshold[name].dtype) for name in threshold.data_vars},
            "attrs": dict(threshold.attrs),
        },
        "overlap": {
            "dataset_units_attr": overlap.attrs.get("units"),
            "semantic_units_attr": overlap.attrs.get("semantic_units"),
            "live_semantic_units": overlap_pipe.semantic_state.units,
            "variable_units": {
                name: overlap[name].attrs.get("units") for name in overlap.data_vars
            },
            "attrs": dict(overlap.attrs),
            "live_state": overlap_pipe.semantic_state.as_dict(),
            "trace": [step.as_dict() for step in overlap_pipe.semantic_trace],
            "validate": str(overlap_pipe.validate()),
        },
    }


def boolean_netcdf():
    condition_pipe = pipe(temperature) | v.threshold_state(
        threshold=30.0, direction="above", name="hot"
    )
    path = OUTPUT / "hot_condition.nc"
    exported_pipe = condition_pipe | v.to_netcdf(str(path))
    original = exported_pipe.unwrap()
    reopened = xr.open_dataset(path)
    try:
        return {
            "bytes": path.stat().st_size,
            "pipe_return_type": type(original).__name__,
            "variables": list(reopened.data_vars),
            "dtypes": {name: str(reopened[name].dtype) for name in reopened.data_vars},
            "dataset_attrs": dict(reopened.attrs),
            "variable_attrs": {name: dict(reopened[name].attrs) for name in reopened.data_vars},
            "state_values": sorted(set(reopened["state"].values.ravel().tolist())),
            "has_serialized_trace": any(
                "trace" in str(key).lower()
                for key in list(reopened.attrs)
                + [item for name in reopened.data_vars for item in reopened[name].attrs]
            ),
        }
    finally:
        reopened.close()


def save_plot(obj, filename, **kwargs):
    viewer = v.plot(obj, **kwargs)
    public = [name for name in dir(viewer) if not name.startswith("_")]
    path = OUTPUT / filename
    saved = False
    error = None
    if hasattr(viewer, "save"):
        try:
            viewer.save(str(path))
            saved = path.exists()
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
    return {
        "type": type(viewer).__name__,
        "public_names": public,
        "saved": saved,
        "save_error": error,
        "bytes": path.stat().st_size if path.exists() else None,
    }


def plotting_matrix():
    condition = (
        pipe(temperature)
        | v.threshold_state(threshold=30.0, direction="above", name="hot")
    ).unwrap()
    aggregate = (pipe(temperature) | v.mean(over="time", keep_dim=False)).unwrap()
    multi = xr.Dataset({"temperature": temperature, "precipitation": precipitation})
    ambiguous_error = None
    try:
        v.plot(multi)
    except Exception as exc:
        ambiguous_error = f"{type(exc).__name__}: {exc}"
    return {
        "dataarray_3d": save_plot(temperature, "temperature_cube.html", title="Temperature"),
        "condition_dataset": save_plot(condition, "hot_condition.html", title="Hot condition"),
        "boolean_dataarray": save_plot(
            condition["state"], "hot_boolean.html", title="Hot Boolean"
        ),
        "aggregated_2d": save_plot(aggregate, "temperature_mean.png", title="Mean temperature"),
        "ambiguous_multivariable_dataset_error": ambiguous_error,
        "selected_multivariable_dataset": save_plot(
            multi, "selected_temperature.html", variable="temperature", title="Selected temperature"
        ),
    }


def runtime_backend():
    try:
        import rasterio  # noqa: F401 - intentional public dependency import check
    except Exception as exc:
        return {
            "rasterio_import": "failed",
            "exception": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }
    return {"rasterio_import": "worked", "version": rasterio.__version__}


run("units_and_metadata", units_and_metadata)
run("boolean_netcdf", boolean_netcdf)
run("plotting_matrix", plotting_matrix)
run("runtime_backend", runtime_backend)

(OUTPUT / "regression_results.json").write_text(
    json.dumps(clean(RESULTS), indent=2, sort_keys=True) + "\n"
)
print("\n===== REGRESSION SUMMARY =====")
print(json.dumps(clean(RESULTS), indent=2, sort_keys=True))
