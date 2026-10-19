"""NRI order-of-magnitude check for the wildfire × real estate model-v0.1 proposal (a check, never a calibration).

For every Hazard 0.25-degree cell, the yearly building loss rate the curves imply is
    rate_b = lambda * sum_k P(class k | fire) * DR_b(k)          (% of structure value per year)
with Hazard's own M1 inputs: lambda = -ln(1 - BP) on burnable pixels (production policy; the all-pixel policy as a
diagnostic) and the conditional FLP1-6 mix, renormalised as Hazard's adapter does. Hazard couples with p_hit = 1.
The analytic rate ignores the one-loss-per-year cap of a single building (negligible at these rates).
It is compared with FEMA NRI (Dec 2025) wildfire building EAL / exposed building value for the same cell.

Writes, in the cell's proposed/ folder:
    NRI_CHECK_<tag>.csv           per building and variant: medians, ratios, exposure-weighted national ratio, rank corr.
    NRI_CHECK_RECEIPT_<tag>.json  input hashes and summary

Usage (from the repository root; needs numpy, pandas, pyarrow):
    python scripts/reference_helpers/wildfire_real_estate_nri_check.py --m1 <wildfire M1 parquet> --nri <NRI parquet>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import derive_wildfire_real_estate_curves as derive  # noqa: E402

CELL_ID = "wildfire_real_estate"
PROP = ROOT / f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
M1_SHA = "2d931d876aa015ee28d01e1047afd9d0bfcfe6c0d8044166a69f0e2ba1592953"
M1_URI = ("gs://infrasure-benchmark/hazard_conus_grid/dev/wildfire/v1_fsim/m1_hazard_layer/run_id=20260702_m1_fsim_conus/"
          "tables/wildfire_v1_fsim_m1_hazard_layer_20260702_m1_fsim_conus.parquet")
NRI_URI = ("gs://infrasure-benchmark/hazard_conus_grid/dev/reference/nri/nri_dec2025/raw/"
           "run_id=20260706T184931Z_nri_reference/nri_raw_conus.parquet")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m1", required=True, type=Path)
    ap.add_argument("--nri", required=True, type=Path)
    a = ap.parse_args()
    m1_sha = sha256(a.m1)
    if m1_sha != M1_SHA:
        print(f"M1 sha256 {m1_sha} differs from Hazard's runtime-input manifest {M1_SHA}")
        return 1
    flp_cols = [f"flp{i}_prob_given_fire" for i in range(1, 7)]
    m1 = pd.read_parquet(a.m1, columns=["cell_id", "lambda_burnable", "lambda_all_pixel"] + flp_cols)
    nri = pd.read_parquet(a.nri, columns=["cell_id", "wfir_ealb", "wfir_expb"])
    m = m1.merge(nri, on="cell_id", how="left")
    flp = m[flp_cols].to_numpy(float)
    tot = flp.sum(axis=1, keepdims=True)
    flp = np.divide(flp, tot, out=np.zeros_like(flp), where=tot > 0)
    ok = ((m.wfir_expb > 0) & (m.wfir_ealb > 0)).to_numpy()
    nri_rate = (m.wfir_ealb / m.wfir_expb).to_numpy()

    table, fac = derive.wrc(), derive.factors()
    alt = {}
    for r in derive.read(f"BUILDING_FACTOR_TABLE_{TAG}.csv"):
        if r["role"] == "sensitivity":
            alt.setdefault(r["reference_building_id"], []).append(float(r["factor_on_house_curve"]))
    head = ["reference_building_id", "variant", "n_cells", "ours_median_pct_per_year", "nri_median_pct_per_year",
            "ours_over_nri_median", "ours_over_nri_p10", "ours_over_nri_p90", "ours_over_nri_national",
            "spearman_rank_corr", "mean_conditional_dr"]
    out = [head]
    summary = {}
    for b in derive.BUILDINGS:
        variants = [("proposal: shrub with burnable-pixel rate (Hazard production)", table["shrub"], fac[b], "lambda_burnable"),
                    ("shrub with all-pixel rate (Hazard diagnostic)", table["shrub"], fac[b], "lambda_all_pixel"),
                    ("lifeform tree", table["tree"], fac[b], "lambda_burnable"),
                    ("lifeform grass/herbaceous", table["grass"], fac[b], "lambda_burnable")]
        variants += [(f"factor {f:.1f}", table["shrub"], f, "lambda_burnable") for f in alt.get(b, [])]
        for name, values, f, lam_col in variants:
            dr = np.array(derive.curve(values, f)[1:])
            e = flp @ dr
            rate = m[lam_col].to_numpy(float) * e
            ratio = rate[ok] / nri_rate[ok]
            national = float((rate[ok] * m.wfir_expb.to_numpy()[ok]).sum() / m.wfir_ealb.to_numpy()[ok].sum())
            rho = float(pd.Series(rate[ok]).rank().corr(pd.Series(nri_rate[ok]).rank()))
            out.append([b, name, int(ok.sum()), f"{np.median(rate[ok]) * 100:.5f}", f"{np.median(nri_rate[ok]) * 100:.5f}",
                        f"{np.median(ratio):.2f}", f"{np.percentile(ratio, 10):.2f}", f"{np.percentile(ratio, 90):.2f}",
                        f"{national:.2f}", f"{rho:.3f}", f"{e[ok].mean():.3f}"])
            if name.startswith("proposal"):
                summary[b] = {"median_ratio": round(float(np.median(ratio)), 2), "national_ratio": round(national, 2)}
    with open(PROP / f"NRI_CHECK_{TAG}.csv", "w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(out)
    receipt = {
        "check": "wildfire_real_estate model v0.1 vs FEMA NRI Dec 2025 (order of magnitude; not calibration)",
        "inputs": {
            "hazard_m1": {"gcs_uri": M1_URI, "sha256": m1_sha, "rows": int(len(m1)),
                          "pinned_by": "Hazard data/wildfire/runtime_inputs/version_1/manifest.json (main 08748ae5)"},
            "nri": {"gcs_uri": NRI_URI, "sha256": sha256(a.nri)},
            "ordinates": {"path": f"docs/cells/{CELL_ID}/proposed/CURVE_ORDINATES_{TAG}.csv",
                          "sha256": sha256(PROP / f"CURVE_ORDINATES_{TAG}.csv")},
        },
        "hazard_rule": {"rate": "lambda = -ln(1 - BP), burnable-pixel policy (production); all-pixel as diagnostic",
                        "severity": "FLP1-6 conditional mix renormalised to 1", "coupling": "p_hit = 1"},
        "cells": {"compared": int(ok.sum()), "total": int(len(m))},
        "hazard_lambda_burnable": {"median": float(np.median(m.lambda_burnable)),
                                   "exposure_weighted": float((m.lambda_burnable * m.wfir_expb.fillna(0)).sum() / m.wfir_expb.fillna(0).sum())},
        "hazard_lambda_all_pixel": {"median": float(np.median(m.lambda_all_pixel))},
        "proposal_summary": summary,
    }
    (PROP / f"NRI_CHECK_RECEIPT_{TAG}.json").write_text(json.dumps(receipt, indent=2) + "\n")
    for r in out[1:]:
        print(r[0], "|", r[1], "| median", r[5], "| national", r[8], "| rho", r[9], "| E[DR]", r[10])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
