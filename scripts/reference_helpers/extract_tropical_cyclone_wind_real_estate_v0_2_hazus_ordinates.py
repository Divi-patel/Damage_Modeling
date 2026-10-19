"""Extract the tropical-cyclone wind × real estate model-v0.2 curve ordinates and variant sensitivity.

Model v0.2 binds the cell to the Hazard reference profiles r1 (decision log D-TCRE-22 to D-TCRE-25):
    - house RE_RES_SFD_1S_SLAB: Hazus WSF1, unchanged from v0.1;
    - retail RE_COM_LOWRISE: Hazus SECBL, unchanged from v0.1 (kept, bound to no profile);
    - warehouse RE_IND_WAREHOUSE: Hazus SPMBL with a new-or-average roof deck (v0.1: old);
    - office RE_COM_OFFICE_3S_SLAB (new): Hazus SECBM, single-ply membrane, medium window area.

Reads the FEMA-provided Hazus hurricane extract (``HazusWindDamFunctions_Hazus61.xlsx``, TCRE-S002) and writes
the governed ordinates CSV (4 buildings × 5 terrains = 20 records, 41 points each, 50–250 mph) and the variant
sensitivity CSV (alternatives at 100/120/140/160 mph, open and suburban terrain). Optionally cross-checks every
written ordinate and every sensitivity row against NHERI SimCenter's independent Hazus 5.1 copy (TCRE-S003).
Requires openpyxl. The workbook is large: a run takes a few minutes.

Usage (from the repository root):
    python scripts/reference_helpers/extract_tropical_cyclone_wind_real_estate_v0_2_hazus_ordinates.py \
        <HazusWindDamFunctions_Hazus61.xlsx> [<simcenter loss_repair.csv>]
"""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROPOSED = ROOT / "docs/cells/tropical_cyclone_wind_real_estate/proposed"
TAG = "tropical_cyclone_wind_real_estate__model_v0_2__docs_r1"
OUT = PROPOSED / f"CURVE_ORDINATES_{TAG}.csv"
OUT_SENS = PROPOSED / f"VARIANT_SENSITIVITY_{TAG}.csv"
EXTRACT_SHA256 = "0fe93bbdc5d4ae3a3eace7f8147436ad63f381175688671aebd769674d1bc353"
SIMCENTER_SHA256 = "6f023f82c4ab56e57d0d20becf72e0c46a13cf4a80ebd28c3ac50f6bb83de222"
BUILDING_LOSS = 5  # huDamLossFunDescription: DamLossDescID 5 = "Building Loss"

