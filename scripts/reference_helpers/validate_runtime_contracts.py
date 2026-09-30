#!/usr/bin/env python3
"""Validate repository-current v2/v3 damage artifacts and selected consumer seams.

This is a dependency-free semantic validator. JSON Schema validation remains the
structural contract; these checks cover cross-file hashes, path resolution,
curve-form payloads, capability semantics, and executable hail known answers.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "docs/contracts/machine_readable_artifact_index.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_curve_record(record: dict) -> None:
    form = record["curve_form"]
    parameters = record["parameters"]
    expected_keys = {
        "logistic": {"D50_mm", "k_per_mm", "max_DR"},
        "piecewise_linear": {"points"},
        "thresholded_logistic_demand": {"R0", "R50", "k", "max_DR"},
        "wind_tornado_logistic_ratio": {
            "D50_ratio_straight_line",
            "k_ratio",
            "max_DR",
            "tornado_D50_shift",
        },
    }
    require(form in expected_keys, f"unsupported curve_form {form!r}")
    require(
        set(parameters) == expected_keys[form],
        f"{record['curve_id']}: parameter keys do not match {form}",
    )
    require(record["y_axis"] == "failure_unit_damage_ratio", "unexpected y_axis")
    if form == "logistic":
        require(record["x_axis"] == "mesh_diameter_mm", "hail logistic x_axis changed")
        require(
            set(record.get("selector_match", {})) == {"module_archetype"},
            f"{record['curve_id']}: selector_match payload changed",
        )
    elif form == "piecewise_linear":
        points = parameters["points"]
        require(len(points) >= 2, f"{record['curve_id']}: too few points")
        require(all(len(point) == 2 for point in points), "piecewise point must be [x, DR]")
        require(all(0 <= point[1] <= 1 for point in points), "piecewise DR outside [0,1]")
    elif form == "wind_tornado_logistic_ratio":
        require(
            isinstance(record.get("include_in_default_structural_aggregate"), bool),
            f"{record['curve_id']}: aggregate flag missing",
        )


def validate_capability(artifact: dict) -> None:
    capability = artifact["capability_declaration"]
    require(capability["schema_version"] == "capability_declaration.v2", "capability v2 required")
    require(capability["cell_id"] == artifact["cell_id"], "capability cell mismatch")
    emit = capability["vulnerability_emit"]
    require(emit["failure_unit_scalar_dr"] == "supported", "current cell DR must be supported")
    annual = capability["consumer_annual_metrics"]
    require(annual["computation_owner"] == "downstream_consumer", "metric owner mismatch")
    require(
        annual["frequency_driven_annual_loss_distribution"]
        == "supported_if_consumer_samples_frequency_intensity_coupling_and_applies_caps",
        "frequency-driven tail contract missing",
    )
    require(
        annual["vulnerability_uncertainty_distribution"]
        == "not_supported_curve_intrinsic_spread_not_carried",
        "curve-intrinsic spread limitation missing",
    )
    require(
        "CURVE_INTRINSIC_SPREAD_NOT_CARRIED" in annual["limitation_flags"],
        "vulnerability-spread flag missing",
    )
    require(
        capability["cap_binding"]["enforcement_owner"] == "downstream_consumer",
        "cap enforcement owner mismatch",
    )


def validate_v3_curve_record(record: dict) -> None:
    form = record["curve_form"]
    parameters = record["parameters"]
    require(record["y_axis"] == "failure_unit_damage_ratio", "unexpected v3 y_axis")
    if form == "piecewise_linear":
        require(set(parameters) == {"points"}, f"{record['curve_id']}: invalid piecewise payload")
        points = parameters["points"]
        require(len(points) >= 2, f"{record['curve_id']}: too few points")
        require(all(len(point) == 2 for point in points), "piecewise point must be [x, DR]")
        require(all(left[0] < right[0] for left, right in zip(points, points[1:])), "v3 axis not increasing")
        require(all(0 <= point[1] <= 1 for point in points), "v3 piecewise DR outside [0,1]")
        return
    if form == "thresholded_weibull_expected_damage":
        require(
            set(parameters) == {"V_zero_kmh", "delta_V50_kmh", "rho", "V_at_DR50_kmh", "max_dr"},
            f"{record['curve_id']}: invalid thresholded-Weibull payload",
        )
        require(parameters["V_zero_kmh"] >= 0, f"{record['curve_id']}: negative threshold")
        require(parameters["delta_V50_kmh"] > 0, f"{record['curve_id']}: nonpositive delta")
        require(parameters["rho"] > 0, f"{record['curve_id']}: nonpositive rho")
        require(0 < parameters["max_dr"] <= 1, f"{record['curve_id']}: invalid max_dr")
        require(
            math.isclose(
                parameters["V_at_DR50_kmh"],
                parameters["V_zero_kmh"] + parameters["delta_V50_kmh"],
                rel_tol=0,
                abs_tol=1e-12,
            ),
            f"{record['curve_id']}: D50 identity mismatch",
        )
        return
    if form == "ordered_damage_state_lognormal":
        require(
            set(parameters) == {"beta_ln", "damage_states", "capacity_scenarios"},
            f"{record['curve_id']}: invalid ordered-state payload",
        )
        require(parameters["beta_ln"] > 0, f"{record['curve_id']}: nonpositive beta")
        states = parameters["damage_states"]
        require(len(states) >= 2, f"{record['curve_id']}: too few damage states")
        state_ids = [state["state_id"] for state in states]
        require(len(state_ids) == len(set(state_ids)), f"{record['curve_id']}: duplicate state")
        cost_ratios = [state["cost_ratio"] for state in states]
        require(all(0 <= value <= 1 for value in cost_ratios), f"{record['curve_id']}: state cost outside [0,1]")
        require(cost_ratios == sorted(cost_ratios), f"{record['curve_id']}: state costs unordered")
        scenarios = parameters["capacity_scenarios"]
        require(scenarios, f"{record['curve_id']}: no capacity scenarios")
        scenario_ids = [scenario["scenario_id"] for scenario in scenarios]
        require(len(scenario_ids) == len(set(scenario_ids)), f"{record['curve_id']}: duplicate scenario")
        for scenario in scenarios:
            medians = scenario["state_medians"]
            require(
                len(medians) == len(states) - 1,
                f"{record['curve_id']}: median/state boundary mismatch",
            )
            require(all(value > 0 for value in medians), f"{record['curve_id']}: nonpositive median")
            require(
                all(left < right for left, right in zip(medians, medians[1:])),
                f"{record['curve_id']}: state medians unordered",
            )
        return
    raise AssertionError(f"unsupported v3 curve_form {form!r}")


def validate_v3_artifact(artifact: dict) -> int:
    capability = artifact["capability_declaration"]
    require(capability["schema_version"] == "capability_declaration.v3", "capability v3 required")
    require(capability["cell_id"] == artifact["cell_id"], "v3 capability cell mismatch")
    require(capability["canonical_runtime_artifact"] is True, "v3 capability is noncanonical")
    require(
        capability["consumer_annual_metrics"]["computation_owner"] == "downstream_consumer",
        "v3 metric owner mismatch",
    )
    require(
        capability["cap_binding"]["enforcement_owner"] == "downstream_consumer",
        "v3 cap enforcement owner mismatch",
    )
    pathways = artifact["pathways"]
    require(pathways, "v3 artifact has no pathways")
    ids = [pathway["pathway_id"] for pathway in pathways]
    require(len(ids) == len(set(ids)), "duplicate v3 pathway_id")
    capability_ids = [item["pathway_id"] for item in capability["pathway_capabilities"]]
    require(capability_ids == ids, "v3 artifact/capability pathway mismatch")
    record_count = 0
    for pathway in pathways:
        records = pathway["curve_records"]
        for record in records:
            validate_v3_curve_record(record)
            record_count += 1
    require(record_count > 0, "indexed v3 artifact has no curve records")
    return record_count


def logistic(record: dict, diameter_mm: float) -> float:
    parameters = record["parameters"]
    return parameters["max_DR"] / (
        1.0
        + math.exp(
            -parameters["k_per_mm"] * (diameter_mm - parameters["D50_mm"])
        )
    )


def select_hail_record(
    records: list[dict], selector: str | None, default_selector: str
) -> tuple[dict | None, str | None, bool]:
    requested = selector if selector is not None else default_selector
    matches = [
        record
        for record in records
        if record["selector_match"]["module_archetype"] == requested
    ]
    if not matches:
        return None, "CURVE_SELECTOR_MATCH_NOT_FOUND", selector is None
    if len(matches) > 1:
        return None, "CURVE_SELECTOR_MATCH_NOT_UNIQUE", selector is None
    return matches[0], None, selector is None


def validate_hail_known_answers(artifact: dict) -> tuple[int, int, int]:
    kat_path = ROOT / artifact["known_answer_tests"]
    tests = load(kat_path)
    require(tests["semantic_damage_model_version"] == "model v1.0", "hail model changed")
    require(tests["documentation_revision"] == "docs r7", "hail KAT docs mismatch")
    tolerance = tests["absolute_tolerance"]
    records_by_selector = {
        record["selector_match"]["module_archetype"]: record
        for record in artifact["curve_records"]
    }
    records = artifact["curve_records"]
    require(len(records_by_selector) == len(records), "duplicate hail selectors")
    default_selector = next(
        item["default"]
        for item in artifact["selector_logic"]
        if item["field"] == "module_archetype"
    )

    for test in tests["runtime_curve_known_answer_tests"]:
        values = test["input"]
        selector = values.get("module_archetype")
        record, error_code, used_default = select_hail_record(
            records, selector, default_selector
        )
        require(error_code is None and record is not None, f"{test['test_id']}: selector missing")
        diameter = values.get("mesh_diameter_mm")
        if diameter is None:
            require(values["source_unit"] == "in", "only inch conversion is governed here")
            diameter = values["hail_diameter"] * 25.4
        expected = test["expected"]
        actual = logistic(record, diameter)
        require(
            abs(actual - expected["failure_unit_damage_ratio"]) <= tolerance,
            f"{test['test_id']}: DR mismatch {actual}",
        )
        require(expected["curve_id"] == record["curve_id"], "curve_id mismatch")
        if "module_archetype" in expected:
            require(
                expected["module_archetype"]
                == record["selector_match"]["module_archetype"],
                "module archetype mismatch",
            )
        if used_default:
            require(
                "DEFAULT_SELECTOR_USED" in expected.get("metadata_flags", []),
                "missing default-selector flag",
            )
        if "mesh_diameter_mm_used" in expected:
            require(abs(diameter - expected["mesh_diameter_mm_used"]) <= tolerance, "unit conversion mismatch")

    for test in tests["selector_contract_tests"]:
        fixture = records
        selector = test.get("input", {}).get("module_archetype")
        if test.get("fixture_mutation") == "duplicate the default module_archetype selector_match":
            default_record = records_by_selector[default_selector]
            fixture = [*records, default_record]
            selector = default_selector
        record, error_code, _ = select_hail_record(fixture, selector, default_selector)
        require(record is None, f"{test['test_id']}: selector should be rejected")
        require(
            error_code == test["expected"]["error_code"],
            f"{test['test_id']}: wrong selector error code",
        )

    profiles = {
        profile["value_profile_id"]: profile
        for profile in artifact["value_linkage"]["value_profiles"]
    }
    require(artifact["value_linkage"]["implicit_default_profile"] is None, "value profile must be explicit")
    for profile in profiles.values():
        require(
            0 <= profile["failure_unit_share_physical_base"] <= 1,
            f"{profile['value_profile_id']}: physical share outside [0,1]",
        )
        require(
            0 <= profile["failure_unit_share_installed_capex"] <= 1,
            f"{profile['value_profile_id']}: installed share outside [0,1]",
        )
    for test in tests["value_linkage_known_answer_tests"]:
        if "value_profile_id" not in test["input"]:
            require(test["expected"]["asset_loss_status"] == "withheld", "missing profile must withhold")
            require(
                test["expected"]["error_code"]
                == "EXPLICIT_VALUE_PROFILE_OR_SITE_VALUE_BASIS_REQUIRED",
                "missing profile reason code changed",
            )
            continue
        profile = profiles[test["input"]["value_profile_id"]]
        dr = test["input"].get("failure_unit_damage_ratio")
        if dr is None:
            selector = test["input"]["module_archetype"]
            dr = logistic(records_by_selector[selector], test["input"]["mesh_diameter_mm"])
        exposure = test["input"].get("array_exposure_fraction", 1.0)
        require(0 <= exposure <= 1, f"{test['test_id']}: exposure outside [0,1]")
        physical_loss = dr * exposure * profile["failure_unit_share_physical_base"]
        installed_loss = dr * exposure * profile["failure_unit_share_installed_capex"]
        expected = test["expected"]
        if "failure_unit_damage_ratio" in expected:
            require(
                abs(dr - expected["failure_unit_damage_ratio"]) <= tolerance,
                f"{test['test_id']}: value-link DR mismatch",
            )
        if "physical_base_loss_fraction" in expected:
            require(abs(physical_loss - expected["physical_base_loss_fraction"]) <= tolerance, "physical loss KAT failed")
            require(abs(installed_loss - expected["installed_capex_loss_fraction"]) <= tolerance, "installed loss KAT failed")
        if "asymptotic_asset_loss_cap_physical_base" in expected:
            require(abs(physical_loss - expected["asymptotic_asset_loss_cap_physical_base"]) <= tolerance, "physical cap KAT failed")
            require(abs(installed_loss - expected["asymptotic_asset_loss_cap_installed_capex"]) <= tolerance, "installed cap KAT failed")

    basis = artifact["value_linkage"]["reference_basis"]
    require(
        abs(
            basis["physical_replaceable_usd_per_kwdc"]
            / basis["installed_capex_usd_per_kwdc"]
            - basis["physical_to_installed_ratio"]
        )
        <= tolerance,
        "value-basis denominator conversion failed",
    )
    for profile in profiles.values():
        require(
            abs(
                profile["failure_unit_share_physical_base"]
                * basis["physical_to_installed_ratio"]
                - profile["failure_unit_share_installed_capex"]
            )
            <= tolerance,
            f"{profile['value_profile_id']}: denominator shares do not reconcile",
        )
    return (
        len(tests["runtime_curve_known_answer_tests"]),
        len(tests["selector_contract_tests"]),
        len(tests["value_linkage_known_answer_tests"]),
    )


def exact_state_value(record: dict, state_index: int) -> float:
    require(isinstance(state_index, int), "wildfire state must be an integer")
    matches = [point[1] for point in record["parameters"]["points"] if point[0] == state_index]
    require(len(matches) == 1, f"{record['curve_id']}: exact state missing or duplicated")
    return float(matches[0])


def wildfire_reference_loss(artifact: dict, dr_by_unit: dict[str, float]) -> tuple[float, float]:
    linkage = artifact["value_linkage"]
    profile = linkage["value_profiles"][0]
    values = profile["failure_unit_values_usd_per_kwdc"]
    require(set(values) == set(dr_by_unit), "wildfire value/curve coverage mismatch")
    direct_total = sum(values.values())
    direct_damage = sum(values[key] * dr_by_unit[key] for key in values)
    physical_dr = direct_damage / direct_total
    installed_dr = physical_dr * linkage["reference_basis"]["physical_to_installed_ratio"]
    return physical_dr, installed_dr


def validate_wildfire_known_answers(artifact: dict) -> tuple[int, int, int, int]:
    tests = load(ROOT / artifact["known_answer_tests"])
    require(tests["semantic_damage_model_version"] == "model v1.0", "wildfire model changed")
    require(tests["documentation_revision"] == "docs r3", "wildfire KAT docs mismatch")
    tolerance = tests["absolute_tolerance"]
    records = {record["failure_unit_id"]: record for record in artifact["curve_records"]}
    require(len(records) == 10, "wildfire failure-unit curve coverage changed")
    require(
        artifact["evaluation_contract"]["state_lookup"] == "exact_integer_only"
        and artifact["evaluation_contract"]["interpolation_between_states"] == "prohibited",
        "wildfire exact-state contract changed",
    )
    class_map = tests["class_map"]
    require(class_map == artifact["hazard_axis"]["native_class_map"], "wildfire class map mismatch")

    for record in records.values():
        points = record["parameters"]["points"]
        require([point[0] for point in points] == list(range(7)), "wildfire states must be 0..6")
        ordinates = [point[1] for point in points]
        require(ordinates[0] == 0, f"{record['curve_id']}: state 0 must be zero")
        require(all(left <= right for left, right in zip(ordinates, ordinates[1:])), "wildfire curve not monotone")

    for test in tests["failure_unit_state_tests"]:
        values = test["input"]
        state_index = values.get("state_index")
        if state_index is None:
            state_index = class_map[values["conditional_flame_length_class"]]
        actual = exact_state_value(records[values["failure_unit_id"]], state_index)
        require(
            abs(actual - test["expected_failure_unit_damage_ratio"]) <= tolerance,
            f"{test['test_id']}: wildfire DR mismatch",
        )

    for test in tests["aggregate_reference_profile_tests"]:
        state_index = test["state_index"]
        dr_by_unit = {
            failure_unit_id: exact_state_value(record, state_index)
            for failure_unit_id, record in records.items()
        }
        physical, installed = wildfire_reference_loss(artifact, dr_by_unit)
        require(abs(physical - test["expected_physical_base_loss_fraction"]) <= tolerance, f"{test['test_id']}: physical loss mismatch")
        require(abs(installed - test["expected_installed_capex_loss_fraction"]) <= tolerance, f"{test['test_id']}: installed loss mismatch")

    for test in tests["conditional_distribution_tests"]:
        probabilities = test["input"]["conditional_flame_length_probability_by_bin"]
        require(set(probabilities) == set(class_map), "wildfire FLP keys changed")
        require(all(0 <= value <= 1 for value in probabilities.values()), "wildfire FLP outside [0,1]")
        require(abs(sum(probabilities.values()) - 1.0) <= tolerance, "wildfire FLP must sum to one")
        dr_by_unit = {}
        for failure_unit_id, record in records.items():
            dr_by_unit[failure_unit_id] = sum(
                probabilities[class_id] * exact_state_value(record, state_index)
                for class_id, state_index in class_map.items()
            )
            require(
                abs(dr_by_unit[failure_unit_id] - test["expected_failure_unit_damage_ratios"][failure_unit_id]) <= tolerance,
                f"{test['test_id']}: distribution DR mismatch for {failure_unit_id}",
            )
        physical, installed = wildfire_reference_loss(artifact, dr_by_unit)
        require(abs(physical - test["expected_physical_base_loss_fraction"]) <= tolerance, "wildfire distribution physical loss mismatch")
        require(abs(installed - test["expected_installed_capex_loss_fraction"]) <= tolerance, "wildfire distribution installed loss mismatch")

    contract_codes = {test["expected"].get("error_code") for test in tests["contract_tests"]}
    require("FSIM_CLASS_NOT_RECOGNIZED" in contract_codes, "wildfire unknown-class test missing")
    require("EXACT_STATE_LOOKUP_REQUIRED" in contract_codes, "wildfire interpolation test missing")
    require("FLP_VECTOR_MUST_SUM_TO_ONE" in contract_codes, "wildfire FLP normalization test missing")
    require("FREQUENCY_FIELD_NOT_ALLOWED_IN_DAMAGE_CALL" in contract_codes, "wildfire frequency-separation test missing")
    require(
        artifact["value_linkage"]["implicit_default_profile"] is None,
        "wildfire value profile must be explicit",
    )
    basis = artifact["value_linkage"]["reference_basis"]
    require(
        abs(
            basis["physical_replaceable_usd_per_kwdc"]
            / basis["installed_capex_usd_per_kwdc"]
            - basis["physical_to_installed_ratio"]
        )
        <= tolerance,
        "wildfire denominator conversion failed",
    )
    return (
        len(tests["failure_unit_state_tests"]),
        len(tests["aggregate_reference_profile_tests"]),
        len(tests["conditional_distribution_tests"]),
        len(tests["contract_tests"]),
    )


def main() -> None:
    index = load(INDEX)
    require(index["schema_version"] == "damage_curve_artifact_index.v2", "artifact index v2 required")
    total_runtime_kats = 0
    total_selector_kats = 0
    total_value_kats = 0
    wildfire_state_kats = 0
    wildfire_aggregate_kats = 0
    wildfire_distribution_kats = 0
    wildfire_contract_tests = 0
    v3_artifact_count = 0
    v3_curve_record_count = 0
    for entry in index["artifacts"]:
        path = ROOT / entry["path"]
        require(path.exists(), f"artifact missing: {entry['path']}")
        require(sha256(path) == entry["sha256"], f"SHA mismatch: {entry['cell_id']}")
        artifact = load(path)
        schema_version = artifact["schema_version"]
        require(
            schema_version in {"damage_curve_record_bundle.v2", "damage_curve_record_bundle.v3"},
            "bundle v2 or v3 required",
        )
        require(artifact["cell_id"] == entry["cell_id"], "index cell mismatch")
        require(artifact["semantic_damage_model_version"] == entry["semantic_damage_model_version"], "model pin mismatch")
        require(artifact["documentation_revision"] == entry["documentation_revision"], "docs pin mismatch")
        require(artifact["canonical_runtime_artifact"] is True, "noncanonical artifact indexed")
        for pointer in (artifact["source_dossier"], artifact["source_workbook"]):
            if pointer is not None:
                require(pointer.startswith("docs/cells/"), f"noncanonical source path: {pointer}")
                require((ROOT / pointer).exists(), f"dangling source path: {pointer}")
        serialized = json.dumps(artifact)
        require("01_cells/" not in serialized, f"legacy source path in {entry['cell_id']}")
        require("Hazard_modeling/" not in serialized, f"downstream path in {entry['cell_id']}")
        if schema_version == "damage_curve_record_bundle.v2":
            for record in artifact["curve_records"]:
                validate_curve_record(record)
            validate_capability(artifact)
        else:
            v3_artifact_count += 1
            v3_curve_record_count += validate_v3_artifact(artifact)
        changelog = load(ROOT / entry["changelog_path"])
        require(changelog["current_pin"] == entry["consumer_pin"], "changelog pin mismatch")
        if entry["cell_id"] == "hail_solar":
            runtime, selector, value = validate_hail_known_answers(artifact)
            total_runtime_kats += runtime
            total_selector_kats += selector
            total_value_kats += value
        elif entry["cell_id"] == "wildfire_solar":
            state, aggregate, distribution, contract = validate_wildfire_known_answers(artifact)
            wildfire_state_kats += state
            wildfire_aggregate_kats += aggregate
            wildfire_distribution_kats += distribution
            wildfire_contract_tests += contract

    print(
        json.dumps(
            {
                "status": "PASS",
                "artifact_count": len(index["artifacts"]),
                "hail_runtime_kats": total_runtime_kats,
                "hail_selector_contract_tests": total_selector_kats,
                "hail_value_linkage_kats": total_value_kats,
                "wildfire_state_kats": wildfire_state_kats,
                "wildfire_aggregate_kats": wildfire_aggregate_kats,
                "wildfire_distribution_kats": wildfire_distribution_kats,
                "wildfire_contract_tests": wildfire_contract_tests,
                "v3_artifact_count": v3_artifact_count,
                "v3_curve_record_count": v3_curve_record_count,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
