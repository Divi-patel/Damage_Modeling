"""Order-of-magnitude check of the convective wind × real estate model-v0.1 curves against FEMA's National Risk Index.

Read-only research check (not a calibration, not a runtime path). For every CONUS 0.25° cell of Hazard's convective-wind
hazard layer it computes the expected yearly building loss (% of structure value) of each reference building with the
cell's curves, using Hazard's own frequency and severity, and compares it with NRI's building expected-annual-loss rate
for the same cell (EAL / exposed building value). It reproduces Hazard's convective M1 -> loss arithmetic for one small
building:
    straight-line wind  yearly loss = sw_lambda * E[DR(V)],  V = mu - sigma * ln(U) (exponential excess above 58 mph),
                        capped at Hazard's physical bound L
    tornado             yearly loss = tor_lambda_collection * sum_EF frac_EF * p_hit_EF * DR(EF band midpoint gust),
                        p_hit_EF = (L_EF + a)(W_EF + a) / (pi * 150 km ^ 2),  a = sqrt(building footprint)
Curves come from the governed ordinates CSV. Variants: the proposal (onset 96 mph), no onset (= the tornado record),
and an onset at 90% of each cell's ASCE 700-year gust.

Inputs outside this repository (SHA-256 recorded in the receipt):
    --hazard-repo  a Hazard_Modeling checkout (the convective_wind package under perils/ or pipelines/, and
                   data/convective_wind/convective_wind_m1_hazard_layer_conus.parquet + raw/spc_actual_tornadoes.csv)
    --nri          the Hazard team's NRI Dec 2025 CONUS parquet keyed by cell_id (gs://infrasure-benchmark/
                   hazard_conus_grid/dev/reference/nri/nri_dec2025/raw/run_id=20260706T184931Z_nri_reference/
                   nri_raw_conus.parquet)
Writes NRI_CHECK_<tag>.csv and NRI_CHECK_RECEIPT_<tag>.json in the cell's proposed/ folder.
Needs numpy, pandas, scipy (pyarrow for parquet).

    python scripts/reference_helpers/convective_wind_real_estate_nri_check.py --hazard-repo <path> --nri <parquet>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
CELL_ID = "convective_wind_real_estate"
PROP = ROOT / f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
FT2_KM2 = 9.290304e-8
FOOTPRINT_FT2 = {"RE_RES_SFD_1S_SLAB": 1800.0, "RE_IND_WAREHOUSE": 100000.0, "RE_COM_OFFICE_3S_SLAB": 18000.0}
N_U = 400  # severity quadrature points


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def curves() -> dict[tuple[str, str], tuple[np.ndarray, np.ndarray]]:
    pts: dict[tuple[str, str], list[tuple[float, float]]] = {}
    with open(PROP / f"CURVE_ORDINATES_{TAG}.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            pts.setdefault((r["reference_building_id"], r["pathway_id"]), []).append(
                (float(r["gust_3s_10m_mph"]), float(r["damage_ratio"])))
    return {k: (np.array([p[0] for p in sorted(v)]), np.array([p[1] for p in sorted(v)])) for k, v in pts.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hazard-repo", required=True, type=Path)
    ap.add_argument("--nri", required=True, type=Path)
    a = ap.parse_args()
    hz = a.hazard_repo.resolve()
    pkg = next(p for p in (hz / "perils/convective_wind/src", hz / "pipelines/convective_wind/src") if p.exists())
    sys.path.insert(0, str(pkg))
    from convective_wind.config import (EF_GUST_MID_MS, EF_LABELS, MPH_MS, PHYSICAL_BOUND_L_MS,  # noqa: E402
                                        TORNADO_POOL_RADIUS_KM)
    from convective_wind.spc_m0 import load_spc_tornadoes, national_path_geometry  # noqa: E402

    m1_path = hz / "data/convective_wind/convective_wind_m1_hazard_layer_conus.parquet"
    spc_path = hz / "data/convective_wind/raw/spc_actual_tornadoes.csv"
    m1 = pd.read_parquet(m1_path)
    nri = pd.read_parquet(a.nri)[["cell_id", "swnd_ealb", "swnd_expb", "trnd_ealb", "trnd_expb"]]
    m = m1.merge(nri, on="cell_id", how="left")
    m["nri_sw_pct"] = np.where(m.swnd_expb > 0, m.swnd_ealb / m.swnd_expb * 100, np.nan)
    m["nri_tor_pct"] = np.where(m.trnd_expb > 0, m.trnd_ealb / m.trnd_expb * 100, np.nan)
    geom = national_path_geometry(load_spc_tornadoes(spc_path))
    area = math.pi * TORNADO_POOL_RADIUS_KM ** 2
    mid_mph = np.asarray(EF_GUST_MID_MS) / MPH_MS
    cv = curves()

    sw_ok = (m.sw_lambda > 0) & np.isfinite(m.sw_sigma_ms) & (m.nri_sw_pct > 0)
    s = m[sw_ok].reset_index(drop=True)
    u = (np.arange(N_U) + 0.5) / N_U
    v_sw = np.minimum(s.sw_mu_ms.to_numpy()[:, None] - s.sw_sigma_ms.to_numpy()[:, None] * np.log(u)[None, :],
                      PHYSICAL_BOUND_L_MS) / MPH_MS
    v700 = (s.sw_mu_ms + s.sw_sigma_ms * np.log(s.sw_lambda * 700)) / MPH_MS
    t_ok = (m.tor_lambda_collection > 0) & (m.nri_tor_pct > 0)
    t = m[t_ok].reset_index(drop=True)
    mix = t[[f"tor_ef{i}_frac" for i in range(len(EF_LABELS))]].to_numpy()

    def summary(building, pathway, variant, ours, ref):
        ratio = ours / ref
        return {"reference_building_id": building, "pathway_id": pathway, "variant": variant, "n_cells": int(len(ours)),
                "ours_median_pct_per_year": f"{np.median(ours):.5f}", "nri_median_pct_per_year": f"{np.median(ref):.5f}",
                "ours_over_nri_median": f"{np.median(ratio):.2f}", "ours_over_nri_p10": f"{np.quantile(ratio, .1):.2f}",
                "ours_over_nri_p90": f"{np.quantile(ratio, .9):.2f}",
                "spearman_rank_corr": f"{spearmanr(ours, ref).statistic:.3f}"}

    rows = []
    for b in FOOTPRINT_FT2:
        xs, ys = cv[(b, "straight_line_convective")]
        xt, yt = cv[(b, "tornado_direct_hit")]
        lam = s.sw_lambda.to_numpy()
        rows.append(summary(b, "straight_line_convective", "proposal: onset 96 mph",
                            lam * np.interp(v_sw, xs, ys).mean(axis=1) * 100, s.nri_sw_pct.to_numpy()))
        rows.append(summary(b, "straight_line_convective", "no onset (tornado record shape)",
                            lam * np.interp(v_sw, xt, yt).mean(axis=1) * 100, s.nri_sw_pct.to_numpy()))
        d0 = np.interp(0.9 * v700.to_numpy(), xt, yt)[:, None]
        local = np.clip((np.interp(v_sw, xt, yt) - d0) / (1 - d0), 0, 1)
        rows.append(summary(b, "straight_line_convective", "onset at 90% of the cell's ASCE 700-year gust",
                            lam * local.mean(axis=1) * 100, s.nri_sw_pct.to_numpy()))
        side = math.sqrt(FOOTPRINT_FT2[b] * FT2_KM2)
        p_hit = np.array([(geom[e][0] + side) * (geom[e][1] + side) / area if e in geom else 0.0 for e in EF_LABELS])
        dr_ef = np.interp(mid_mph, xt, yt)
        rows.append(summary(b, "tornado_direct_hit", "proposal",
                            t.tor_lambda_collection.to_numpy() * (mix * p_hit * dr_ef).sum(axis=1) * 100,
                            t.nri_tor_pct.to_numpy()))
    with open(PROP / f"NRI_CHECK_{TAG}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    receipt = {
        "check": "convective_wind_real_estate model v0.1 vs FEMA NRI Dec 2025 (order of magnitude; not calibration)",
        "inputs": {
            "hazard_m1": {"path": "data/convective_wind/convective_wind_m1_hazard_layer_conus.parquet", "sha256": sha256(m1_path),
                          "rows": int(len(m1))},
            "spc_tornadoes": {"path": "data/convective_wind/raw/spc_actual_tornadoes.csv", "sha256": sha256(spc_path)},
            "hazard_package": str(pkg.relative_to(hz)),
            "nri": {"gcs_uri": "gs://infrasure-benchmark/hazard_conus_grid/dev/reference/nri/nri_dec2025/raw/"
                               "run_id=20260706T184931Z_nri_reference/nri_raw_conus.parquet", "sha256": sha256(a.nri)},
            "ordinates": {"path": f"docs/cells/{CELL_ID}/proposed/CURVE_ORDINATES_{TAG}.csv",
                          "sha256": sha256(PROP / f"CURVE_ORDINATES_{TAG}.csv")},
        },
        "hazard_constants": {"physical_bound_mph": round(PHYSICAL_BOUND_L_MS / MPH_MS, 2),
                             "tornado_pool_radius_km": TORNADO_POOL_RADIUS_KM,
                             "ef_midpoint_gust_mph": [round(float(x), 2) for x in mid_mph],
                             "national_median_path_km": {k: [round(x, 4) for x in v] for k, v in geom.items()}},
        "footprint_ft2": FOOTPRINT_FT2,
        "cells": {"straight_line_compared": int(sw_ok.sum()), "tornado_compared": int(t_ok.sum())},
        "asce_700yr_gust_mph": {"p10": round(float(v700.quantile(.1)), 1), "median": round(float(v700.median()), 1),
                                "p90": round(float(v700.quantile(.9)), 1), "max": round(float(v700.max()), 1)},
        "straight_line_rate": {"median_events_per_year_ge_58mph": round(float(s.sw_lambda.median()), 3)},
    }
    (PROP / f"NRI_CHECK_RECEIPT_{TAG}.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(pd.DataFrame(rows).to_string(index=False))
    print(json.dumps({k: receipt[k] for k in ("cells", "asce_700yr_gust_mph", "straight_line_rate")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
