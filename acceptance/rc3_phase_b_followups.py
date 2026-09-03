"""Explicit follow-ups to the preserved Q03/Q10 rc3 failures."""

import json
from pathlib import Path
import traceback

from cubedynamics import compare_temporal_support, data, pipe, verbs as v


output = Path("/rc3_phase_b/followups.json")
results = {}

temperature = data.temperature(
    source="prism",
    statistic="maximum",
    bbox=[-105.30, 39.95, -105.20, 40.05],
    start="2024-07-01",
    end="2024-07-31",
)
precipitation = data.precipitation(
    source="prism",
    bbox=[-105.30, 39.95, -105.20, 40.05],
    start="2024-07-01",
    end="2024-07-31",
)
hot = pipe(temperature) | v.threshold_state(
    threshold=30.0, direction="above", name="hot"
)
dry = pipe(precipitation) | v.threshold_state(
    threshold=1.0, direction="below", name="dry"
)

support = compare_temporal_support(temperature, precipitation)
results["prism_temperature_vs_precipitation_support"] = {
    "coordinates": support.coordinates,
    "temporal_support": support.temporal_support,
    "exact": support.exact,
    "report": str(support),
}

try:
    compound = pipe(hot.unwrap()) | v.overlap(
        dry.unwrap(), name="hot_and_dry", temporal_alignment="labels"
    )
    compound_result = compound.unwrap()
    results["Q03_label_followup"] = {
        "status": "worked_with_explicit_label_policy",
        "true_cell_days": int(compound_result["state"].sum().compute()),
        "attrs": dict(compound_result.attrs),
        "state": compound.semantic_state.as_dict(),
        "trace": [step.as_dict() for step in compound.semantic_trace],
        "explain": str(compound.explain()),
        "validate": str(compound.validate()),
    }
except Exception as exc:
    results["Q03_label_followup"] = {
        "status": "failed",
        "exception": f"{type(exc).__name__}: {exc}",
        "traceback": traceback.format_exc(),
    }

try:
    lagged = pipe(hot.unwrap()) | v.sync_with(
        dry.unwrap(),
        synchrony="occurrence",
        spatial_relation="same_pixel",
        lags=("-2D", "0D", "+2D"),
    )
    lagged_result = lagged.unwrap()
    results["Q10_lagged_followup"] = {
        "status": "worked",
        "scientific_interpretation": (
            "+2D compares hot at t with dry at t+2D. This is a coordinate-label "
            "association and neither aligns observation support nor implies causality."
        ),
        "sizes": dict(lagged_result.sizes),
        "variables": list(lagged_result.data_vars),
        "attrs": dict(lagged_result.attrs),
        "result": str(lagged_result.compute()),
        "state": lagged.semantic_state.as_dict(),
        "trace": [step.as_dict() for step in lagged.semantic_trace],
        "explain": str(lagged.explain()),
        "validate": str(lagged.validate()),
    }
except Exception as exc:
    results["Q10_lagged_followup"] = {
        "status": "failed",
        "exception": f"{type(exc).__name__}: {exc}",
        "traceback": traceback.format_exc(),
    }

output.write_text(json.dumps(results, indent=2, default=str, sort_keys=True) + "\n")
print(json.dumps(results, indent=2, default=str, sort_keys=True))
