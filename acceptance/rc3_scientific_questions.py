"""Public-surface scientific questions for CubeDynamics 0.1.0rc3.

This script intentionally uses only documented public APIs, ordinary xarray,
and public object attributes. It records failures without changing the package
or substituting generated data.
"""

from __future__ import annotations

import json
from pathlib import Path
import traceback

import numpy as np
import xarray as xr

import cubedynamics as cd
from cubedynamics import data, pipe, verbs as v


OUTPUT = Path("/rc3_phase_b")
OUTPUT.mkdir(exist_ok=True)
RESULTS: dict[str, dict] = {}
OBJECTS: dict[str, object] = {}


def clean(value):
    """Convert public results into JSON-friendly evidence."""
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


def inspect_pipe(analysis):
    return {
        "state": clean(analysis.semantic_state.as_dict()),
        "trace": clean([step.as_dict() for step in analysis.semantic_trace]),
        "explain": str(analysis.explain()),
        "validate": str(analysis.validate()),
    }


def question(identifier, text, function):
    print(f"\n===== {identifier}: {text} =====")
    try:
        detail = clean(function())
        RESULTS[identifier] = {"question": text, "status": "worked", "detail": detail}
        print(json.dumps(RESULTS[identifier], indent=2, sort_keys=True))
    except Exception as exc:  # preserve evidence and continue independent coverage
        rendered = traceback.format_exc()
        RESULTS[identifier] = {
            "question": text,
            "status": "failed",
            "exception": f"{type(exc).__name__}: {exc}",
            "traceback": rendered,
        }
        print(rendered)


def q01_temperature():
    temperature = data.temperature(
        source="prism",
        statistic="maximum",
        bbox=[-105.30, 39.95, -105.20, 40.05],
        start="2024-07-01",
        end="2024-07-31",
    )
    OBJECTS["temperature"] = temperature
    analysis = pipe(temperature) | v.mean(over=("time", "y", "x"), keep_dim=False)
    value = analysis.unwrap().compute()
    return {
        "data": "PRISM maximum temperature, Boulder-area 3x3 cells, July 2024",
        "input_sizes": dict(temperature.sizes),
        "input_units": temperature.attrs.get("units"),
        "input_source": temperature.attrs.get("source_flavor"),
        "regional_period_mean": float(value),
        "result_units": value.attrs.get("units"),
        "pipe": inspect_pipe(analysis),
    }


def q02_unusually_warm():
    temperature = OBJECTS["temperature"]
    analysis = pipe(temperature) | v.quantile_state(
        quantile=0.8, direction="above", name="unusually_warm"
    )
    result = analysis.unwrap()
    occurrence = result["state"].mean("time").compute()
    thresholds = result["threshold"].compute()
    OBJECTS["unusually_warm_pipe"] = analysis
    return {
        "method": "cell-wise upper 0.8 quantile over the selected 31 days",
        "true_cell_days": int(result["state"].sum().compute()),
        "occurrence_fraction_range": [float(occurrence.min()), float(occurrence.max())],
        "threshold_degC_range": [float(thresholds.min()), float(thresholds.max())],
        "condition_attrs": dict(result.attrs),
        "pipe": inspect_pipe(analysis),
    }


def q03_hot_and_dry():
    temperature = OBJECTS["temperature"]
    precipitation = data.precipitation(
        source="prism",
        bbox=[-105.30, 39.95, -105.20, 40.05],
        start="2024-07-01",
        end="2024-07-31",
    )
    OBJECTS["precipitation"] = precipitation
    hot = pipe(temperature) | v.threshold_state(
        threshold=30.0, direction="above", name="hot"
    )
    dry = pipe(precipitation) | v.threshold_state(
        threshold=1.0, direction="below", name="dry"
    )
    compound = pipe(hot.unwrap()) | v.overlap(
        dry.unwrap(), name="hot_and_dry", temporal_alignment="require_exact_support"
    )
    result = compound.unwrap()
    OBJECTS["hot_pipe"] = hot
    OBJECTS["dry_pipe"] = dry
    OBJECTS["compound_pipe"] = compound
    return {
        "hot_threshold": "temperature > 30 degC",
        "dry_threshold": "precipitation < 1 mm",
        "hot_cell_days": int(hot.unwrap()["state"].sum().compute()),
        "dry_cell_days": int(dry.unwrap()["state"].sum().compute()),
        "compound_cell_days": int(result["state"].sum().compute()),
        "compound_attrs": dict(result.attrs),
        "pipe": inspect_pipe(compound),
    }


