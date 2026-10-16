"""Validator for the noncanonical flood × real estate model-v0.1 / docs-r1 package.

Checks: required files; JSON schemas (bundle v3, capability v3, damage emit v2, when jsonschema is
installed); embedded vs standalone capability; rectangular registers and resolvable source IDs; artifact
ordinates vs the governed ordinates CSV; builder reproducibility of the JSON outputs; every known-answer test
through the reference evaluator; non-promotion (absent from the artifact index and version registry, no
current/ package); workbook sheets; links in the cell's Markdown.

Usage (from the repository root):
    python scripts/reference_helpers/validate_flood_real_estate_v0_1_package.py
Exit code 0 when every check passes.
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from flood_real_estate_curve_eval import DamageCallError, evaluate_damage_call  # noqa: E402
import build_flood_real_estate_v0_1_package as builder  # noqa: E402

CELL = ROOT / "docs/cells/flood_real_estate"
PROP = CELL / "proposed"
TAG = "flood_real_estate__model_v0_1__docs_r1"
SCHEMAS = ROOT / "docs/contracts/schemas"
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def load(path: Path):
    with open(path) as fh:
        return json.load(fh)


def csv_rows(path: Path) -> list[list[str]]:
    with open(path, newline="") as fh:
        return list(csv.reader(fh))


def main() -> int:
    files = {
        "artifact": PROP / f"{TAG}__curve_artifact.json",
        "capability": PROP / f"{TAG}__capability.json",
        "kats": PROP / f"known_answer_tests_{TAG}.json",
        "workbook": PROP / f"damage_curve_records_{TAG}.xlsx",
        "dossier": PROP / "flood_real_estate_curve_derivation_dossier__model_v0_1__docs_r1.md",
        "metadata_spec": PROP / "flood_real_estate_damage_code_metadata_spec__model_v0_1__docs_r1.md",
        "source_register": PROP / f"SOURCE_REGISTER_{TAG}.csv",
        "claim_register": PROP / f"CLAIM_PARAMETER_REGISTER_{TAG}.csv",
        "tiers": PROP / f"PARAMETER_TIER_TABLE_{TAG}.csv",
        "crosswalk": PROP / f"VALUE_CROSSWALK_{TAG}.csv",
        "ordinates": PROP / f"CURVE_ORDINATES_{TAG}.csv",
    }
    missing = [k for k, p in files.items() if not p.exists()]
    check("required files exist", not missing, ", ".join(missing))
    if missing:
        return report()

    art, cap, kats = load(files["artifact"]), load(files["capability"]), load(files["kats"])
    check("embedded capability equals standalone capability", art["capability_declaration"] == cap)
    for key in ("source_dossier", "source_workbook", "known_answer_tests", "source_register",
                "claim_parameter_register", "value_crosswalk"):
        check(f"artifact path resolves: {key}", (ROOT / art[key]).exists(), art[key])

    # schemas
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        sch = {n: load(SCHEMAS / f"{n}.schema.json") for n in
               ("curve_artifact_bundle.v3", "capability_declaration.v3", "damage_emit.v2")}
        reg = Registry().with_resources([(s["$id"], Resource.from_contents(s)) for s in sch.values()])
        validators = {n: Draft202012Validator(s, registry=reg) for n, s in sch.items()}
        errs = list(validators["curve_artifact_bundle.v3"].iter_errors(art))
        check("artifact validates against bundle v3", not errs, "; ".join(e.message[:120] for e in errs[:3]))
        errs = list(validators["capability_declaration.v3"].iter_errors(cap))
        check("capability validates against capability v3", not errs, "; ".join(e.message[:120] for e in errs[:3]))
        emit_validator = validators["damage_emit.v2"]
    except ModuleNotFoundError:
        check("jsonschema available for schema checks", False, "install jsonschema>=4.17")
        emit_validator = None

    # registers
    for k in ("source_register", "claim_register", "tiers", "crosswalk", "ordinates"):
        widths = {len(r) for r in csv_rows(files[k])}
        check(f"register rectangular: {files[k].name}", len(widths) == 1, str(widths))
    sources = {r[0] for r in csv_rows(files["source_register"])[1:]}
    refs = {ref.split("#")[0] for r in art["pathways"][0]["curve_records"] for ref in r["source_parameter_refs"]}
    check("curve source refs resolve to the source register", refs <= sources, str(refs - sources))
    claim_src = set()
    for r in csv.DictReader(open(files["claim_register"])):
        claim_src |= {s for s in r["source_ids"].split(";") if s.startswith("FRE-S")}
    check("claim source IDs resolve", claim_src <= sources, str(claim_src - sources))
    tier_src = set()
    for r in csv.DictReader(open(files["tiers"])):
        tier_src |= {s for s in r["source_ids"].split(";") if s}
    check("parameter-tier source IDs resolve", tier_src <= sources, str(tier_src - sources))

    # ordinates
    pts = builder.ordinates()
    mism = []
    for r in art["pathways"][0]["curve_records"]:
        band = r["selector_match"]["band"]
        cid = r["curve_id"].removesuffix("_MIN").removesuffix("_MAX")
        if r["parameters"]["points"] != pts[(cid, band)]:
            mism.append(r["curve_id"])
        if r["valid_range"] != [r["parameters"]["points"][0][0], r["parameters"]["points"][-1][0]]:
            mism.append(r["curve_id"] + ":range")
    check("artifact ordinates equal the governed ordinates CSV (12 records)", not mism and len(art["pathways"][0]["curve_records"]) == 12, str(mism))
    mono = [r["curve_id"] for r in art["pathways"][0]["curve_records"]
            if any(b[1] < a[1] for a, b in zip(r["parameters"]["points"], r["parameters"]["points"][1:]))]
    check("every record is non-decreasing with depth", not mono, str(mono))

    # reproducibility of JSON outputs
    check("builder reproduces the artifact JSON", builder.artifact(pts) == art)
    check("builder reproduces the known-answer tests", builder.known_answer_tests(pts) == kats)

    # known-answer tests
    tol = kats["absolute_tolerance"]
    fails = []
    n = 0
    for t in kats["formula_known_answer_tests"] + kats["withheld_tests"]:
        n += 1
        try:
            out = evaluate_damage_call(art, t["input"])
        except DamageCallError as e:
            fails.append(f"{t['test_id']}: error {e.code}")
            continue
        if emit_validator is not None:
            emit_errs = list(emit_validator.iter_errors(out))
            if emit_errs:
                fails.append(f"{t['test_id']}: emit schema {emit_errs[0].message[:80]}")
        res, exp = out["failure_unit_results"][0], t["expected"]
        if res["status"] != exp["status"]:
            fails.append(f"{t['test_id']}: status {res['status']}")
            continue
        if exp["status"] == "withheld":
            if exp["reason_code"] not in res["withheld_reason_codes"]:
                fails.append(f"{t['test_id']}: reasons {res['withheld_reason_codes']}")
            continue
        if res["curve_id"] != exp["curve_id"] or not math.isclose(res["scalar_central_dr"], exp["failure_unit_damage_ratio"], rel_tol=0, abs_tol=tol):
            fails.append(f"{t['test_id']}: {res['curve_id']} {res['scalar_central_dr']}")
        for f in exp.get("metadata_flags_include", []):
            if f not in res["metadata_flags"]:
                fails.append(f"{t['test_id']}: missing flag {f}")
        for k, v in exp.get("scenario_drs", {}).items():
            if not math.isclose(res.get("scenario_drs", {}).get(k, -1), v, rel_tol=0, abs_tol=tol):
                fails.append(f"{t['test_id']}: bound {k}")
    for t in kats["error_tests"]:
        n += 1
        try:
            evaluate_damage_call(art, t["input"])
            fails.append(f"{t['test_id']}: no error raised")
        except DamageCallError as e:
            if e.code != t["expected_error_code"]:
                fails.append(f"{t['test_id']}: {e.code}")
    check(f"known-answer tests pass ({n})", not fails, "; ".join(fails[:5]))

    # non-promotion
    index = (ROOT / "docs/contracts/machine_readable_artifact_index.json").read_text()
    registry = (ROOT / "docs/cells/VERSION_REGISTRY.md").read_text()
    check("cell absent from the machine-readable artifact index", "flood_real_estate" not in index)
    check("cell absent from the version registry", "flood_real_estate" not in registry)
    check("no current/ package", not (CELL / "current").exists())
    check("artifact is noncanonical and proposed",
          art["canonical_runtime_artifact"] is False and art["schema_status"] == "proposed_draft"
          and art["promotion_status"] == "proposed" and cap["promotion_gate"]["status"] == "blocked")

    # profile binding (Hazard reference profiles r1)
    bind_path = PROP / f"PROFILE_BINDING_{TAG}.csv"
    if bind_path.exists():
        with bind_path.open(newline="") as fh:
            binding = list(csv.DictReader(fh))
        by_id = {r["curve_id"]: r for r in art["pathways"][0]["curve_records"]}
        ids = {r[0] for r in csv_rows(files["source_register"])[1:]} | {r[0] for r in csv_rows(files["claim_register"])[1:]}
        bad = []
        for b in binding:
            tag = f"{b['profile_id']}/{b['pathway_id']}/{b['flood_water_type']}"
            if b["applicability"] == "unavailable":
                if b["point_record_id"] or b["bound_record_ids"]:
                    bad.append(f"{tag}: unavailable row names a record")
                continue
            want = {"reference_building_id": b["damage_selector_reference_building_id"],
                    "flood_water_type": b["flood_water_type"]}
            point = by_id.get(b["point_record_id"])
            if not point or point["selector_match"] != {**want, "band": "point"}:
                bad.append(f"{tag}: point record {b['point_record_id']} missing or mismatched")
            for cid in filter(None, b["bound_record_ids"].split(";")):
                r = by_id.get(cid)
                if not r or {k: r["selector_match"][k] for k in want} != want or r["selector_match"]["band"] == "point":
                    bad.append(f"{tag}: bound record {cid} missing or mismatched")
            bad += [f"{tag}: evidence {e} unknown" for e in b["evidence_ids"].split(";") if e and e not in ids]
        check("profile binding records and evidence resolve", binding and not bad, "; ".join(bad[:5]))
        check("profile binding pinned to one profile revision",
              len({(b["profile_revision"], b["profile_commit"]) for b in binding}) == 1)

    # workbook
    try:
        from openpyxl import load_workbook
        wb = load_workbook(files["workbook"], read_only=True)
        need = {"README", "curve_records", "reference_buildings", "sources", "claims", "parameter_tiers",
                "value_crosswalk", "known_answer_tests"}
        check("workbook has the expected sheets", need <= set(wb.sheetnames), str(need - set(wb.sheetnames)))
    except ModuleNotFoundError:
        check("openpyxl available for workbook check", False, "install openpyxl")

    # links
    broken = []
    for md in CELL.rglob("*.md"):
        for m in re.finditer(r"\]\(([^)#]+)(#[^)]*)?\)", md.read_text()):
            target = m.group(1)
            if not target.startswith("http") and not (md.parent / target).exists():
                broken.append(f"{md.name} -> {target}")
    check("Markdown links in the cell resolve", not broken, "; ".join(broken[:5]))
    return report()


def report() -> int:
    width = max(len(n) for n, _, _ in results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name.ljust(width)}  {detail if not ok else ''}")
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