# reference building -> (curve-id stem, Hazus SBT, Hazus charDescription, CaseID, SimCenter ID stem)
BUILDINGS = {
    "RE_RES_SFD_1S_SLAB": ("TCRE_RES_HAZUS_WSF1", "WSF1", "rsgabswrnorda6dtnailgdnodshtnorcshg", 1,
                           "W.SF.1.gab.0.6d.tnail.no.0"),
    "RE_COM_LOWRISE": ("TCRE_COM_HAZUS_SECBL", "SECBL", "rcburwalowshtnowiddBrd100", 3,
                       "S.ECB.L.bur.0.B.std.low"),
    "RE_IND_WAREHOUSE": ("TCRE_IND_HAZUS_SPMBL_NEWDECK", "SPMBL", "dqgodshtnord100", 3,
                         "S.PMB.L.0.god.std"),
    "RE_COM_OFFICE_3S_SLAB": ("TCRE_OFF_HAZUS_SECBM", "SECBM", "rcspmwamedshtnowiddBrd100", 3,
                              "S.ECB.M.spm.0.B.std.med"),
}
# sensitivity rows: (reference building, label, role, SBT, charDescription, CaseID, SimCenter stem or None)
VARIANTS = [
    ("RE_RES_SFD_1S_SLAB", "reference (most common)", "reference", "WSF1", "rsgabswrnorda6dtnailgdnodshtnorcshg", 1, "W.SF.1.gab.0.6d.tnail.no.0"),
    ("RE_RES_SFD_1S_SLAB", "roof-to-wall straps", "code_built_sensitivity", "WSF1", "rsgabswrnorda6dstrapgdnodshtnorcshg", 1, None),
    ("RE_RES_SFD_1S_SLAB", "roof deck 8d @ 6\"/12\" + straps", "code_built_sensitivity", "WSF1", "rsgabswrnorda8dstrapgdnodshtnorcshg", 1, None),
    ("RE_RES_SFD_1S_SLAB", "roof deck 8d @ 6\"/6\" + straps", "code_built_sensitivity", "WSF1", "rsgabswrnorda8sstrapgdnodshtnorcshg", 1, None),
    ("RE_RES_SFD_1S_SLAB", "roof deck 8d @ 6\"/12\", toe-nail", "code_built_sensitivity", "WSF1", "rsgabswrnorda8dtnailgdnodshtnorcshg", 1, None),
    ("RE_RES_SFD_1S_SLAB", "shutters", "measure_candidate", "WSF1", "rsgabswrnorda6dtnailgdno2shtysrcshg", 1, None),
    ("RE_IND_WAREHOUSE", "reference (new or average roof deck)", "reference", "SPMBL", "dqgodshtnord100", 3, "S.PMB.L.0.god.std"),
    ("RE_IND_WAREHOUSE", "old roof deck (v0.1 reference)", "previous_reference", "SPMBL", "dqporshtnord100", 3, "S.PMB.L.0.por.std"),
    ("RE_IND_WAREHOUSE", "shutters", "measure_candidate", "SPMBL", "dqgodshtysrd100", 3, None),
    ("RE_IND_WAREHOUSE", "SPMBM medium metal building (4,000-50,000 ft2)", "alternative_type", "SPMBM", "dqgodshtnord100", 3, None),
    ("RE_COM_OFFICE_3S_SLAB", "reference (single-ply membrane, medium windows)", "reference", "SECBM", "rcspmwamedshtnowiddBrd100", 3, "S.ECB.M.spm.0.B.std.med"),
    ("RE_COM_OFFICE_3S_SLAB", "built-up roof, medium windows", "alternative_attribute", "SECBM", "rcburwamedshtnowiddBrd100", 3, None),
    ("RE_COM_OFFICE_3S_SLAB", "single-ply membrane, high windows", "alternative_attribute", "SECBM", "rcspmwahigshtnowiddBrd100", 3, None),
    ("RE_COM_OFFICE_3S_SLAB", "shutters", "measure_candidate", "SECBM", "rcspmwamedshtyswiddBrd100", 3, None),
    ("RE_COM_OFFICE_3S_SLAB", "MECBM masonry engineered (same characteristics)", "alternative_type", "MECBM", "rcspmwamedshtnowiddBrd100", 3, None),
    ("RE_COM_OFFICE_3S_SLAB", "SECBL 1-2 storey retail reference (v0.1 commercial)", "previous_reference", "SECBL", "rcburwalowshtnowiddBrd100", 3, "S.ECB.L.bur.0.B.std.low"),
    ("RE_COM_LOWRISE", "reference (most common)", "reference", "SECBL", "rcburwalowshtnowiddBrd100", 3, "S.ECB.L.bur.0.B.std.low"),
]
TERRAINS = {1: ("open", 0.03, "3"), 2: ("light_suburban", 0.15, "15"), 3: ("suburban", 0.35, "35"),
            4: ("light_trees", 0.70, "70"), 5: ("trees", 1.00, "100")}