def q04_operation_order():
    temperature = OBJECTS["temperature"]
    threshold_then_mean = (
        pipe(temperature)
        | v.threshold_state(threshold=30.0, direction="above", name="hot_day")
        | v.mean(over="time", keep_dim=False)
    )
    mean_then_threshold = (
        pipe(temperature)
        | v.mean(over="time", keep_dim=False)
        | v.threshold_state(threshold=30.0, direction="above", name="hot_mean")
    )
    prevalence = threshold_then_mean.unwrap()["state"].compute()
    mean_condition = mean_then_threshold.unwrap()["state"].compute()
    return {
        "threshold_then_mean": {
            "meaning": "fraction of days above 30 degC at each cell",
            "range": [float(prevalence.min()), float(prevalence.max())],
            "pipe": inspect_pipe(threshold_then_mean),
        },
        "mean_then_threshold": {
            "meaning": "whether the July mean exceeds 30 degC at each cell",
            "true_cells": int(mean_condition.sum()),
            "pipe": inspect_pipe(mean_then_threshold),
        },
    }


def q05_two_variables():
    temperature = OBJECTS["temperature"]
    precipitation = OBJECTS["precipitation"]
    paired = xr.Dataset(
        {
            "temperature": temperature.rename("temperature"),
            "precipitation": precipitation.rename("precipitation"),
        }
    )
    analysis = pipe(paired) | v.mean(over="time", keep_dim=False)
    result = analysis.unwrap().compute()
    return {
        "input_variables": list(paired.data_vars),
        "input_units": {name: paired[name].attrs.get("units") for name in paired.data_vars},
        "result_variables": list(result.data_vars),
        "result_units": {name: result[name].attrs.get("units") for name in result.data_vars},
        "result_means": {name: float(result[name].mean()) for name in result.data_vars},
        "dataset_attrs": dict(result.attrs),
        "pipe": inspect_pipe(analysis),
    }


def q06_hot_events():
    condition = OBJECTS["unusually_warm_pipe"]
    analysis = condition | v.detect_events(min_duration=1, max_gap=0)
    result = analysis.unwrap()
    OBJECTS["local_events_pipe"] = analysis
    return {
        "type": type(result).__name__,
        "event_scope": result.event_scope,
        "row_meaning": result.row_meaning,
        "event_count": len(result.catalog),
        "catalog_columns": list(result.catalog.columns),
        "duration_range_days": [
            int(result.catalog["duration"].min()),
            int(result.catalog["duration"].max()),
        ],
        "integral_range": [
            float(result.catalog["integral"].min()),
            float(result.catalog["integral"].max()),
        ],
        "pipe": inspect_pipe(analysis),
    }


def q07_regional_episodes():
    local = OBJECTS["local_events_pipe"]
    analysis = local | v.consolidate_events(
        spatial_relation="neighbors",
        max_gap="1D",
        min_participating_cells=1,
        min_local_events=1,
    )
    result = analysis.unwrap()
    OBJECTS["regional_events_pipe"] = analysis
    return {
        "local_event_count": len(local.unwrap().catalog),
        "regional_event_count": len(result.catalog),
        "event_scope": result.event_scope,
        "row_meaning": result.row_meaning,
        "catalog_columns": list(result.catalog.columns),
        "catalog_preview": result.catalog.head().to_dict(orient="records"),
        "pipe": inspect_pipe(analysis),
    }


def q08_event_metrics():
    local = OBJECTS["local_events_pipe"]
    regional = OBJECTS["regional_events_pipe"]
    local_metrics = local | v.event_metrics(period="month")
    regional_metrics = regional | v.event_metrics(period="month")
    local_result = local_metrics.unwrap()
    regional_result = regional_metrics.unwrap()
    local_catalog = local.unwrap().catalog
    return {
        "local_metrics_type": type(local_result).__name__,
        "local_metrics": str(local_result),
        "regional_metrics_type": type(regional_result).__name__,
        "regional_metrics": str(regional_result),
        "catalog_intensity_summary": {
            "mean_integral": float(local_catalog["integral"].mean()),
            "max_integral": float(local_catalog["integral"].max()),
        },
        "local_pipe": inspect_pipe(local_metrics),
        "regional_pipe": inspect_pipe(regional_metrics),
    }


def q09_timing_synchrony():
    local = OBJECTS["local_events_pipe"]
    analysis = local | v.timing_synchrony(
        event_anchor="start",
        match_tolerance="4D",
        score="exponential",
        timescale="3D",
        spatial_mode="neighbors",
    )
    result = analysis.unwrap()
    return {
        "type": type(result).__name__,
        "sizes": dict(result.sizes),
        "variables": list(result.data_vars),
        "attrs": dict(result.attrs),
        "summaries": {
            name: float(result[name].mean(skipna=True).compute())
            for name in result.data_vars
            if np.issubdtype(result[name].dtype, np.number)
        },
        "pipe": inspect_pipe(analysis),
    }


