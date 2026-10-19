"""Derive the wildfire × real estate model-v0.1 state tables from the governed source tables.

Reads   docs/cells/wildfire_real_estate/proposed/WRC_RESPONSE_FUNCTION_TABLE_<tag>.csv   (USFS response values)
        docs/cells/wildfire_real_estate/proposed/BUILDING_FACTOR_TABLE_<tag>.csv         (house = 1, warehouse, office)
        docs/cells/wildfire_real_estate/proposed/DINS_BUILDING_COMPARISON_<tag>.csv      (same-fire 90% range, sensitivity)
Writes  CURVE_ORDINATES_<tag>.csv      three records (one per reference building), exact FSim class states 0..6
        SENSITIVITY_<tag>.csv          damage per class under the alternative lifeform and building-factor readings
        ../previews/wildfire_real_estate_v0_1_curves.png   (only with --chart; needs matplotlib)

The curve (decision log D-WFRE-03 to D-WFRE-08):
    DR_b(state 0) = 0                                   (no-event control state)
    DR_b(state k) = factor_b * WRC_shrub(FLP_k) / 100   for k = 1..6
where WRC_shrub is the USFS Wildfire Risk to Communities structure response for the shrub lifeform
(20, 35, 50, 65, 80, 95) and factor_b is 1.0 (house), 0.8 (warehouse) or 0.9 (office). Values are rounded to 6
decimals; the rounded table is the governed curve. Exact integer states only; nothing is interpolated.

Usage (from the repository root):
    python scripts/reference_helpers/derive_wildfire_real_estate_curves.py [--chart]
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CELL_ID = "wildfire_real_estate"
PROP = ROOT / f"docs/cells/{CELL_ID}/proposed"
TAG = f"{CELL_ID}__model_v0_1__docs_r1"
PATHWAY = "wildfire_building_exposure"
LIFEFORM = "shrub"
DECIMALS = 6
BUILDINGS = ["RE_RES_SFD_1S_SLAB", "RE_IND_WAREHOUSE", "RE_COM_OFFICE_3S_SLAB"]
STEM = {"RE_RES_SFD_1S_SLAB": "RES", "RE_IND_WAREHOUSE": "IND", "RE_COM_OFFICE_3S_SLAB": "OFF"}
DINS_GROUP = {"RE_IND_WAREHOUSE": "warehouse_like", "RE_COM_OFFICE_3S_SLAB": "office_like"}
CLASS_LABEL = {0: "no event (control)", 1: "< 2 ft", 2: "2 to < 4 ft", 3: "4 to < 6 ft", 4: "6 to < 8 ft",
               5: "8 to < 12 ft", 6: "12+ ft"}


def read(name: str) -> list[dict[str, str]]:
    with open(PROP / name, newline="") as fh:
        return list(csv.DictReader(fh))


def wrc() -> dict[str, dict[int, float]]:
    out: dict[str, dict[int, float]] = {}
    for r in read(f"WRC_RESPONSE_FUNCTION_TABLE_{TAG}.csv"):
        out.setdefault(r["lifeform"], {})[int(r["state_index"])] = float(r["wrc_response_value"])
    return out


def factors(role: str = "adopted") -> dict[str, float]:
    return {r["reference_building_id"]: float(r["factor_on_house_curve"])
            for r in read(f"BUILDING_FACTOR_TABLE_{TAG}.csv") if r["role"] == role}


def factor_label(f: float) -> str:
    return "" if f == 1.0 else f"_X{f:.1f}".replace(".", "_")


def record_id(building: str, factor: float) -> str:
    return f"WFRE_{STEM[building]}_WRC_{LIFEFORM.upper()}{factor_label(factor)}"


def curve(values: dict[int, float], factor: float) -> list[float]:
    """DR at states 0..6, clipped to [0, 1] (clipping only matters for sensitivity factors above 1)."""
    return [0.0] + [min(1.0, round(factor * values[k] / 100.0, DECIMALS)) for k in range(1, 7)]


def ordinates(table, fac) -> list[list]:
    out = [["curve_id", "reference_building_id", "pathway_id", "state_index", "flame_length_class", "damage_ratio",
            "source_ids"]]
    for b in BUILDINGS:
        dr = curve(table[LIFEFORM], fac[b])
        src = "WFRE-S001" if fac[b] == 1.0 else "WFRE-S001;WFRE-S002"
        for k in range(7):
            out.append([record_id(b, fac[b]), b, PATHWAY, k, CLASS_LABEL[k], f"{dr[k]:.6f}", src])
    return out


def same_fire_range() -> dict[str, tuple[float, float]]:
    return {r["group"]: (float(r["ratio_p05"]), float(r["ratio_p95"]))
            for r in read(f"DINS_BUILDING_COMPARISON_{TAG}.csv") if r["section"] == "same_fire_ratio"}


def sensitivity(table, fac) -> list[list]:
    out = [["reference_building_id", "variant", "role"] + [f"dr_state{k}" for k in range(1, 7)]]
    rng = same_fire_range()
    alt = {}
    for r in read(f"BUILDING_FACTOR_TABLE_{TAG}.csv"):
        if r["role"] == "sensitivity":
            alt.setdefault(r["reference_building_id"], []).append(float(r["factor_on_house_curve"]))
    for b in BUILDINGS:
        rows = [("reference: shrub with the adopted factor", "reference", table[LIFEFORM], fac[b]),
                ("lifeform tree", "lifeform", table["tree"], fac[b]),
                ("lifeform grass/herbaceous", "lifeform", table["grass"], fac[b])]
        if b in DINS_GROUP:
            lo, hi = rng[DINS_GROUP[b]]
            rows += [(f"same-fire 90% low ({lo:.2f})", "building_factor", table[LIFEFORM], lo),
                     (f"same-fire 90% high ({hi:.2f}; capped at 100%)", "building_factor", table[LIFEFORM], hi)]
            rows += [(f"factor {f:.1f}" + (" (pooled DINS ratio)" if f < 1 else " (same as house)"), "building_factor",
                      table[LIFEFORM], f) for f in alt[b]]
        for name, role, values, f in rows:
            out.append([b, name, role] + [f"{v:.4f}" for v in curve(values, f)[1:]])
    return out


def write(name: str, data: list[list]) -> None:
    with open(PROP / name, "w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(data)


def chart(table, fac) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = {"RE_RES_SFD_1S_SLAB": "House (USFS home response)", "RE_IND_WAREHOUSE": "Warehouse (0.8 x house)",
             "RE_COM_OFFICE_3S_SLAB": "Office (0.9 x house)"}
    colors = {"RE_RES_SFD_1S_SLAB": "#b4462f", "RE_IND_WAREHOUSE": "#2f6db4", "RE_COM_OFFICE_3S_SLAB": "#3c8c4a"}
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    xs = list(range(7))
    hi, lo = curve(table["tree"], 1.0), curve(table["grass"], 1.0)
    ax.fill_between(xs[1:], lo[1:], hi[1:], color="#b4462f", alpha=0.10, step=None,
                    label="House: grass to tree lifeform (sensitivity)")
    for i, b in enumerate(BUILDINGS):
        dr = curve(table[LIFEFORM], fac[b])
        off = (i - 1) * 0.08
        ax.plot([x + off for x in xs], dr, "o", ms=7, color=colors[b], label=names[b])
        ax.plot([x + off for x in xs], dr, ":", lw=0.8, color=colors[b])
    ax.set_xticks(xs, [CLASS_LABEL[k].replace(" (control)", "") for k in xs], fontsize=8)
    ax.set_xlabel("FSim conditional flame-length class (exact states 0-6; no values between classes)")
    ax.set_ylabel("Damage ratio (fraction of structure value)")
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)
    fig.suptitle("wildfire_real_estate model v0.1 (proposal): USFS Wildfire Risk to Communities response, shrub",
                 fontsize=10)
    fig.tight_layout()
    out = PROP.parent / "previews" / "wildfire_real_estate_v0_1_curves.png"
    fig.savefig(out, dpi=110, metadata={"Software": None})
    print("wrote", out.relative_to(ROOT))


def main(argv: list[str]) -> int:
    table, fac = wrc(), factors()
    assert sorted(table) == ["grass", "shrub", "tree"] and all(sorted(v) == list(range(1, 7)) for v in table.values())
    assert sorted(fac) == sorted(BUILDINGS), fac
    write(f"CURVE_ORDINATES_{TAG}.csv", ordinates(table, fac))
    write(f"SENSITIVITY_{TAG}.csv", sensitivity(table, fac))
    print(f"wrote CURVE_ORDINATES_{TAG}.csv and SENSITIVITY_{TAG}.csv")
    if "--chart" in argv:
        chart(table, fac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
