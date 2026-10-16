"""NFIP claims check for the noncanonical flood × real estate model-v0.1 proposal.

Compares the proposed curves with paid NFIP building claims (OpenFEMA NfipClaims v3) for one-floor slab
buildings that resemble the three reference buildings. It is a comparison, not a calibration: the curves are
not changed by it.

    python scripts/reference_helpers/flood_real_estate_nfip_claims_check.py fetch   [--cache build/nfip_claims]
    python scripts/reference_helpers/flood_real_estate_nfip_claims_check.py compare [--cache build/nfip_claims]

`fetch` pages the public OpenFEMA API (about 60 MB) into the cache directory (gitignored `build/`).
`compare` reads the cache and the proposed artifact and writes, inside the cell's `proposed/` folder, the
band comparison CSV, the sensitivity CSV and the pull manifest, plus the chart in `previews/`.
Needs numpy and matplotlib.
"""
import argparse
import csv
import datetime
import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CELL = ROOT / "docs/cells/flood_real_estate"
TAG = "flood_real_estate__model_v0_1__docs_r1"
ARTIFACT = CELL / "proposed" / f"{TAG}__curve_artifact.json"
OUT_BANDS = CELL / "proposed" / f"NFIP_CLAIMS_COMPARISON_{TAG}.csv"
OUT_SENS = CELL / "proposed" / f"NFIP_CLAIMS_SENSITIVITY_{TAG}.csv"
OUT_MANIFEST = CELL / "proposed" / f"NFIP_CLAIMS_PULL_MANIFEST_{TAG}.json"
OUT_CHART = CELL / "previews" / "flood_real_estate_v0_1_nfip_claims_check.png"

API = "https://www.fema.gov/api/open/v3/NfipClaims"
FIELDS = ("id,occupancyType,foundationType,numberOfFloorsInTheInsuredBuilding,buildingDescriptionCode,causeOfDamage,"
          "ratedFloodZone,floodZoneCurrent,yearOfLoss,state,exteriorWaterDepth,interiorWaterDepth,waterDepth,"
          "lowestAdjacentGrade,lowestFloorElevation,elevatedBuildingIndicator,buildingDamageAmount,buildingPropertyValue,"
          "buildingReplacementCost,replacementCostBasis,floodWaterDuration,postFIRMConstructionIndicator")
ONE_FLOOR_SLAB = "numberOfFloorsInTheInsuredBuilding eq 1 and foundationType eq '1' and exteriorWaterDepth gt 0"
PULLS = {
    # occupancy 1/11 = single-family residential; 4/6/18 = non-residential (business and other)
    "house": f"(occupancyType eq 1 or occupancyType eq 11) and {ONE_FLOOR_SLAB} and buildingDamageAmount gt 0",
    "nonres": f"(occupancyType eq 4 or occupancyType eq 6 or occupancyType eq 18) and {ONE_FLOOR_SLAB} and buildingDamageAmount gt 0",
    "house_zero": f"(occupancyType eq 1 or occupancyType eq 11) and {ONE_FLOOR_SLAB} and buildingDamageAmount eq 0",
}

FRESH, COAST = "freshwater_riverine_or_pluvial", "coastal_surge_saline"
# NFIP causeOfDamage: 1 tidal water overflow, 2 stream/river/lake overflow, 4 accumulation of rainfall or snowmelt
CAUSE_TO_WATER = {"1": COAST, "2": FRESH, "4": FRESH}
# analogue -> (pull, filter, reference building in the artifact, reference first-floor height ft)
ANALOGUES = {
    "house": ("house", lambda r: r.get("buildingDescriptionCode") in (1, None), "RE_RES_SFD_1S_SLAB", 0.75),
    "commercial": ("nonres", lambda r: r.get("buildingDescriptionCode") in (1, 8, None) and r.get("occupancyType") in (6, 18),
                   "RE_COM_LOWRISE", 0.25),
    "warehouse": ("nonres", lambda r: r.get("buildingDescriptionCode") == 5, "RE_IND_WAREHOUSE", 0.25),
}
BINS = [0, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 15, 24]
MIN_BAND = 20
NORTHEAST = {"ME", "NH", "MA", "RI", "CT", "NY", "NJ", "PA", "DE", "MD", "VA", "DC"}
GULF = {"TX", "LA", "MS", "AL", "FL"}


