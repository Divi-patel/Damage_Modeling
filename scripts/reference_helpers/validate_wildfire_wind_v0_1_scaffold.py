#!/usr/bin/env python3.12
"""Validate the noncanonical wildfire x wind model-v0.1 coverage scaffold.

The cell is intentionally fail closed: it contains no runtime curve record and
must never become a numerical fallback for Hazard.  This validator checks the
governed JSON, evidence/value CSVs, workbook, repository-local links, artifact
pointers, and absence from the canonical artifact index using only the Python
standard library.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
CELL = ROOT / "docs/cells/wildfire_wind"
PROPOSED = CELL / "proposed"
ARTIFACT_PATH = (
    PROPOSED / "wildfire_wind__model_v0_1__docs_r1__curve_artifact.json"
)
CAPABILITY_PATH = (
    PROPOSED / "wildfire_wind__model_v0_1__docs_r1__capability.json"
)
KAT_PATH = (
    PROPOSED / "known_answer_tests_wildfire_wind__model_v0_1__docs_r1.json"
)
SOURCE_PATH = (
    PROPOSED / "SOURCE_REGISTER_wildfire_wind__model_v0_1__docs_r1.csv"
)
CLAIM_PATH = (
    PROPOSED / "CLAIM_PARAMETER_REGISTER_wildfire_wind__model_v0_1__docs_r1.csv"
)
PARAMETER_PATH = (
    PROPOSED / "PARAMETER_TIER_TABLE_wildfire_wind__model_v0_1__docs_r1.csv"
)
VALUE_PATH = (
    PROPOSED / "VALUE_CROSSWALK_wildfire_wind__model_v0_1__docs_r1.csv"
)
WORKBOOK_PATH = (
    PROPOSED
    / "damage_curve_records_wildfire_wind__model_v0_1__docs_r1.xlsx"
)
HANDOFF_PATH = (
    ROOT / "docs/contracts/hazard_handoff/wildfire_wind_model_v0_1_boundary.md"
)
ARTIFACT_INDEX_PATH = (
    ROOT / "docs/contracts/machine_readable_artifact_index.json"
)
BUNDLE_SCHEMA_PATH = (
    ROOT / "docs/contracts/schemas/curve_artifact_bundle.schema.json"
)
CAPABILITY_SCHEMA_PATH = (
    ROOT / "docs/contracts/schemas/capability_declaration.schema.json"
)

EXPECTED_SOURCE_COUNT = 21
EXPECTED_CLAIM_COUNT = 30
EXPECTED_PARAMETER_COUNT = 55
EXPECTED_VALUE_COUNT = 26
EXPECTED_KAT_COUNT = 18
EXPECTED_KAT_IDS = {
    "WW_THERMAL_COMPLETE_INPUT_STILL_WITHHOLDS",
    "WW_FIREBRAND_COMPLETE_INPUT_STILL_WITHHOLDS",
    "WW_RESIDUE_COMPLETE_INPUT_STILL_WITHHOLDS",
    "WW_MISSING_PATHWAY_REJECTS",
    "WW_UNKNOWN_PATHWAY_REJECTS",
    "WW_FSIM_CLASS_ALONE_CANNOT_UNLOCK_DAMAGE",
    "WW_NO_WILDFIRE_SOLAR_NUMERICAL_FALLBACK",
    "WW_NO_LEGACY_THREE_CURVE_FALLBACK",
    "WW_ENDOGENOUS_TURBINE_FIRE_REJECTS",
    "WW_LEASE_POLYGON_FULL_EXPOSURE_REJECTS",
    "WW_UNKNOWN_CLEARANCE_OR_MITIGATION_GETS_NO_CREDIT",
    "WW_TURBINE_ASSEMBLY_STATES_MUST_BE_DEPENDENCY_SAFE",
    "WW_AGGREGATE_GSU_FAILURE_UNIT_REJECTS",
    "WW_SHARED_GSU_VALUE_IS_COUNTED_ONCE",
    "WW_NONDESTRUCTIVE_SMOKE_CLEANING_IS_OUT_OF_ORDINATE",
    "WW_REFERENCE_VALUE_CANNOT_UNLOCK_LOSS",
    "WW_SUPPORT_ROWS_CANNOT_RECEIVE_INDEPENDENT_DR",
    "WW_ANNUAL_AND_TAIL_METRICS_WITHHOLD",
}

EXPECTED_PATHWAYS = {
    "wildfire_thermal_attack",
    "wildfire_firebrand_ignition",
    "wildfire_residue_destructive_contamination",
}
EXPECTED_FAILURE_UNITS = {
    "WT_TURBINE_FIRE_ASSEMBLY",
    "WT_PAD_ELECTRICAL",
    "WT_COLLECTION_NETWORK",
    "WT_GSU_MAIN_TRANSFORMER",
    "WT_GSU_SWITCHGEAR_BUS",
    "WT_GSU_PROTECTION_CONTROL_DC",
    "WT_GSU_CABLE_TERMINATIONS",
    "WT_CONTROL_MET_OM",
    "WT_FOUNDATION",
    "WT_CIVIL_INFRA",
    "SUPPORT_FIELDWORK",
    "SUPPORT_TRANSPORT_LOGISTICS",
}
EXPECTED_GSU_UNITS = {
    "WT_GSU_MAIN_TRANSFORMER",
    "WT_GSU_SWITCHGEAR_BUS",
    "WT_GSU_PROTECTION_CONTROL_DC",
    "WT_GSU_CABLE_TERMINATIONS",
}
NON_FAILURE_UNIT_LABELS = {
    "OUTSIDE_PHYSICAL_CELL",
    "MULTIPLE_WITHHELD_UNITS",
    "SUPPORT_ONCE",
    "REFERENCE_DENOMINATOR_ONLY",
    "REFERENCE_REPORTING_DENOMINATOR",
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
    "Candidate_Audit",
    "Site_Adapter",
    "Legacy_Audit",
    "Claim_Register",
    "Source_Register",
    "Parameter_Tiers",
    "QA_Checks",
]
EXPECTED_QA_FORMULA_COUNT = 13
EXPECTED_QA_PASS_CELLS = {f"B{row}" for row in range(5, 18)}


class ValidationFailure(AssertionError):
    """Raised when a binding scaffold invariant fails."""


class Counter:
    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, message: str) -> None:
        self.count += 1
        if not condition:
            raise ValidationFailure(message)


CHECKS = Counter()


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


def split_ids(value: str, separators: str = r"[;|]") -> set[str]:
    return {
        part.strip()
        for part in re.split(separators, value)
        if part.strip()
    }


def is_type(instance: Any, expected: str) -> bool:
    checks = {
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
    require(expected in checks, f"unsupported schema type {expected}")
    return checks[expected](instance)


def validate_schema_subset(
    instance: Any, schema: Mapping[str, Any], path: str = "$"
) -> None:
    """Evaluate the schema keywords used by the selected v1 envelope."""

    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        require(
            any(is_type(instance, candidate) for candidate in expected_type),
            f"{path}: expected one of {expected_type}",
        )
    elif isinstance(expected_type, str):
        require(is_type(instance, expected_type), f"{path}: expected {expected_type}")

    if "const" in schema:
        require(instance == schema["const"], f"{path}: const mismatch")
    if "enum" in schema:
        require(instance in schema["enum"], f"{path}: enum mismatch")
    if isinstance(instance, str):
        if "minLength" in schema:
            require(len(instance) >= schema["minLength"], f"{path}: string too short")
        if "pattern" in schema:
            require(re.search(schema["pattern"], instance) is not None, f"{path}: pattern mismatch")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            require(key in instance, f"{path}: missing required key {key}")
        for key, child_schema in schema.get("properties", {}).items():
            if key in instance:
                validate_schema_subset(instance[key], child_schema, f"{path}.{key}")
    if isinstance(instance, list):
        if "minItems" in schema:
            require(len(instance) >= schema["minItems"], f"{path}: too few items")
        if "maxItems" in schema:
            require(len(instance) <= schema["maxItems"], f"{path}: too many items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(value, sort_keys=True) for value in instance]
            require(len(encoded) == len(set(encoded)), f"{path}: duplicate items")
        if "items" in schema:
            for index, value in enumerate(instance):
                validate_schema_subset(value, schema["items"], f"{path}[{index}]")


def collect_pathway_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "pathway_id" and isinstance(child, str):
                found.add(child)
            elif key == "pathway_ids":
                if isinstance(child, str):
                    found |= split_ids(child)
                elif isinstance(child, list):
                    found |= {item for item in child if isinstance(item, str)}
            found |= collect_pathway_ids(child)
    elif isinstance(value, list):
        for child in value:
            found |= collect_pathway_ids(child)
    return found


def validate_top_level(
    artifact: Mapping[str, Any], capability: Mapping[str, Any]
) -> None:
    validate_schema_subset(artifact, load_json(BUNDLE_SCHEMA_PATH))
    validate_schema_subset(capability, load_json(CAPABILITY_SCHEMA_PATH))

    require(
        artifact["schema_version"] == "damage_curve_record_bundle.v1",
        "zero-curve scaffold must stay in the documented v1 envelope",
    )
    require(artifact["cell_id"] == "wildfire_wind", "artifact cell changed")
    require(
        artifact["damage_code_id"] == "WILDFIRE_WIND_PROPOSED_V0_1",
        "damage_code_id changed",
    )
    require(artifact["semantic_damage_model_version"] == "model v0.1", "model changed")
    require(artifact["documentation_revision"] == "docs r1", "docs changed")
    require(artifact["package_release"] == "unreleased", "scaffold named a release")
    require(artifact["lifecycle_state"] == "scaffold", "lifecycle is not scaffold")
    require(artifact["promotion_status"] == "proposed", "promotion status changed")
    require(artifact["canonical_runtime_artifact"] is False, "scaffold became canonical")
    require(artifact["curve_records"] == [], "runtime curve leaked into scaffold")
    require(
        artifact["parameter_tier_table"] == [],
        "runtime parameter row leaked into scaffold",
    )
    require(artifact["ordinate_status"] == "withheld", "ordinate must remain withheld")
    require(
        artifact["withheld_reason_codes"] == ["NO_RUNTIME_CURVE"],
        "runtime withholding reason changed",
    )
    require(
        artifact["schema_envelope_status"]["runtime_publication_allowed"] is False,
        "schema exception became publishable",
    )
    require(
        collect_pathway_ids(artifact) >= EXPECTED_PATHWAYS,
        "one or more governed wildfire pathways are absent",
    )
    require(
        artifact["candidate_evidence"]["numeric_values_embedded"] is False,
        "candidate evidence became numerically embedded",
    )
    require(
        artifact["candidate_evidence"]["runtime_enabled"] is False,
        "candidate evidence became runtime-enabled",
    )
    require(artifact["hazard_axis"]["valid_range"] is None, "runtime axis range appeared")
    require(artifact["emit_contract"]["runtime_status"] == "withheld", "emit became active")

    require(capability == artifact["capability_declaration"], "capability copies differ")
    require(
        capability["schema_version"] == "capability_declaration.v1",
        "capability schema changed",
    )
    require(capability["cell_id"] == "wildfire_wind", "capability cell mismatch")
    require(capability["spread_carried"] is False, "scaffold cannot carry spread")
    require(capability["emit_modes_populated_by_cell"] == [], "emit mode populated")
    require(set(capability["metrics_supportable"]) == EXPECTED_METRICS, "metric set changed")
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

    emit = artifact["emit_contract"]
    for field in ("numeric_damage_emit_allowed", "numeric_loss_emit_allowed"):
        if field in emit:
            require(emit[field] is False, f"{field} became true")
    for field in ("solar_curve_fallback_allowed", "legacy_curve_fallback_allowed"):
        if field in emit:
            require(emit[field] is False, f"{field} became true")


def iter_repository_pointers(value: Any) -> list[str]:
    pointers: list[str] = []
    if isinstance(value, dict):
        for child in value.values():
            pointers.extend(iter_repository_pointers(child))
    elif isinstance(value, list):
        for child in value:
            pointers.extend(iter_repository_pointers(child))
    elif isinstance(value, str) and value.startswith("docs/"):
        pointers.append(value)
    return pointers


def resolve_repository_pointer(pointer: str) -> Path:
    target = pointer.split("#", 1)[0].split("::", 1)[0]
    return ROOT / target


def validate_artifact_pointers(artifact: Mapping[str, Any]) -> int:
    required_fields = {
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
    }
    for field in required_fields:
        require(field in artifact, f"artifact pointer field missing: {field}")
        require(isinstance(artifact[field], str), f"{field}: pointer must be a string")
        require(artifact[field].startswith("docs/"), f"{field}: invalid repository pointer")
    require(
        resolve_repository_pointer(artifact["source_workbook"]) == WORKBOOK_PATH,
        "artifact workbook pointer changed",
    )

    pointers = sorted(set(iter_repository_pointers(artifact)))
    for pointer in pointers:
        require(
            resolve_repository_pointer(pointer).exists(),
            f"artifact pointer missing: {pointer}",
        )
    require(HANDOFF_PATH.is_file(), "Hazard handoff is missing")

    artifact_text = ARTIFACT_PATH.read_text()
    require("infrasure-damage-curves/" not in artifact_text, "artifact embeds legacy-repo runtime path")
    require("Hazard_modeling/" not in artifact_text, "artifact embeds consumer-local runtime path")
    return len(pointers) + 1


def validate_failure_units_and_values(
    artifact: Mapping[str, Any], value_rows: list[dict[str, str]]
) -> None:
    pathways = {pathway["pathway_id"]: pathway for pathway in artifact["pathways"]}
    require(len(pathways) == len(artifact["pathways"]), "duplicate pathway ID")
    require(set(pathways) == EXPECTED_PATHWAYS, "pathway set changed")
    units = {unit["id"]: unit for unit in artifact["failure_units"]}
    require(len(units) == len(artifact["failure_units"]), "duplicate failure-unit ID")
    require(set(units) == EXPECTED_FAILURE_UNITS, "failure-unit set changed")
    physical_units = EXPECTED_FAILURE_UNITS - {
        "SUPPORT_FIELDWORK",
        "SUPPORT_TRANSPORT_LOGISTICS",
    }
    for unit_id in physical_units:
        require(
            set(units[unit_id]["pathway_ids"]) == EXPECTED_PATHWAYS,
            f"{unit_id}: pathway coverage changed",
        )
        require(
            units[unit_id]["ordinate_status"] == "withheld",
            f"{unit_id}: physical ordinate is not withheld",
        )
    for unit_id in EXPECTED_FAILURE_UNITS - physical_units:
        require(
            units[unit_id]["pathway_ids"] == ["all_shared"],
            f"{unit_id}: support allocation scope changed",
        )
        require(
            units[unit_id]["ordinate_status"] == "not_applicable",
            f"{unit_id}: support row gained an ordinate",
        )
    for pathway in pathways.values():
        require(
            pathway["failure_unit_ids_supported"] == [],
            f"{pathway['pathway_id']}: supported failure unit appeared",
        )
        require(
            set(pathway["failure_unit_ids_withheld"]) == physical_units,
            f"{pathway['pathway_id']}: withheld unit coverage changed",
        )
    require(
        all(unit.get("ordinate_status", "withheld") != "zero" for unit in units.values()),
        "withheld unit was converted to zero",
    )
    require(
        units["WT_TURBINE_FIRE_ASSEMBLY"].get("exposure_grain", "").startswith("per_turbine"),
        "turbine assembly is no longer per-turbine",
    )
    require(
        "segment" in units["WT_COLLECTION_NETWORK"].get("exposure_grain", "")
        or "network" in units["WT_COLLECTION_NETWORK"].get("exposure_grain", ""),
        "collection-network grain changed",
    )
    expected_gsu_grain_terms = {
        "WT_GSU_MAIN_TRANSFORMER": {"transformer", "point", "footprint", "yard"},
        "WT_GSU_SWITCHGEAR_BUS": {"component", "yard"},
        "WT_GSU_PROTECTION_CONTROL_DC": {"control", "room", "cabinet"},
        "WT_GSU_CABLE_TERMINATIONS": {"termination", "point", "pathway"},
    }
    for unit_id, required_terms in expected_gsu_grain_terms.items():
        grain = units[unit_id].get("exposure_grain", "")
        require(
            required_terms <= set(grain.split("_")),
            f"{unit_id}: GSU component grain changed",
        )

    require(len(value_rows) == EXPECTED_VALUE_COUNT, "value-row count changed")
    by_id = {row["row_or_bucket_id"]: row for row in value_rows}
    require(len(by_id) == len(value_rows), "duplicate value row ID")
    expected_values = {
        "TURBINE_EQUIPMENT_TOTAL": 1090.0,
        "FOUNDATION_REFERENCE_TOTAL": 120.0,
        "CIVIL_ELECTRICAL_REFERENCE_TOTAL": 119.0,
        "WITHHELD_DIRECT_OTHER_TOTAL": 239.0,
        "SUPPORT_TOTAL": 294.0,
        "PHYSICAL_REFERENCE_TOTAL": 1623.0,
        "EXCLUDED_TOTAL": 345.0,
        "INSTALLED_REFERENCE_TOTAL": 1968.0,
    }
    for row_id, expected in expected_values.items():
        require(row_id in by_id, f"missing value summary {row_id}")
        require(abs(float(by_id[row_id]["value"]) - expected) < 1e-9, f"{row_id}: value changed")
    require(1090 + 239 + 294 == 1623, "physical value does not reconcile")
    require(1623 + 345 == 1968, "installed value does not reconcile")

    for row in value_rows:
        require(
            row["include_in_direct_denominator"] in {"true", "false"},
            f"{row['row_or_bucket_id']}: invalid denominator boolean",
        )
        mapped_units = split_ids(row["failure_unit_id"])
        require(
            mapped_units <= EXPECTED_FAILURE_UNITS | NON_FAILURE_UNIT_LABELS,
            f"{row['row_or_bucket_id']}: unknown failure-unit mapping",
        )
        pathways = split_ids(row["applicable_pathway_ids"])
        require(
            pathways <= EXPECTED_PATHWAYS | {"all_wildfire"},
            f"{row['row_or_bucket_id']}: unknown pathway mapping",
        )
    electrical_units = split_ids(by_id["WIND_VALUE_012_ELECTRICAL"]["failure_unit_id"])
    require(
        EXPECTED_GSU_UNITS <= electrical_units,
        "mixed electrical row no longer preserves all four GSU units",
    )

    basis = artifact["value_basis"]
    require(basis["physical_reference"] == 1623, "artifact physical reference changed")
    require(basis["installed_reference"] == 1968, "artifact installed reference changed")
    if "support_once" in basis:
        require(basis["support_once"] == 294, "artifact support total changed")
    if "site_override_required_for_loss" in basis:
        require(basis["site_override_required_for_loss"] is True, "site value no longer required")


def validate_registers(
    source_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    parameter_rows: list[dict[str, str]],
) -> None:
    require(len(source_rows) == EXPECTED_SOURCE_COUNT, "source count changed")
    require(len(claim_rows) == EXPECTED_CLAIM_COUNT, "claim count changed")
    require(len(parameter_rows) == EXPECTED_PARAMETER_COUNT, "parameter count changed")

    source_ids = {row["source_id"] for row in source_rows}
    require(len(source_ids) == len(source_rows), "duplicate source_id")
    require(all(row["url"] for row in source_rows), "source without URL/path")
    require(
        all(row["evidence_tier"] in ALLOWED_TIERS for row in source_rows),
        "invalid source tier",
    )
    require("NREL_CWER_2024" in source_ids, "value-source alias missing")

    claim_ids = {row["claim_id"] for row in claim_rows}
    require(len(claim_ids) == len(claim_rows), "duplicate claim_id")
    for row in claim_rows:
        require(row["evidence_tier"] in ALLOWED_TIERS, f"{row['claim_id']}: invalid tier")
        require(row["exact_locator"], f"{row['claim_id']}: missing locator")
        unresolved = split_ids(row["source_ids"], r"[;]") - source_ids
        require(not unresolved, f"{row['claim_id']}: unknown sources {sorted(unresolved)}")
        if "pathway_id" in row:
            require(
                row["pathway_id"] in EXPECTED_PATHWAYS | {"all_wildfire", "all_shared"},
                f"{row['claim_id']}: unknown pathway",
            )

    parameter_names = {row["parameter"] for row in parameter_rows}
    require(len(parameter_names) == len(parameter_rows), "duplicate parameter")
    for row in parameter_rows:
        require(row["tier"] in ALLOWED_TIERS, f"{row['parameter']}: invalid tier")
        unresolved = split_ids(row["source_ids"], r"[;]") - source_ids
        require(not unresolved, f"{row['parameter']}: unknown sources {sorted(unresolved)}")
    by_parameter = {row["parameter"]: row for row in parameter_rows}
    require(by_parameter["runtime_curve_count"]["value"] == "0", "runtime count parameter changed")
    require(
        by_parameter["canonical_runtime_artifact"]["value"] == "false",
        "canonical parameter changed",
    )
    require(
        by_parameter["failure_unit_scalar_dr"]["value"] == "withheld_NO_RUNTIME_CURVE",
        "DR parameter changed",
    )


def validate_kats() -> int:
    kats = load_json(KAT_PATH)
    require(kats["schema_version"] == "known_answer_tests.v1", "KAT schema changed")
    require(kats["cell_id"] == "wildfire_wind", "KAT cell changed")
    require(kats["semantic_damage_model_version"] == "model v0.1", "KAT model changed")
    require(kats["documentation_revision"] == "docs r1", "KAT docs changed")
    require(kats["runtime_curve_count"] == 0, "KAT runtime count changed")
    require(kats["runtime_curve_known_answer_tests"] == [], "runtime curve KAT appeared")
    require(set(kats["pathway_ids"]) == EXPECTED_PATHWAYS, "KAT pathways changed")
    require(
        set(kats["failure_unit_ids"]) == EXPECTED_FAILURE_UNITS,
        "KAT failure units changed",
    )
    require(len(kats["tests"]) == EXPECTED_KAT_COUNT, "fail-closed fixture count changed")
    test_ids = {test["test_id"] for test in kats["tests"]}
    require(len(test_ids) == len(kats["tests"]), "duplicate test_id")
    require(test_ids == EXPECTED_KAT_IDS, "fail-closed KAT set changed")

    for test in kats["tests"]:
        require(test["curve_id"] is None, f"{test['test_id']}: curve ID populated")
        require(test["tolerance"] is None, f"{test['test_id']}: numeric tolerance invalid")
        output = test["expected_output"]
        numeric_metrics = EXPECTED_METRICS & set(output)
        require(numeric_metrics, f"{test['test_id']}: no numeric-output assertion")
        for metric in numeric_metrics:
            result = output[metric]
            require(result["value"] is None, f"{test['test_id']}/{metric}: numeric output leaked")
            require(
                result["status"] in {"withheld", "not_evaluated"},
                f"{test['test_id']}/{metric}: status changed",
            )
            if result["status"] == "withheld":
                reasons = result.get("reason_codes", result.get("reason_codes_include", []))
                require(
                    "NO_RUNTIME_CURVE" in reasons,
                    f"{test['test_id']}/{metric}: reason missing",
                )
        for key, value in output.items():
            if isinstance(value, bool):
                require(value is False, f"{test['test_id']}/{key}: fail-closed flag enabled")

    by_id = {test["test_id"]: test["expected_output"] for test in kats["tests"]}
    require(
        set(by_id["WW_AGGREGATE_GSU_FAILURE_UNIT_REJECTS"]["accepted_gsu_failure_unit_ids"])
        == EXPECTED_GSU_UNITS,
        "aggregate GSU rejection no longer names the four component units",
    )
    require(
        by_id["WW_TURBINE_ASSEMBLY_STATES_MUST_BE_DEPENDENCY_SAFE"][
            "accepted_independent_damage_charges"
        ]
        == 0,
        "independent turbine-assembly damage charges became accepted",
    )
    require(
        by_id["WW_SHARED_GSU_VALUE_IS_COUNTED_ONCE"][
            "accepted_component_value_instances"
        ]
        == 1,
        "shared GSU value is not counted exactly once",
    )
    return len(kats["tests"])


def xlsx_sheet_map(archive: zipfile.ZipFile) -> tuple[list[str], dict[str, str]]:
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    pkg_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        relation.attrib["Id"]: relation.attrib["Target"]
        for relation in relationships.findall(f"{{{pkg_ns}}}Relationship")
    }
    names: list[str] = []
    paths: dict[str, str] = {}
    for sheet in workbook.findall(f".//{{{main_ns}}}sheet"):
        name = sheet.attrib["name"]
        relationship_id = sheet.attrib[f"{{{rel_ns}}}id"]
        target = targets[relationship_id].lstrip("/")
        path = target if target.startswith("xl/") else f"xl/{target}"
        names.append(name)
        paths[name] = path
    return names, paths


def xlsx_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return [
        "".join(text_node.text or "" for text_node in item.findall(f".//{{{main_ns}}}t"))
        for item in root.findall(f"{{{main_ns}}}si")
    ]


def cached_cell_value(
    cell: ET.Element, shared_strings: list[str], main_ns: str
) -> str | None:
    cell_type = cell.attrib.get("t")
    value = cell.find(f"{{{main_ns}}}v")
    if cell_type == "inlineStr":
        return "".join(
            node.text or "" for node in cell.findall(f".//{{{main_ns}}}t")
        )
    if value is None or value.text is None:
        return None
    if cell_type == "s":
        return shared_strings[int(value.text)]
    return html.unescape(value.text)


def validate_workbook() -> int:
    require(WORKBOOK_PATH.is_file(), "workbook missing")
    require(WORKBOOK_PATH.stat().st_size > 20_000, "workbook unexpectedly small")
    with zipfile.ZipFile(WORKBOOK_PATH) as archive:
        require(archive.testzip() is None, "XLSX ZIP integrity failure")
        names, paths = xlsx_sheet_map(archive)
        require(names == EXPECTED_SHEETS, "workbook sheet order changed")
        shared_strings = xlsx_shared_strings(archive)
        main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        qa = ET.fromstring(archive.read(paths["QA_Checks"]))
        qa_results: dict[str, str] = {}
        formula_count = 0
        for cell in qa.findall(f".//{{{main_ns}}}c"):
            reference = cell.attrib.get("r", "")
            if cell.find(f"{{{main_ns}}}f") is not None:
                formula_count += 1
            value = cached_cell_value(cell, shared_strings, main_ns)
            if reference.startswith("B") and value is not None:
                qa_results[reference] = value
        require(formula_count == EXPECTED_QA_FORMULA_COUNT, "QA formula count changed")
        for reference in EXPECTED_QA_PASS_CELLS:
            require(qa_results.get(reference) == "PASS", f"QA_Checks!{reference} is not PASS")
        for path in paths.values():
            sheet = ET.fromstring(archive.read(path))
            for cell in sheet.findall(f".//{{{main_ns}}}c"):
                require(cell.attrib.get("t") != "e", f"{path}: formula error cell")
    return len(EXPECTED_SHEETS)


def validate_markdown_links() -> int:
    documents = sorted(CELL.rglob("*.md")) + [HANDOFF_PATH]
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    checked = 0
    for document in documents:
        for raw_target in link_pattern.findall(document.read_text()):
            target = html.unescape(raw_target.strip()).split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (document.parent / target).resolve()
            require(resolved.exists(), f"{document}: broken local link {raw_target}")
            checked += 1
    return checked


def validate_index_absence() -> None:
    index = load_json(ARTIFACT_INDEX_PATH)
    # A later canonical wildfire_wind release may be indexed; this v0.1 scaffold must never be.
    paths = [
        entry.get("path", "")
        for entry in index.get("artifacts", [])
        if entry.get("cell_id") == "wildfire_wind"
    ]
    require(
        not any("/proposed/" in path or path.endswith(ARTIFACT_PATH.name) for path in paths),
        "noncanonical scaffold entered artifact index",
    )


def main() -> int:
    try:
        artifact = load_json(ARTIFACT_PATH)
        capability = load_json(CAPABILITY_PATH)
        source_rows = read_csv(SOURCE_PATH)
        claim_rows = read_csv(CLAIM_PATH)
        parameter_rows = read_csv(PARAMETER_PATH)
        value_rows = read_csv(VALUE_PATH)

        validate_top_level(artifact, capability)
        pointer_count = validate_artifact_pointers(artifact)
        validate_failure_units_and_values(artifact, value_rows)
        validate_registers(source_rows, claim_rows, parameter_rows)
        tests = validate_kats()
        sheets = validate_workbook()
        links = validate_markdown_links()
        validate_index_absence()
    except (
        OSError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
        ValidationFailure,
        zipfile.BadZipFile,
        ET.ParseError,
    ) as error:
        print(
            f"FAIL wildfire_wind model v0.1/docs r1 scaffold: {error}",
            file=sys.stderr,
        )
        return 1

    print("PASS wildfire_wind model v0.1/docs r1 scaffold")
    print(f"checks={CHECKS.count}")
    print(f"sources={len(source_rows)}")
    print(f"claims={len(claim_rows)}")
    print(f"parameters={len(parameter_rows)}")
    print(f"value_rows={len(value_rows)}")
    print(f"failure_units={len(EXPECTED_FAILURE_UNITS)}")
    print(f"pathways={len(EXPECTED_PATHWAYS)}")
    print(f"fail_closed_contract_tests={tests}")
    print(f"workbook_sheets={sheets}")
    print(f"local_links_checked={links}")
    print(f"artifact_pointers_checked={pointer_count}")
    print(f"artifact_sha256={sha256(ARTIFACT_PATH)}")
    print(f"capability_sha256={sha256(CAPABILITY_PATH)}")
    print(f"kat_sha256={sha256(KAT_PATH)}")
    print(f"workbook_sha256={sha256(WORKBOOK_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
