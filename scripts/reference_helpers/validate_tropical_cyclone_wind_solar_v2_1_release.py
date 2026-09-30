#!/usr/bin/env python3
"""Validate the canonical TC-wind x solar v2.1 release and promotion parity."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
CELL = ROOT / "docs/cells/tropical_cyclone_wind_solar"
PROPOSED = CELL / "proposed"
CURRENT = CELL / "current"
PROPOSED_NAME = "tropical_cyclone_wind_solar__model_v2_1__docs_r1"
CURRENT_NAME = "tropical_cyclone_wind_solar__model_v2_1__docs_r2"
PROPOSED_ARTIFACT = PROPOSED / f"{PROPOSED_NAME}__curve_artifact.json"
CURRENT_ARTIFACT = CURRENT / f"{CURRENT_NAME}__curve_artifact.json"
PROPOSED_CAPABILITY = PROPOSED / f"{PROPOSED_NAME}__capability.json"
CURRENT_CAPABILITY = CURRENT / f"{CURRENT_NAME}__capability.json"
PROPOSED_KATS = PROPOSED / f"known_answer_tests_{PROPOSED_NAME}.json"
CURRENT_KATS = CURRENT / f"known_answer_tests_{CURRENT_NAME}.json"
INDEX = ROOT / "docs/contracts/machine_readable_artifact_index.json"
SCHEMA_DIR = ROOT / "docs/contracts/schemas"

PROPOSAL_SHA = "4dd951495a9fedd975b5e519d778dae1e3c01b8bc48db0f6b1bebbec78146602"
PROPOSED_CODE = "TROPICAL_CYCLONE_WIND_SOLAR_SCREENING_COMPLETE_V2_1_PROPOSED"
CURRENT_CODE = "TROPICAL_CYCLONE_WIND_SOLAR_SCREENING_COMPLETE_V2_1"

sys.path.insert(0, str(ROOT / "scripts/reference_helpers"))
import tropical_cyclone_wind_solar_v2_curve_eval as v20  # noqa: E402
import tropical_cyclone_wind_solar_v2_1_curve_eval as evaluator  # noqa: E402
from build_tropical_cyclone_wind_solar_v2_1_package import (  # noqa: E402
    direct_gsu_request,
    full_fixed_request,
    full_tracker_request,
)


class ValidationFailure(AssertionError):
    pass


class Checks:
    count = 0


def require(condition: bool, message: str) -> None:
    Checks.count += 1
    if not condition:
        raise ValidationFailure(message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalized_ids(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalized_ids(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalized_ids(item) for item in value]
    if value == CURRENT_CODE:
        return PROPOSED_CODE
    if value == "CANONICAL_SCREENING_RELEASE":
        return "NONCANONICAL_MODEL_V2_1"
    if isinstance(value, str):
        return value.replace("model_v2_1__docs_r2", "model_v2_1__docs_r1").replace(
            "docs r2", "docs r1"
        )
    return value


def _json_differences(left: Any, right: Any, path: str = "") -> list[str]:
    differences: list[str] = []
    if type(left) is not type(right):
        return [path]
    if isinstance(left, dict):
        for key in sorted(set(left) | set(right)):
            child = f"{path}/{key}"
            if key not in left or key not in right:
                differences.append(child)
            else:
                differences.extend(_json_differences(left[key], right[key], child))
        return differences
    if isinstance(left, list):
        if len(left) != len(right):
            differences.append(f"{path}/length")
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences.extend(_json_differences(left_item, right_item, f"{path}/{index}"))
        return differences
    if left != right:
        differences.append(path)
    return differences


def validate_identity(
    proposed: Mapping[str, Any],
    current: Mapping[str, Any],
    capability: Mapping[str, Any],
) -> None:
    require(sha(PROPOSED_ARTIFACT) == PROPOSAL_SHA, "immutable proposal bytes changed")
    require(proposed["canonical_runtime_artifact"] is False, "proposal became canonical")
    require(proposed["damage_code_id"] == PROPOSED_CODE, "proposal identity changed")
    require(current["schema_status"] == "released", "release schema status")
    require(current["documentation_revision"] == "docs r2", "release docs revision")
    require(current["lifecycle_state"] == "released_v2_1", "release lifecycle")
    require(current["promotion_status"] == "released", "release promotion status")
    require(current["canonical_runtime_artifact"] is True, "release is not canonical")
    require(current["damage_code_id"] == CURRENT_CODE, "canonical damage-code identity")
    require(
        current["package_inclusion_status"] == "repository_canonical_not_in_portable_package",
        "package inclusion status",
    )
    require(current["capability_declaration"] == capability, "embedded capability mismatch")
    require(capability["canonical_runtime_artifact"] is True, "capability is noncanonical")
    require(capability["promotion_gate"]["status"] == "passed", "promotion gate not passed")
    require(
        current["pathways"][0]["exposure_contract"]["scenario_loss_status"]
        == "supported_only_with_explicit_named_value_profile_and_exposure_basis",
        "scenario-loss capability remains stale",
    )


def validate_schemas(artifact: Mapping[str, Any], capability: Mapping[str, Any]) -> None:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    schema_paths = [
        SCHEMA_DIR / "curve_artifact_bundle.v3.schema.json",
        SCHEMA_DIR / "capability_declaration.v3.schema.json",
        SCHEMA_DIR / "damage_emit.v2.schema.json",
        SCHEMA_DIR / "physical_damage_assembly.v1.schema.json",
    ]
    schemas = [load(path) for path in schema_paths]
    registry = Registry().with_resources(
        [(schema["$id"], Resource.from_contents(schema)) for schema in schemas]
    )
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    Draft202012Validator(schemas[1], registry=registry).validate(capability)
    Draft202012Validator(schemas[0], registry=registry).validate(artifact)
    fixed = evaluator.evaluate_damage_call(artifact, full_fixed_request(1.0, 1.0))
    direct = evaluator.evaluate_damage_call(artifact, direct_gsu_request(1.0))
    Draft202012Validator(schemas[2], registry=registry).validate(fixed["damage_emit"])
    Draft202012Validator(schemas[3], registry=registry).validate(
        fixed["physical_damage_assembly"]
    )
    Draft202012Validator(schemas[2], registry=registry).validate(direct)


def validate_promotion_diff(
    proposed: Mapping[str, Any], current: Mapping[str, Any]
) -> None:
    expected = {
        "/canonical_runtime_artifact",
        "/capability_declaration/canonical_runtime_artifact",
        "/capability_declaration/promotion_gate/required_before_canonical_use/0",
        "/capability_declaration/promotion_gate/required_before_canonical_use/1",
        "/capability_declaration/promotion_gate/required_before_canonical_use/2",
        "/capability_declaration/promotion_gate/required_before_canonical_use/3",
        "/capability_declaration/promotion_gate/status",
        "/claim_parameter_register",
        "/claim_supersession_map",
        "/damage_code_id",
        "/documentation_revision",
        "/failure_units/1/denominator",
        "/failure_units/2/denominator",
        "/failure_units/3/denominator",
        "/failure_units/4/denominator",
        "/known_answer_tests",
        "/legacy_comparison/artifact_index_status",
        "/lifecycle_state",
        "/package_inclusion_status",
        "/pathways/0/exposure_contract/scenario_loss_status",
        "/promotion_status",
        "/review_status",
        "/schema_status",
        "/screening_curve_table",
        "/source_dossier",
        "/source_register",
        "/source_workbook",
        "/value_crosswalk",
    }
    actual = set(_json_differences(proposed, current))
    require(actual == expected, f"unexpected proposal-to-current artifact diff: {sorted(actual ^ expected)}")
    require(
        proposed["pathways"][0]["curve_records"] == current["pathways"][0]["curve_records"],
        "curve records changed during promotion",
    )
    require(proposed["value_linkage"] == current["value_linkage"], "value linkage changed")
    require(proposed["emit_contract"] == current["emit_contract"], "emit contract changed")
    require(proposed["evaluation_contract"] == current["evaluation_contract"], "evaluation contract changed")


def validate_supporting_bytes() -> None:
    proposed_names = [
        "SOURCE_REGISTER_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv",
        "CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv",
        "CLAIM_SUPERSESSION_MAP_tropical_cyclone_wind_solar__model_v2_0__docs_r1.csv",
        "PARAMETER_TIER_TABLE_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv",
        "VALUE_CROSSWALK_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv",
        "OLD_VS_NEW_COMPARISON_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv",
        "FULL_PLANT_SCREENING_CURVE_TABLE_tropical_cyclone_wind_solar__model_v2_1__docs_r1.csv",
        "damage_curve_records_tropical_cyclone_wind_solar__model_v2_1__docs_r1.xlsx",
    ]
    for proposed_name in proposed_names:
        current_name = proposed_name.replace("model_v2_1__docs_r1", "model_v2_1__docs_r2")
        if proposed_name.endswith(".xlsx"):
            same = sha(PROPOSED / proposed_name) == sha(CURRENT / current_name)
        else:
            same = (PROPOSED / proposed_name).read_text() == (
                CURRENT / current_name
            ).read_text().replace("model_v2_1__docs_r2", "model_v2_1__docs_r1")
        require(same, f"supporting content changed beyond docs revision: {current_name}")


def validate_dual_read(
    proposed: Mapping[str, Any], current: Mapping[str, Any]
) -> int:
    ratios = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
    comparisons = 0
    for request_factory in (full_fixed_request, full_tracker_request):
        for array_ratio in ratios:
            for site_ratio in ratios:
                request = request_factory(array_ratio, site_ratio)
                proposal_output = evaluator.evaluate_damage_call(proposed, request)
                current_output = evaluator.evaluate_damage_call(current, request)
                require(
                    proposal_output == _normalized_ids(current_output),
                    f"dual-read drift for {request['array_architecture']} at {array_ratio}, {site_ratio}",
                )
                comparisons += 1
    for site_ratio in ratios:
        request = direct_gsu_request(site_ratio)
        proposal_output = evaluator.evaluate_damage_call(proposed, request)
        current_output = evaluator.evaluate_damage_call(current, request)
        require(proposal_output == _normalized_ids(current_output), f"GSU drift at {site_ratio}")
        comparisons += 1
    return comparisons


def validate_kats(artifact: Mapping[str, Any]) -> tuple[int, int]:
    proposed_fixture = load(PROPOSED_KATS)
    fixture = load(CURRENT_KATS)
    require(proposed_fixture == _normalized_ids(fixture), "KAT promotion changed more than identity")
    for test in fixture["runtime_known_answer_tests"]:
        actual = evaluator.evaluate_damage_call(artifact, test["request"])
        require(actual == test["expected"], f"{test['test_id']}: canonical KAT drift")
    for test in fixture["rejection_tests"]:
        try:
            evaluator.evaluate_damage_call(artifact, test["request"])
        except (
            evaluator.TropicalCycloneWindSolarV21EvaluationError,
            v20.TropicalCycloneWindSolarV2EvaluationError,
        ) as error:
            require(error.code == test["expected_error_code"], f"{test['test_id']}: wrong error")
        else:
            raise ValidationFailure(f"{test['test_id']}: rejection missing")
    return len(fixture["runtime_known_answer_tests"]), len(fixture["rejection_tests"])


def validate_index(artifact: Mapping[str, Any]) -> None:
    index = load(INDEX)
    entries = [
        entry for entry in index["artifacts"]
        if entry["cell_id"] == "tropical_cyclone_wind_solar"
    ]
    require(len(entries) == 1, "expected one artifact-index entry")
    entry = entries[0]
    require(entry["damage_code_id"] == CURRENT_CODE, "index damage-code identity")
    require(entry["semantic_damage_model_version"] == "model v2.1", "index model version")
    require(entry["documentation_revision"] == "docs r2", "index docs revision")
    require(entry["artifact_schema_version"] == "damage_curve_record_bundle.v3", "index schema")
    require(entry["capability_schema_version"] == "capability_declaration.v3", "index capability schema")
    require(ROOT / entry["path"] == CURRENT_ARTIFACT, "index does not point at current artifact")
    require(entry["sha256"] == sha(CURRENT_ARTIFACT), "index SHA mismatch")
    require("/proposed/" not in entry["path"], "index points at proposal")
    require((ROOT / entry["known_answer_tests_path"]) == CURRENT_KATS, "index KAT path")
    require((ROOT / entry["changelog_path"]).exists(), "index changelog missing")
    pin = {
        "cell_id": artifact["cell_id"],
        "semantic_damage_model_version": artifact["semantic_damage_model_version"],
        "documentation_revision": artifact["documentation_revision"],
        "schema_version": artifact["schema_version"],
        "artifact_sha256": entry["sha256"],
    }
    v20.verify_artifact_pin(artifact, pin, artifact_sha256_hex=entry["sha256"])


def main() -> int:
    proposed = load(PROPOSED_ARTIFACT)
    current = load(CURRENT_ARTIFACT)
    capability = load(CURRENT_CAPABILITY)
    validate_identity(proposed, current, capability)
    validate_schemas(current, capability)
    validate_promotion_diff(proposed, current)
    validate_supporting_bytes()
    comparisons = validate_dual_read(proposed, current)
    runtime_kats, rejection_kats = validate_kats(current)
    validate_index(current)
    print("PASS tropical_cyclone_wind_solar model v2.1/docs r2 canonical screening release")
    print(f"checks={Checks.count}")
    print(f"proposal_sha256={sha(PROPOSED_ARTIFACT)}")
    print(f"canonical_sha256={sha(CURRENT_ARTIFACT)}")
    print(f"dual_read_comparisons={comparisons}")
    print(f"runtime_kats={runtime_kats}")
    print(f"rejection_kats={rejection_kats}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationFailure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