def fetch(cache: Path) -> None:
    cache.mkdir(parents=True, exist_ok=True)
    for name, flt in PULLS.items():
        rows, skip = [], 0
        while True:
            q = urllib.parse.urlencode({"$filter": flt, "$select": FIELDS, "$top": 10000, "$skip": skip, "$orderby": "id"})
            with urllib.request.urlopen(f"{API}?{q}", timeout=300) as r:
                page = json.load(r)["NfipClaims"]
            rows += page
            skip += len(page)
            print(name, "fetched", len(rows), flush=True)
            if len(page) < 10000:
                break
            time.sleep(1)
        (cache / f"{name}.json").write_text(json.dumps(rows))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (cache / "retrieved_at.txt").write_text(stamp + "\n")
    print("done", stamp)


def compare(cache: Path) -> None:
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    recs = json.loads(ARTIFACT.read_text())["pathways"][0]["curve_records"]

    def curve(building, water, band="point"):
        r = next(r for r in recs if r["selector_match"]["reference_building_id"] == building
                 and r["selector_match"]["flood_water_type"] == water and r["selector_match"]["band"] == band)
        p = np.array(r["parameters"]["points"])
        lo, hi = r["valid_range"]

        def f(x):
            x = np.asarray(x, float)
            y = np.where(x < lo, 0.0, np.interp(x, p[:, 0], p[:, 1]))
            return np.where(x > hi, np.nan, y)  # above the published range: withheld
        return f

    def water_of(r):
        if (r.get("ratedFloodZone") or "").startswith("V"):
            return None  # wave zones excluded: the still-water curves do not cover wave damage
        return CAUSE_TO_WATER.get(r.get("causeOfDamage"))

    pulls = {n: json.loads((cache / f"{n}.json").read_text()) for n in PULLS}
    usable = lambda r: (r.get("buildingReplacementCost") or 0) > 0

    def depth_and_dr(S, ffh):
        x = np.array([r["exteriorWaterDepth"] / 12 - ffh for r in S])  # inches above grade -> ft above floor
        dr = np.clip(np.array([r["buildingDamageAmount"] / r["buildingReplacementCost"] for r in S]), 0, 1)
        return x, dr

    head = ["analogue", "water_type", "depth_band_ft", "n_claims", "claims_median_dr", "claims_mean_dr",
            "curve_mean_dr_same_claims", "curve_minus_claims_mean", "naccs_min_mean", "naccs_max_mean",
            "fema_freshwater_curve_mean_dr", "fema_freshwater_minus_claims_mean"]
    bands, totals = [head], {}
    for g, (pull, keep, building, ffh) in ANALOGUES.items():
        R = [r for r in pulls[pull] if keep(r) and usable(r)]
        fresh_curve = curve(building, FRESH)
        for water in (FRESH, COAST):
            S = [r for r in R if water_of(r) == water]
            x, dr = depth_and_dr(S, ffh)
            pred = curve(building, water)(x)
            ok = ~np.isnan(pred)
            totals[(g, water)] = (len(S), int(ok.sum()))
            lo_f = curve(building, water, "lower_bound") if water == COAST else None
            hi_f = curve(building, water, "upper_bound") if water == COAST else None
            for a, b in zip(BINS, BINS[1:]):
                m = ok & (x >= a) & (x < b)
                if m.sum() < MIN_BAND:
                    continue
                fema = fresh_curve(x[m]) if water == COAST else None
                bands.append([g, water, f"{a:g}-{b:g}", int(m.sum()), round(float(np.median(dr[m])), 3),
                              round(float(dr[m].mean()), 3), round(float(pred[m].mean()), 3),
                              round(float(pred[m].mean() - dr[m].mean()), 3),
                              round(float(lo_f(x[m]).mean()), 3) if lo_f else "",
                              round(float(hi_f(x[m]).mean()), 3) if hi_f else "",
                              round(float(np.nanmean(fema)), 3) if fema is not None else "",
                              round(float(np.nanmean(fema) - dr[m].mean()), 3) if fema is not None else ""])
    with OUT_BANDS.open("w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(bands)

    # sensitivity: house only (largest sample)
    _, keep, building, ffh = ANALOGUES["house"]
    H = [r for r in pulls["house"] if keep(r) and usable(r)]
    Z = [r for r in pulls["house_zero"] if keep(r) and usable(r)]
    sens = [["analogue", "water_type", "variant", "depth_band_ft", "n_claims", "claims_mean_dr", "curve_mean_dr"]]

    def add(S, water, variant, ffh_used=ffh):
        x, dr = depth_and_dr(S, ffh_used)
        pred = curve(building, water)(x)
        for a, b in [(0, 1), (1, 3), (3, 6)]:
            m = (x >= a) & (x < b) & ~np.isnan(pred)
            if m.sum() >= 15:
                sens.append(["house", water, variant, f"{a}-{b}", int(m.sum()), round(float(dr[m].mean()), 3),
                             round(float(pred[m].mean()), 3)])
    for water in (FRESH, COAST):
        S = [r for r in H if water_of(r) == water]
        add(S, water, "baseline")
        add(S + [r for r in Z if water_of(r) == water], water, "including zero-damage claims")
        add([r for r in S if r.get("replacementCostBasis") == "R"], water, "settled at replacement cost")
        add([r for r in S if r.get("replacementCostBasis") == "A"], water, "settled at actual cash value")
        add([r for r in S if r.get("state") in NORTHEAST], water, "Northeast states (NACCS study region)")
        add([r for r in S if r.get("state") in GULF], water, "Gulf states")
        # first-floor height: claims 0.5-2.0 ft above grade, curve evaluated at several assumed heights
        shallow = [r for r in S if 6 <= r["exteriorWaterDepth"] <= 24]
        g_ft = np.array([r["exteriorWaterDepth"] / 12 for r in shallow])
        dr = np.clip(np.array([r["buildingDamageAmount"] / r["buildingReplacementCost"] for r in shallow]), 0, 1)
        for h in (0.0, 0.25, 0.75, 1.0):
            sens.append(["house", water, f"floor height {h:g} ft", "0.5-2.0 above grade", len(shallow),
                         round(float(dr.mean()), 3), round(float(np.nanmean(curve(building, water)(g_ft - h))), 3)])
    with OUT_SENS.open("w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(sens)

    retrieved = (cache / "retrieved_at.txt").read_text().strip()
    manifest = {
        "source": "OpenFEMA FIMA NFIP Redacted Claims, dataset NfipClaims version 3",
        "api": API, "retrieved_at_utc": retrieved,
        "pulls": {n: {"filter": PULLS[n], "records": len(pulls[n]),
                      "sha256_of_cached_json": hashlib.sha256((cache / f"{n}.json").read_bytes()).hexdigest()}
                  for n in PULLS},
        "year_of_loss_range": [min(r["yearOfLoss"] for n in ("house", "nonres") for r in pulls[n]),
                               max(r["yearOfLoss"] for n in ("house", "nonres") for r in pulls[n])],
        "analogue_claims_compared": {f"{g}|{w}": {"claims": n, "within_curve_range": k} for (g, w), (n, k) in totals.items()},
        "exclusions": ["V-zone (wave) claims", "cause of damage other than tidal overflow, river overflow or rainfall",
                       "zero or missing building replacement cost", f"depth bands with fewer than {MIN_BAND} claims"],
        "damage_ratio": "buildingDamageAmount / buildingReplacementCost, clipped to [0, 1]",
        "depth": "exteriorWaterDepth (inches above grade) / 12 minus the reference first-floor height",
        "artifact_sha256": hashlib.sha256(ARTIFACT.read_bytes()).hexdigest(),
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")

    rows = list(csv.DictReader(OUT_BANDS.open()))
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
    for ax, g in zip(axes, ANALOGUES):
        for w, col, lab in [(FRESH, "#2563eb", "freshwater"), (COAST, "#ea580c", "coastal surge")]:
            R = [r for r in rows if r["analogue"] == g and r["water_type"] == w]
            if not R:
                continue
            mid = [sum(map(float, r["depth_band_ft"].split("-"))) / 2 for r in R]
            ax.plot(mid, [float(r["claims_mean_dr"]) for r in R], "o-", color=col, lw=2, label=f"NFIP claims, {lab}")
            ax.plot(mid, [float(r["curve_mean_dr_same_claims"]) for r in R], "s--", color=col, lw=1.4, alpha=.8,
                    label=f"proposed curve, {lab}")
            for m, r in zip(mid, R):
                ax.annotate(r["n_claims"], (m, float(r["claims_mean_dr"])), fontsize=6, color=col, xytext=(2, 4),
                            textcoords="offset points")
        ax.set_title(g)
        ax.set_xlabel("water depth above first floor (ft), band midpoint")
        ax.grid(alpha=.3)
        ax.legend(fontsize=7)
    axes[0].set_ylabel("mean damage ratio (building damage / replacement cost)")
    y0, y1 = manifest["year_of_loss_range"]
    fig.suptitle(f"NFIP claims {y0}–{y1} (v3, one floor, slab, V zones excluded) vs proposed flood_real_estate curves"
                 " — numbers = claims per band", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT_CHART, dpi=130)
    print("wrote", OUT_BANDS.name, OUT_SENS.name, OUT_MANIFEST.name, OUT_CHART.name)
    for (g, w), (n, k) in totals.items():
        print(f"  {g:10} {w:32} claims {n:6}  within range {k:6}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("step", choices=["fetch", "compare"])
    ap.add_argument("--cache", type=Path, default=ROOT / "build/nfip_claims")
    a = ap.parse_args()
    fetch(a.cache) if a.step == "fetch" else compare(a.cache)
