#!/usr/bin/env python3
"""Validate the noncanonical TC-wind x solar model-v1 screening proposal."""

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
PROPOSED = ROOT / "docs/cells/tropical_cyclone_wind_solar/proposed"
ARTIFACT = PROPOSED / "tropical_cyclone_wind_solar__model_v1_0__docs_r1__curve_artifact.json"
CAPABILITY = PROPOSED / "tropical_cyclone_wind_solar__model_v1_0__docs_r1__capability.json"
KATS = PROPOSED / "known_answer_tests_tropical_cyclone_wind_solar__model_v1_0__docs_r1.json"
SOURCES = PROPOSED / "SOURCE_REGISTER_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
CLAIMS = PROPOSED / "CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
R2_SOURCES = PROPOSED / "SOURCE_REGISTER_ADDENDUM_tropical_cyclone_wind_solar__model_v1_0__docs_r2.csv"
R2_CLAIMS = PROPOSED / "CLAIM_PARAMETER_REGISTER_ADDENDUM_tropical_cyclone_wind_solar__model_v1_0__docs_r2.csv"
PARAMETERS = PROPOSED / "PARAMETER_TIER_TABLE_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
VALUES = PROPOSED / "VALUE_CROSSWALK_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
FIT_STATS = PROPOSED / "FIT_SUFFICIENT_STATISTICS_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
FIT_SENSITIVITY = PROPOSED / "FIT_EVENT_SENSITIVITY_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
CROSS_METHOD_MATCHES = PROPOSED / "CROSS_METHOD_MATCH_AUDIT_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
OLD_VS_NEW = PROPOSED / "OLD_VS_NEW_COMPARISON_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv"
WORKBOOK = PROPOSED / "damage_curve_records_tropical_cyclone_wind_solar__model_v1_0__docs_r1.xlsx"
INDEX = ROOT / "docs/contracts/machine_readable_artifact_index.json"
BUNDLE_SCHEMA = ROOT / "docs/contracts/schemas/curve_artifact_bundle.v3.schema.json"
CAPABILITY_SCHEMA = ROOT / "docs/contracts/schemas/capability_declaration.v3.schema.json"
EMIT_SCHEMA = ROOT / "docs/contracts/schemas/damage_emit.v2.schema.json"
V0_VALIDATOR = ROOT / "scripts/reference_helpers/validate_tropical_cyclone_wind_solar_v0_1_scaffold.py"
EVALUATOR = ROOT / "scripts/reference_helpers/tropical_cyclone_wind_solar_curve_eval.py"
DERIVER = ROOT / "scripts/reference_helpers/derive_tropical_cyclone_wind_solar_v1_fit.py"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from derive_tropical_cyclone_wind_solar_v1_fit import derive  # noqa: E402
from tropical_cyclone_wind_solar_curve_eval import (  # noqa: E402
    EXPECTED_SELECTORS,
    SUPPORTED_FAILURE_UNIT,
    TropicalCycloneWindSolarEvaluationError,
    artifact_sha256,
    evaluate_damage_call,
    evaluate_piecewise_linear_record,
    verify_artifact_pin,
)


