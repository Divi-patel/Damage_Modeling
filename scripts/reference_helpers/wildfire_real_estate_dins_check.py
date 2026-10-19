"""CAL FIRE damage-inspection (DINS) evidence for the wildfire × real estate model-v0.1 building factors.

Reads the public CAL FIRE Damage Inspection (DINS) master table (CSV export) and writes, in the cell's proposed/
folder:
    DINS_BUILDING_COMPARISON_<tag>.csv      damage-band shares per comparison group and the warehouse/office ratios
    DINS_CHECK_RECEIPT_<tag>.json           input file hash, row counts and group definitions

Comparison groups (decision log D-WFRE-07):
    house           single-family one-storey residence, wood / vinyl / combustible siding, asphalt roof
    warehouse_like  commercial building (one or more storeys), metal siding and metal roof
    office_like     commercial building multi-storey, stucco / brick / cement siding
A record's damage band is read as a damage ratio at the band midpoint (Affected 5%, Minor 17.5%, Major 37.5%) and
Destroyed (>50%) at 100% (75% as an alternative column); "Inaccessible" records are dropped.

Ratios to the house:
    pooled      mean damage of the group / mean damage of houses, all fires together (sensitive to which fires
                hit which buildings)
    same_fire   only fires with at least one group record and at least 10 house records; each fire's house mean is
                weighted by the group's record count in that fire; 90% interval from 5,000 bootstrap draws of fires
                (seed 20261018)
It is evidence for a ratio between building types in the same fire, not a calibration of the curve level.

Usage (from the repository root; needs pandas and numpy):
    python scripts/reference_helpers/wildfire_real_estate_dins_check.py --dins <dins_master.csv>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CELL_ID = "wildfire_real_estate"
PROP = ROOT / f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
SOURCE_URL = ("https://gis.data.cnra.ca.gov/api/download/v1/items/994d3dc4569640caadbbc3198d5a3da1/csv?layers=0")
BANDS = ["No Damage", "Affected (>0-10%)", "Minor (10-25%)", "Major (25-50%)", "Destroyed (>50%)"]
MID = {"No Damage": 0.0, "Affected (>0-10%)": 0.05, "Minor (10-25%)": 0.175, "Major (25-50%)": 0.375,
       "Destroyed (>50%)": 1.0}
SEED, DRAWS, MIN_HOUSE_PER_FIRE = 20261018, 5000, 10
GROUP_TEXT = {
    "house": "Structure Type 'Single Family Residence Single Story'; Exterior Siding Wood, Vinyl or Combustible; Roof Construction Asphalt",
    "warehouse_like": "Structure Type 'Commercial Building Single Story' or 'Multi Story'; Exterior Siding Metal; Roof Construction Metal",
    "office_like": "Structure Type 'Commercial Building Multi Story'; Exterior Siding Stucco Brick Cement",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    counts = {"rows": int(len(df)), "inaccessible_dropped": int((df["* Damage"] == "Inaccessible").sum())}
    df = df[df["* Damage"].isin(BANDS)].copy()
    st = df["* Structure Type"].fillna("").str.strip()
    sid = df["* Exterior Siding"].fillna("").str.strip()
    roof = df["* Roof Construction"].fillna("").str.strip()
    df["group"] = ""
    df.loc[st.str.startswith("Single Fam") & st.str.endswith("Single Story") & sid.isin(["Wood", "Vinyl", "Combustible"])
           & (roof == "Asphalt"), "group"] = "house"
    df.loc[st.str.startswith("Commercial Building") & (sid == "Metal") & (roof == "Metal"), "group"] = "warehouse_like"
    df.loc[(st == "Commercial Building Multi Story") & sid.str.startswith("Stucco"), "group"] = "office_like"
    df["dr"] = df["* Damage"].map(MID)
    df["dr75"] = df["dr"].where(df["* Damage"] != "Destroyed (>50%)", 0.75)
    df["fire"] = df["* Incident Name"].fillna("") + " | " + df["Incident Start Date"].fillna("").str[:10]
    df["year"] = pd.to_datetime(df["Incident Start Date"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce").dt.year
    counts["rows_used"] = int(len(df))
    counts["fires"] = int(df["fire"].nunique())
    counts["years"] = [int(df["year"].min()), int(df["year"].max())]
    return df, counts


def same_fire(df: pd.DataFrame, group: str) -> tuple[float, float, float, int, int]:
    g = df[df.group == group].groupby("fire")["dr"].agg(["mean", "size"])
    h = df[df.group == "house"].groupby("fire")["dr"].agg(["mean", "size"])
    j = g.join(h, lsuffix="_g", rsuffix="_h", how="inner")
    j = j[j["size_h"] >= MIN_HOUSE_PER_FIRE]
    w, mg, mh = j["size_g"].to_numpy(float), j["mean_g"].to_numpy(), j["mean_h"].to_numpy()
    point = float((mg * w).sum() / (mh * w).sum())
    rng = np.random.default_rng(SEED)
    draws = []
    for _ in range(DRAWS):
        i = rng.integers(0, len(j), len(j))
        den = (mh[i] * w[i]).sum()
        if den > 0:
            draws.append((mg[i] * w[i]).sum() / den)
    p05, p95 = np.percentile(draws, [5, 95])
    return point, float(p05), float(p95), int(w.sum()), int(len(j))


def table(df: pd.DataFrame) -> list[list]:
    head = ["section", "subset", "group", "n_buildings", "n_fires", "no_damage", "affected", "minor", "major",
            "destroyed", "destroyed_given_any_damage", "mean_dr_destroyed_100", "mean_dr_destroyed_75",
            "ratio_to_house", "ratio_p05", "ratio_p95"]
    out = [head]
    f4 = lambda v: f"{v:.4f}"  # noqa: E731
    subsets = {
        "all fires": df.index == df.index,
        "fires recording at least 20% no-damage": df.groupby("fire")["* Damage"].transform(lambda s: (s == "No Damage").mean()) >= 0.2,
        "excluding 2025 Eaton and Palisades fires": df["year"] != 2025,
        "excluding Camp 2018": ~df["* Incident Name"].fillna("").eq("Camp"),
    }
    for name, m in subsets.items():
        sub = df[m]
        house = sub[sub.group == "house"]["dr"].mean()
        for g in ("house", "warehouse_like", "office_like"):
            s = sub[sub.group == g]
            sh = s["* Damage"].value_counts(normalize=True)
            dmg = (s["* Damage"] != "No Damage").sum()
            row = ["band_shares_and_pooled_ratio", name, g, len(s), s["fire"].nunique()]
            row += [f4(sh.get(b, 0.0)) for b in BANDS]
            row += [f4((s["* Damage"] == BANDS[-1]).sum() / dmg) if dmg else "", f4(s["dr"].mean()), f4(s["dr75"].mean()),
                    f4(s["dr"].mean() / house), "", ""]
            out.append(row)
    for g in ("warehouse_like", "office_like"):
        point, p05, p95, n, nf = same_fire(df, g)
        out.append(["same_fire_ratio", f"fires with >=1 {g} and >={MIN_HOUSE_PER_FIRE} house records", g, n, nf]
                   + [""] * 8 + [f4(point), f4(p05), f4(p95)])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dins", required=True, type=Path)
    a = ap.parse_args()
    df, counts = load(a.dins)
    rows = table(df)
    with open(PROP / f"DINS_BUILDING_COMPARISON_{TAG}.csv", "w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)
    receipt = {
        "check": "CAL FIRE DINS building-type comparison for wildfire_real_estate model v0.1 (evidence for the building factors; not a calibration)",
        "input": {"source_url": SOURCE_URL, "dataset": "CAL FIRE Damage Inspection (DINS) Data, master table, CSV export",
                  "catalog_metadata_modified": "2026-02-04", "downloaded_on": "2026-10-18",
                  "bytes": a.dins.stat().st_size, "sha256": sha256(a.dins)},
        "counts": counts,
        "group_sizes": {g: int((df.group == g).sum()) for g in GROUP_TEXT},
        "group_definitions": GROUP_TEXT,
        "damage_ratio_reading": {**MID, "Destroyed (>50%) alternative": 0.75},
        "same_fire_rule": {"min_house_records_per_fire": MIN_HOUSE_PER_FIRE, "bootstrap_draws": DRAWS, "seed": SEED,
                           "fire_key": "incident name + start date"},
    }
    (PROP / f"DINS_CHECK_RECEIPT_{TAG}.json").write_text(json.dumps(receipt, indent=2) + "\n")
    for r in rows[1:]:
        if r[0] == "same_fire_ratio" or r[1] == "all fires":
            print(r[2], r[0], "n", r[3], "fires", r[4], "ratio", r[13], r[14:16])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
