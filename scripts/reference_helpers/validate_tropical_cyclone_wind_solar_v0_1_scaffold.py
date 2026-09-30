#!/usr/bin/env python3
"""Validate the noncanonical tropical-cyclone-wind × solar model-v0.1 scaffold.

The package intentionally contains no runtime curve.  This validator therefore
checks the fail-closed contract, evidence/value registries, candidate-isolation
rules, workbook integrity, local links, and absence from the canonical artifact
index.  It uses only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
CELL = ROOT / "docs/cells/tropical_cyclone_wind_solar"
PROPOSED = CELL / "proposed"

ARTIFACT_PATH = (
    PROPOSED
    / "tropical_cyclone_wind_solar__model_v0_1__docs_r1__curve_artifact.json"
)
CAPABILITY_PATH = (
    PROPOSED
    / "tropical_cyclone_wind_solar__model_v0_1__docs_r1__capability.json"
)
KAT_PATH = (
    PROPOSED
    / "known_answer_tests_tropical_cyclone_wind_solar__model_v0_1__docs_r1.json"
)
SOURCE_PATH = (
    PROPOSED
    / "SOURCE_REGISTER_tropical_cyclone_wind_solar__model_v0_1__docs_r1.csv"
)
CLAIM_PATH = (
    PROPOSED
    / "CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_solar__model_v0_1__docs_r1.csv"
)
PARAMETER_PATH = (
    PROPOSED
    / "PARAMETER_TIER_TABLE_tropical_cyclone_wind_solar__model_v0_1__docs_r1.csv"
)
VALUE_PATH = (
    PROPOSED
    / "VALUE_CROSSWALK_tropical_cyclone_wind_solar__model_v0_1__docs_r1.csv"
)
WORKBOOK_PATH = (
    PROPOSED
    / "damage_curve_records_tropical_cyclone_wind_solar__model_v0_1__docs_r1.xlsx"
)
BUNDLE_SCHEMA_PATH = ROOT / "docs/contracts/schemas/curve_artifact_bundle.schema.json"
CAPABILITY_SCHEMA_PATH = ROOT / "docs/contracts/schemas/capability_declaration.schema.json"
ARTIFACT_INDEX_PATH = ROOT / "docs/contracts/machine_readable_artifact_index.json"
HANDOFF_PATH = (
    ROOT
    / "docs/contracts/hazard_handoff/tropical_cyclone_wind_solar_model_v0_1_boundary.md"
)

EXPECTED_FAILURE_UNITS = {
    "PV_FIXED_TILT_MODULE_FIELD",
    "PV_FIXED_TILT_SUPPORT_STRUCTURE",
    "PV_TRACKER_MODULE_FIELD",
    "PV_TRACKER_SBOS_ASSEMBLY",
    "PV_FOUNDATION",
    "PV_POWER_CONVERSION_AND_COLLECTION",
    "PV_GSU_SUBSTATION",
    "PV_SCADA_COMMUNICATIONS",
    "PV_CIVIL_INFRA",
    "PV_REPLACEMENT_SUPPORT",
}
NON_FAILURE_UNIT_VALUE_LABELS = {
    "OUTSIDE_PHYSICAL_CELL",
    "ALL_DIRECT_FAILURE_UNITS",
    "ALL_PHYSICAL_FAILURE_UNITS_AND_SUPPORT",
    "OUTSIDE_INTRINSIC_CURVE",
}
EXPECTED_METRICS = {
    "failure_unit_scalar_dr",
    "scenario_loss_given_value_basis",
    "scalar_eal",
    "pml",
    "var",
    "tvar",
}
ALLOWED_TIERS = {
    "T1_claims_or_field_calibrated",
    "T2_public_lab_standard_or_physics",
    "T3_engineering_proxy_or_adjacent_empirical",
    "T4_placeholder_or_expert_judgment",
}
EXPECTED_SHEETS = [
    "README",
    "Seven_Steps",
    "Asset_Value",
    "Value_Crosswalk",
    "Failure_Units",
    "Candidate_Fragility",
    "Site_Adapter",
    "Legacy_Audit",
    "Claim_Register",
    "Source_Register",
    "Parameter_Tiers",
    "QA_Checks",
]


class ValidationFailure(AssertionError):
    """Raised when the scaffold violates a binding invariant."""


class CheckCounter:
    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, message: str) -> None:
        self.count += 1
        if not condition:
            raise ValidationFailure(message)


CHECKS = CheckCounter()


def require(condition: bool, message: str) -> None:
    CHECKS.require(condition, message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_ids(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames is not None, f"{path}: missing CSV header")
        rows = list(reader)
    require(bool(rows), f"{path}: empty governed CSV")
    for line_number, row in enumerate(rows, start=2):
        require(None not in row, f"{path}:{line_number}: extra CSV fields")
        require(
            all(value is not None for value in row.values()),
            f"{path}:{line_number}: missing CSV field",
        )
    return rows


def validate_schema_subset(instance: Any, schema: Mapping[str, Any], path: str = "$") -> None:
    """Execute every JSON-Schema keyword used by the two selected v1 schemas."""

    expected_type = schema.get("type")
    if expected_type is not None:
        type_checks = {
            "object": lambda value: isinstance(value, dict),
            "array": lambda value: isinstance(value, list),
            "string": lambda value: isinstance(value, str),
            "boolean": lambda value: isinstance(value, bool),
            "number": lambda value: isinstance(value, (int, float))
            and not isinstance(value, bool),
            "integer": lambda value: isinstance(value, int)
            and not isinstance(value, bool),
            "null": lambda value: value is None,
        }
        require(expected_type in type_checks, f"{path}: unsupported schema type {expected_type}")
        require(type_checks[expected_type](instance), f"{path}: expected {expected_type}")

    if "const" in schema:
        require(instance == schema["const"], f"{path}: const mismatch")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            require(key in instance, f"{path}: missing required key {key}")
        for key, child_schema in schema.get("properties", {}).items():
            if key in instance:
                validate_schema_subset(instance[key], child_schema, f"{path}.{key}")

    if isinstance(instance, list) and "items" in schema:
        for index, value in enumerate(instance):
            validate_schema_subset(value, schema["items"], f"{path}[{index}]")


def validate_top_level(
    artifact: Mapping[str, Any], capability: Mapping[str, Any]
) -> None:
    validate_schema_subset(artifact, load_json(BUNDLE_SCHEMA_PATH))
    validate_schema_subset(capability, load_json(CAPABILITY_SCHEMA_PATH))

    require(artifact["cell_id"] == "tropical_cyclone_wind_solar", "cell_id changed")
    require(
        artifact["damage_code_id"] == "TROPICAL_CYCLONE_WIND_SOLAR_PROPOSED_V0_1",
        "damage_code_id changed",
    )
    require(artifact["semantic_damage_model_version"] == "model v0.1", "model changed")
    require(artifact["documentation_revision"] == "docs r1", "docs revision changed")
    require(artifact["package_release"] == "unreleased", "scaffold named a release")
    require(artifact["lifecycle_state"] == "scaffold", "lifecycle is not scaffold")
    require(artifact["promotion_status"] == "proposed", "promotion status changed")
    require(artifact["canonical_runtime_artifact"] is False, "scaffold became canonical")
    require(artifact["curve_records"] == [], "scaffold contains a runtime curve record")
    require(
        artifact["schema_envelope_status"]["selected_schema"]
        == "damage_curve_record_bundle.v1",
        "zero-curve scaffold must stay in the documented v1 envelope",
    )
    require(
        artifact["schema_envelope_status"]["runtime_publication_allowed"] is False,
        "schema exception cannot authorize runtime publication",
    )
    require(capability == artifact["capability_declaration"], "capability copies differ")
    require(capability["cell_id"] == artifact["cell_id"], "capability cell mismatch")
    require(capability["spread_carried"] is False, "scaffold cannot claim spread")
    require(capability["emit_modes_populated_by_cell"] == [], "emit mode unexpectedly populated")
    require(set(capability["metrics_supportable"]) == EXPECTED_METRICS, "metric registry changed")
    require(
        set(capability["metrics_supportable"].values()) == {"withheld"},
        "every metric must be withheld",
    )
    for metric in EXPECTED_METRICS:
        require(
            "NO_RUNTIME_CURVE" in capability["withheld_reason_by_metric"][metric],
            f"{metric}: missing NO_RUNTIME_CURVE",
        )
    require(capability["cap_binding"]["policy"] == "fail_closed", "cap policy changed")
    require(
        capability["cap_binding"]["tolerance_pct"] is None,
        "no-distribution scaffold cannot carry a numeric cap tolerance",
    )


def validate_paths_and_links(artifact: Mapping[str, Any]) -> int:
    ref_fields = [
        "source_dossier",
        "source_workbook",
        "known_answer_tests",
        "source_register",
        "claim_parameter_register",
        "bounded_evidence_search_log",
        "parameter_tier_table_ref",
        "value_crosswalk_ref",
        "site_condition_adapter_ref",
        "pressure_test_ref",
    ]
    for field in ref_fields:
        value = artifact[field]
        require(isinstance(value, str), f"{field}: path must be a string")
        require((ROOT / value).exists(), f"{field}: missing path {value}")
    audit_path = artifact["candidate_fragility_evidence"]["audit_record"]
    require((ROOT / audit_path).exists(), f"candidate audit path missing: {audit_path}")
    require(HANDOFF_PATH.exists(), "Hazard handoff is missing")

    artifact_text = ARTIFACT_PATH.read_text()
    require("01_cells/" not in artifact_text, "artifact contains stale 01_cells path")
    require("Hazard_modeling/" not in artifact_text, "artifact embeds consumer-local path")

    markdown_paths = list(CELL.rglob("*.md")) + [
        HANDOFF_PATH,
        ROOT / "docs/cells/README.md",
        ROOT / "docs/cells/VERSION_REGISTRY.md",
        ROOT / "docs/contracts/hazard_handoff/README.md",
    ]
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    checked = 0
    for markdown_path in markdown_paths:
        for raw_target in link_pattern.findall(markdown_path.read_text()):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            checked += 1
            resolved = (markdown_path.parent / target).resolve()
            require(resolved.exists(), f"{markdown_path}: broken local link {raw_target}")
    return checked


def validate_failure_units_and_value(
    artifact: Mapping[str, Any], value_rows: list[dict[str, str]]
) -> None:
    failure_units = {unit["id"]: unit for unit in artifact["failure_units"]}
    require(len(failure_units) == len(artifact["failure_units"]), "duplicate failure-unit ID")
    require(set(failure_units) == EXPECTED_FAILURE_UNITS, "failure-unit registry changed")
    require(
        all(unit["ordinate_status"] != "zero" for unit in failure_units.values()),
        "withheld unit was converted to zero",
    )

    require(
        failure_units["PV_GSU_SUBSTATION"]["exposure_grain"]
        == "shared_point_or_yard_polygon",
        "GSU exposure grain changed",
    )
    require(
        failure_units["PV_GSU_SUBSTATION"]["ordinate_status"] == "withheld",
        "GSU must remain withheld, not zero",
    )

    require(len(value_rows) == 18, "expected 18 governed Q1-2025 value rows")
    row_ids = [row["row_or_bucket_id"] for row in value_rows]
    require(len(set(row_ids)) == len(row_ids), "duplicate value row ID")
    detail = {row["row_or_bucket_id"]: float(row["value"]) for row in value_rows}
    for row in value_rows:
        require(row["include_in_direct_denominator"] in {"true", "false"}, "invalid value boolean")
        require(float(row["value"]) >= 0, "negative reference value")
        require(
            row["applicable_pathway_ids"] == "tropical_cyclone_wind",
            f"{row['row_or_bucket_id']}: pathway mapping changed",
        )
        mapped_ids = {part.strip() for part in row["failure_unit_id"].split("|")}
        require(
            mapped_ids <= EXPECTED_FAILURE_UNITS | NON_FAILURE_UNIT_VALUE_LABELS,
            f"value row has unknown failure-unit label: {row['failure_unit_id']}",
        )

    expected_values = {
        "SOLAR_VALUE_002_MODULE": 291.21485143992487,
        "SOLAR_VALUE_003_MOUNTING": 109.98972602739727,
        "SOLAR_VALUE_004_FOUNDATION": 31.12448715327472,
        "SOLAR_VALUE_005_INVERTER": 32.306366410372384,
        "SOLAR_VALUE_006_COMBINER": 6.82625,
        "SOLAR_VALUE_007_CABLE": 69.3201119402985,
        "SOLAR_VALUE_008_MV": 106.50466417910448,
        "SOLAR_VALUE_009_GROUNDING": 8.385,
        "SOLAR_VALUE_010_SCADA": 1.31,
        "SOLAR_VALUE_011_NETWORK": 0.0,
        "SOLAR_VALUE_012_SBOS_LABOR": 43.273972602739725,
        "SOLAR_VALUE_013_EBOS_LABOR": 39.447761194029844,
        "SOLAR_VALUE_014_CIVIL": 31.223744292237445,
        "SOLAR_VALUE_015_GENERAL_SUPPORT": 106.86876712328767,
        "SOLAR_VALUE_016_017_EXCLUDED": 242.20429763733296,
        "SOLAR_VALUE_SUMMARY_DIRECT": 656.9814571503722,
        "SOLAR_VALUE_SUMMARY_PHYSICAL": 877.7957023626668,
        "SOLAR_VALUE_SUMMARY_INSTALLED": 1120.0,
    }
    require(set(detail) == set(expected_values), "value row registry changed")
    for row_id, expected in expected_values.items():
        require(
            math.isclose(detail[row_id], expected, rel_tol=0.0, abs_tol=1e-12),
            f"{row_id}: reference value changed",
        )

    direct_ids = [
        "SOLAR_VALUE_002_MODULE",
        "SOLAR_VALUE_003_MOUNTING",
        "SOLAR_VALUE_004_FOUNDATION",
        "SOLAR_VALUE_005_INVERTER",
        "SOLAR_VALUE_006_COMBINER",
        "SOLAR_VALUE_007_CABLE",
        "SOLAR_VALUE_008_MV",
        "SOLAR_VALUE_009_GROUNDING",
        "SOLAR_VALUE_010_SCADA",
    ]
    support_ids = [
        "SOLAR_VALUE_012_SBOS_LABOR",
        "SOLAR_VALUE_013_EBOS_LABOR",
        "SOLAR_VALUE_015_GENERAL_SUPPORT",
    ]
    direct = sum(detail[key] for key in direct_ids)
    civil = detail["SOLAR_VALUE_014_CIVIL"]
    support = sum(detail[key] for key in support_ids)
    excluded = detail["SOLAR_VALUE_016_017_EXCLUDED"]
    physical = direct + civil + support
    installed = physical + excluded
    require(math.isclose(direct, 656.9814571503722, abs_tol=1e-12), "direct value does not reconcile")
    require(math.isclose(physical, 877.7957023626668, abs_tol=1e-12), "physical value does not reconcile")
    require(math.isclose(installed, 1120.0, abs_tol=1e-12), "installed value does not reconcile")
    require(
        value_rows[6]["failure_unit_id"] == "PV_GSU_SUBSTATION",
        "MV/substation row no longer maps to the separate GSU unit",
    )
    basis = artifact["value_basis"]
    require(math.isclose(basis["direct_hardware"], direct, abs_tol=1e-12), "artifact direct value mismatch")
    require(math.isclose(basis["civil_mixed_row"], civil, abs_tol=1e-12), "artifact civil mismatch")
    require(math.isclose(basis["replacement_support"], support, abs_tol=1e-12), "artifact support mismatch")
    require(math.isclose(basis["physical_reference"], physical, abs_tol=1e-12), "artifact physical mismatch")
    require(math.isclose(basis["installed_reference"], installed, abs_tol=1e-12), "artifact installed mismatch")
    require(
        math.isclose(
            basis["module_plus_mounting_candidate_subtotal"],
            detail["SOLAR_VALUE_002_MODULE"] + detail["SOLAR_VALUE_003_MOUNTING"],
            abs_tol=1e-12,
        ),
        "artifact module+mounting subtotal mismatch",
    )


def validate_registers(
    source_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    parameter_rows: list[dict[str, str]],
    value_rows: list[dict[str, str]],
) -> None:
    source_ids = {row["source_id"] for row in source_rows}
    require(len(source_ids) == len(source_rows), "duplicate source ID")
    require(len(source_ids) == 19, "source register count changed")
    require(len({row["claim_id"] for row in claim_rows}) == len(claim_rows), "duplicate claim ID")
    require(len(claim_rows) == 30, "claim register count changed")
    require(
        len({row["parameter"] for row in parameter_rows}) == len(parameter_rows),
        "duplicate parameter ID",
    )
    require(len(parameter_rows) == 47, "parameter-tier count changed")
    for row in claim_rows:
        require(row["evidence_tier"] in ALLOWED_TIERS, f"{row['claim_id']}: invalid tier")
        require(row["exact_locator"], f"{row['claim_id']}: missing locator")
        require(row["permitted_inference"], f"{row['claim_id']}: missing permitted inference")
        require(row["prohibited_inference"], f"{row['claim_id']}: missing prohibited inference")
        unresolved = split_ids(row["source_ids"]) - source_ids
        require(not unresolved, f"{row['claim_id']}: unresolved sources {sorted(unresolved)}")
    for row in parameter_rows:
        require(row["tier"] in ALLOWED_TIERS, f"{row['parameter']}: invalid tier")
        unresolved = split_ids(row["source_ids"]) - source_ids
        require(not unresolved, f"{row['parameter']}: unresolved sources {sorted(unresolved)}")
    for row in value_rows:
        require(
            row["value_source_id"] == "NLR_Q1_2025_UPV_PV_ONLY_2024_USD",
            f"{row['row_or_bucket_id']}: value-source alias changed",
        )
    require("TCWS-S013" in source_ids, "governed parent value source is missing")


def walk_values(value: Any):
    if isinstance(value, dict):
        for child in value.values():
            yield from walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_values(child)
    else:
        yield value


def validate_known_answers(kats: Mapping[str, Any]) -> None:
    require(kats["cell_id"] == "tropical_cyclone_wind_solar", "KAT cell mismatch")
    require(kats["runtime_curve_count"] == 0, "KAT runtime curve count changed")
    require(kats["runtime_curve_known_answer_tests"] == [], "runtime curve KATs must be empty")
    tests = kats["tests"]
    require(len(tests) == 16, "expected 16 fail-closed contract tests")
    require(len({test["test_id"] for test in tests}) == len(tests), "duplicate KAT ID")
    test_ids = {test["test_id"] for test in tests}
    require(
        {
            "TCWS_VALID_NHC_UPSTREAM_WITHHOLDS",
            "TCWS_FIXED_TILT_COMPLETE_SITE_STILL_WITHHOLDS",
            "TCWS_TRACKER_QUALIFIED_STATE_STILL_WITHHOLDS",
            "TCWS_STRONG_WIND_PATHWAY_REJECTS",
            "TCWS_CEFERINO_CROSS_AXIS_REJECTS",
            "TCWS_UNKNOWN_TRACKER_STATE_NO_CREDIT",
            "TCWS_WHOLE_PLANT_EXPOSURE_DEFAULT_REJECTS",
            "TCWS_UNMODELED_GSU_WITHHELD_NOT_ZERO",
        }
        <= test_ids,
        "required solar/GSU fail-closed KAT coverage is missing",
    )
    for test in tests:
        expected = test["expected_output"]
        for metric in EXPECTED_METRICS:
            if metric not in expected:
                continue
            metric_result = expected[metric]
            require(isinstance(metric_result, dict), f"{test['test_id']}: malformed metric result")
            require(metric_result.get("value") is None, f"{test['test_id']}: numeric metric leaked")
        numeric_expected = [
            value
            for value in walk_values(expected)
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        ]
        require(not numeric_expected, f"{test['test_id']}: numeric expected output leaked")


def validate_candidate_isolation_and_math(artifact: Mapping[str, Any]) -> None:
    candidate = artifact["candidate_fragility_evidence"]
    require(candidate["status"] == "audit_only_not_runtime_shaped", "candidate status changed")
    require(candidate["numeric_values_embedded"] is False, "candidate numbers embedded in artifact")
    require(candidate["runtime_enabled"] is False, "candidate enabled for runtime")
    require(
        candidate["primary_candidate"] == "CEFERINO_GROUND_MOUNT_EXTENSIVE_FAILURE",
        "primary audit candidate changed",
    )
    require(set(candidate["source_ids"]) == {"TCWS-S002", "TCWS-S003", "TCWS-S004"}, "candidate source set changed")
    require("parameters" not in candidate, "candidate contains runtime-shaped parameters")
    require("valid_range" not in candidate, "candidate contains runtime-shaped valid range")

    speeds = [73.0, 83.0, 90.0, 100.0, 116.0]
    v_median = 90.0
    beta_median = 0.15
    probabilities = [
        0.5
        * (
            1.0
            + math.erf(
                (math.log(speed) - math.log(v_median))
                / (beta_median * math.sqrt(2.0))
            )
        )
        for speed in speeds
    ]
    require(all(0 <= value <= 1 for value in probabilities), "Ceferino diagnostic out of bounds")
    require(probabilities == sorted(probabilities), "Ceferino diagnostic is not monotone")
    require(math.isclose(probabilities[2], 0.5), "Ceferino median diagnostic check failed")
    require(probabilities[0] < 0.10 and probabilities[-1] > 0.90, "Ceferino fixture range changed")

    def anchored_logistic(L: float, k: float, x0: float, x: float) -> float:
        raw = L / (1.0 + math.exp(-k * (x - x0)))
        base = L / (1.0 + math.exp(-k * (0.0 - x0)))
        return max(raw - base, 0.0)

    pv_stow = (0.85, 0.055, 148.0)
    pv_midtilt = (0.95, 0.065, 115.0)
    mounting = (0.80, 0.055, 120.0)
    substation = (0.80, 0.040, 120.0)

    def legacy_asset_dr(x: float, pv: tuple[float, float, float]) -> float:
        return (
            0.35 * anchored_logistic(*pv, x)
            + 0.15 * anchored_logistic(*mounting, x)
            + 0.08 * anchored_logistic(*substation, x)
        )

    require(math.isclose(legacy_asset_dr(90.0, pv_stow), 0.045140, abs_tol=5e-7), "legacy 90-mph fixture changed")
    require(math.isclose(legacy_asset_dr(180.0, pv_stow), 0.427466, abs_tol=5e-7), "legacy 180-mph fixture changed")
    require(math.isclose(legacy_asset_dr(300.0, pv_stow), 0.480604, abs_tol=5e-7), "legacy 300-mph fixture changed")
    require(
        legacy_asset_dr(150.0, pv_midtilt) > legacy_asset_dr(150.0, pv_stow),
        "legacy mid-tilt sensitivity ordering changed",
    )
    require(math.isclose(0.35 + 0.15 + 0.08 + 0.42, 1.0), "legacy TIV weights no longer reconcile")

    audit_text = (
        PROPOSED
        / "NUMERICAL_CANDIDATE_AUDIT_tropical_cyclone_wind_solar__model_v0_1__docs_r1.md"
    ).read_text()
    require("median-parameter diagnostic" in audit_text, "posterior diagnostic caveat is missing")
    require("P(more than 50% panels" in audit_text, "candidate endpoint guardrail is missing")
    require("REJECT_RUNTIME_RETAIN_REGRESSION" in audit_text, "legacy rejection is missing")


def validate_workbook() -> None:
    require(WORKBOOK_PATH.exists(), "governed workbook is missing")
    require(zipfile.is_zipfile(WORKBOOK_PATH), "workbook is not a valid ZIP/XLSX")
    with zipfile.ZipFile(WORKBOOK_PATH) as archive:
        require(archive.testzip() is None, "workbook ZIP contains a corrupt member")
        workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
        sheets = [
            html.unescape(name)
            for name in re.findall(
                r"<(?:[A-Za-z_][\w.-]*:)?sheet\b[^>]*\bname=\"([^\"]+)\"",
                workbook_xml,
            )
        ]
        require(sheets == EXPECTED_SHEETS, "workbook sheet manifest changed")
        worksheet_xml = "\n".join(
            archive.read(name).decode("utf-8")
            for name in archive.namelist()
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        )
        qa_xml = archive.read("xl/worksheets/sheet12.xml").decode("utf-8")
    require(
        "NORM.S.DIST((LN(H$5)-LN($D6))/$E6,TRUE)" in worksheet_xml,
        "Ceferino diagnostic formula lost visible source-native fixtures",
    )
    require("0.35*MAX($B$5/" in worksheet_xml, "legacy weighted stow formula is missing")
    require(
        "ABS('Asset_Value'!B16-C5)" in worksheet_xml,
        "QA formula lost quoted cross-sheet reference",
    )
    require(qa_xml.count(">PASS<") == 13, "not every workbook QA assertion is cached PASS")
    require(
        not any(token in worksheet_xml for token in ["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"]),
        "workbook contains a formula error token",
    )


def validate_index_absence() -> None:
    index = load_json(ARTIFACT_INDEX_PATH)
    matching = [
        row for row in index["artifacts"]
        if (ROOT / row["path"]).resolve() == ARTIFACT_PATH.resolve()
    ]
    require(not matching, "noncanonical v0.1 scaffold appears in runtime artifact index")


def main() -> int:
    artifact = load_json(ARTIFACT_PATH)
    capability = load_json(CAPABILITY_PATH)
    kats = load_json(KAT_PATH)
    source_rows = read_csv(SOURCE_PATH)
    claim_rows = read_csv(CLAIM_PATH)
    parameter_rows = read_csv(PARAMETER_PATH)
    value_rows = read_csv(VALUE_PATH)

    validate_top_level(artifact, capability)
    local_link_count = validate_paths_and_links(artifact)
    validate_registers(source_rows, claim_rows, parameter_rows, value_rows)
    validate_failure_units_and_value(artifact, value_rows)
    validate_known_answers(kats)
    validate_candidate_isolation_and_math(artifact)
    validate_workbook()
    validate_index_absence()

    print("PASS tropical_cyclone_wind_solar model v0.1/docs r1 scaffold")
    print(f"checks={CHECKS.count}")
    print(
        "counts="
        f"sources:{len(source_rows)},claims:{len(claim_rows)},"
        f"parameters:{len(parameter_rows)},value_rows:{len(value_rows)},"
        f"failure_units:{len(artifact['failure_units'])},kats:{len(kats['tests'])},"
        f"workbook_sheets:{len(EXPECTED_SHEETS)},local_links:{local_link_count}"
    )
    for label, path in [
        ("artifact_sha256", ARTIFACT_PATH),
        ("capability_sha256", CAPABILITY_PATH),
        ("kat_sha256", KAT_PATH),
        ("workbook_sha256", WORKBOOK_PATH),
    ]:
        print(f"{label}={sha256(path)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationFailure, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
