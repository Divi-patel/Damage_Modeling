#!/usr/bin/env python3
"""Validate the preserved tropical-cyclone-wind × wind model-v0.1 scaffold.

The package intentionally contains no runtime curve.  This validator therefore
checks the fail-closed contract, evidence/value registries, candidate-isolation
rules, workbook integrity, local links, and isolation from the later canonical
model-v1.0 release. It uses only the Python standard library.
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
CELL = ROOT / "docs/cells/tropical_cyclone_wind_wind"
PROPOSED = CELL / "proposed"

ARTIFACT_PATH = (
    PROPOSED
    / "tropical_cyclone_wind_wind__model_v0_1__docs_r1__curve_artifact.json"
)
CAPABILITY_PATH = (
    PROPOSED
    / "tropical_cyclone_wind_wind__model_v0_1__docs_r1__capability.json"
)
KAT_PATH = (
    PROPOSED
    / "known_answer_tests_tropical_cyclone_wind_wind__model_v0_1__docs_r1.json"
)
SOURCE_PATH = (
    PROPOSED
    / "SOURCE_REGISTER_tropical_cyclone_wind_wind__model_v0_1__docs_r1.csv"
)
CLAIM_PATH = (
    PROPOSED
    / "CLAIM_PARAMETER_REGISTER_tropical_cyclone_wind_wind__model_v0_1__docs_r1.csv"
)
PARAMETER_PATH = (
    PROPOSED
    / "PARAMETER_TIER_TABLE_tropical_cyclone_wind_wind__model_v0_1__docs_r1.csv"
)
VALUE_PATH = (
    PROPOSED
    / "VALUE_CROSSWALK_tropical_cyclone_wind_wind__model_v0_1__docs_r1.csv"
)
WORKBOOK_PATH = (
    PROPOSED
    / "damage_curve_records_tropical_cyclone_wind_wind__model_v0_1__docs_r1.xlsx"
)
BUNDLE_SCHEMA_PATH = ROOT / "docs/contracts/schemas/curve_artifact_bundle.schema.json"
CAPABILITY_SCHEMA_PATH = ROOT / "docs/contracts/schemas/capability_declaration.schema.json"
ARTIFACT_INDEX_PATH = ROOT / "docs/contracts/machine_readable_artifact_index.json"
HANDOFF_PATH = (
    ROOT
    / "docs/contracts/hazard_handoff/tropical_cyclone_wind_wind_model_v0_1_boundary.md"
)

EXPECTED_FAILURE_UNITS = {
    "WT_TURBINE_EQUIPMENT_ASSEMBLY",
    "WT_FOUNDATION",
    "WT_EXTERNAL_ELECTRICAL",
    "WT_CIVIL_INFRA",
    "SUPPORT_FIELDWORK",
    "SUPPORT_TRANSPORT_LOGISTICS",
}
NON_FAILURE_UNIT_VALUE_LABELS = {
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

    require(artifact["cell_id"] == "tropical_cyclone_wind_wind", "cell_id changed")
    require(
        artifact["damage_code_id"] == "TROPICAL_CYCLONE_WIND_WIND_PROPOSED_V0_1",
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

    detail = {
        row["row_or_bucket_id"]: float(row["value"])
        for row in value_rows
        if row["row_or_bucket_id"].startswith("WIND_VALUE_")
    }
    require(len(detail) == 18, "expected 18 detailed CWER value rows")
    for row in value_rows:
        require(row["include_in_direct_denominator"] in {"true", "false"}, "invalid value boolean")
        require(float(row["value"]) >= 0, "negative reference value")
        require(
            row["failure_unit_id"] in EXPECTED_FAILURE_UNITS | NON_FAILURE_UNIT_VALUE_LABELS,
            f"value row has unknown failure-unit label: {row['failure_unit_id']}",
        )

    equipment_ids = [f"WIND_VALUE_{index:03d}_{name}" for index, name in [
        (2, "BLADE"), (3, "PITCH"), (4, "HUB"), (5, "NACELLE_STRUCTURE"),
        (6, "DRIVETRAIN"), (7, "POWER_ELECTRONICS"), (8, "YAW"), (9, "TOWER")
    ]]
    other_ids = [
        "WIND_VALUE_010_FOUNDATION",
        "WIND_VALUE_011_CIVIL",
        "WIND_VALUE_012_ELECTRICAL",
    ]
    support_ids = ["WIND_VALUE_013_FIELDWORK", "WIND_VALUE_014_TRANSPORT"]
    excluded_ids = [
        "WIND_VALUE_015_ENGINEERING_DEVELOPMENT",
        "WIND_VALUE_016_PROJECT_MANAGEMENT",
        "WIND_VALUE_017_FINANCE",
        "WIND_VALUE_018_CONTINGENCY",
        "WIND_VALUE_019_WARRANTY",
    ]
    equipment = sum(detail[key] for key in equipment_ids)
    other = sum(detail[key] for key in other_ids)
    support = sum(detail[key] for key in support_ids)
    excluded = sum(detail[key] for key in excluded_ids)
    require(equipment == 1090, "equipment value does not reconcile")
    require(other == 239, "other-direct value does not reconcile")
    require(support == 294, "support value does not reconcile")
    require(excluded == 345, "excluded value does not reconcile")
    require(equipment + other + support == 1623, "physical total does not reconcile")
    require(equipment + other + support + excluded == 1968, "installed total does not reconcile")
    basis = artifact["value_basis"]
    require(basis["turbine_equipment_direct"] == equipment, "artifact equipment value mismatch")
    require(basis["other_direct_withheld"] == other, "artifact other-direct mismatch")
    require(basis["support_once"] == support, "artifact support mismatch")
    require(basis["physical_reference"] == 1623, "artifact physical total mismatch")
    require(basis["installed_reference"] == 1968, "artifact installed total mismatch")


def validate_registers(
    source_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    parameter_rows: list[dict[str, str]],
    value_rows: list[dict[str, str]],
) -> None:
    source_ids = {row["source_id"] for row in source_rows}
    require(len(source_ids) == len(source_rows), "duplicate source ID")
    require(len(source_ids) >= 19, "source register unexpectedly small")
    require(len({row["claim_id"] for row in claim_rows}) == len(claim_rows), "duplicate claim ID")
    require(
        len({row["parameter"] for row in parameter_rows}) == len(parameter_rows),
        "duplicate parameter ID",
    )
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
            row["value_source_id"] in source_ids | {"SUMMARY"},
            f"{row['row_or_bucket_id']}: unresolved value source",
        )


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
    require(kats["cell_id"] == "tropical_cyclone_wind_wind", "KAT cell mismatch")
    require(kats["runtime_curve_count"] == 0, "KAT runtime curve count changed")
    require(kats["runtime_curve_known_answer_tests"] == [], "runtime curve KATs must be empty")
    tests = kats["tests"]
    require(len(tests) == 14, "expected 14 fail-closed contract tests")
    require(len({test["test_id"] for test in tests}) == len(tests), "duplicate KAT ID")
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
    require("parameters" not in candidate, "candidate contains runtime-shaped parameters")
    require("valid_range" not in candidate, "candidate contains runtime-shaped valid range")

    speeds = [160.0, 180.0, 200.0, 220.0]
    jaimes = [
        (5.3165, 0.0485),
        (5.2276, 0.0516),
        (5.1642, 0.0567),
    ]
    for mu, sigma in jaimes:
        probabilities = [
            0.5 * (1.0 + math.erf((math.log(speed) - mu) / (sigma * math.sqrt(2.0))))
            for speed in speeds
        ]
        require(all(0 <= value <= 1 for value in probabilities), "Jaimes probability out of bounds")
        require(
            probabilities == sorted(probabilities),
            "Jaimes candidate is not monotone on audit fixtures",
        )
        require(108 <= math.exp(mu) <= 252, "Jaimes median outside source-modeled range")

    rose_active = 1.0 / (1.0 + (174.0 / 174.0) ** 19.3)
    rose_perpendicular = 1.0 / (1.0 + (140.0 / 140.0) ** 18.6)
    require(math.isclose(rose_active, 0.5), "Rose active-yaw median check failed")
    require(math.isclose(rose_perpendicular, 0.5), "Rose perpendicular median check failed")

    weighted_rotor_cap = 0.55 * 0.90 + 0.25 * 0.70 + 0.20 * 0.75
    require(math.isclose(weighted_rotor_cap, 0.82), "legacy weighted rotor cap check failed")
    require(not math.isclose(weighted_rotor_cap, 0.88), "legacy aggregate mismatch disappeared")


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
    require("LN(H$5)" in worksheet_xml, "Jaimes formulas do not reference visible speed fixtures")
    require("$B14/D$13" in worksheet_xml, "Rose formulas do not reference visible speed fixtures")
    require("'Asset_Value'!B15=C5" in worksheet_xml, "QA formula lost quoted cross-sheet reference")


def validate_index_isolation() -> None:
    index = load_json(ARTIFACT_INDEX_PATH)
    matching = [
        row for row in index["artifacts"] if row["cell_id"] == "tropical_cyclone_wind_wind"
    ]
    require(len(matching) == 1, "expected one later canonical TC-wind release")
    row = matching[0]
    require(row["semantic_damage_model_version"] != "model v0.1", "v0.1 scaffold model is indexed")
    require("/current/" in row["path"], "indexed TC-wind release is not current")
    require("model_v0_1" not in row["path"], "v0.1 scaffold appears in runtime artifact index")


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
    validate_index_isolation()

    print("PASS tropical_cyclone_wind_wind model v0.1/docs r1 scaffold")
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
