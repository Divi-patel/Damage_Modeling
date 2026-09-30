"""Every repository-current cell has one easy Hazard-facing request guide."""

import json
import math
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / "docs/extra/guides"
INDEX = ROOT / "docs/contracts/machine_readable_artifact_index.json"

GUIDE_BY_CELL = {
    "hail_solar": "hail_solar_curve_request_guide.md",
    "flood_solar": "flood_solar_curve_request_guide.md",
    "wind_tornado_wind": "wind_tornado_wind_curve_request_guide.md",
    "strong_wind_solar": "strong_wind_solar_curve_request_guide.md",
    "wildfire_solar": "wildfire_solar_curve_request_guide.md",
    "flood_wind": "flood_wind_curve_request_guide.md",
    "wildfire_wind": "wildfire_wind_curve_request_guide.md",
    "tropical_cyclone_wind_wind": "tropical_cyclone_wind_wind_curve_request_guide.md",
    "tropical_cyclone_wind_solar": "tropical_cyclone_wind_solar_v2_1_curve_request_guide.md",
}


def test_every_current_cell_has_an_exact_pin_request_guide():
    index = json.loads(INDEX.read_text())
    entries = {item["cell_id"]: item for item in index["artifacts"]}
    assert set(GUIDE_BY_CELL) == set(entries)

    guide_index = (GUIDES / "README.md").read_text()
    for cell_id, filename in GUIDE_BY_CELL.items():
        path = GUIDES / filename
        assert path.exists(), f"{cell_id}: missing {filename}"
        text = path.read_text()
        entry = entries[cell_id]
        assert entry["consumer_pin"] in text, f"{cell_id}: consumer pin missing"
        assert entry["sha256"] in text, f"{cell_id}: exact artifact SHA missing"
        assert Path(entry["path"]).name in text, f"{cell_id}: canonical artifact link missing"
        assert filename in guide_index, f"{cell_id}: guide absent from guide index"


def test_current_request_guide_local_links_resolve():
    for filename in GUIDE_BY_CELL.values():
        path = GUIDES / filename
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                continue
            assert (path.parent / target).resolve().exists(), f"{filename}: broken link {target}"


def test_hurricane_inline_request_example_executes():
    artifact = ROOT / (
        "docs/cells/tropical_cyclone_wind_wind/current/"
        "tropical_cyclone_wind_wind__model_v1_2__docs_r2__curve_artifact.json"
    )
    request = {
        "pathway_id": "tropical_cyclone_wind",
        "failure_unit_id": "WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT",
        "turbine_archetype_id": "CONUS_WIND_FARM_5MW_HH100_TOWER_PROXY_V1",
        "source_model_assumption_set_id": (
            "JAIMES_2020_GENERIC_FIXED_BASE_STEEL_PARKED_ROTOR_AS_DOCUMENTED"
        ),
        "tc_peak_gust_3s_10m_kmh": 163.3,
        "actual_operating_control_state": "unknown",
        "proxy_policy_id": "TCWW_OWNER_APPROVED_3P3MW_FOR_CANONICAL_5MW_TOWER_ONLY_V1",
        "canonical_asset_profile_id": "CONUS_WIND_FARM_REFERENCE_V1",
        "covered_value_basis_id": "CONUS_WIND_FARM_TOWER_16PCT_V1",
    }
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/reference_helpers/tropical_cyclone_wind_wind_curve_eval.py"),
            str(artifact),
            json.dumps(request),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)["failure_unit_results"][0]
    assert result["curve_id"] == "TCWW_JAIMES_3P3MW_AS_CANONICAL_5MW_TOWER_PROXY_V1"
    assert math.isclose(result["scalar_central_dr"], 0.5, rel_tol=0, abs_tol=1e-12)
