"""Derive the convective wind × real estate model-v0.1 curves from the governed EF degree-of-damage table.

Reads   docs/cells/convective_wind_real_estate/proposed/EF_DEGREE_OF_DAMAGE_TABLE_<tag>.csv
Writes  CURVE_ORDINATES_<tag>.csv      the six records (3 buildings × 2 pathways), tabulated every 1 mph, 0-255 mph
        SENSITIVITY_<tag>.csv          damage at 80/100/120/140/160 mph under the alternative assumptions
        ../previews/convective_wind_real_estate_v0_1_curves.png   (only with --chart; needs matplotlib)

The curve (decision log D-CWRE-06 to D-CWRE-09):
    each degree of damage i has an expected gust EXP_i and a lower/upper bound LB_i, UB_i (EF scale, expert
    elicitation); the gust that causes it is read as lognormal with median EXP_i and
        beta_i = ln(UB_i / LB_i) / (2 * 1.645)          (LB-UB read as a 90% range; T4 reading, D-CWRE-06)
    each degree carries a cost ratio c_i (FEMA Hazus damage-state loss ratios, made non-decreasing):
        DR(v) = sum_i (c_i - c_{i-1}) * Phi(ln(v / EXP_i) / beta_i)            tornado_direct_hit
    straight-line wind starts from zero at the onset gust x0 = 96 mph (D-CWRE-09):
        DR_SL(v) = max(0, (DR(v) - DR(x0)) / (1 - DR(x0)))                     straight_line_convective
Values are rounded to 6 decimals; the rounded table is the governed curve. Standard library only (chart aside).

Usage (from the repository root):
    python scripts/reference_helpers/derive_convective_wind_real_estate_ef_curves.py [--chart]
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[2]
CELL_ID = "convective_wind_real_estate"
PROP = ROOT / f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
Z90 = 1.645            # LB-UB read as the 5th-95th percentile range
ONSET_MPH = 96.0       # straight-line onset gust (90% of the CONUS median ASCE 700-year gust, 107 mph)
V_MAX = 255            # tabulated range 0..255 mph (Hazard's physical bound is 252.8 mph)
DECIMALS = 6
BUILDINGS = ["RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB"]
PATHWAYS = ["straight_line_convective", "tornado_direct_hit"]
PHI = NormalDist().cdf


def dod_table() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    with open(PROP / f"EF_DEGREE_OF_DAMAGE_TABLE_{TAG}.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            out.setdefault(r["reference_building_id"], []).append(r)
    for rows in out.values():
        rows.sort(key=lambda r: int(r["dod"]))
    return out


def ef_dr(rows: list[dict], v: float, z: float = Z90, cost_override: dict[int, float] | None = None,
          minor_scale: float = 1.0) -> float:
    """Expected damage ratio at gust v (mph) before any onset."""
    if v <= 0:
        return 0.0
    total, prev = 0.0, 0.0
    for r in rows:
        c = float(r["cost_ratio"])
        if cost_override and int(r["dod"]) in cost_override:
            c = cost_override[int(r["dod"])]
        if c <= 0.05:
            c *= minor_scale
        c = max(c, prev)
        beta = math.log(float(r["upper_bound_mph"]) / float(r["lower_bound_mph"])) / (2 * z)
        total += (c - prev) * PHI(math.log(v / float(r["expected_mph"])) / beta)
        prev = c
    return total


def with_onset(f, x0: float):
    d0 = f(x0)
    return lambda v: max(0.0, (f(v) - d0) / (1.0 - d0))


def curve(rows: list[dict], pathway: str, onset: float = ONSET_MPH, **kw):
    """The pathway curve; onset applies to straight-line wind only (0 = no onset)."""
    base = lambda v: ef_dr(rows, v, **kw)  # noqa: E731
    return with_onset(base, onset) if pathway == "straight_line_convective" and onset > 0 else base


def record_id(building: str, pathway: str, rows: list[dict]) -> str:
    stem = {"RE_RES_SFD_1S_SLAB": "RES", "RE_IND_WAREHOUSE": "IND", "RE_COM_OFFICE_3S_SLAB": "OFF"}[building]
    tail = "STRAIGHT_LINE_ONSET96" if pathway == "straight_line_convective" else "TORNADO"
    return f"CWRE_{stem}_EF_{rows[0]['ef_damage_indicator']}_{tail}"


def ordinates(table) -> list[list]:
    out = [["curve_id", "reference_building_id", "pathway_id", "ef_damage_indicator", "gust_3s_10m_mph",
            "damage_ratio", "source_ids"]]
    for b in BUILDINGS:
        rows = table[b]
        for p in PATHWAYS:
            f = curve(rows, p)
            cid = record_id(b, p, rows)
            for v in range(0, V_MAX + 1):
                out.append([cid, b, p, rows[0]["ef_damage_indicator"], v, f"{round(f(float(v)), DECIMALS):.6f}",
                            "CWRE-S001;CWRE-S002;CWRE-S003"])
    return out


def sensitivity(table) -> list[list]:
    speeds = [80, 100, 120, 140, 160]
    variants = [
        ("reference", "reference", {}),
        ("bounds read as +/-1 sigma (68% range)", "spread_reading", {"z": 1.0}),
        ("bounds read as +/-1.96 sigma (95% range)", "spread_reading", {"z": 1.96}),
        ("light-damage costs (5% or less) x0.5", "cost_assumption", {"minor_scale": 0.5}),
        ("light-damage costs (5% or less) x2", "cost_assumption", {"minor_scale": 2.0}),
        ("house shifted off foundation = complete (100%)", "cost_assumption", {"cost_override": {5: 1.0}}),
        ("straight-line onset 90 mph", "onset", {"onset": 90.0}),
        ("straight-line onset 100 mph", "onset", {"onset": 100.0}),
        ("no straight-line onset", "onset", {"onset": 0.0}),
    ]
    out = [["reference_building_id", "pathway_id", "variant", "role"] + [f"dr_{s}mph" for s in speeds]]
    for b in BUILDINGS:
        rows = table[b]
        for p in PATHWAYS:
            for name, role, kw in variants:
                if "cost_override" in kw and b != "RE_RES_SFD_1S_SLAB":
                    continue
                if role == "onset" and p != "straight_line_convective":
                    continue
                f = curve(rows, p, **kw)
                out.append([b, p, name, role] + [f"{f(float(s)):.4f}" for s in speeds])
    return out


def write(name: str, data: list[list]) -> None:
    with open(PROP / name, "w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(data)


def chart(table) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    names = {"RE_RES_SFD_1S_SLAB": "House (EF FR12)", "RE_IND_WAREHOUSE": "Warehouse (EF MBS)",
             "RE_COM_OFFICE_3S_SLAB": "Office (EF LRB)"}
    vs = [v / 2 for v in range(0, 2 * V_MAX + 1)]
    for ax, b in zip(axes, BUILDINGS):
        rows = table[b]
        ax.plot(vs, [curve(rows, "tornado_direct_hit")(v) for v in vs], color="#b4462f", lw=2, label="Tornado")
        ax.plot(vs, [curve(rows, "straight_line_convective")(v) for v in vs], color="#2f6db4", lw=2,
                label="Straight-line wind (onset 96 mph)")
        for r in rows:
            ax.plot([float(r["expected_mph"])], [float(r["cost_ratio"])], "o", ms=4, color="#555")
        ax.axvline(ONSET_MPH, color="#999", lw=0.8, ls=":")
        ax.set_title(names[b])
        ax.set_xlabel("3-second gust at 10 m (mph)")
        ax.set_xlim(40, 230)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Damage ratio (fraction of structure value)")
    axes[0].legend(loc="lower right", fontsize=8)
    fig.suptitle("convective_wind_real_estate model v0.1 (proposal): EF degrees of damage (dots: expected gust, "
                 "assigned cost)", fontsize=10)
    fig.tight_layout()
    out = PROP.parent / "previews" / "convective_wind_real_estate_v0_1_curves.png"
    fig.savefig(out, dpi=110, metadata={"Software": None})
    print("wrote", out.relative_to(ROOT))


def main(argv: list[str]) -> int:
    table = dod_table()
    assert sorted(table) == sorted(BUILDINGS), sorted(table)
    write(f"CURVE_ORDINATES_{TAG}.csv", ordinates(table))
    write(f"SENSITIVITY_{TAG}.csv", sensitivity(table))
    print(f"wrote CURVE_ORDINATES_{TAG}.csv and SENSITIVITY_{TAG}.csv")
    if "--chart" in argv:
        chart(table)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