def q10_lagged_processes():
    hot = OBJECTS["hot_pipe"]
    dry = OBJECTS["dry_pipe"]
    analysis = pipe(hot.unwrap()) | v.sync_with(
        dry.unwrap(),
        synchrony="occurrence",
        spatial_relation="same_pixel",
        lags=("-2D", "0D", "+2D"),
    )
    result = analysis.unwrap()
    return {
        "interpretation": (
            "Association only: +2D compares left hot at t with right dry at t+2D; "
            "no causal claim is made."
        ),
        "type": type(result).__name__,
        "sizes": dict(result.sizes),
        "variables": list(result.data_vars),
        "attrs": dict(result.attrs),
        "result": str(result.compute()),
        "pipe": inspect_pipe(analysis),
    }


def q11_temporal_support():
    prism = OBJECTS["temperature"].sel(time=slice("2024-07-01", "2024-07-10"))
    gridmet = data.vpd(
        source="gridmet",
        bbox=[-105.30, 39.95, -105.20, 40.05],
        start="2024-07-01",
        end="2024-07-10",
    )
    report = cd.compare_temporal_support(prism, gridmet)
    left_intervals = cd.observation_intervals(prism)
    right_intervals = cd.observation_intervals(gridmet)

    aligned_gridmet_pipe = pipe(gridmet) | v.align_cube(like=prism)
    aligned_gridmet = aligned_gridmet_pipe.unwrap()
    prism_state = (
        pipe(prism)
        | v.threshold_state(threshold=30.0, direction="above", name="hot_prism")
    ).unwrap()
    gridmet_state = (
        pipe(aligned_gridmet)
        | v.threshold_state(threshold=1.5, direction="above", name="high_vpd_gridmet")
    ).unwrap()

    strict_error = None
    try:
        (pipe(prism_state) | v.overlap(
            gridmet_state,
            name="strict_hot_high_vpd",
            temporal_alignment="require_exact_support",
        )).unwrap()
    except Exception as exc:
        strict_error = f"{type(exc).__name__}: {exc}"

    labels = pipe(prism_state) | v.overlap(
        gridmet_state,
        name="label_aligned_hot_high_vpd",
        temporal_alignment="labels",
    )
    label_result = labels.unwrap()
    return {
        "comparison_type": type(report).__name__,
        "comparison": str(report),
        "comparison_public": {
            name: clean(getattr(report, name))
            for name in dir(report)
            if not name.startswith("_") and not callable(getattr(report, name))
        },
        "prism_first_interval": {
            name: str(left_intervals[name].values[0]) for name in left_intervals.data_vars
        },
        "gridmet_first_interval": {
            name: str(right_intervals[name].values[0]) for name in right_intervals.data_vars
        },
        "strict_overlap_error": strict_error,
        "labels_overlap_true_cell_days": int(label_result["state"].sum().compute()),
        "labels_overlap_attrs": dict(label_result.attrs),
        "labels_pipe": inspect_pipe(labels),
        "alignment_pipe": inspect_pipe(aligned_gridmet_pipe),
    }


question("Q01", "What was temperature over a small region during a short period?", q01_temperature)
question("Q02", "Where was it unusually warm within the selected data?", q02_unusually_warm)
question("Q03", "Where was it both hot and dry?", q03_hot_and_dry)
question("Q04", "Does changing operation order change the scientific meaning?", q04_operation_order)
question("Q05", "Can two variables be compared while retaining their identities?", q05_two_variables)
question("Q06", "Can hot events be identified through time?", q06_hot_events)
question("Q07", "Can local-cell events be distinguished from regional episodes?", q07_regional_episodes)
question("Q08", "Can event frequency, duration, and intensity be summarized?", q08_event_metrics)
question("Q09", "Can event timing or synchrony be compared among locations?", q09_timing_synchrony)
question("Q10", "Can a lagged relationship be investigated without implying causality?", q10_lagged_processes)
question("Q11", "Can equal labels be distinguished from equal observation support?", q11_temporal_support)

summary = {
    "attempted": len(RESULTS),
    "worked": sum(item["status"] == "worked" for item in RESULTS.values()),
    "failed": sum(item["status"] == "failed" for item in RESULTS.values()),
    "results": RESULTS,
}
(OUTPUT / "scientific_questions.json").write_text(
    json.dumps(clean(summary), indent=2, sort_keys=True) + "\n"
)
print("\n===== SUMMARY =====")
print(json.dumps(clean(summary), indent=2, sort_keys=True))
