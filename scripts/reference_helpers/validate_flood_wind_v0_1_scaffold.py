#!/usr/bin/env python3
"""Validate the noncanonical flood × wind model-v0.1 research scaffold.

The package intentionally contains zero runtime curves. The validator checks the
fail-closed contract, provenance and value registries, shared-component boundary,
candidate isolation, legacy reproduction, workbook integrity, local links, and
absence from the canonical runtime artifact index.
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
CELL = ROOT / "docs/cells/flood_wind"
PROPOSED = CELL / "proposed"

ARTIFACT_PATH = PROPOSED / "flood_wind__model_v0_1__docs_r1__curve_artifact.json"
CAPABILITY_PATH = PROPOSED / "flood_wind__model_v0_1__docs_r1__capability.json"
KAT_PATH = PROPOSED / "known_answer_tests_flood_wind__model_v0_1__docs_r1.json"
SOURCE_PATH = PROPOSED / "SOURCE_REGISTER_flood_wind__model_v0_1__docs_r1.csv"
CLAIM_PATH = PROPOSED / "CLAIM_PARAMETER_REGISTER_flood_wind__model_v0_1__docs_r1.csv"
PARAMETER_PATH = PROPOSED / "PARAMETER_TIER_TABLE_flood_wind__model_v0_1__docs_r1.csv"
VALUE_PATH = PROPOSED / "VALUE_CROSSWALK_flood_wind__model_v0_1__docs_r1.csv"
SHARED_PATH = PROPOSED / "SHARED_COMPONENT_REUSE_CROSSWALK_flood_wind__model_v0_1__docs_r1.csv"
SHARED_CATALOG_PATH = (
    ROOT / "docs/method/shared_components/flood_electrical/failure_unit_catalog.csv"
)
SHARED_EVIDENCE_PATH = (
    ROOT / "docs/method/shared_components/flood_electrical/evidence_register.csv"
)
WORKBOOK_PATH = PROPOSED / "damage_curve_records_flood_wind__model_v0_1__docs_r1.xlsx"
OUTPUT_WORKBOOK_PATH = (
    ROOT
    / "outputs/flood_wind_v0_1"
    / "damage_curve_records_flood_wind__model_v0_1__docs_r1.xlsx"
)
BUNDLE_SCHEMA_PATH = ROOT / "docs/contracts/schemas/curve_artifact_bundle.schema.json"
CAPABILITY_SCHEMA_PATH = ROOT / "docs/contracts/schemas/capability_declaration.schema.json"
ARTIFACT_INDEX_PATH = ROOT / "docs/contracts/machine_readable_artifact_index.json"
HANDOFF_PATH = ROOT / "docs/contracts/hazard_handoff/flood_wind_model_v0_1_boundary.md"
FLOOD_SOLAR_PATH = (
    ROOT
    / "docs/cells/flood_solar/current/flood_solar__model_v1_0__docs_r4__curve_artifact.json"
)

PINNED_FLOOD_SOLAR_SHA = (
    "a08e77ef034e1ecea3e7cd05d13c825921b54d610fca9de8651ebda8e857082d"
)
EXPECTED_FAILURE_UNITS = {
    "FW_GSU_SWITCHGEAR",
    "FW_GSU_TRANSFORMER_MAIN",
    "FW_GSU_TRANSFORMER_AUX_CONTROLS",
    "FW_GSU_PROTECTION_SCADA",
    "FW_GSU_STATION_SERVICE_DC",
    "FW_GSU_CABLE_TERMINATIONS",
    "FW_TURBINE_BASE_ELECTRICAL",
    "FW_PADMOUNT_STEPUP_TRANSFORMER",
    "FW_COLLECTION_CABLE_TERMINATIONS",
    "FW_TURBINE_FOUNDATION",
    "FW_CIVIL_ACCESS_DRAINAGE",
    "FW_ELEVATED_TURBINE_EQUIPMENT",
    "SUPPORT_FIELDWORK",
    "SUPPORT_TRANSPORT_LOGISTICS",
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
    "Shared_Substrate",
    "Failure_Units",
    "Exposure_Value",
    "Value_Crosswalk",
    "Candidate_Audit",
    "Legacy_Audit",
    "Site_Adapter",
    "Claim_Register",
    "Source_Register",
    "Parameter_Tiers",
    "QA_Checks",
]
EXPECTED_KATS = {
    "FW_COMPLETE_COMPONENT_INPUT_STILL_WITHHOLDS",
    "FW_NO_FLOOD_SOLAR_FALLBACK",
    "FW_NO_LEGACY_FALLBACK",
    "FW_MISSING_PATHWAY_REJECTS",
    "FW_UNKNOWN_PATHWAY_REJECTS",
    "FW_MISSING_DATUM_NOT_DRY",
    "FW_VERTICAL_DATUM_MISMATCH_REJECTS",
    "FW_AGGREGATE_SUBSTATION_REJECTS",
    "FW_SCOUR_WRONG_PATHWAY_REJECTS",
    "FW_UNKNOWN_OWNERSHIP_WITHHOLDS_BASELINE",
    "FW_UTILITY_OWNED_POI_EXCLUDED",
    "FW_SHARED_GSU_VALUED_ONCE",
    "FW_ASSET_LABEL_DOES_NOT_SELECT_CURVE",
    "FW_DIRECT_DR_EXCLUDES_OUTAGE_AND_BI",
    "FW_UNKNOWN_CONDITIONER_NO_PROTECTION_CREDIT",
    "FW_M3_M4_NO_BYPASS_MIGRATION_GATE",
}
COMPLETE_FIXTURE_SELECTOR_FIELDS = {
    "equipment_family",
    "voltage_class",
    "indoor_outdoor",
    "enclosure_or_submersion_listing",
}


class ValidationFailure(AssertionError):
    pass


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


def read_xlsx_sheet_cells(path: Path, sheet_name: str) -> dict[str, str]:
    """Read cached cell values from one XLSX sheet without an office dependency."""

    attribute_pattern = re.compile(r'([A-Za-z_:][\w:.-]*)="([^"]*)"')
    with zipfile.ZipFile(path) as archive:
        workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
        relationship_xml = archive.read("xl/_rels/workbook.xml.rels").decode("utf-8")

        relationship_targets: dict[str, str] = {}
        for tag in re.findall(
            r"<(?:[A-Za-z_][\w.-]*:)?Relationship\b[^>]*/?>",
            relationship_xml,
        ):
            attributes = dict(attribute_pattern.findall(tag))
            if attributes.get("Id") and attributes.get("Target"):
                relationship_targets[attributes["Id"]] = attributes["Target"]

        relationship_id = None
        for tag in re.findall(
            r"<(?:[A-Za-z_][\w.-]*:)?sheet\b[^>]*/?>",
            workbook_xml,
        ):
            attributes = dict(attribute_pattern.findall(tag))
            if html.unescape(attributes.get("name", "")) == sheet_name:
                relationship_id = attributes.get("r:id") or attributes.get("id")
                break
        require(relationship_id is not None, f"workbook sheet missing: {sheet_name}")
        require(
            relationship_id in relationship_targets,
            f"workbook relationship missing for sheet: {sheet_name}",
        )

        target = relationship_targets[relationship_id].lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"

        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_xml = archive.read("xl/sharedStrings.xml").decode("utf-8")
            for item in re.findall(
                r"<(?:[A-Za-z_][\w.-]*:)?si\b[^>]*>(.*?)"
                r"</(?:[A-Za-z_][\w.-]*:)?si>",
                shared_xml,
                re.DOTALL,
            ):
                text_fragments = re.findall(
                    r"<(?:[A-Za-z_][\w.-]*:)?t\b[^>]*>(.*?)"
                    r"</(?:[A-Za-z_][\w.-]*:)?t>",
                    item,
                    re.DOTALL,
                )
                shared_strings.append(html.unescape("".join(text_fragments)))

        worksheet_xml = archive.read(target).decode("utf-8")
        cells: dict[str, str] = {}
        for attributes_text, body in re.findall(
            r"<(?:[A-Za-z_][\w.-]*:)?c\b([^>]*)>(.*?)"
            r"</(?:[A-Za-z_][\w.-]*:)?c>",
            worksheet_xml,
            re.DOTALL,
        ):
            attributes = dict(attribute_pattern.findall(attributes_text))
            reference = attributes.get("r")
            value_match = re.search(
                r"<(?:[A-Za-z_][\w.-]*:)?v>(.*?)"
                r"</(?:[A-Za-z_][\w.-]*:)?v>",
                body,
                re.DOTALL,
            )
            if reference is None or value_match is None:
                continue
            value = html.unescape(value_match.group(1))
            if attributes.get("t") == "s":
                value = shared_strings[int(value)]
            cells[reference] = value
    return cells


def validate_schema_subset(instance: Any, schema: Mapping[str, Any], path: str = "$") -> None:
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
        require(expected_type in type_checks, f"{path}: unsupported schema type")
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
    require(artifact["cell_id"] == "flood_wind", "artifact cell changed")
    require(
        artifact["damage_code_id"] == "FLOOD_WIND_PROPOSED_V0_1",
        "damage_code_id changed",
    )
    require(artifact["semantic_damage_model_version"] == "model v0.1", "model changed")
    require(artifact["documentation_revision"] == "docs r1", "docs revision changed")
    require(artifact["package_release"] == "unreleased", "scaffold named a release")
    require(artifact["lifecycle_state"] == "scaffold", "lifecycle is not scaffold")
    require(artifact["promotion_status"] == "proposed", "promotion status changed")
    require(artifact["canonical_runtime_artifact"] is False, "scaffold became canonical")
    require(artifact["curve_records"] == [], "scaffold contains runtime curves")
    require(
        artifact["schema_envelope_status"]["runtime_publication_allowed"] is False,
        "schema exception authorizes runtime publication",
    )
    require(capability == artifact["capability_declaration"], "capability copies differ")
    require(capability["cell_id"] == artifact["cell_id"], "capability cell mismatch")
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
        "no-distribution scaffold has cap tolerance",
    )
    emit = artifact["emit_contract"]
    require(emit["numeric_damage_emit_allowed"] is False, "numeric damage enabled")
    require(emit["numeric_loss_emit_allowed"] is False, "numeric loss enabled")
    require(emit["solar_curve_fallback_allowed"] is False, "solar fallback enabled")
    require(emit["legacy_curve_fallback_allowed"] is False, "legacy fallback enabled")


def validate_failure_units_and_values(
    artifact: Mapping[str, Any], value_rows: list[dict[str, str]]
) -> None:
    units = {row["id"]: row for row in artifact["failure_units"]}
    require(len(units) == len(artifact["failure_units"]), "duplicate failure-unit ID")
    require(set(units) == EXPECTED_FAILURE_UNITS, "failure-unit set changed")
    require(
        all(row["ordinate_status"] != "zero" for row in units.values()),
        "withheld unit converted to zero",
    )
    require(
        units["FW_TURBINE_FOUNDATION"]["pathway"] == "flood_scour_erosion",
        "foundation moved into direct contact pathway",
    )
    require(
        units["FW_GSU_SWITCHGEAR"]["shared_failure_unit_id"]
        == "FE_SUBSTATION_SWITCHGEAR",
        "shared switchgear binding changed",
    )

    by_id = {row["row_or_bucket_id"]: row for row in value_rows}
    require(len(by_id) == len(value_rows), "duplicate value row")
    require(float(by_id["WIND_VALUE_012_ELECTRICAL"]["value"]) == 72, "electrical row changed")
    require(float(by_id["WIND_VALUE_010_FOUNDATION"]["value"]) == 120, "foundation row changed")
    require(float(by_id["WIND_VALUE_011_CIVIL"]["value"]) == 47, "civil row changed")
    require(float(by_id["WT_ELEVATED_EQUIPMENT_TOTAL"]["value"]) == 1090, "equipment row changed")
    require(float(by_id["WIND_VALUE_013_FIELDWORK"]["value"]) == 100, "fieldwork changed")
    require(float(by_id["WIND_VALUE_014_TRANSPORT"]["value"]) == 194, "transport changed")
    require(float(by_id["PHYSICAL_REFERENCE_TOTAL"]["value"]) == 1623, "physical total changed")
    require(float(by_id["EXCLUDED_TOTAL"]["value"]) == 345, "excluded total changed")
    require(float(by_id["INSTALLED_REFERENCE_TOTAL"]["value"]) == 1968, "installed total changed")
    for row in value_rows:
        require(
            row["include_in_direct_denominator"] == "false",
            f"{row['row_or_bucket_id']}: scaffold enabled direct denominator",
        )
    site_rows = [
        row
        for row in value_rows
        if row["unit"] == "site_USD_required"
    ]
    require(len(site_rows) == 9, "site-specific electrical split row count changed")
    require(
        all(not row["value"] for row in site_rows),
        "site-specific value was silently populated",
    )
    basis = artifact["value_basis"]
    require(basis["external_electrical_mixed"] == 72, "artifact electrical value mismatch")
    require(basis["support_once"] == 294, "artifact support value mismatch")
    require(basis["physical_reference"] == 1623, "artifact physical total mismatch")
    require(basis["installed_reference"] == 1968, "artifact installed total mismatch")
    require(basis["site_override_required_for_loss"] is True, "site value no longer required")
    require(
        basis["ownership_required_for_baseline_loss"] is True,
        "ownership no longer required",
    )


def validate_registers(
    source_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    parameter_rows: list[dict[str, str]],
    shared_rows: list[dict[str, str]],
    shared_catalog_rows: list[dict[str, str]],
    shared_evidence_rows: list[dict[str, str]],
) -> None:
    source_ids = {row["source_id"] for row in source_rows}
    require(len(source_ids) == len(source_rows), "duplicate source ID")
    require(len(source_rows) == 15, "source row count changed")
    require(len({row["claim_id"] for row in claim_rows}) == len(claim_rows), "duplicate claim ID")
    require(len(claim_rows) == 18, "claim row count changed")
    require(
        len({row["parameter"] for row in parameter_rows}) == len(parameter_rows),
        "duplicate parameter ID",
    )
    require(len(parameter_rows) == 13, "parameter row count changed")
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
    require(len(shared_rows) == 6, "shared crosswalk row count changed")
    require(
        all(row["runtime_approved"] == "false" for row in shared_rows),
        "shared numeric runtime approval leaked",
    )
    require(
        all(row["source_artifact_sha256"] == PINNED_FLOOD_SOLAR_SHA for row in shared_rows),
        "shared candidate pin changed",
    )
    numeric_candidates = [
        row for row in shared_rows if row["reuse_numeric_candidate"] == "true"
    ]
    require(
        [row["flood_solar_source_record"] for row in numeric_candidates] == ["FS_SWG"],
        "numeric candidate isolation changed",
    )
    v0_shared_evidence_rows = [
        row
        for row in shared_evidence_rows
        if row["shared_evidence_id"]
        not in {
            "FEMA_HAZUS_MH_2_1_TABLE_7_9",
            "FEMA_HAZUS_7_0_ELECTRIC_MAPPING_ONLY_DISABLED",
        }
    ]
    shared_evidence_ids = {
        row["shared_evidence_id"] for row in v0_shared_evidence_rows
    }
    require(len(v0_shared_evidence_rows) == 7, "v0.1 shared evidence subset changed")
    require(
        len({row["shared_evidence_id"] for row in shared_evidence_rows})
        == len(shared_evidence_rows),
        "duplicate shared evidence ID across additive substrate versions",
    )
    require(
        all(row["source_register_id"] in source_ids for row in v0_shared_evidence_rows),
        "v0.1 shared evidence does not resolve to its governed source register",
    )
    v0_shared_catalog_rows = [
        row
        for row in shared_catalog_rows
        if row["shared_failure_unit_id"] != "FE_HAZUS_SUBSTATION_SCREENING_ASSEMBLY"
    ]
    require(len(v0_shared_catalog_rows) == 6, "v0.1 shared failure catalog subset changed")
    for row in v0_shared_catalog_rows:
        unresolved = split_ids(row["evidence_ids"]) - shared_evidence_ids
        require(
            not unresolved,
            f"{row['shared_failure_unit_id']}: unresolved shared evidence {sorted(unresolved)}",
        )
        require(
            row["runtime_loadable"] == "false",
            f"{row['shared_failure_unit_id']}: shared catalog became runtime-loadable",
        )
    additive_rows = [
        row
        for row in shared_catalog_rows
        if row["shared_failure_unit_id"] == "FE_HAZUS_SUBSTATION_SCREENING_ASSEMBLY"
    ]
    require(len(additive_rows) == 1, "additive shared screening assembly missing")
    require(additive_rows[0]["runtime_loadable"] == "false", "additive shared assembly became runtime-loadable")


def validate_axis_shared_and_candidate(
    artifact: Mapping[str, Any], parameter_rows: list[dict[str, str]]
) -> None:
    axis = artifact["hazard_axis"]
    require(axis["id"] == "FLOOD_LOCAL_DEPTH_COMPONENT_DATUM", "axis ID changed")
    require(
        axis["formula"] == "max(0, water_surface_elevation_m - component_vulnerable_elevation_m)",
        "axis formula changed",
    )
    require(axis["vertical_datum_match_required"] is True, "datum match no longer required")
    require(axis["runtime_valid_range_m"] is None, "runtime range populated without curve")
    require(axis["missing_policy"] == "withhold_not_dry", "missing policy changed")
    shared = artifact["shared_component_substrate"]
    require(shared["runtime_authority"] is False, "shared docs became runtime authority")
    require(shared["asset_label_is_intrinsic_selector"] is False, "asset label became selector")
    require(shared["numeric_runtime_inheritance_allowed"] is False, "numeric inheritance enabled")
    require(
        shared["flood_solar_candidate_artifact_sha256"] == PINNED_FLOOD_SOLAR_SHA,
        "artifact shared pin changed",
    )
    candidate = artifact["candidate_numeric_evidence"]
    require(candidate["status"] == "audit_only_not_runtime_shaped", "candidate status changed")
    require(candidate["numeric_values_embedded"] is False, "candidate numbers embedded")
    require(candidate["runtime_enabled"] is False, "candidate runtime enabled")

    require(FLOOD_SOLAR_PATH.exists(), "pinned flood-solar artifact missing")
    require(sha256(FLOOD_SOLAR_PATH) == PINNED_FLOOD_SOLAR_SHA, "flood-solar SHA drift")

    source_records = {
        row["curve_id"]: row
        for row in load_json(FLOOD_SOLAR_PATH)["curve_records"]
    }
    candidate_ids = ["FS_SWG", "FS_XFMR", "FS_SCADA", "FS_CABLE"]
    require(
        all(candidate_id in source_records for candidate_id in candidate_ids),
        "pinned flood-solar candidate record missing",
    )
    source_points = {
        candidate_id: [
            [float(point[0]), float(point[1])]
            for point in source_records[candidate_id]["parameters"]["points"]
        ]
        for candidate_id in candidate_ids
    }

    parameter_by_id = {row["parameter"]: row for row in parameter_rows}
    require(
        "FS_SWG_candidate_points_m_dr" in parameter_by_id,
        "governed FS_SWG parameter row missing",
    )
    parameter_points = [
        [float(point[0]), float(point[1])]
        for point in json.loads(
            parameter_by_id["FS_SWG_candidate_points_m_dr"]["value"]
        )
    ]

    workbook_cells = read_xlsx_sheet_cells(WORKBOOK_PATH, "Candidate_Audit")
    workbook_columns = {
        "FS_SWG": "B",
        "FS_XFMR": "D",
        "FS_SCADA": "F",
        "FS_CABLE": "H",
    }
    workbook_points = {
        candidate_id: [
            [float(workbook_cells[f"A{row_number}"]), float(workbook_cells[f"{column}{row_number}"])]
            for row_number in range(6, 15)
        ]
        for candidate_id, column in workbook_columns.items()
    }
    for candidate_id in candidate_ids:
        require(
            workbook_points[candidate_id] == source_points[candidate_id],
            f"{candidate_id}: workbook differs from pinned flood-solar source",
        )
    require(
        parameter_points == source_points["FS_SWG"],
        "FS_SWG: parameter register differs from pinned flood-solar source",
    )
    require(
        parameter_points == workbook_points["FS_SWG"],
        "FS_SWG: governed CSV and workbook differ",
    )

    depths = [point[0] for point in source_points["FS_SWG"]]
    candidates = {
        candidate_id: [point[1] for point in source_points[candidate_id]]
        for candidate_id in candidate_ids
    }
    require(depths == sorted(depths), "candidate depth grid not sorted")
    for candidate_id, values in candidates.items():
        candidate_depths = [point[0] for point in source_points[candidate_id]]
        require(candidate_depths == depths, f"{candidate_id}: depth grid mismatch")
        require(len(values) == len(depths), f"{candidate_id}: ordinate count mismatch")
        require(values == sorted(values), f"{candidate_id}: not monotone")
        require(all(0 <= value <= 1 for value in values), f"{candidate_id}: outside [0,1]")

    legacy = {
        "electrical": (0.90, 3.00, 0.75, 0.09),
        "substation": (0.95, 2.50, 1.50, 0.09),
        "civil": (0.70, 1.20, 2.00, 0.07),
        "foundation": (0.40, 0.80, 3.00, 0.12),
    }
    contributions = {}
    for name, (limit, steepness, midpoint, share) in legacy.items():
        raw_zero = limit / (1 + math.exp(steepness * midpoint))
        asymptote = limit - raw_zero
        contributions[name] = asymptote * share
    require(
        math.isclose(sum(contributions.values()), 0.24574437665595447),
        "legacy combined asymptote changed",
    )
    require(
        math.isclose(
            contributions["electrical"] + contributions["substation"],
            0.15681212821586493,
        ),
        "legacy electrical/substation asymptote changed",
    )


def validate_known_answers(
    kats: Mapping[str, Any], artifact: Mapping[str, Any]
) -> None:
    require(kats["cell_id"] == "flood_wind", "KAT cell mismatch")
    require(kats["runtime_curve_count"] == 0, "KAT runtime curve count changed")
    require(kats["runtime_curve_known_answer_tests"] == [], "runtime curve KATs not empty")
    tests = kats["tests"]
    require(len(tests) == 16, "expected 16 contract tests")
    ids = {test["test_id"] for test in tests}
    require(len(ids) == len(tests), "duplicate KAT ID")
    require(ids == EXPECTED_KATS, "KAT registry changed")
    tests_by_id = {test["test_id"]: test for test in tests}

    complete_test = tests_by_id["FW_COMPLETE_COMPONENT_INPUT_STILL_WITHHOLDS"]
    required_contract_fields: set[str] = set()
    for contract_group in (
        "identity_required",
        "exposure_required_for_contact_evaluation",
        "value_required_for_future_scenario_loss",
    ):
        required_contract_fields.update(artifact["input_field_contract"][contract_group])
    required_contract_fields.update(COMPLETE_FIXTURE_SELECTOR_FIELDS)
    required_contract_fields.update(
        artifact["hazard_axis"]["required_conditioners_capture_only"]
    )
    missing_complete_fields = required_contract_fields - set(complete_test["input"])
    require(
        not missing_complete_fields,
        f"complete KAT omits contract fields: {sorted(missing_complete_fields)}",
    )
    require(
        all(complete_test["input"][field] is not None for field in required_contract_fields),
        "complete KAT contains null contract fields",
    )
    require(
        complete_test["expected_output"]["identity_contract"] == "accepted",
        "complete KAT identity is not accepted",
    )
    require(
        complete_test["expected_output"]["axis_contract"]
        == "accepted_research_state",
        "complete KAT axis is not accepted",
    )
    expected_local_depth = max(
        0.0,
        complete_test["input"]["water_surface_elevation_m"]
        - complete_test["input"]["component_vulnerable_elevation_m"],
    )
    require(
        math.isclose(
            complete_test["expected_output"]["local_depth_above_component_datum_m"],
            expected_local_depth,
        ),
        "complete KAT local-depth known answer changed",
    )
    for metric in (
        "failure_unit_scalar_dr",
        "scenario_loss_given_value_basis",
    ):
        result = complete_test["expected_output"][metric]
        require(result["value"] is None, f"complete KAT {metric}: numeric value leaked")
        require(result["status"] == "withheld", f"complete KAT {metric}: status changed")
        reason_codes = result.get("reason_codes", result.get("reason_codes_include", []))
        require(
            "NO_RUNTIME_CURVE" in reason_codes,
            f"complete KAT {metric}: NO_RUNTIME_CURVE missing",
        )

    pathway_cases = {
        "FW_MISSING_PATHWAY_REJECTS": (False, "PATHWAY_ID_REQUIRED"),
        "FW_UNKNOWN_PATHWAY_REJECTS": (True, "UNSUPPORTED_PATHWAY_ID"),
    }
    for test_id, (pathway_present, error_code) in pathway_cases.items():
        test = tests_by_id[test_id]
        require(
            ("pathway_id" in test["input"]) is pathway_present,
            f"{test_id}: pathway presence fixture changed",
        )
        require(
            test["expected_output"]["pathway_contract"] == "rejected",
            f"{test_id}: pathway is not rejected",
        )
        require(
            test["expected_output"]["error_code"] == error_code,
            f"{test_id}: wrong rejection code",
        )
        require(
            test["expected_output"]["fallback_curve_used"] is False,
            f"{test_id}: fallback was enabled",
        )
    unknown_pathway = tests_by_id["FW_UNKNOWN_PATHWAY_REJECTS"]["input"]["pathway_id"]
    supported_pathways = {artifact["pathway"]["pathway_id"]}
    require(
        unknown_pathway not in supported_pathways,
        "unknown-pathway KAT uses a supported pathway",
    )
    for test in tests:
        expected = test["expected_output"]
        for metric in EXPECTED_METRICS:
            if metric not in expected:
                continue
            result = expected[metric]
            require(isinstance(result, dict), f"{test['test_id']}: malformed metric")
            require(result.get("value") is None, f"{test['test_id']}: numeric metric leaked")
    text = json.dumps(kats)
    require('"fallback_curve_used": true' not in text, "KAT expects fallback")
    require('"legacy_curve_used": true' not in text, "KAT expects legacy use")
    require('"dry_assumed": true' not in text, "KAT converts missing to dry")


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
        "shared_component_crosswalk_ref",
        "site_condition_adapter_ref",
        "pressure_test_ref",
    ]
    for field in ref_fields:
        value = artifact[field]
        require(isinstance(value, str), f"{field}: path must be string")
        require((ROOT / value).exists(), f"{field}: missing path {value}")
    audit_path = artifact["candidate_numeric_evidence"]["audit_record"]
    require((ROOT / audit_path).exists(), f"candidate audit path missing: {audit_path}")
    require(HANDOFF_PATH.exists(), "Hazard handoff missing")

    required_docs = [
        PROPOSED / "CHANGE_CLASSIFICATION_flood_wind__model_v0_1__docs_r1.md",
        PROPOSED / "DECISION_LOG_flood_wind__model_v0_1__docs_r1.md",
        PROPOSED / "LEGACY_EVIDENCE_INGESTION_flood_wind__model_v0_1__docs_r1.md",
        PROPOSED / "NUMERICAL_CANDIDATE_AUDIT_flood_wind__model_v0_1__docs_r1.md",
        PROPOSED / "SEVEN_STEP_AUDIT_flood_wind__model_v0_1__docs_r1.md",
        PROPOSED / "PROMOTION_GATE_MATRIX_flood_wind__model_v0_1__docs_r1.md",
        PROPOSED / "workbook_sheet_manifest_flood_wind__model_v0_1__docs_r1.md",
        ROOT / "docs/method/standards/20_shared_component_substrate_standard.md",
        ROOT / "docs/method/shared_components/flood_electrical/README.md",
        ROOT / "docs/plans/flood_wind_shared_electrical/asset_model.json",
        ROOT / "docs/extra/discussion/flood_wind_shared_electrical/README.md",
    ]
    for path in required_docs:
        require(path.exists(), f"required controlled record missing: {path}")

    markdown_paths = (
        list(CELL.rglob("*.md"))
        + list((ROOT / "docs/method/shared_components/flood_electrical").rglob("*.md"))
        + list((ROOT / "docs/plans/flood_wind_shared_electrical").rglob("*.md"))
        + list((ROOT / "docs/extra/discussion/flood_wind_shared_electrical").rglob("*.md"))
        + [
            HANDOFF_PATH,
            ROOT / "docs/cells/README.md",
            ROOT / "docs/cells/VERSION_REGISTRY.md",
            ROOT / "docs/contracts/hazard_handoff/README.md",
        ]
    )
    link_pattern = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
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


def validate_workbook() -> None:
    require(WORKBOOK_PATH.exists(), "governed workbook missing")
    require(OUTPUT_WORKBOOK_PATH.exists(), "output workbook missing")
    require(sha256(WORKBOOK_PATH) == sha256(OUTPUT_WORKBOOK_PATH), "workbook copies differ")
    require(zipfile.is_zipfile(WORKBOOK_PATH), "workbook is not a valid XLSX")
    with zipfile.ZipFile(WORKBOOK_PATH) as archive:
        require(archive.testzip() is None, "workbook ZIP corrupt")
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
    formulas = [
        html.unescape(value)
        for value in re.findall(
            r"<(?:[A-Za-z_][\w.-]*:)?f(?:\s[^>]*)?>(.*?)</(?:[A-Za-z_][\w.-]*:)?f>",
            worksheet_xml,
        )
    ]
    require(len(formulas) >= 40, "workbook formula count unexpectedly low")
    require(
        'IF(OR(D6="",E6="",F6<>G6),"",MAX(0,D6-E6))' in formulas,
        "missing-to-unknown exposure formula changed",
    )
    require("SUM(H6:H9)" in formulas, "legacy reconciliation formula missing")
    require(
        "COUNTBLANK('Exposure_Value'!H8:H9)" in formulas,
        "missing-state QA formula missing",
    )
    require(
        not re.search(r"#REF!|#DIV/0!|#VALUE!|#NAME\?|#N/A", worksheet_xml),
        "workbook XML contains a formula error",
    )
    inspect_files = list(ROOT.rglob("*.inspect.ndjson"))
    require(not inspect_files, f"inspection sidecars remain: {inspect_files}")


def validate_index_and_runtime_absence() -> None:
    index = load_json(ARTIFACT_INDEX_PATH)
    artifacts = index.get("artifacts", index if isinstance(index, list) else [])
    # A later canonical flood_wind release may be indexed; this v0.1 scaffold must never be.
    paths = [row.get("path", "") for row in artifacts if row.get("cell_id") == "flood_wind"]
    require(
        not any("/proposed/" in path or path.endswith(ARTIFACT_PATH.name) for path in paths),
        "noncanonical scaffold appears in runtime artifact index",
    )
    # src/ now holds the durable publisher (standard 23); the scaffold must not add flood_wind code there.
    require(
        not any("flood_wind" in path.name for path in (ROOT / "src").rglob("*")),
        "flood_wind scaffold code entered the src package",
    )
    handoff = HANDOFF_PATH.read_text()
    require("do_not_load_or_cut_over" in handoff, "handoff no-load action missing")
    require("M3 and M4" in handoff, "handoff omits dual bypass migration")


def main() -> int:
    artifact = load_json(ARTIFACT_PATH)
    capability = load_json(CAPABILITY_PATH)
    kats = load_json(KAT_PATH)
    source_rows = read_csv(SOURCE_PATH)
    claim_rows = read_csv(CLAIM_PATH)
    parameter_rows = read_csv(PARAMETER_PATH)
    value_rows = read_csv(VALUE_PATH)
    shared_rows = read_csv(SHARED_PATH)
    shared_catalog_rows = read_csv(SHARED_CATALOG_PATH)
    shared_evidence_rows = read_csv(SHARED_EVIDENCE_PATH)

    validate_top_level(artifact, capability)
    validate_failure_units_and_values(artifact, value_rows)
    validate_registers(
        source_rows,
        claim_rows,
        parameter_rows,
        shared_rows,
        shared_catalog_rows,
        shared_evidence_rows,
    )
    validate_axis_shared_and_candidate(artifact, parameter_rows)
    validate_known_answers(kats, artifact)
    local_links = validate_paths_and_links(artifact)
    validate_workbook()
    validate_index_and_runtime_absence()

    print("PASS flood_wind model v0.1/docs r1 scaffold")
    print(f"checks={CHECKS.count}")
    print(
        "counts="
        f"sources:{len(source_rows)},claims:{len(claim_rows)},"
        f"parameters:{len(parameter_rows)},value_rows:{len(value_rows)},"
        f"shared_rows:{len(shared_rows)},shared_catalog:{len(shared_catalog_rows)},"
        f"shared_evidence:{len(shared_evidence_rows)},"
        f"failure_units:{len(artifact['failure_units'])},"
        f"kats:{len(kats['tests'])},workbook_sheets:{len(EXPECTED_SHEETS)},"
        f"local_links:{local_links}"
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