SENS_SPEEDS = (100, 120, 140, 160)
SOURCE_IDS = "TCRE-S001;TCRE-S002;TCRE-S003"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_extract(path: Path):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True)
    types = {}
    for row in wb["huListOfWindBldgTypes"].iter_rows(min_row=2, values_only=True):
        wb_id, sbt, desc, _n, case = row[:5]
        types.setdefault((sbt.strip(), desc.strip(), case), []).append(wb_id)
    keys = {(s, d, c) for _b, (_st, s, d, c, _sc) in BUILDINGS.items()} | {(v[3], v[4], v[5]) for v in VARIANTS}
    wbid = {}
    for k in keys:
        if len(types.get(k, [])) != 1:
            raise SystemExit(f"expected one wbID for {k}, got {types.get(k)}")
        wbid[k] = types[k][0]
    sheet = wb["huDamLossFun"]
    header = next(sheet.iter_rows(max_row=1, values_only=True))
    speeds = [int(h[2:]) for h in header[3:]]
    if speeds != list(range(50, 255, 5)):
        raise SystemExit(f"unexpected wind-speed columns {speeds[:3]}…{speeds[-3:]}")
    wanted = set(wbid.values())
    curves = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        wb_id, terrain, desc_id = row[:3]
        if wb_id in wanted and desc_id == BUILDING_LOSS:
            curves[(wb_id, terrain)] = [float(v) for v in row[3:]]
    return speeds, wbid, curves


def read_simcenter(path: Path) -> dict[str, list[float]]:
    out = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            ys, xs = r["LossFunction-Theta_0"].split("|")
            if [float(x) for x in xs.split(",")] != [float(s) for s in range(50, 255, 5)]:
                continue
            out[r["ID"].removesuffix("-Cost")] = [float(y) for y in ys.split(",")]
    return out


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    extract = Path(argv[1])
    if sha256(extract) != EXTRACT_SHA256:
        raise SystemExit("extract SHA-256 differs from TCRE-S002")
    simcenter = None
    if len(argv) == 3:
        if sha256(Path(argv[2])) != SIMCENTER_SHA256:
            raise SystemExit("SimCenter file SHA-256 differs from TCRE-S003")
        simcenter = read_simcenter(Path(argv[2]))
    speeds, wbid, curves = read_extract(extract)

    rows, max_diff, checked = [], 0.0, 0
    for building, (stem, sbt, desc, case, sc_stem) in BUILDINGS.items():
        wid = wbid[(sbt, desc, case)]
        for tid, (tname, z0, sc_suffix) in TERRAINS.items():
            values = curves[(wid, tid)]
            if simcenter is not None:
                ref = simcenter[f"{sc_stem}.{sc_suffix}"]
                max_diff = max(max_diff, max(abs(a - b) for a, b in zip(values, ref)))
                checked += 1
            for mph, value in zip(speeds, values):
                rows.append([f"{stem}_{tname.upper()}", building, sbt, desc, wid, tid, tname, f"{z0:.2f}",
                             mph, repr(value), SOURCE_IDS])
    sens = []
    idx = [speeds.index(s) for s in SENS_SPEEDS]
    for building, label, role, sbt, desc, case, sc_stem in VARIANTS:
        wid = wbid[(sbt, desc, case)]
        for tid in (1, 3):
            values = curves[(wid, tid)]
            if simcenter is not None and sc_stem:
                ref = simcenter[f"{sc_stem}.{TERRAINS[tid][2]}"]
                max_diff = max(max_diff, max(abs(a - b) for a, b in zip(values, ref)))
                checked += 1
            sens.append([building, label, role, sbt, desc, wid, TERRAINS[tid][0]] + [round(values[i], 4) for i in idx])
    if simcenter is not None and max_diff != 0.0:
        raise SystemExit(f"extract and SimCenter copy differ (max abs diff {max_diff})")

    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["curve_id", "reference_building_id", "hazus_sbt", "hazus_wind_building_characteristics",
                    "hazus_wbid", "hazus_terrain_id", "hazus_terrain_class", "surface_roughness_z0_m",
                    "peak_gust_3s_10m_open_terrain_mph", "building_loss_ratio", "source_ids"])
        w.writerows(rows)
    with open(OUT_SENS, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["reference_building_id", "variant", "role", "hazus_sbt", "hazus_wind_building_characteristics",
                    "hazus_wbid", "terrain"] + [f"loss_ratio_{s}mph" for s in SENS_SPEEDS])
        w.writerows(sens)
    note = f"cross-checked {checked} curves against SimCenter: identical" if simcenter is not None else "not cross-checked"
    print(f"wrote {len(rows)} ordinates ({len(rows) // len(speeds)} records) and {len(sens)} sensitivity rows; {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
