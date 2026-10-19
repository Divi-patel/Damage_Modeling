"""Derive the hail × real estate model-v0.1 curves from the governed component fragility table.

Reads   docs/cells/hail_real_estate/proposed/COMPONENT_FRAGILITY_TABLE_<tag>.csv
Writes  CURVE_ORDINATES_<tag>.csv      six records (3 buildings × 2 failure units), knots every 1 mm, 0-203.2 mm
        SENSITIVITY_<tag>.csv          unit damage ratio and building-level % at 1-4 in under the alternatives
        ../previews/hail_real_estate_v0_1_curves.png   (only with --chart; needs matplotlib)

The curve (decision log D-HRE-04 to D-HRE-08):
    each part p (a roof cover, siding, windows) needs replacing with probability
        P_p(D) = Phi(ln(D / m_p) / beta_p),   m_p = sqrt(onset_p * full_p),   beta_p = ln(full_p / onset_p) / (2 * 1.645)
    (onset = 5%, full = 95%: the threshold band read as a 90% range; D = hailstone diameter in mm);
    a failure unit's damage ratio is the expected replaced fraction of the unit's own value:
        DR_unit(D) = sum_p (v_p / V_unit) * e_p * P_p(D),   V_unit = sum_p v_p
    with v_p the part's share of structure replacement cost new and e_p the share of the part that hail reaches
    (1 for a roof; less than 1 for walls and windows, which are hit on the hail-facing side only).
    The building-level ratio on the shared real-estate denominator is sum_units V_unit * DR_unit.
Values are rounded to 6 decimals; the rounded table is the governed curve. Standard library only (chart aside).

Usage (from the repository root):
    python scripts/reference_helpers/derive_hail_real_estate_curves.py [--chart]
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[2]
CELL_ID = "hail_real_estate"
PROP = ROOT / f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
MM_PER_IN = 25.4
Z90 = 1.645                  # onset-full read as the 5th-95th percentile band
D_MAX = 203.2                # Hazard's physical hail-size cap (mm)
KNOTS = [float(d) for d in range(0, 204)] + [D_MAX]
DECIMALS = 6
BUILDINGS = ["RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB"]
ROOF, WALLS = "HRE_ROOF_COVER", "HRE_WALLS_AND_WINDOWS"
UNITS = [ROOF, WALLS]
STEM = {"RE_RES_SFD_1S_SLAB": "RES", "RE_IND_WAREHOUSE": "IND", "RE_COM_OFFICE_3S_SLAB": "OFF"}
SIZES_IN = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0]
PHI = NormalDist().cdf


def parts_table() -> dict[tuple[str, str], list[dict]]:
    out: dict[tuple[str, str], list[dict]] = {}
    with open(PROP / f"COMPONENT_FRAGILITY_TABLE_{TAG}.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            out.setdefault((r["reference_building_id"], r["failure_unit_id"]), []).append(r)
    return out


def part_p(d_mm: float, onset_in: float, full_in: float, z: float = Z90) -> float:
    """Probability that the part needs replacing at hailstone diameter d_mm."""
    if d_mm <= 0:
        return 0.0
    lo, hi = onset_in * MM_PER_IN, full_in * MM_PER_IN
    beta = math.log(hi / lo) / (2 * z)
    return PHI(math.log(d_mm / math.sqrt(lo * hi)) / beta)


def unit_value(parts: list[dict], value_scale: float = 1.0) -> float:
    return sum(float(p["part_value_fraction_of_structure_rcn"]) for p in parts) * value_scale


def unit_dr(parts: list[dict], d_mm: float, z: float = Z90, overrides: dict[str, dict] | None = None) -> float:
    """Expected replaced fraction of the unit's own value. overrides: part_id -> {onset_in, full_in, exposure, value}."""
    overrides = overrides or {}
    vals, total = [], 0.0
    for p in parts:
        o = overrides.get(p["part_id"], {})
        v = o.get("value", float(p["part_value_fraction_of_structure_rcn"]))
        vals.append(v)
        total += v * o.get("exposure", float(p["exposure_fraction"])) * part_p(
            d_mm, o.get("onset_in", float(p["onset_in"])), o.get("full_in", float(p["full_in"])), z)
    return total / sum(vals)


