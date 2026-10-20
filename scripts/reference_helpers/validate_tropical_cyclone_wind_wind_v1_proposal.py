#!/usr/bin/env python3
"""Validate the preserved noncanonical TC-wind × wind model-v1 proposal.

Checks the proposed bundle-v3 curve-form extension, exact Jaimes Eq. 1
implementation, selector/range/value fail-closed behavior, governed registers,
known answers, workbook structure, links, and isolation from the canonical
current copy. The validator is dependency-free except for optional JSON
Schema execution when ``jsonschema`` and ``referencing`` are available.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable, Mapping
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
PROPOSED = ROOT / "docs/cells/tropical_cyclone_wind_wind/proposed"
ARTIFACT = PROPOSED / "tropical_cyclone_wind_wind__model_v1_0__docs_r1__curve_artifact.json"
CAPABILITY = PROPOSED / "tropical_cyclone_wind_wind__model_v1_0__docs_r1__capability.json"
KATS = PROPOSED / "known_answer_tests_tropical_cyclone_wind_wind__model_v1_0__docs_r1.json"
SOURCES = PROPOSED / "SOURCE_REGISTER_tropical_cyclone_wind_wind__model_v1_0__docs_r1.csv"
CLAIMS = PROPOSED / "CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_wind__model_v1_0__docs_r1.csv"
PARAMETERS = PROPOSED / "PARAMETER_TIER_TABLE_tropical_cyclone_wind_wind__model_v1_0__docs_r1.csv"
VALUES = PROPOSED / "VALUE_CROSSWALK_tropical_cyclone_wind_wind__model_v1_0__docs_r1.csv"
WORKBOOK = PROPOSED / "damage_curve_records_tropical_cyclone_wind_wind__model_v1_0__docs_r1.xlsx"
INDEX = ROOT / "docs/contracts/machine_readable_artifact_index.json"
BUNDLE_SCHEMA = ROOT / "docs/contracts/schemas/curve_artifact_bundle.v3.schema.json"
CAPABILITY_SCHEMA = ROOT / "docs/contracts/schemas/capability_declaration.v3.schema.json"
EMIT_SCHEMA = ROOT / "docs/contracts/schemas/damage_emit.v2.schema.json"
V0_VALIDATOR = ROOT / "scripts/reference_helpers/validate_tropical_cyclone_wind_wind_v0_1_scaffold.py"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tropical_cyclone_wind_wind_curve_eval import (  # noqa: E402
    TropicalCycloneWindEvaluationError,
    artifact_sha256,
    evaluate_damage_call,
    evaluate_thresholded_weibull_expected_damage_record,
    verify_artifact_pin,
)


EXPECTED_CURVES = {
    "TCWW_JAIMES_GENERIC_1MW_HH44_V1": (
        "TCWW_JAIMES_1MW_44M_SCREENING",
        1.0,
        44.0,
        50.0,
        106.77,
        8.94,
        196.77,
    ),
    "TCWW_JAIMES_GENERIC_2P5MW_HH80_V1": (
        "TCWW_JAIMES_2P5MW_80M_SCREENING",
        2.5,
        80.0,
        90.0,
        82.52,
        4.54,
        172.52,
    ),
    "TCWW_JAIMES_GENERIC_3P3MW_HH100_V1": (
        "TCWW_JAIMES_3P3MW_100M_SCREENING",
        3.3,
        100.0,
        114.0,
        73.30,
        4.99,
        163.30,
    ),
}
EXPECTED_SHEETS = [
    "README",
    "Scope_Coverage",
    "Inputs",
    "Jaimes_Curves",
    "Failure_Units",
    "Value_Crosswalk",
    "Old_vs_New",
    "KATs",
    "Source_Register",
    "Claim_Register",
    "Parameter_Tiers",
    "QA",
]
ALLOWED_TIERS = {
    "T1_claims_or_field_calibrated",
    "T2_public_lab_standard_or_physics",
    "T3_engineering_proxy_or_adjacent_empirical",
    "T4_placeholder_or_expert_judgment",
}


class ValidationFailure(AssertionError):
    pass


class Counter:
    def __init__(self) -> None:
        self.value = 0

    def require(self, condition: bool, message: str) -> None:
        self.value += 1
        if not condition:
            raise ValidationFailure(message)


CHECKS = Counter()


def require(condition: bool, message: str) -> None:
    CHECKS.require(condition, message)


def close(actual: float, expected: float, tolerance: float, message: str) -> None:
    require(
        math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance),
        f"{message}: expected {expected!r}, got {actual!r}",
    )


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_ids(value: str) -> set[str]:
    return {item.strip() for item in value.split(";") if item.strip()}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames is not None, f"{path}: missing header")
        result = list(reader)
    require(result, f"{path}: empty CSV")
    for line_number, row in enumerate(result, start=2):
        require(None not in row, f"{path}:{line_number}: extra fields")
        require(
            all(value is not None for value in row.values()),
            f"{path}:{line_number}: missing field",
        )
    return result


def optional_schema_checks(
    artifact: Mapping[str, Any], capability: Mapping[str, Any]
) -> str:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ModuleNotFoundError:
        return "jsonschema unavailable; semantic checks executed"

    schemas = [load(BUNDLE_SCHEMA), load(CAPABILITY_SCHEMA), load(EMIT_SCHEMA)]
    registry = Registry().with_resources(
        [(schema["$id"], Resource.from_contents(schema)) for schema in schemas]
    )
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    capability_validator = Draft202012Validator(schemas[1], registry=registry)
    bundle_validator = Draft202012Validator(schemas[0], registry=registry)
    emit_validator = Draft202012Validator(schemas[2], registry=registry)
    capability_validator.validate(capability)
    bundle_validator.validate(artifact)
    emit = evaluate_damage_call(
        artifact,
        {
            "pathway_id": "tropical_cyclone_wind",
            "failure_unit_id": "WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT",
            "turbine_archetype_id": "TCWW_JAIMES_GENERIC_3P3MW_HH100_V1",
            "source_model_assumption_set_id": "JAIMES_2020_GENERIC_FIXED_BASE_STEEL_PARKED_ROTOR_AS_DOCUMENTED",
            "tc_peak_gust_3s_10m_kmh": 180,
        },
    )
    emit_validator.validate(emit)

    # The schema must reject a silently renamed parameter and missing selector.
    broken = json.loads(json.dumps(artifact))
    parameters = broken["pathways"][0]["curve_records"][0]["parameters"]
    parameters["V50_kmh"] = parameters.pop("delta_V50_kmh")
    require(
        bool(list(bundle_validator.iter_errors(broken))),
        "bundle schema accepted a renamed Eq. 1 parameter",
    )
    broken = json.loads(json.dumps(artifact))
    broken["pathways"][0]["curve_records"][0].pop("selector_match")
    require(
        bool(list(bundle_validator.iter_errors(broken))),
        "bundle schema accepted a curve without selector_match",
    )
    return "bundle v3/capability v3/emit v2 executed; two negative schema tests passed"


def validate_top_level(
    artifact: Mapping[str, Any], capability: Mapping[str, Any]
) -> None:
    require(artifact["schema_version"] == "damage_curve_record_bundle.v3", "bundle v3 required")
    require(artifact["schema_status"] == "proposed_draft", "schema status changed")
    require(artifact["cell_id"] == "tropical_cyclone_wind_wind", "cell changed")
    require(artifact["semantic_damage_model_version"] == "model v1.0", "model changed")
    require(artifact["documentation_revision"] == "docs r1", "docs changed")
    require(artifact["promotion_status"] == "proposed", "proposal status changed")
    require(artifact["canonical_runtime_artifact"] is False, "proposal became canonical")
    require(artifact["package_inclusion_status"] == "not_included", "package inclusion changed")
    require(artifact["model_grade"] == "screening_source_derived_engineering_proxy", "grade changed")
    require(capability == artifact["capability_declaration"], "capability copies differ")
    require(capability["schema_version"] == "capability_declaration.v3", "capability v3 required")
    require(capability["canonical_runtime_artifact"] is False, "capability became canonical")
    require(capability["promotion_gate"]["status"] == "blocked", "promotion gate must remain blocked")
    require(artifact["emit_contract"]["schema_version"] == "damage_emit.v2", "emit v2 required")


def validate_paths(artifact: Mapping[str, Any], allow_incomplete: bool) -> list[str]:
    missing: list[str] = []
    for field in (
        "source_dossier",
        "source_workbook",
        "known_answer_tests",
        "source_register",
        "claim_parameter_register",
        "value_crosswalk",
    ):
        value = artifact[field]
        require(isinstance(value, str) and value.startswith("docs/"), f"{field}: bad path")
        path = ROOT / value
        if path.exists():
            continue
        if allow_incomplete and field in {"source_dossier", "source_workbook"}:
            missing.append(value)
            continue
        raise ValidationFailure(f"missing required path: {value}")
    return missing


def validate_schema_extension() -> None:
    schema = load(BUNDLE_SCHEMA)
    definition = schema["$defs"]["thresholdedWeibullExpectedDamageRecord"]
    require(
        definition["properties"]["curve_form"]["const"]
        == "thresholded_weibull_expected_damage",
        "curve-form schema extension missing",
    )
    required_parameters = set(
        definition["properties"]["parameters"]["required"]
    )
    require(
        required_parameters
        == {"V_zero_kmh", "delta_V50_kmh", "rho", "V_at_DR50_kmh", "max_dr"},
        "Eq. 1 parameter schema drifted",
    )
    selector_required = set(
        definition["properties"]["selector_match"]["required"]
    )
    require(
        selector_required
        == {"turbine_archetype_id", "rated_power_mw", "hub_height_m", "rotor_diameter_m"},
        "selector schema drifted",
    )


def validate_curves(artifact: Mapping[str, Any]) -> None:
    pathways = artifact["pathways"]
    require(len(pathways) == 1, "expected one pathway")
    pathway = pathways[0]
    require(pathway["pathway_id"] == "tropical_cyclone_wind", "pathway changed")
    axis = pathway["hazard_axis"]
    require(axis["id"] == "TC_PEAK_GUST_3S_10M_KMH_JAIMES", "axis ID changed")
    require(axis["preferred_input_field"] == "tc_peak_gust_3s_10m_kmh", "axis field changed")
    require(axis["unit"] == "km/h", "axis unit changed")
    require(axis["source_simulation_range"] == [108, 252], "simulation range changed")
    require(axis["valid_range"] == [0, 252], "axis envelope changed")
    selector = pathway["selector_logic"][0]
    require(selector["default"] is None, "selector default prohibited")
    require(set(selector["allowed"]) == set(EXPECTED_CURVES), "selector set changed")
    require(selector["interpolation"] == "prohibited", "selector interpolation enabled")
    records = pathway["curve_records"]
    require(len(records) == 3, "expected three source-family records")
    by_selector = {
        record["selector_match"]["turbine_archetype_id"]: record
        for record in records
    }
    require(len(by_selector) == 3 and set(by_selector) == set(EXPECTED_CURVES), "selector records mismatch")
    for selector_id, expected in EXPECTED_CURVES.items():
        curve_id, power, hub, rotor, delta, rho, d50 = expected
        record = by_selector[selector_id]
        require(record["curve_id"] == curve_id, f"{selector_id}: curve ID changed")
        require(record["failure_unit_id"] == "WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT", "wrong atom")
        require(record["curve_form"] == "thresholded_weibull_expected_damage", "wrong form")
        match = record["selector_match"]
        close(float(match["rated_power_mw"]), power, 1e-12, f"{selector_id}: power")
        close(float(match["hub_height_m"]), hub, 1e-12, f"{selector_id}: hub")
        close(float(match["rotor_diameter_m"]), rotor, 1e-12, f"{selector_id}: rotor")
        parameters = record["parameters"]
        close(float(parameters["V_zero_kmh"]), 90.0, 1e-12, "V_zero")
        close(float(parameters["delta_V50_kmh"]), delta, 1e-12, "delta V50")
        close(float(parameters["rho"]), rho, 1e-12, "rho")
        close(float(parameters["V_at_DR50_kmh"]), d50, 1e-12, "absolute D50")
        close(
            evaluate_thresholded_weibull_expected_damage_record(record, d50),
            0.5,
            1e-12,
            f"{selector_id}: half damage",
        )
        previous = -1.0
        for index in range((252 - 108) * 4 + 1):
            speed = 108 + index / 4
            value = evaluate_thresholded_weibull_expected_damage_record(record, speed)
            require(math.isfinite(value), f"{selector_id}: nonfinite")
            require(0 <= value <= 1, f"{selector_id}: outside [0,1]")
            require(value + 1e-14 >= previous, f"{selector_id}: nonmonotone")
            previous = value


def result_for_request(emit: Mapping[str, Any], failure_unit_id: str) -> Mapping[str, Any]:
    matches = [
        result
        for result in emit["failure_unit_results"]
        if result["failure_unit_id"] == failure_unit_id
    ]
    require(len(matches) == 1, f"{failure_unit_id}: result not unique")
    return matches[0]


def validate_kats(artifact: Mapping[str, Any]) -> tuple[int, int]:
    kats = load(KATS)
    require(kats["schema_version"] == "known_answer_tests.v3", "KAT schema changed")
    require(kats["semantic_damage_model_version"] == "model v1.0", "KAT model changed")
    tolerance = float(kats["absolute_tolerance"])
    for test in kats["formula_known_answer_tests"]:
        emit = evaluate_damage_call(artifact, test["input"])
        result = result_for_request(emit, test["input"]["failure_unit_id"])
        expected = test["expected"]
        require(result["status"] == expected["status"], f"{test['test_id']}: status")
        require(result["curve_id"] == expected["curve_id"], f"{test['test_id']}: curve")
        close(
            float(result["scalar_central_dr"]),
            float(expected["failure_unit_damage_ratio"]),
            tolerance,
            test["test_id"],
        )

    for test in kats["contract_tests"]:
        expected = test["expected"]
        if expected.get("status") == "rejected":
            try:
                evaluate_damage_call(artifact, test["input"])
            except TropicalCycloneWindEvaluationError as exc:
                require(exc.code == expected["error_code"], f"{test['test_id']}: error code {exc.code}")
            else:
                raise ValidationFailure(f"{test['test_id']}: expected rejection")
            continue

        emit = evaluate_damage_call(artifact, test["input"])
        failure_unit_id = test["input"].get(
            "failure_unit_id", "WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT"
        )
        result = result_for_request(emit, failure_unit_id)
        if "status" in expected:
            require(result["status"] == expected["status"], f"{test['test_id']}: status")
        if "failure_unit_damage_ratio" in expected:
            require(
                result["scalar_central_dr"] == expected["failure_unit_damage_ratio"],
                f"{test['test_id']}: scalar result",
            )
        expected_reasons = expected.get("reason_codes", expected.get("reason_codes_include", []))
        require(
            set(expected_reasons) <= set(result.get("withheld_reason_codes", [])),
            f"{test['test_id']}: reason codes",
        )
        required_flags = expected.get("metadata_flags_include", [])
        require(
            set(required_flags) <= set(result.get("metadata_flags", [])),
            f"{test['test_id']}: metadata flags",
        )
        if "failure_unit_scalar_dr_status" in expected:
            require(result["status"] == expected["failure_unit_scalar_dr_status"], f"{test['test_id']}: scalar status")
            require(emit["input_quality"]["scenario_loss_status"] == "withheld", f"{test['test_id']}: scenario loss")
            require(
                expected["error_code"]
                in {
                    "SOURCE_DENOMINATOR_CROSSWALK_NOT_APPROVED",
                    "NONCANONICAL_PROPOSAL_NO_SCENARIO_LOSS",
                },
                f"{test['test_id']}: unknown scenario withhold code",
            )
        if "control_credit_applied" in expected:
            require(expected["control_credit_applied"] is False, "control credit fixture changed")

    return len(kats["formula_known_answer_tests"]), len(kats["contract_tests"])


def validate_capability(artifact: Mapping[str, Any]) -> None:
    capability = artifact["capability_declaration"]
    pathways = capability["pathway_capabilities"]
    require(len(pathways) == 1, "expected one capability pathway")
    item = pathways[0]
    require(item["failure_unit_scalar_dr"] == "conditional", "scalar capability changed")
    require(item["scenario_loss_given_value_basis"] == "withheld", "scenario loss enabled")
    require(item["curve_intrinsic_spread"] == "not_carried", "spread capability changed")
    withheld = {row["failure_unit_id"] for row in item["withheld_failure_units"]}
    expected = {unit["id"] for unit in artifact["failure_units"]} - {
        "WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT"
    }
    require(withheld == expected, "withheld-unit capability does not cover every other unit")
    annual = capability["consumer_annual_metrics"]
    require(annual["status_before_promotion"] == "withheld_noncanonical_proposal", "pre-promotion status")
    require(annual["status_after_promotion"] == "withheld", "annual metrics unexpectedly enabled")


def validate_registers(artifact: Mapping[str, Any]) -> tuple[int, int, int, int]:
    source_rows = rows(SOURCES)
    claim_rows = rows(CLAIMS)
    parameter_rows = rows(PARAMETERS)
    value_rows = rows(VALUES)
    source_ids = {row["source_id"] for row in source_rows}
    require(len(source_ids) == len(source_rows) and len(source_rows) >= 10, "source registry")
    for row in source_rows:
        require(row["evidence_tier"] in ALLOWED_TIERS, f"{row['source_id']}: bad tier")
        require(row["exact_locator"] and row["permitted_inference"] and row["prohibited_inference"], f"{row['source_id']}: incomplete")
    claim_ids = {row["claim_id"] for row in claim_rows}
    require(len(claim_ids) == len(claim_rows) and len(claim_rows) >= 18, "claim registry")
    for row in claim_rows:
        require(not (split_ids(row["source_ids"]) - source_ids), f"{row['claim_id']}: unresolved sources")
        require(row["evidence_tier"] in ALLOWED_TIERS, f"{row['claim_id']}: bad tier")
    require(len(parameter_rows) >= 20, "parameter table too small")
    for row in parameter_rows:
        require(not (split_ids(row["source_ids"]) - source_ids), f"{row['parameter']}: unresolved sources")
        require(row["tier"] in ALLOWED_TIERS, f"{row['parameter']}: bad tier")
    for row in value_rows:
        float(row["value"])
        require(row["status"] and row["double_count_guardrail"], "value row incomplete")
    embedded_sources: set[str] = set()
    for item in artifact["parameter_tier_table"]:
        embedded_sources.update(item["source_ids"])
    require(not (embedded_sources - source_ids), f"unresolved artifact sources {sorted(embedded_sources-source_ids)}")

    source_value_rows = [row for row in value_rows if row["value_source_id"] == "JAIMES_CT_H"]
    require(len(source_value_rows) == 3, "source-native value rows changed")
    expected_by_id = {
        "JAIMES_VALUE_1MW_HH44": (44.0, 1281322.377752261),
        "JAIMES_VALUE_2P5MW_HH80": (80.0, 3803630.4553727144),
        "JAIMES_VALUE_3P3MW_HH100": (100.0, 5709190.569869134),
    }
    for row in source_value_rows:
        height, expected = expected_by_id[row["row_or_bucket_id"]]
        close(float(row["value"]), 1307.9 * height**1.82, 1e-6, row["row_or_bucket_id"])
        close(float(row["value"]), expected, 1e-6, row["row_or_bucket_id"])
    require(artifact["value_linkage"]["implicit_default_profile"] is None, "implicit value default")
    require(artifact["value_linkage"]["scenario_loss_status"] == "withheld", "scenario loss enabled")
    return len(source_rows), len(claim_rows), len(parameter_rows), len(value_rows)


def workbook_inventory(path: Path) -> tuple[list[str], int, list[str]]:
    with zipfile.ZipFile(path) as archive:
        workbook_root = ET.fromstring(archive.read("xl/workbook.xml"))
        namespace = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        relationship_namespace = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        sheet_nodes = workbook_root.findall("m:sheets/m:sheet", namespace)
        sheet_names = [node.attrib["name"] for node in sheet_nodes]
        formula_count = 0
        for name in archive.namelist():
            if not name.startswith("xl/worksheets/sheet") or not name.endswith(".xml"):
                continue
            root = ET.fromstring(archive.read(name))
            formula_count += len(root.findall(".//m:f", namespace))

        rel_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rels = {
            node.attrib["Id"]: node.attrib["Target"]
            for node in rel_root
        }
        qa_node = next(node for node in sheet_nodes if node.attrib["name"] == "QA")
        qa_target = rels[qa_node.attrib[f"{{{relationship_namespace}}}id"]]
        qa_path = qa_target.lstrip("/")
        if not qa_path.startswith("xl/"):
            qa_path = f"xl/{qa_path}"
        qa_root = ET.fromstring(archive.read(qa_path))
        qa_values = {
            cell.attrib["r"]: (cell.findtext("m:v", default="", namespaces=namespace))
            for cell in qa_root.findall(".//m:c", namespace)
        }
        qa_results = [qa_values.get(f"B{row_number}", "") for row_number in range(5, 25)]
    return sheet_names, formula_count, qa_results


def validate_workbook(allow_incomplete: bool) -> tuple[int, int, int]:
    if not WORKBOOK.exists():
        if allow_incomplete:
            return 0, 0, 0
        raise ValidationFailure(f"workbook missing: {WORKBOOK}")
    names, formulas, qa_results = workbook_inventory(WORKBOOK)
    require(names == EXPECTED_SHEETS, f"workbook sheet order changed: {names}")
    require(formulas >= 35, f"workbook has too few formulas: {formulas}")
    require(len(qa_results) == 20, f"workbook QA result count changed: {len(qa_results)}")
    for row_number, result in enumerate(qa_results, start=5):
        require(result == "PASS", f"workbook QA!B{row_number} is {result!r}, expected 'PASS'")
    return len(names), formulas, len(qa_results)


def iter_markdown_links(text: str) -> Iterable[str]:
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        if target and not re.match(r"^[a-z]+://", target) and not target.startswith("mailto:"):
            yield target


def validate_local_links(allow_incomplete: bool) -> int:
    count = 0
    for path in [
        PROPOSED / "README_tropical_cyclone_wind_wind__model_v1_0__docs_r1.md",
        PROPOSED / "tropical_cyclone_wind_wind_curve_derivation_dossier__model_v1_0__docs_r1.md",
        PROPOSED / "tropical_cyclone_wind_wind_damage_code_metadata_spec__model_v1_0__docs_r1.md",
        PROPOSED / "CHANGE_CLASSIFICATION_tropical_cyclone_wind_wind__model_v1_0__docs_r1.md",
        PROPOSED / "PROMOTION_GATE_MATRIX_tropical_cyclone_wind_wind__model_v1_0__docs_r1.md",
        PROPOSED / "workbook_sheet_manifest_tropical_cyclone_wind_wind__model_v1_0__docs_r1.md",
    ]:
        if not path.exists():
            if allow_incomplete:
                continue
            raise ValidationFailure(f"documentation missing: {path}")
        for target in iter_markdown_links(path.read_text()):
            count += 1
            resolved = (path.parent / target).resolve()
            require(resolved.exists(), f"dangling link in {path.name}: {target}")
    return count


def validate_index() -> None:
    index = load(INDEX)
    require(index["schema_version"] == "damage_curve_artifact_index.v2", "index schema changed")
    matches = [item for item in index["artifacts"] if item["cell_id"] == "tropical_cyclone_wind_wind"]
    require(len(matches) == 1, "expected one canonical TC-wind current entry")
    row = matches[0]
    require("/current/" in row["path"], "canonical TC-wind entry does not point to current")
    require("/proposed/" not in row["path"], "noncanonical proposal entered the canonical index")
    current_path = ROOT / row["path"]
    require(current_path.exists(), "canonical TC-wind current artifact is missing")
    current = load(current_path)
    require(current["canonical_runtime_artifact"] is True, "indexed TC-wind artifact is not canonical")
    require(
        current["semantic_damage_model_version"] != load(ARTIFACT)["semantic_damage_model_version"],
        "model-v1.0 proposal became the current TC-wind model",
    )
    require(artifact_sha256(current_path) == row["sha256"], "canonical TC-wind index SHA mismatch")


def main() -> None:
    allow_incomplete = "--allow-incomplete" in sys.argv[1:]
    artifact = load(ARTIFACT)
    capability = load(CAPABILITY)
    validate_top_level(artifact, capability)
    missing = validate_paths(artifact, allow_incomplete)
    validate_schema_extension()
    schema_note = optional_schema_checks(artifact, capability)
    validate_curves(artifact)
    validate_capability(artifact)
    formula_kats, contract_kats = validate_kats(artifact)
    source_count, claim_count, parameter_count, value_count = validate_registers(artifact)
    sheet_count, formula_count, workbook_qa_count = validate_workbook(allow_incomplete)
    link_count = validate_local_links(allow_incomplete)
    validate_index()

    digest = artifact_sha256(ARTIFACT)
    verify_artifact_pin(
        artifact,
        {
            "cell_id": artifact["cell_id"],
            "semantic_damage_model_version": artifact["semantic_damage_model_version"],
            "documentation_revision": artifact["documentation_revision"],
            "schema_version": artifact["schema_version"],
            "artifact_sha256": digest,
        },
        artifact_sha256_hex=digest,
    )
    try:
        verify_artifact_pin(
            artifact,
            {
                "cell_id": artifact["cell_id"],
                "semantic_damage_model_version": artifact["semantic_damage_model_version"],
                "documentation_revision": artifact["documentation_revision"],
                "schema_version": artifact["schema_version"],
                "artifact_sha256": "0" * 64,
            },
            artifact_sha256_hex=digest,
        )
    except TropicalCycloneWindEvaluationError as exc:
        require(exc.code == "ARTIFACT_PIN_MISMATCH", "bad pin error changed")
    else:
        raise ValidationFailure("bad artifact pin was accepted")

    print("PASS preserved tropical_cyclone_wind_wind model v1.0/docs r1 noncanonical proposal")
    print(f"checks={CHECKS.value}")
    print(f"schema_validation={schema_note}")
    print(f"formula_kats={formula_kats}")
    print(f"contract_kats={contract_kats}")
    print(f"sources={source_count}")
    print(f"claims={claim_count}")
    print(f"parameters={parameter_count}")
    print(f"value_rows={value_count}")
    print(f"workbook_sheets={sheet_count}")
    print(f"workbook_formulas={formula_count}")
    print(f"workbook_qa_passes={workbook_qa_count}")
    print(f"local_links={link_count}")
    print(f"missing_allowed={len(missing)}")
    print(f"artifact_sha256={sha256(ARTIFACT)}")
    print(f"capability_sha256={sha256(CAPABILITY)}")
    print(f"known_answer_tests_sha256={sha256(KATS)}")
    if WORKBOOK.exists():
        print(f"workbook_sha256={sha256(WORKBOOK)}")


if __name__ == "__main__":
    main()