EXPECTED_POINTS = [
    (17.4, 0.0),
    (18.3, 0.0),
    (20.7, 0.00027276656),
    (24.6, 0.00027276656),
    (24.8, 0.000955175835),
    (25.1, 0.000955175835),
    (25.9, 0.001853190692857),
    (29.5, 0.001853190692857),
    (29.8, 0.004054775905),
    (31.7, 0.00441454805),
    (37.9, 0.00441454805),
    (38.9, 0.0182729376325),
    (39.1, 0.0182729376325),
]
EXPECTED_SHEETS = [
    "README",
    "Scope_Coverage",
    "Source_Evidence",
    "Cohort_Fit",
    "PAVA_Curve",
    "Event_Sensitivity",
    "Failure_Units",
    "Value_Crosswalk",
    "KATs",
    "Source_Register",
    "Claim_Register",
    "Parameter_Tiers",
    "QA",
]
BASE_EXPECTED_DOCS = [
    "README_tropical_cyclone_wind_solar__model_v1_0__docs_r1.md",
    "CHANGE_CLASSIFICATION_tropical_cyclone_wind_solar__model_v1_0__docs_r1.md",
    "SEVEN_STEP_AUDIT_tropical_cyclone_wind_solar__model_v1_0__docs_r1.md",
    "PRESSURE_TEST_tropical_cyclone_wind_solar__model_v1_0__docs_r1.md",
    "PROMOTION_GATE_MATRIX_tropical_cyclone_wind_solar__model_v1_0__docs_r1.md",
    "tropical_cyclone_wind_solar_curve_derivation_dossier__model_v1_0__docs_r1.md",
    "tropical_cyclone_wind_solar_damage_code_metadata_spec__model_v1_0__docs_r1.md",
    "CROSS_METHOD_MATCH_AUDIT_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv",
    "OLD_VS_NEW_COMPARISON_tropical_cyclone_wind_solar__model_v1_0__docs_r1.csv",
    "workbook_sheet_manifest_tropical_cyclone_wind_solar__model_v1_0__docs_r1.md",
    "VALIDATION_REPORT_tropical_cyclone_wind_solar__model_v1_0__docs_r1.md",
]
R2_REQUIRED_DOCS = [
    PROPOSED / "README_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md",
    PROPOSED / "CHANGE_CLASSIFICATION_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md",
    PROPOSED / "DEEP_CURATION_DECISION_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md",
    PROPOSED / "BOUNDED_EVIDENCE_SEARCH_LOG_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md",
    PROPOSED / "STRONG_WIND_REUSE_AND_V2_ACQUISITION_BLUEPRINT_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md",
    PROPOSED / "PROMOTION_GATE_MATRIX_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md",
    PROPOSED / "VALIDATION_REPORT_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md",
    ROOT / "docs/cells/tropical_cyclone_wind_solar/README.md",
    ROOT / "docs/cells/tropical_cyclone_wind_solar/basics/README.md",
    ROOT / "docs/cells/tropical_cyclone_wind_solar/basics/HOW_THE_MODEL_IS_BUILT.md",
    ROOT / "docs/cells/tropical_cyclone_wind_solar/basics/MODEL_REFERENCE.md",
    ROOT / "docs/cells/README.md",
    ROOT / "docs/cells/VERSION_REGISTRY.md",
    ROOT / "docs/contracts/README.md",
    ROOT / "docs/contracts/hazard_handoff/README.md",
    ROOT / "docs/plans/README.md",
    ROOT / "docs/plans/hazard_asset_coverage/README.md",
    ROOT / "docs/plans/hazard_asset_coverage/DECISIONS.md",
    ROOT / "docs/plans/tropical_cyclone_wind_solar_completion/README.md",
    ROOT / "docs/plans/tropical_cyclone_wind_solar_completion/decisions.md",
    ROOT / "docs/plans/tropical_cyclone_wind_solar_completion/assumptions.md",
    ROOT / "docs/plans/repo_information_architecture/inventory_mapping.md",
    ROOT / "docs/contracts/hazard_handoff/tropical_cyclone_wind_solar_model_v1_0_docs_r2_no_cutover.md",
    ROOT / "docs/contracts/hazard_handoff/tropical_cyclone_wind_solar_model_v1_0_proposal.md",
]
ALLOWED_TIERS = {
    "T1_claims_or_field_calibrated",
    "T2_public_lab_standard_or_physics",
    "T3_engineering_proxy_or_adjacent_empirical",
    "T4_placeholder_or_expert_judgment",
}
ALLOWED_ADOPTION_STATUSES = {
    "adopt",
    "adopt_as_limitation",
    "adopt_with_limits",
    "audit_only",
    "withhold",
    "withhold_runtime",
}
EXPECTED_SOURCE_SHA = "edb34e74cc078bba1fdbe34463abadc794fd416caa66eb64ac3d0ed176ac5e00"
EXPECTED_AGGREGATE_SHA = "c1ab48731f875142c571efcfd6323d7e048b35b2d2525418e25e6fefb3487062"
EXPECTED_AGGREGATE_FILE_ID = "f5355652-f2e1-4bdb-8ff2-3623ce15a1d4"
EXPECTED_ALWAYS_FLAGS = {
    "NONCANONICAL_PROPOSAL",
    "SCREENING_REMOTE_SENSING_LABELED_VISIBLE_FRACTION_WITH_T4_ECONOMIC_BRIDGE",
    "SOURCE_COHORT_MIXED_SCALE",
    "SOURCE_AXIS_PRODUCT_QUERY_SEMANTICS_UNRESOLVED",
    "SOURCE_COMPOSITE_HURRICANE_MODULE_LOSS",
    "VISIBLE_DAMAGE_ONLY_HIDDEN_DAMAGE_UNOBSERVED",
    "PAVA_DERIVED_KNOTS",
    "EQUAL_SITE_WEIGHT_NOT_MODULE_WEIGHTED",
    "EVENT_CLUSTERED_SAMPLE",
    "SPARSE_SEVERE_TAIL_WITHHELD",
    "CROSS_METHOD_SAME_EVENT_ENDPOINT_CONFLICT",
    "PARTIAL_FAILURE_UNIT_COVERAGE",
    "CURVE_INTRINSIC_SPREAD_NOT_CARRIED",
    "NO_EXTRAPOLATION",
    "SCENARIO_DOLLAR_LOSS_WITHHELD",
}
EXPECTED_RUNTIME_HASHES = {
    ARTIFACT: "bb01300d3e76114203dd826be5bff4bb9f2b98490880327dd57575007a180840",
    CAPABILITY: "5cd4f5501961a9d7f2c21259b4cfabd9e74eef30b5fdd9ceff72729b83ffc4fc",
    KATS: "2e18603a9efb5cbb8bdd1c7f3b162e1a3e0c4b0723df5e1afbdc27def84f7cd2",
    WORKBOOK: "748031c226187e3b43d83f6a57b2dbd5554457edc01a06debe16b7ef640f3105",
}
EXPECTED_HELPER_SCHEMA_HASHES = {
    EVALUATOR: "a483b00df1e8f7647945f1e69daf8eb8e9c473bb27cf282e68ab46667868e7b5",
    DERIVER: "cf6c244eb8e86fda12c53bc0afb008822385d8632d69a00dead08e430734f03e",
    BUNDLE_SCHEMA: "a2287a7dc6d5ec19a04a1e25c4d130c282af5956318dcee6d3c137a1a50e33cb",
    CAPABILITY_SCHEMA: "73e76744b6ae5c39f5503d2be454e5407674f301c24b0de0f586ade0980fd5b9",
    EMIT_SCHEMA: "9dda3b0dd831d14668526f9ed5aa653a98c7230412410f0286e9eedabc526060",
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
    require(bool(result), f"{path}: empty CSV")
    for line_number, row in enumerate(result, start=2):
        require(None not in row, f"{path}:{line_number}: extra fields")
        require(all(value is not None for value in row.values()), f"{path}:{line_number}: missing field")
    return result


def csv_header(path: Path) -> list[str]:
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration as exc:
            raise ValidationFailure(f"{path}: empty CSV") from exc


def fenced_yaml_value(text: str, key: str) -> str:
    values: list[str] = []
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*(.*?)\s*$")
    for block in re.findall(r"```yaml\s*\n(.*?)```", text, flags=re.DOTALL):
        for line in block.splitlines():
            match = pattern.match(line)
            if match:
                values.append(match.group(1).strip().strip("\"'"))
    require(len(values) == 1, f"expected one fenced-YAML value for {key}, found {len(values)}")
    return values[0]


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
    Draft202012Validator(schemas[1], registry=registry).validate(capability)
    Draft202012Validator(schemas[0], registry=registry).validate(artifact)
    emit = evaluate_damage_call(artifact, base_request(30.75))
    Draft202012Validator(schemas[2], registry=registry).validate(emit)
    return "bundle v3 + capability v3 + damage emit v2 validated"


def base_request(gust_mps: float = 30.75) -> dict[str, Any]:
    return {
        "pathway_id": "tropical_cyclone_wind",
        "failure_unit_id": SUPPORTED_FAILURE_UNIT,
        **EXPECTED_SELECTORS,
        "perry_event_max_gust_mps": gust_mps,
    }


def result_for_request(emit: Mapping[str, Any], unit_id: str) -> Mapping[str, Any]:
    matches = [item for item in emit["failure_unit_results"] if item["failure_unit_id"] == unit_id]
    require(len(matches) == 1, f"{unit_id}: result not unique")
    return matches[0]


def validate_top_level(
    artifact: Mapping[str, Any], capability: Mapping[str, Any]
) -> None:
    require(artifact["schema_version"] == "damage_curve_record_bundle.v3", "bundle schema changed")
    require(artifact["schema_status"] == "proposed_draft", "bundle schema status changed")
    require(artifact["cell_id"] == "tropical_cyclone_wind_solar", "cell changed")
    require(
        artifact["damage_code_id"] == "TROPICAL_CYCLONE_WIND_SOLAR_PERRY_MODULE_SCREENING_V1",
        "damage code changed",
    )
    require(artifact["semantic_damage_model_version"] == "model v1.0", "model changed")
    require(artifact["documentation_revision"] == "docs r1", "docs changed")
    require(artifact["canonical_runtime_artifact"] is False, "proposal became canonical")
    require(artifact["package_inclusion_status"] == "not_included", "proposal entered package")
    require(
        artifact["model_grade"]
        == "screening_remote_sensing_labeled_visible_fraction_with_T4_economic_bridge",
        "model grade changed",
    )
    require(artifact["capability_declaration"] == capability, "embedded capability drifted")
    require(capability["canonical_runtime_artifact"] is False, "capability became canonical")


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
        if (ROOT / value).exists():
            continue
        if allow_incomplete and field in {"source_dossier", "source_workbook"}:
            missing.append(value)
            continue
        raise ValidationFailure(f"missing required path: {value}")
    return missing


def validate_curve(artifact: Mapping[str, Any]) -> None:
    require(len(artifact["pathways"]) == 1, "expected one pathway")
    pathway = artifact["pathways"][0]
    require(pathway["pathway_id"] == "tropical_cyclone_wind", "pathway changed")
    axis = pathway["hazard_axis"]
    require(axis["id"] == "PERRY_DATASET_REPORTED_EVENT_MAX_GUST_MPS", "axis ID changed")
    require(axis["preferred_input_field"] == "perry_event_max_gust_mps", "axis field changed")
    require(axis["permitted_proxy_fields"] == [], "axis aliases introduced")
    require(axis["unit"] == "m/s", "axis unit changed")
    require(axis["valid_range"] == [17.4, 39.1], "axis range changed")
    require("provider" in axis["source_semantics"], "axis uncertainty disclosure missing")
    selectors = {item["field"]: item for item in pathway["selector_logic"]}
    require(set(selectors) == set(EXPECTED_SELECTORS), "selector fields changed")
    for field, expected in EXPECTED_SELECTORS.items():
        require(selectors[field]["default"] is None, f"{field}: default prohibited")
        require(selectors[field]["allowed"] == [expected], f"{field}: allowed value changed")
    require(len(pathway["curve_records"]) == 1, "expected one curve")
    record = pathway["curve_records"][0]
    require(record["curve_id"] == "TCWS_PERRY_GROUND_FIXED_VISIBLE_REPLACEMENT_PROXY_V1", "curve ID changed")
    require(record["failure_unit_id"] == SUPPORTED_FAILURE_UNIT, "source atom changed")
    require(record["curve_form"] == "piecewise_linear", "curve form changed")
    require(record["x_axis"] == axis["preferred_input_field"], "record axis changed")
    require(record["valid_range"] == axis["valid_range"], "record range changed")
    require(record["selector_match"] == EXPECTED_SELECTORS, "record selectors changed")
    require(record["interpolation_policy"] == "linear_between_source_knots", "interpolation changed")
    require("no endpoint clamp" in record["extrapolation_policy"], "no-clamp guard missing")
    require("SPARSE_SEVERE_TAIL_WITHHELD" in record["metadata_flags"], "tail flag missing")
    require(
        set(artifact["evaluation_contract"]["metadata_flags_always"]) == EXPECTED_ALWAYS_FLAGS,
        "always-on emit flags changed",
    )
    capability_flags = set(
        artifact["capability_declaration"]["pathway_capabilities"][0]["limitation_flags"]
    )
    require(capability_flags == EXPECTED_ALWAYS_FLAGS, "capability limitation flags changed")
    emitted = evaluate_damage_call(artifact, base_request(17.4))
    emitted_result = result_for_request(emitted, SUPPORTED_FAILURE_UNIT)
    require(emitted["cell_id"] == "tropical_cyclone_wind_solar", "evaluator emit cell changed")
    require(emitted["model_version"] == "model v1.0", "evaluator emit model changed")
    require(emitted["pathway_id"] == "tropical_cyclone_wind", "evaluator emit pathway changed")
    require(emitted["emit_mode"] == "scalar_mean", "evaluator emit mode changed")
    require(emitted["selectors_used"] == EXPECTED_SELECTORS, "evaluator selector echo changed")
    require(
        emitted["hazard_input_used"]
        == {
            "axis_id": "PERRY_DATASET_REPORTED_EVENT_MAX_GUST_MPS",
            "input_field": "perry_event_max_gust_mps",
            "value": 17.4,
            "unit": "m/s",
            "source_height_and_averaging_period": "unspecified_in_source_package",
        },
        "evaluator hazard-input emit changed",
    )
    require(set(emitted_result["metadata_flags"]) == EXPECTED_ALWAYS_FLAGS, "evaluator emit flags changed")
    actual = [(float(x), float(y)) for x, y in record["parameters"]["points"]]
    require(len(actual) == len(EXPECTED_POINTS), "knot count changed")
    for index, ((actual_x, actual_y), (expected_x, expected_y)) in enumerate(zip(actual, EXPECTED_POINTS)):
        close(actual_x, expected_x, 1e-14, f"point {index} x")
        close(actual_y, expected_y, 5e-16, f"point {index} DR")
    previous = -1.0
    for index in range(218):
        gust = 17.4 + index / 10
        if gust > 39.1:
            break
        dr = evaluate_piecewise_linear_record(record, gust)
        require(math.isfinite(dr) and 0 <= dr <= 1, f"invalid DR at {gust}")
        require(dr + 1e-14 >= previous, f"nonmonotone DR at {gust}")
        previous = dr
    for out_of_range in (17.399, 39.101, 48.2):
        try:
            evaluate_damage_call(artifact, base_request(out_of_range))
        except TropicalCycloneWindSolarEvaluationError as exc:
            require(exc.code == "AXIS_OUTSIDE_VALID_RANGE", f"bad range code at {out_of_range}")
        else:
            raise ValidationFailure(f"out-of-range gust accepted: {out_of_range}")


def validate_fit_statistics(artifact: Mapping[str, Any]) -> tuple[int, int]:
    stats = rows(FIT_STATS)
    require(len(stats) == 9, "fit-stat row count changed")
    fit = [row for row in stats if row["fit_role"] == "runtime_fit"]
    tail = [row for row in stats if row["fit_role"] == "audit_only_excluded_sparse_tail"]
    require(len(fit) == 8 and len(tail) == 1, "fit/tail partition changed")
    require(sum(int(row["n_sites"]) for row in fit) == 34, "runtime fit n changed")
    require(int(tail[0]["n_sites"]) == 1, "tail n changed")
    close(float(tail[0]["x_low_mps"]), 48.2, 0, "tail x")
    close(float(tail[0]["mean_damage_ratio"]), 0.4142383192, 1e-15, "tail DR")
    for row in stats:
        expected = float(row["sum_damage_ratio"]) / int(row["n_sites"])
        close(float(row["mean_damage_ratio"]), expected, 5e-16, row["block_id"])
    block_points: list[tuple[float, float]] = []
    for row in fit:
        level = float(row["mean_damage_ratio"])
        for x_value in (float(row["x_low_mps"]), float(row["x_high_mps"])):
            point = (x_value, level)
            if not block_points or point != block_points[-1]:
                block_points.append(point)
    artifact_points = [tuple(map(float, point)) for point in artifact["pathways"][0]["curve_records"][0]["parameters"]["points"]]
    require(len(block_points) == len(artifact_points), "block-edge point count changed")
    for index, (left, right) in enumerate(zip(block_points, artifact_points)):
        close(left[0], right[0], 0, f"block point {index} x")
        close(left[1], right[1], 5e-16, f"block point {index} DR")
    sensitivity = rows(FIT_SENSITIVITY)
    require(len(sensitivity) == 6, "event sensitivity count changed")
    require(sum(int(row["n_runtime_fit_rows"]) for row in sensitivity) == 34, "event counts do not sum")
    by_event = {row["event_id"]: row for row in sensitivity}
    require(int(by_event["Florence"]["n_runtime_fit_rows"]) == 20, "Florence count changed")
    close(float(by_event["Maria"]["leave_one_event_out_highest_block_dr"]), 0.003376381028, 5e-16, "Maria LOO")
    close(float(by_event["Florence"]["leave_one_event_out_highest_block_dr"]), 0.024363916843333, 5e-16, "Florence LOO")
    return len(stats), len(sensitivity)


def validate_optional_source_csv(path: Path | None, artifact: Mapping[str, Any]) -> str:
    if path is None:
        return "not supplied; governed sufficient statistics validated"
    derived = derive(path)
    require(derived["source_sha256"] == EXPECTED_SOURCE_SHA, "source SHA changed")
    require(derived["source_row_count"] == 47, "source row count changed")
    require(derived["ground_row_count"] == 37, "ground count changed")
    require(derived["ground_tracking_false_count"] == 35, "fixed cohort count changed")
    require(derived["ground_tracking_true_count"] == 2, "tracker count changed")
    require(derived["runtime_fit_count"] == 34, "derived runtime fit n changed")
    require(derived["sparse_tail_audit_count"] == 1, "derived tail n changed")
    artifact_points = artifact["pathways"][0]["curve_records"][0]["parameters"]["points"]
    require(len(derived["runtime_points"]) == len(artifact_points), "derived point count changed")
    for index, (left, right) in enumerate(zip(derived["runtime_points"], artifact_points)):
        close(float(left[0]), float(right[0]), 0, f"source-derived point {index} x")
        close(float(left[1]), float(right[1]), 0, f"source-derived point {index} DR")
    return "source SHA, schema, cohort, PAVA, tail, and event sensitivity reproduced"


def validate_kats(artifact: Mapping[str, Any]) -> tuple[int, int, int]:
    kats = load(KATS)
    require(kats["schema_version"] == "known_answer_tests.v3", "KAT schema changed")
    tolerance = float(kats["absolute_tolerance"])
    for test in kats["formula_known_answer_tests"]:
        emit = evaluate_damage_call(artifact, test["input"])
        result = result_for_request(emit, test["input"]["failure_unit_id"])
        expected = test["expected"]
        require(result["status"] == expected["status"], f"{test['test_id']}: status")
        require(result["curve_id"] == expected["curve_id"], f"{test['test_id']}: curve")
        close(float(result["scalar_central_dr"]), float(expected["failure_unit_damage_ratio"]), tolerance, test["test_id"])
    base = kats["formula_known_answer_tests"][0]["input"]
    for test in kats["rejection_tests"]:
        request = json.loads(json.dumps(base))
        if "mutation" in test:
            request.update(test["mutation"])
        if "remove_field" in test:
            request.pop(test["remove_field"], None)
        try:
            evaluate_damage_call(artifact, request)
        except TropicalCycloneWindSolarEvaluationError as exc:
            require(exc.code == test["expected_error_code"], f"{test['test_id']}: {exc.code}")
        else:
            raise ValidationFailure(f"{test['test_id']}: expected rejection")
    for test in kats["withheld_unit_tests"]:
        emit = evaluate_damage_call(
            artifact,
            {"pathway_id": "tropical_cyclone_wind", "failure_unit_id": test["failure_unit_id"]},
        )
        result = result_for_request(emit, test["failure_unit_id"])
        require(result["status"] == "withheld", f"{test['test_id']}: status")
        require(result["scalar_central_dr"] is None, f"{test['test_id']}: nonnull DR")
        require(test["expected_reason_code"] in result["withheld_reason_codes"], f"{test['test_id']}: reason")
    source_tests = {item["test_id"]: item for item in kats["source_data_known_answers"]}
    close(source_tests["TCWS_PERCENT_CONVERSION_HIGH"]["input_percent"] / 100, source_tests["TCWS_PERCENT_CONVERSION_HIGH"]["expected_damage_ratio"], 0, "high percent conversion")
    require(source_tests["TCWS_SOURCE_FILE_HASH"]["expected_manual_csv_sha256"] == EXPECTED_SOURCE_SHA, "KAT source SHA changed")
    return len(kats["formula_known_answer_tests"]), len(kats["rejection_tests"]), len(kats["withheld_unit_tests"])


def validate_capability_and_value(artifact: Mapping[str, Any]) -> None:
    capability = artifact["capability_declaration"]
    item = capability["pathway_capabilities"][0]
    require(item["failure_unit_scalar_dr"] == "conditional", "scalar capability changed")
    require(item["scenario_loss_given_value_basis"] == "withheld", "scenario loss enabled")
    require(item["curve_intrinsic_spread"] == "not_carried", "spread unexpectedly carried")
    withheld = {row["failure_unit_id"] for row in item["withheld_failure_units"]}
    expected = {unit["id"] for unit in artifact["failure_units"]} - {SUPPORTED_FAILURE_UNIT}
    require(withheld == expected, "withheld matrix does not cover every other unit")
    value = artifact["value_linkage"]
    require(value["runtime_loss_status"] == "withheld_before_canonical_promotion", "runtime loss enabled")
    require("full plant TIV" in value["prohibited_denominators"], "full TIV guard missing")
    value_rows = rows(VALUES)
    source_rows = [row for row in value_rows if row["failure_unit_id"] == SUPPORTED_FAILURE_UNIT]
    require(len(source_rows) == 1, "source-unit value row not unique")
    require(source_rows[0]["include_in_direct_denominator"] == "false", "proposal activated a dollar denominator")
    require(capability["consumer_annual_metrics"]["status_after_promotion"] == "withheld", "annual metrics enabled")


def validate_cross_method_match_audit() -> tuple[int, float]:
    audit_rows = rows(CROSS_METHOD_MATCHES)
    expected = {
        "TCWS-XM-001": (2, 242, 13.0, 3.661981002, 72.363, "high"),
        "TCWS-XM-002": (3, 74, 60.0, 41.42383192, 244.253, "high"),
        "TCWS-XM-003": (4, 7, 90.0, 81.81441591, 36.781, "high"),
        "TCWS-XM-004": (7, 257, 13.0, 0.447129082, 405.681, "moderate"),
    }
    require({row["audit_match_id"] for row in audit_rows} == set(expected), "cross-method match IDs changed")
    method = (
        "Nearest Perry aggregate row after filtering associated_hurricane=Maria, type=utility, mount=ground; "
        "retain only great-circle distance <=500 m; coordinate-nearest match is apparent, not identity-adjudicated."
    )
    differences: list[float] = []
    for row in audit_rows:
        ceferino_row, perry_line, ceferino_pct, perry_pct, distance_m, confidence = expected[row["audit_match_id"]]
        require(row["ceferino_source_id"] == "TCWS-S022", f"{row['audit_match_id']}: Ceferino source changed")
        require(row["perry_source_id"] == "TCWS-S020", f"{row['audit_match_id']}: Perry source changed")
        require(row["perry_file_id"] == EXPECTED_AGGREGATE_FILE_ID, f"{row['audit_match_id']}: aggregate file ID changed")
        require(row["perry_file_sha256"] == EXPECTED_AGGREGATE_SHA, f"{row['audit_match_id']}: aggregate SHA changed")
        require(int(row["ceferino_data_row"]) == ceferino_row, f"{row['audit_match_id']}: Ceferino row changed")
        require(int(row["perry_csv_line_number"]) == perry_line, f"{row['audit_match_id']}: Perry line changed")
        close(float(row["ceferino_damage_pct"]), ceferino_pct, 0, f"{row['audit_match_id']}: Ceferino percentage")
        close(float(row["perry_damage_pct"]), perry_pct, 0, f"{row['audit_match_id']}: Perry percentage")
        observed_difference = abs(ceferino_pct - perry_pct)
        close(float(row["absolute_difference_percentage_points"]), observed_difference, 5e-10, f"{row['audit_match_id']}: absolute difference")
        longitude_1 = math.radians(float(row["ceferino_longitude_deg"]))
        latitude_1 = math.radians(float(row["ceferino_latitude_deg"]))
        longitude_2 = math.radians(float(row["perry_longitude_deg"]))
        latitude_2 = math.radians(float(row["perry_latitude_deg"]))
        haversine = (
            math.sin((latitude_2 - latitude_1) / 2.0) ** 2
            + math.cos(latitude_1) * math.cos(latitude_2) * math.sin((longitude_2 - longitude_1) / 2.0) ** 2
        )
        calculated_distance = 6_371_000.0 * 2.0 * math.asin(math.sqrt(haversine))
        close(float(row["great_circle_distance_m"]), round(calculated_distance, 3), 0, f"{row['audit_match_id']}: distance")
        close(float(row["great_circle_distance_m"]), distance_m, 0, f"{row['audit_match_id']}: frozen distance")
        require(float(row["great_circle_distance_m"]) <= 500.0, f"{row['audit_match_id']}: match exceeds 500 m")
        require(row["perry_event"] == "Maria" and row["perry_type"] == "utility" and row["perry_mount"] == "ground", f"{row['audit_match_id']}: Perry filter changed")
        require(row["match_method"] == method, f"{row['audit_match_id']}: match method changed")
        require(row["match_confidence"] == confidence, f"{row['audit_match_id']}: confidence changed")
        require(row["audit_status"] == "audit_only", f"{row['audit_match_id']}: audit status changed")
        differences.append(float(row["absolute_difference_percentage_points"]))
    mean_difference = sum(differences) / len(differences)
    close(mean_difference, 12.1631605215, 5e-13, "cross-method mean absolute difference")
    return len(audit_rows), mean_difference


def validate_registers(
    artifact: Mapping[str, Any],
) -> tuple[int, int, int, int, int, int, int]:
    base_source_rows = rows(SOURCES)
    base_claim_rows = rows(CLAIMS)
    r2_source_rows = rows(R2_SOURCES)
    r2_claim_rows = rows(R2_CLAIMS)
    require(csv_header(SOURCES) == csv_header(R2_SOURCES), "docs-r2 source-register header drifted")
    require(csv_header(CLAIMS) == csv_header(R2_CLAIMS), "docs-r2 claim-register header drifted")
    require(len(base_source_rows) == 10, "docs-r1 source count changed")
    require(len(base_claim_rows) == 18, "docs-r1 claim count changed")
    require(len(r2_source_rows) == 18, "docs-r2 source addendum count changed")
    require(len(r2_claim_rows) == 21, "docs-r2 claim addendum count changed")
    source_rows = base_source_rows + r2_source_rows
    claim_rows = base_claim_rows + r2_claim_rows
    parameter_rows = rows(PARAMETERS)
    value_rows = rows(VALUES)
    old_rows = rows(OLD_VS_NEW)
    source_ids = {row["source_id"] for row in source_rows}
    require(len(source_ids) == len(source_rows), "duplicate effective source ID")
    required_r2_sources = {f"TCWS-S{number:03d}" for number in range(23, 41)}
    r2_source_ids = {row["source_id"] for row in r2_source_rows}
    require(r2_source_ids == required_r2_sources, "docs-r2 source ID set changed")
    require({"TCWS-S020", "TCWS-S021", "TCWS-S022", "GOVERNANCE_CONTRACT"} <= source_ids, "base primary/governance sources missing")
    for row in source_rows:
        require(row["evidence_tier"] in ALLOWED_TIERS, f"{row['source_id']}: bad tier")
        require(bool(row["exact_locator"] and row["permitted_inference"] and row["prohibited_inference"]), f"{row['source_id']}: incomplete")
    required_source_fields = {
        "citation",
        "url",
        "accessed_on",
        "exact_locator",
        "source_type",
        "source_role",
        "pathway_ids",
        "evidence_tier",
        "target_asset_match",
        "target_failure_unit_match",
        "measured_or_modeled_endpoint",
        "permitted_inference",
        "prohibited_inference",
        "decision",
        "status",
        "notes",
    }
    for row in r2_source_rows:
        require(all(row[field].strip() for field in required_source_fields), f"{row['source_id']}: incomplete docs-r2 source row")
        require(row["pathway_ids"] == "tropical_cyclone_wind", f"{row['source_id']}: bad pathway")
        require(row["decision"] in {"adopt_with_limits", "audit_only"}, f"{row['source_id']}: bad decision")
        require(row["status"] == "reviewed", f"{row['source_id']}: bad review status")
    claim_ids = {row["claim_id"] for row in claim_rows}
    require(len(claim_ids) == len(claim_rows), "duplicate effective claim ID")
    required_r2_claims = {f"TCWS-C{number}" for number in range(201, 222)}
    r2_claim_ids = {row["claim_id"] for row in r2_claim_rows}
    require(r2_claim_ids == required_r2_claims, "docs-r2 claim ID set changed")
    require({"TCWS-C115", "TCWS-C116", "TCWS-C117", "TCWS-C118"} <= claim_ids, "strict-gate base claims missing")
    required_claim_fields = {
        "claim_text",
        "claim_type",
        "source_ids",
        "exact_locator",
        "evidence_tier",
        "parameter_or_rule",
        "adoption_status",
        "permitted_inference",
        "prohibited_inference",
        "reasoning",
        "update_trigger",
    }
    for row in claim_rows:
        require(not (split_ids(row["source_ids"]) - source_ids), f"{row['claim_id']}: unresolved source")
        require(row["evidence_tier"] in ALLOWED_TIERS, f"{row['claim_id']}: bad tier")
        require(row["pathway_id"] == "tropical_cyclone_wind", f"{row['claim_id']}: bad pathway")
        require(row["adoption_status"] in ALLOWED_ADOPTION_STATUSES, f"{row['claim_id']}: bad adoption status")
        require(all(row[field].strip() for field in required_claim_fields), f"{row['claim_id']}: incomplete claim row")
    by_source = {row["source_id"]: row for row in r2_source_rows}
    by_claim = {row["claim_id"]: row for row in r2_claim_rows}
    require(by_source["TCWS-S037"]["url"] == "https://doi.org/10.2172/1659785", "NREL 75804 DOI drifted")
    require("Solar Photovoltaics in Severe Weather" in by_source["TCWS-S037"]["citation"], "NREL 75804 title drifted")
    require(by_claim["TCWS-C220"]["parameter_or_rule"] == "fit_weighting_interpretation", "fit-weighting claim drifted")
    require(by_claim["TCWS-C220"]["adoption_status"] == "adopt_as_limitation", "fit-weighting adoption drifted")
    require(by_claim["TCWS-C221"]["parameter_or_rule"] == "predictive_use_status", "predictive-use claim drifted")
    require(by_claim["TCWS-C221"]["adoption_status"] == "withhold", "predictive-use adoption drifted")
    require(len(parameter_rows) >= 17, "parameter table incomplete")
    for row in parameter_rows:
        require(not (split_ids(row["source_ids"]) - source_ids), f"{row['parameter']}: unresolved source")
        require(row["tier"] in ALLOWED_TIERS, f"{row['parameter']}: bad tier")
    embedded_sources: set[str] = set()
    for item in artifact["parameter_tier_table"]:
        embedded_sources.update(item["source_ids"])
    require(not (embedded_sources - source_ids), f"unresolved embedded sources {sorted(embedded_sources-source_ids)}")
    require(len(value_rows) >= 11, "value crosswalk incomplete")
    require(len(old_rows) >= 6, "old-vs-new comparison incomplete")
    return (
        len(base_source_rows),
        len(base_claim_rows),
        len(source_rows),
        len(claim_rows),
        len(parameter_rows),
        len(value_rows),
        len(old_rows),
    )


def workbook_inventory(path: Path) -> tuple[list[str], int, list[str], set[str], set[str], set[str]]:
    with zipfile.ZipFile(path) as archive:
        namespace = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        relationship_namespace = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        workbook_root = ET.fromstring(archive.read("xl/workbook.xml"))
        sheet_nodes = workbook_root.findall("m:sheets/m:sheet", namespace)
        sheet_names = [node.attrib["name"] for node in sheet_nodes]
        formula_count = 0
        for name in archive.namelist():
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
                root = ET.fromstring(archive.read(name))
                formula_count += len(root.findall(".//m:f", namespace))
        rel_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rels = {node.attrib["Id"]: node.attrib["Target"] for node in rel_root}

        def sheet_root(sheet_name: str) -> ET.Element:
            node = next(item for item in sheet_nodes if item.attrib["name"] == sheet_name)
            target = rels[node.attrib[f"{{{relationship_namespace}}}id"]].lstrip("/")
            if not target.startswith("xl/"):
                target = f"xl/{target}"
            return ET.fromstring(archive.read(target))

        qa_root = sheet_root("QA")
        qa_values = {
            cell.attrib["r"]: cell.findtext("m:v", default="", namespaces=namespace)
            for cell in qa_root.findall(".//m:c", namespace)
        }
        qa_results = [qa_values.get(f"B{row}", "") for row in range(5, 23)]

        def first_column_ids(sheet_name: str) -> set[str]:
            result: set[str] = set()
            for cell in sheet_root(sheet_name).findall(".//m:c", namespace):
                reference = cell.attrib.get("r", "")
                match = re.fullmatch(r"A([0-9]+)", reference)
                if not match or int(match.group(1)) < 5:
                    continue
                value = cell.findtext("m:v", default="", namespaces=namespace)
                if value:
                    result.add(value)
            return result

        workbook_source_ids = first_column_ids("Source_Register")
        workbook_claim_ids = first_column_ids("Claim_Register")
        source_evidence_root = sheet_root("Source_Evidence")
        workbook_cross_match_ids = {
            cell.findtext("m:v", default="", namespaces=namespace)
            for cell in source_evidence_root.findall(".//m:c", namespace)
            if cell.attrib.get("r") in {"A14", "A15", "A16", "A17"}
        }
        workbook_cross_match_ids.discard("")
    return sheet_names, formula_count, qa_results, workbook_source_ids, workbook_claim_ids, workbook_cross_match_ids


def validate_workbook(allow_incomplete: bool) -> tuple[int, int, int]:
    if not WORKBOOK.exists():
        if allow_incomplete:
            return 0, 0, 0
        raise ValidationFailure(f"workbook missing: {WORKBOOK}")
    names, formulas, qa_results, workbook_source_ids, workbook_claim_ids, workbook_cross_match_ids = workbook_inventory(WORKBOOK)
    require(names == EXPECTED_SHEETS, f"workbook sheet order changed: {names}")
    require(formulas >= 70, f"workbook has too few formulas: {formulas}")
    require(len(qa_results) == 18, "workbook QA result count changed")
    for row_number, result in enumerate(qa_results, start=5):
        require(result == "PASS", f"workbook QA!B{row_number} is {result!r}")
    require(workbook_source_ids == {row["source_id"] for row in rows(SOURCES)}, "workbook source register stale")
    require(workbook_claim_ids == {row["claim_id"] for row in rows(CLAIMS)}, "workbook claim register stale")
    require(workbook_cross_match_ids == {row["audit_match_id"] for row in rows(CROSS_METHOD_MATCHES)}, "workbook cross-method audit stale")
    return len(names), formulas, len(qa_results)


def iter_markdown_links(text: str) -> Iterable[str]:
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        if target and not re.match(r"^[a-z]+://", target) and not target.startswith("mailto:"):
            yield target.strip("<>")


def validate_local_links(allow_incomplete: bool) -> int:
    count = 0
    paths = [PROPOSED / name for name in BASE_EXPECTED_DOCS] + R2_REQUIRED_DOCS
    for path in dict.fromkeys(paths):
        if not path.exists():
            if allow_incomplete:
                continue
            raise ValidationFailure(f"documentation missing: {path}")
        if path.suffix != ".md":
            continue
        text = path.read_text()
        require("/Users/" not in text, f"absolute local path in {path.name}")
        for target in iter_markdown_links(text):
            count += 1
            require((path.parent / target).resolve().exists(), f"dangling link in {path.name}: {target}")
    return count


def validate_docs_r2_state() -> tuple[int, int]:
    for path in [R2_SOURCES, R2_CLAIMS, *R2_REQUIRED_DOCS]:
        require(path.is_file(), f"docs-r2 required file missing: {path}")
    classification = (PROPOSED / "CHANGE_CLASSIFICATION_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md").read_text()
    decision = (PROPOSED / "DEEP_CURATION_DECISION_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md").read_text()
    blueprint = (PROPOSED / "STRONG_WIND_REUSE_AND_V2_ACQUISITION_BLUEPRINT_tropical_cyclone_wind_solar__model_v1_0__docs_r2.md").read_text()
    root_readme = (ROOT / "docs/cells/tropical_cyclone_wind_solar/README.md").read_text()
    handoff = (ROOT / "docs/contracts/hazard_handoff/tropical_cyclone_wind_solar_model_v1_0_docs_r2_no_cutover.md").read_text()
    require(fenced_yaml_value(classification, "primary_change_class") == "EVIDENCE_ONLY_NO_OUTPUT_CHANGE", "docs-r2 change class drifted")
    require(fenced_yaml_value(classification, "outputs_can_change_for_same_inputs") == "false", "docs-r2 output-change flag drifted")
    require(fenced_yaml_value(classification, "runtime_proposal_revision") == "docs r1", "docs-r1 runtime boundary missing")
    require(fenced_yaml_value(decision, "portable_Hazard_axis_bridge") == "NO_GO", "axis bridge decision drifted")
    require(fenced_yaml_value(decision, "tracker_route") == "NO_GO", "tracker decision drifted")
    require(fenced_yaml_value(decision, "severe_tail_extension") == "NO_GO", "tail decision drifted")
    require(fenced_yaml_value(decision, "same_unit_economic_DR_expansion") == "NO_GO", "economic decision drifted")
    require(fenced_yaml_value(decision, "predictive_relationship_validated") == "false", "predictive-validity decision drifted")
    require(fenced_yaml_value(decision, "model_v1_1_earned") == "false", "model-v1.1 decision drifted")
    require(fenced_yaml_value(decision, "model_v2_0_earned") == "false", "model-v2.0 decision drifted")
    require("equal-record weighting" in decision, "equal-record weighting correction missing")
    require("no scientifically validated" in decision, "predictive-use prohibition missing")
    require("direct material, direct labor" in blueprint, "v2 economic acquisition field missing")
    require("command and attained tracker state" in blueprint, "v2 tracker-state acquisition field missing")
    # Model v2.1 is now the canonical lead. Historical model-v1 validation
    # must keep checking its own docs-r2 evidence package without requiring the
    # cell entrypoint to masquerade as the current v1 lead.
    require(
        fenced_yaml_value(root_readme, "semantic_damage_model_version") == "model v2.1",
        "cell entrypoint does not identify the later model-v2.1 lead",
    )
    require(
        fenced_yaml_value(root_readme, "documentation_revision") == "docs r2",
        "cell entrypoint model-v2.1 docs revision stale",
    )
    require(
        "model v1.0/docs r2 human, r1 runtime" in root_readme,
        "cell entrypoint no longer preserves the model-v1/docs-r2 alternative",
    )
    require(fenced_yaml_value(handoff, "consumer_cutover") == "prohibited", "no-cutover handoff drifted")
    require(fenced_yaml_value(handoff, "ordinary_Hazard_3s_gust_compatible") == "false", "Hazard-axis rejection missing")
    prohibited_r2_runtime_files = [
        PROPOSED / "tropical_cyclone_wind_solar__model_v1_0__docs_r2__curve_artifact.json",
        PROPOSED / "tropical_cyclone_wind_solar__model_v1_0__docs_r2__capability.json",
        PROPOSED / "known_answer_tests_tropical_cyclone_wind_solar__model_v1_0__docs_r2.json",
        PROPOSED / "damage_curve_records_tropical_cyclone_wind_solar__model_v1_0__docs_r2.xlsx",
    ]
    require(not [path for path in prohibited_r2_runtime_files if path.exists()], "docs-only revision created runtime-shaped docs-r2 files")
    for path, expected in EXPECTED_RUNTIME_HASHES.items():
        require(sha256(path) == expected, f"unchanged runtime-shaped file drifted: {path.name}")
    for path, expected in EXPECTED_HELPER_SCHEMA_HASHES.items():
        require(sha256(path) == expected, f"unchanged helper/schema file drifted: {path.name}")
    return len(EXPECTED_RUNTIME_HASHES), len(EXPECTED_HELPER_SCHEMA_HASHES)


def validate_index_and_raw_guard() -> None:
    index = load(INDEX)
    require(index["schema_version"] == "damage_curve_artifact_index.v2", "index schema changed")
    require(
        not [item for item in index["artifacts"] if (ROOT / item["path"]).resolve() == ARTIFACT.resolve()],
        "model-v1 proposal entered canonical index",
    )
    forbidden_names = {
        "hurricane_sites_manual.csv",
        "hurricane_sites_aggregated.csv",
        "ew_data_description.pdf",
        "ceferino_supplement.docx",
    }
    require(not [path for path in PROPOSED.rglob("*") if path.name in forbidden_names], "unlicensed raw source vendored")


def validate_pin(artifact: Mapping[str, Any]) -> str:
    digest = artifact_sha256(ARTIFACT)
    pin = {
        "cell_id": artifact["cell_id"],
        "semantic_damage_model_version": artifact["semantic_damage_model_version"],
        "documentation_revision": artifact["documentation_revision"],
        "schema_version": artifact["schema_version"],
        "artifact_sha256": digest,
    }
    verify_artifact_pin(artifact, pin, artifact_sha256_hex=digest)
    bad = dict(pin)
    bad["artifact_sha256"] = "0" * 64
    try:
        verify_artifact_pin(artifact, bad, artifact_sha256_hex=digest)
    except TropicalCycloneWindSolarEvaluationError as exc:
        require(exc.code == "ARTIFACT_PIN_MISMATCH", "bad pin error changed")
    else:
        raise ValidationFailure("bad artifact pin accepted")
    return digest


def main() -> None:
    allow_incomplete = "--allow-incomplete" in sys.argv[1:]
    if allow_incomplete:
        raise SystemExit("--allow-incomplete is not supported for the finalized docs-r2 evidence package")
    source_path: Path | None = None
    if "--source-csv" in sys.argv[1:]:
        index = sys.argv.index("--source-csv")
        try:
            source_path = Path(sys.argv[index + 1])
        except IndexError as exc:
            raise SystemExit("--source-csv requires a path") from exc
    artifact = load(ARTIFACT)
    capability = load(CAPABILITY)
    validate_top_level(artifact, capability)
    missing = validate_paths(artifact, allow_incomplete)
    schema_note = optional_schema_checks(artifact, capability)
    validate_curve(artifact)
    stats_count, sensitivity_count = validate_fit_statistics(artifact)
    source_note = validate_optional_source_csv(source_path, artifact)
    validate_capability_and_value(artifact)
    cross_match_count, cross_match_mean = validate_cross_method_match_audit()
    formula_kats, rejection_kats, withheld_kats = validate_kats(artifact)
    (
        base_source_count,
        base_claim_count,
        effective_source_count,
        effective_claim_count,
        parameter_count,
        value_count,
        old_count,
    ) = validate_registers(artifact)
    sheet_count, formula_count, workbook_qa_count = validate_workbook(allow_incomplete)
    link_count = validate_local_links(allow_incomplete)
    unchanged_runtime_hash_count, unchanged_helper_schema_hash_count = validate_docs_r2_state()
    validate_index_and_raw_guard()
    digest = validate_pin(artifact)

    print("PASS tropical_cyclone_wind_solar model v1.0/docs r2 evidence revision")
    print("runtime_proposal_revision=docs_r1_unchanged")
    print(f"checks={CHECKS.value}")
    print(f"schema_validation={schema_note}")
    print(f"source_derivation={source_note}")
    print(f"formula_kats={formula_kats}")
    print(f"rejection_kats={rejection_kats}")
    print(f"withheld_unit_kats={withheld_kats}")
    print(f"fit_stat_rows={stats_count}")
    print(f"event_sensitivity_rows={sensitivity_count}")
    print(f"cross_method_matches={cross_match_count}")
    print(f"cross_method_mean_absolute_difference_pp={cross_match_mean:.10f}")
    print(f"base_sources={base_source_count}")
    print(f"base_claims={base_claim_count}")
    print(f"effective_sources={effective_source_count}")
    print(f"effective_claims={effective_claim_count}")
    print(f"parameters={parameter_count}")
    print(f"value_rows={value_count}")
    print(f"old_vs_new_rows={old_count}")
    print(f"workbook_sheets={sheet_count}")
    print(f"workbook_formulas={formula_count}")
    print(f"workbook_qa_passes={workbook_qa_count}")
    print(f"local_links={link_count}")
    print(f"unchanged_runtime_hashes={unchanged_runtime_hash_count}")
    print(f"unchanged_helper_schema_hashes={unchanged_helper_schema_hash_count}")
    print(f"missing_allowed={len(missing)}")
    print(f"artifact_sha256={digest}")
    print(f"capability_sha256={sha256(CAPABILITY)}")
    print(f"known_answer_tests_sha256={sha256(KATS)}")
    print(f"workbook_sha256={sha256(WORKBOOK)}")


if __name__ == "__main__":
    main()