def curve_id(building: str, unit: str, parts: list[dict]) -> str:
    if unit == ROOF:
        return f"HRE_{STEM[building]}_ROOF_{parts[0]['part_id'].removeprefix('ROOF_')}"
    return f"HRE_{STEM[building]}_{'WALLS_WINDOWS' if len(parts) > 1 else 'WINDOWS'}_T4"


def ordinates(table) -> list[list]:
    out = [["curve_id", "reference_building_id", "failure_unit_id", "mesh_diameter_mm", "damage_ratio", "source_ids"]]
    for b in BUILDINGS:
        for u in UNITS:
            parts = table[(b, u)]
            src = ";".join(dict.fromkeys(s for p in parts for s in p["source_ids"].split(";")))
            cid = curve_id(b, u, parts)
            for d in KNOTS:
                out.append([cid, b, u, f"{d:g}", f"{round(unit_dr(parts, d), DECIMALS):.6f}", src])
    return out


def sensitivity(table) -> list[list]:
    sizes = [s * MM_PER_IN for s in SIZES_IN]
    head = ["reference_building_id", "failure_unit_id", "variant", "role", "metric"] + [f"at_{s:g}in" for s in SIZES_IN]
    variants: list[tuple[str, str, str, str, dict]] = [  # building, unit, name, role, kwargs
        (b, u, "reference (central)", "reference", {}) for b in BUILDINGS for u in UNITS]
    for b in BUILDINGS:
        for u in UNITS:
            variants += [(b, u, "band read as +/-1 sigma (68% range)", "spread_reading", {"z": 1.0}),
                         (b, u, "band read as +/-1.96 sigma (95% range)", "spread_reading", {"z": 1.96})]
    R, W, O = "RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB"
    variants += [
        (R, ROOF, "low: no Hazus repair factor (roof 3.0%)", "low", {"value_scale": 0.8}),
        (R, ROOF, "high: 3-tab shingles (1.0-1.75 in)", "high",
         {"overrides": {"ROOF_ASPHALT_SHINGLE_LAMINATED": {"onset_in": 1.0, "full_in": 1.75}}}),
        (W, ROOF, "low: fully failed by 4.0 in, roof 9%", "low",
         {"overrides": {"ROOF_STANDING_SEAM_STEEL": {"full_in": 4.0}}, "value_scale": 0.75}),
        (W, ROOF, "high: fully failed by 3.0 in, roof 15%", "high",
         {"overrides": {"ROOF_STANDING_SEAM_STEEL": {"full_in": 3.0}}, "value_scale": 1.25}),
        (W, ROOF, "alternative: cosmetic denting counted (1.5-2.5 in)", "alternative_not_adopted",
         {"overrides": {"ROOF_STANDING_SEAM_STEEL": {"onset_in": 1.5, "full_in": 2.5}}}),
        (O, ROOF, "low: adhered TPO on cover board (1.5-2.0 in), membrane only 1.65%", "low",
         {"overrides": {"ROOF_TPO_MEMBRANE_AND_INSULATION": {"onset_in": 1.5, "full_in": 2.0}},
          "value_scale": 1.1 / 1.8}),
        (O, ROOF, "high: membrane fails 1.0-1.5 in", "high",
         {"overrides": {"ROOF_TPO_MEMBRANE_AND_INSULATION": {"onset_in": 1.0, "full_in": 1.5}}}),
    ]
    for b in BUILDINGS:
        pw = table[(b, WALLS)]
        variants += [
            (b, WALLS, "low: wall and window unit costs x0.5", "low", {"value_scale": 0.5}),
            (b, WALLS, "high: wall and window unit costs x2", "high", {"value_scale": 2.0}),
            (b, WALLS, "high: hail-facing share doubled", "high",
             {"overrides": {p["part_id"]: {"exposure": 2 * float(p["exposure_fraction"])} for p in pw}}),
        ]
    out = [head]
    for b, u, name, role, kw in variants:
        parts = table[(b, u)]
        z, ov, scale = kw.get("z", Z90), kw.get("overrides"), kw.get("value_scale", 1.0)
        drs = [unit_dr(parts, d, z, ov) for d in sizes]
        out.append([b, u, name, role, "unit_damage_ratio"] + [f"{x:.4f}" for x in drs])
        out.append([b, u, name, role, "building_pct_of_structure_rcn"]
                   + [f"{100 * unit_value(parts, scale) * x:.3f}" for x in drs])
    for b in BUILDINGS:  # building totals, central
        tot = [sum(unit_value(table[(b, u)]) * unit_dr(table[(b, u)], d) for u in UNITS) for d in sizes]
        roof = [unit_value(table[(b, ROOF)]) * unit_dr(table[(b, ROOF)], d) for d in sizes]
        out.append([b, "ALL", "reference (central): roof cover only", "building_total", "building_pct_of_structure_rcn"]
                   + [f"{100 * x:.3f}" for x in roof])
        out.append([b, "ALL", "reference (central): roof cover + walls and windows (T4)", "building_total",
                    "building_pct_of_structure_rcn"] + [f"{100 * x:.3f}" for x in tot])
    return out


