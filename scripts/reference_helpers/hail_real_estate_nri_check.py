"""Order-of-magnitude check of the hail × real estate model-v0.1 curves against FEMA's National Risk Index.

Read-only research check (not a calibration, not a runtime path). For every CONUS 0.25° cell it computes the expected
yearly building loss (% of structure replacement cost new) of each reference building from Hazard's MRMS daily
native-pixel evidence and compares it with NRI's hail building expected-annual-loss rate (EAL / exposed building value).
It follows Hazard's per-pixel rule for a building placed at a uniformly random pixel of the cell
(native_response.py: damage = 1[raw MESH >= 25.4 mm] x d(MESH75(raw)), MESH75 = 15.096 x ((raw/2.54)^2)^0.206):
    yearly loss = (1 / years) * sum over severe cell-days of (n_severe_pixels / n_pixels) * E_q[ DR(MESH75(Q_day(q))) ]
where Q_day is the day's raw-MESH quantile function over its severe pixels, built from the five values Hazard keeps
(25.4 mm at q = 0, p50, p90, p95, maximum at q = 1; straight lines between them; raw capped at 203.2 mm).
This uses the raw five-and-a-half-year MRMS record, not Hazard's pooled M1 frequency and size model.
Building DR = sum over units of unit DR x unit share of structure value (roof cover; walls and windows).

Variants: central roof cover; central roof + walls and windows (T4); roof low and high cases (SENSITIVITY); and the
earlier Hazard size transform (raw x 25.4/35.56, Hazard Version 1) for the central roof, to show the axis sensitivity.

Inputs outside this repository (SHA-256 recorded in the receipt):
    --hazard-repo  a Hazard_Modeling checkout holding data/hazard_conus_grid/hail/v1_mrms_only/ (the M0 reconciled daily
                   cell evidence run 20260616T225000Z_m0_full_conus_reconciled and the M1 QC table run
                   20260625_m1_mrms_only_qcd; both also on GCS under gs://infrasure-benchmark/hazard_conus_grid/dev/hail/)
    --nri          the Hazard team's NRI Dec 2025 CONUS parquet keyed by cell_id (gs://infrasure-benchmark/
                   hazard_conus_grid/dev/reference/nri/nri_dec2025/raw/run_id=20260706T184931Z_nri_reference/
                   nri_raw_conus.parquet)
Writes NRI_CHECK_<tag>.csv and NRI_CHECK_RECEIPT_<tag>.json in the cell's proposed/ folder.
Needs numpy, pandas, scipy (pyarrow for parquet).

    python scripts/reference_helpers/hail_real_estate_nri_check.py --hazard-repo <path> --nri <parquet>
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
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import derive_hail_real_estate_curves as derive  # noqa: E402

CELL_ID = "hail_real_estate"
PROP = ROOT / f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
M0 = "data/hazard_conus_grid/hail/v1_mrms_only/m0_reconciled_daily_cell_evidence/run_id=20260616T225000Z_m0_full_conus_reconciled"
M1 = ("data/hazard_conus_grid/hail/v1_mrms_only/m1_hazard_layer/run_id=20260625_m1_mrms_only_qcd/tables/"
      "mrms_v1_m1_hazard_layer_20260625_m1_mrms_only_qcd.parquet")
GCS = "gs://infrasure-benchmark/hazard_conus_grid/dev/hail/v1_mrms_only/"
SEVERE, CAP, ARTIFACT_MM = 25.4, 203.2, 300.0
N_Q = 200
Q = (np.arange(N_Q) + 0.5) / N_Q
BUILDINGS = derive.BUILDINGS
ROOF, WALLS = derive.ROOF, derive.WALLS


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mesh75(raw: np.ndarray) -> np.ndarray:
    return np.minimum(15.096 * ((raw / 2.54) ** 2) ** 0.206, CAP)


def v1_scale(raw: np.ndarray) -> np.ndarray:
    return np.minimum(raw * 25.4 / 35.56, CAP)


def governed_curves() -> dict[tuple[str, str], tuple[np.ndarray, np.ndarray]]:
    pts: dict[tuple[str, str], list[tuple[float, float]]] = {}
    with open(PROP / f"CURVE_ORDINATES_{TAG}.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            pts.setdefault((r["reference_building_id"], r["failure_unit_id"]), []).append(
                (float(r["mesh_diameter_mm"]), float(r["damage_ratio"])))
    return {k: (np.array([p[0] for p in sorted(v)]), np.array([p[1] for p in sorted(v)])) for k, v in pts.items()}


def load_days(m0: Path, eligible: set[int]) -> pd.DataFrame:
    cols = ["cell_id", "n_native_pixels_observed", "n_native_pixels_severe", "mesh_max_mm", "mesh_p50_severe_mm",
            "mesh_p90_severe_mm", "mesh_p95_severe_mm"]
    frames = []
    for part in sorted(m0.glob("date=*/part-000.parquet")):
        d = pd.read_parquet(part, columns=cols)
        d = d[(d.n_native_pixels_severe > 0) & d.cell_id.isin(eligible)]
        if len(d):
            frames.append(d)
    return pd.concat(frames, ignore_index=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hazard-repo", required=True, type=Path)
    ap.add_argument("--nri", required=True, type=Path)
    a = ap.parse_args()
    hz = a.hazard_repo.resolve()
    m1 = pd.read_parquet(hz / M1)
    years = float(m1.observed_years.iloc[0])
    elig = m1[m1.reportable_loss_eligible & ~m1.hard_artifact_flag]
    eligible = set(elig.cell_id.astype(int))
    m0_dir = hz / M0
    m0_parts = sorted(m0_dir.glob("date=*/part-000.parquet"))
    n_dates = len(m0_parts)
    m0_digest = hashlib.sha256("".join(f"{q.parent.name}:{sha256(q)}\n" for q in m0_parts).encode()).hexdigest()
    days = load_days(m0_dir, eligible)
    n_artifact = int((days.mesh_max_mm >= ARTIFACT_MM).sum())
    days = days[days.mesh_max_mm < ARTIFACT_MM].reset_index(drop=True)

    # raw-MESH quantile function per severe cell-day over its severe pixels
    knots_q = np.array([0.0, 0.5, 0.9, 0.95, 1.0])
    vals = np.column_stack([np.full(len(days), SEVERE), days.mesh_p50_severe_mm, days.mesh_p90_severe_mm,
                            days.mesh_p95_severe_mm, days.mesh_max_mm]).astype(float)
    vals = np.minimum(np.maximum.accumulate(np.maximum(vals, SEVERE), axis=1), CAP)
    raw = np.empty((len(days), N_Q))
    for i in range(len(knots_q) - 1):
        sel = (Q >= knots_q[i]) & (Q < knots_q[i + 1])
        t = (Q[sel] - knots_q[i]) / (knots_q[i + 1] - knots_q[i])
        raw[:, sel] = vals[:, [i]] + (vals[:, [i + 1]] - vals[:, [i]]) * t[None, :]
    frac = (days.n_native_pixels_severe / days.n_native_pixels_observed).to_numpy()
    sizes = {"mesh75": mesh75(raw), "v1_scale": v1_scale(raw)}
    cell_idx = days.cell_id.to_numpy()

    nri = pd.read_parquet(a.nri)[["cell_id", "hail_ealb", "hail_expb"]]
    base = elig[["cell_id"]].merge(nri, on="cell_id", how="left")
    base["nri_pct"] = np.where(base.hail_expb > 0, base.hail_ealb / base.hail_expb * 100, np.nan)
    base = base[base.nri_pct > 0].reset_index(drop=True)

    table = derive.parts_table()
    cv = governed_curves()

    def yearly_pct(dr_of_size, transform: str) -> np.ndarray:
        per_day = frac * dr_of_size(sizes[transform]).mean(axis=1)
        s = pd.Series(per_day).groupby(cell_idx).sum() / years * 100
        return base.cell_id.map(s).fillna(0.0).to_numpy()

    def governed(b: str, units: list[str]):
        def f(d):
            return sum(derive.unit_value(table[(b, u)]) * np.interp(d, *cv[(b, u)]) for u in units)
        return f

    def variant(b: str, unit: str, overrides=None, value_scale=1.0):
        parts = table[(b, unit)]
        grid = np.linspace(0, CAP, 2033)
        g = np.array([derive.unit_dr(parts, x, overrides=overrides) for x in grid]) * derive.unit_value(parts, value_scale)
        return lambda d: np.interp(d, grid, g)

    R, W, O = "RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB"
    cases = []
    for b in BUILDINGS:
        cases += [(b, "central: roof cover only", governed(b, [ROOF]), "mesh75"),
                  (b, "central: roof cover + walls and windows (T4)", governed(b, [ROOF, WALLS]), "mesh75"),
                  (b, "central roof cover, Hazard Version-1 size transform (raw x 25.4/35.56)", governed(b, [ROOF]), "v1_scale")]
    cases += [
        (R, "roof low: no Hazus repair factor (3.0%)", variant(R, ROOF, value_scale=0.8), "mesh75"),
        (R, "roof high: 3-tab shingles (1.0-1.75 in)", variant(R, ROOF, {"ROOF_ASPHALT_SHINGLE_LAMINATED": {"onset_in": 1.0, "full_in": 1.75}}), "mesh75"),
        (W, "roof low: full at 4.0 in, 9%", variant(W, ROOF, {"ROOF_STANDING_SEAM_STEEL": {"full_in": 4.0}}, 0.75), "mesh75"),
        (W, "roof high: full at 3.0 in, 15%", variant(W, ROOF, {"ROOF_STANDING_SEAM_STEEL": {"full_in": 3.0}}, 1.25), "mesh75"),
        (W, "roof alternative not adopted: cosmetic denting (1.5-2.5 in)", variant(W, ROOF, {"ROOF_STANDING_SEAM_STEEL": {"onset_in": 1.5, "full_in": 2.5}}), "mesh75"),
        (O, "roof low: adhered on cover board (1.5-2.0 in), membrane only", variant(O, ROOF, {"ROOF_TPO_MEMBRANE_AND_INSULATION": {"onset_in": 1.5, "full_in": 2.0}}, 1.1 / 1.8), "mesh75"),
        (O, "roof high: 1.0-1.5 in", variant(O, ROOF, {"ROOF_TPO_MEMBRANE_AND_INSULATION": {"onset_in": 1.0, "full_in": 1.5}}), "mesh75"),
    ]
    ref = base.nri_pct.to_numpy()
    rows = []
    for b, name, f, tr in cases:
        ours = yearly_pct(f, tr)
        pos = ours > 0
        ratio = ours[pos] / ref[pos]
        rows.append({"reference_building_id": b, "variant": name, "n_cells": int(len(ours)), "n_cells_nonzero": int(pos.sum()),
                     "ours_median_pct_per_year": f"{np.median(ours):.5f}", "ours_p90_pct_per_year": f"{np.quantile(ours, .9):.5f}",
                     "nri_median_pct_per_year": f"{np.median(ref):.5f}",
                     "ours_over_nri_median": f"{np.median(ratio):.2f}" if pos.any() else "",
                     "ours_over_nri_p10": f"{np.quantile(ratio, .1):.2f}" if pos.any() else "",
                     "ours_over_nri_p90": f"{np.quantile(ratio, .9):.2f}" if pos.any() else "",
                     "spearman_rank_corr": f"{spearmanr(ours, ref).statistic:.3f}"})
    with open(PROP / f"NRI_CHECK_{TAG}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    # context: point frequency of severe hail and the house roof replacement rate
    point_rate = pd.Series(frac).groupby(cell_idx).sum() / years
    pr = base.cell_id.map(point_rate).fillna(0.0)
    house_roof = yearly_pct(governed(R, [ROOF]), "mesh75") / 100 / derive.unit_value(table[(R, ROOF)])
    plains = base.cell_id.isin(elig[elig.state_abbr.isin(["TX", "OK", "KS", "NE", "CO", "SD"])].cell_id)
    receipt = {
        "check": "hail_real_estate model v0.1 vs FEMA NRI Dec 2025 (order of magnitude; not calibration)",
        "inputs": {
            "hazard_m0_daily_evidence": {"gcs_uri": GCS + M0.split("v1_mrms_only/")[1], "dates": n_dates,
                                         "partitions_digest_sha256": m0_digest,
                                         "partitions_digest_rule": "sha256 of 'date=YYYY-MM-DD:<sha256 of part-000.parquet>' lines, sorted by date",
                                         "severe_cell_days_used": int(len(days)),
                                         "severe_cell_days_dropped_max_ge_300mm": n_artifact},
            "hazard_m1_qc_table": {"gcs_uri": GCS + M1.split("v1_mrms_only/")[1], "sha256": sha256(hz / M1),
                                   "observed_years": round(years, 6), "cells_eligible": len(eligible)},
            "nri": {"gcs_uri": "gs://infrasure-benchmark/hazard_conus_grid/dev/reference/nri/nri_dec2025/raw/"
                               "run_id=20260706T184931Z_nri_reference/nri_raw_conus.parquet", "sha256": sha256(a.nri)},
            "ordinates": {"path": f"docs/cells/{CELL_ID}/proposed/CURVE_ORDINATES_{TAG}.csv",
                          "sha256": sha256(PROP / f"CURVE_ORDINATES_{TAG}.csv")},
        },
        "method": {"pixel_rule": "1[raw >= 25.4 mm] x DR(MESH75(raw)); building at a uniformly random native pixel",
                   "quantile_points": "25.4 mm (q=0), p50, p90, p95, max (q=1) of the day's severe pixels; linear between",
                   "raw_cap_mm": CAP, "cell_eligibility": "M1 QC reportable_loss_eligible and not hard_artifact_flag"},
        "cells": {"compared": int(len(base)), "plains_compared": int(plains.sum())},
        "point_severe_hail_days_per_year": {"median": round(float(pr.median()), 4), "p90": round(float(pr.quantile(.9)), 4),
                                            "plains_median": round(float(pr[plains].median()), 4)},
        "house_roof_replacements_per_year": {"median": round(float(np.median(house_roof)), 5),
                                             "p90": round(float(np.quantile(house_roof, .9)), 5),
                                             "plains_median": round(float(np.median(house_roof[plains.to_numpy()])), 5)},
        "mesh75_at_threshold_mm": round(float(mesh75(np.array([SEVERE]))[0]), 2),
    }
    (PROP / f"NRI_CHECK_RECEIPT_{TAG}.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(pd.DataFrame(rows).to_string(index=False))
    print(json.dumps({k: receipt[k] for k in ("cells", "point_severe_hail_days_per_year", "house_roof_replacements_per_year")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
