#!/usr/bin/env python3
"""Build the DD-G31 physical tower-value successor without changing response."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[2]
CELL = ROOT / "docs/cells/tropical_cyclone_wind_wind"
PARENT = CELL / "current/tropical_cyclone_wind_wind__model_v1_2__docs_r2__curve_artifact.json"
PARENT_SHA = "009996c07eb8150f79f11741d42b6cd37562d655ee336f82f178ccdeb987c992"
STEM = "tropical_cyclone_wind_wind__model_v1_3__docs_r1"
DEST = CELL / "proposed"
POLICY = "TCWW_OWNER_APPROVED_3P3MW_FOR_CANONICAL_5MW_PHYSICAL_TOWER_V1"
PROFILE = "CONUS_WIND_FARM_REFERENCE_V2"
BASIS = "CONUS_WIND_FARM_SOURCE_TOWER_VALUE_V1"
SHARE = 276 / 1623


def build() -> dict:
    raw = PARENT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PARENT_SHA:
        raise ValueError("parent Damage bytes changed")
    a = deepcopy(json.loads(raw))
    a.update(damage_code_id="TROPICAL_CYCLONE_WIND_WIND_JAIMES_TOWER_SCREENING_V1_3",
             semantic_damage_model_version="model v1.3", documentation_revision="docs r1",
             lifecycle_state="proposed_v1_3", promotion_status="proposed",
             review_status="owner_approved_DD_G31_value_binding_pending_consumer_verification",
             canonical_runtime_artifact=False, package_release="unreleased", package_inclusion_status="not_included")
    a["source_dossier"] = f"docs/cells/tropical_cyclone_wind_wind/proposed/README_{STEM}.md"
    a["source_workbook"] = f"docs/cells/tropical_cyclone_wind_wind/proposed/{STEM}__value_audit.xlsx"
    a["value_crosswalk"] = f"docs/cells/tropical_cyclone_wind_wind/proposed/{STEM}__value_crosswalk.csv"
    a["known_answer_tests"] = f"docs/cells/tropical_cyclone_wind_wind/proposed/{STEM}__verification.json"
    contract = a["derivation_rationale"]["owner_approved_proxy_contract"]
    contract.update(proxy_policy_id=POLICY, canonical_asset_profile_id=PROFILE, covered_value_basis_id=BASIS,
                    covered_value_share_of_project_tiv=SHARE, uncovered_value_share_of_project_tiv=1-SHARE)
    a["derivation_rationale"]["v1_3_decision"] = (
        "DD-G31: preserve the response and tower-only scope; replace the flat 16% x $140M binding with "
        "100,000 kW x $276/kW tower value against $1,623/kW physical TIV. No 5/3.3 multiplier."
    )
    a["derivation_rationale"]["source_denominator_limit"] = (
        "Jaimes source denominator remains ambiguous. This is an explicit owner-approved screening "
        "transfer to source-cost tower dollars, not a calibrated source-to-CWER conversion."
    )
    a["evaluation_contract"]["proxy_screening_completion"]["applies_only_when_proxy_policy_id"] = POLICY
    a["pathways"][0]["exposure_contract"]["value_rule"] = (
        "Only the exact physical tower binding is covered: $27.6M / $162.3M; $134.7M remains withheld."
    )
    for u in a["failure_units"]:
        if "proxy_value_binding" in u:
            u["proxy_value_binding"].update(covered_value_basis_id=BASIS, covered_value_share_of_project_tiv=SHARE)
    a["value_linkage"]["owner_approved_proxy_value_basis"].update(
        id=BASIS, canonical_asset_profile_id=PROFILE, project_tiv_usd_at_activation=162_300_000,
        covered_subsystem_shares={"tower": SHARE}, covered_value_share=SHARE, covered_value_usd_at_activation=27_600_000,
        uncovered_value_share=1-SHARE, uncovered_value_usd_at_activation=134_700_000,
        source_workbook_sha256="9edb7a64cf36df6c6e7a95f5b3d06aa5b50cb502792b9012b95af4692b542d52",
        source_costs_sha256="53a4dc028639f479dba6de9b6173dd43c6ec1b3d00137c02ce692a78f901a75e",
        source_rows=["Wind_Map:9"], source_price_year=2023,
        resolved_reference_sha256="b0c6c62957a93061de26f03c5775ccd7af835ac28044857b4d65b317ee63c7fd")
    cwer = a["value_linkage"]["cwer_comparison_basis"]
    cwer.update(runtime_crosswalk_status="approved_only_for_exact_DD_G31_physical_tower_proxy",
                prohibited_use="All general CWER/equipment/whole-plant substitutions remain prohibited; only the exact named physical tower binding is admitted.")
    cap = json.loads(json.dumps(a["capability_declaration"]).replace("0.16", "276/1623").replace("0.84", "1347/1623")
                     .replace("PARTIAL_TOWER_VALUE_COVERAGE_16PCT", "PARTIAL_SOURCE_COST_TOWER_VALUE_COVERAGE")
                     .replace("UNCOVERED_PROJECT_VALUE_84PCT_WITHHELD_NOT_ZERO", "NON_TOWER_PHYSICAL_VALUE_WITHHELD_NOT_ZERO"))
    cap["canonical_runtime_artifact"] = False
    cap["promotion_gate"] = {"status": "ready_for_review", "required_before_canonical_use": [
        "unchanged source and proxy response KATs", "exact physical reference/value source pins",
        "13,085-cell consumer build with preserved placement/rate identity and $27.6M caps"]}
    a["capability_declaration"] = cap
    a["legacy_comparison"]["v1_3_parent"] = {"sha256": PARENT_SHA, "retained": True,
        "old_tiv_usd": 140_000_000, "old_tower_usd": 22_400_000, "response_changed": False}
    a["legacy_comparison"]["canonical_index"] = "v1.2 remains selected until the explicit v1.3 consumer/release gates close"
    a["emit_contract"]["scenario_loss"] = "consumer-computable only with the exact physical tower-value basis and caps"
    return a


def main() -> None:
    a = build()
    for name, obj in ((f"{STEM}__curve_artifact.json", a), (f"{STEM}__capability.json", a["capability_declaration"])):
        path = DEST / name
        with path.open("x") as f:
            json.dump(obj, f, indent=2); f.write("\n")
    (DEST / f"{STEM}__value_crosswalk.csv").write_text(
        "scope,usd_per_kw,capacity_kw,value_usd,treatment\n"
        "tower,276,100000,27600000,modeled\nother_physical,1347,100000,134700000,withheld_not_zero\n"
        "full_physical,1623,100000,162300000,denominator_not_additive\n")
    book = Workbook()
    sheet = book.active; sheet.title = "Value binding"
    for row in [("Quantity", "Parent", "Successor"), ("Full TIV", 140000000, 162300000),
                ("Tower value", 22400000, 27600000), ("Covered share", .16, SHARE),
                ("Unmodeled value", 117600000, 134700000), ("Curve change", "none", "none")]:
        sheet.append(row)
    sheet.column_dimensions["A"].width=30;sheet.column_dimensions["B"].width=24;sheet.column_dimensions["C"].width=24
    book.save(DEST / f"{STEM}__value_audit.xlsx")
    print(hashlib.sha256((DEST / f"{STEM}__curve_artifact.json").read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