def write(name: str, data: list[list]) -> None:
    with open(PROP / name, "w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(data)


def chart(table) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = {"RE_RES_SFD_1S_SLAB": "House (asphalt shingles)", "RE_IND_WAREHOUSE": "Warehouse (standing-seam steel)",
             "RE_COM_OFFICE_3S_SLAB": "Office (TPO membrane)"}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    ds = [d / 4 for d in range(0, 4 * 130 + 1)]
    for ax, b in zip(axes, BUILDINGS):
        roof = [100 * unit_value(table[(b, ROOF)]) * unit_dr(table[(b, ROOF)], d) for d in ds]
        walls = [100 * unit_value(table[(b, WALLS)]) * unit_dr(table[(b, WALLS)], d) for d in ds]
        ax.plot(ds, roof, color="#2f6db4", lw=2, label="Roof cover")
        ax.plot(ds, walls, color="#b4462f", lw=1.6, ls="--", label="Walls & windows (T4)")
        ax.plot(ds, [r + w for r, w in zip(roof, walls)], color="#333", lw=1.2, label="Total")
        ax.axvline(15.096 * 10 ** 0.412, color="#999", lw=0.8, ls=":")
        ax.set_title(names[b])
        ax.set_xlabel("Hail diameter (mm)")
        ax.set_xlim(0, 130)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Damage, % of structure replacement cost new")
    axes[0].legend(loc="upper left", fontsize=8)
    fig.suptitle("hail_real_estate model v0.1 (proposal): building-level damage per event, central curves "
                 "(dotted line: 39 mm, Hazard's MESH75 value at the 25.4 mm raw-MESH event threshold)", fontsize=10)
    fig.tight_layout()
    out = PROP.parent / "previews" / "hail_real_estate_v0_1_curves.png"
    fig.savefig(out, dpi=110, metadata={"Software": None})
    print("wrote", out.relative_to(ROOT))


def main(argv: list[str]) -> int:
    table = parts_table()
    assert sorted(table) == sorted((b, u) for b in BUILDINGS for u in UNITS), sorted(table)
    write(f"CURVE_ORDINATES_{TAG}.csv", ordinates(table))
    write(f"SENSITIVITY_{TAG}.csv", sensitivity(table))
    print(f"wrote CURVE_ORDINATES_{TAG}.csv and SENSITIVITY_{TAG}.csv")
    if "--chart" in argv:
        chart(table)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
