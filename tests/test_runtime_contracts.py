"""Known capability spellings must not weaken spread or annual-use semantics."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("runtime_validator",ROOT/"scripts/reference_helpers/validate_runtime_contracts.py")
VALIDATOR=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def artifact():
    return json.loads((ROOT/"docs/cells/flood_bess/current/curve_artifact.json").read_text())


@pytest.mark.parametrize("flag",["CURVE_INTRINSIC_SPREAD_NOT_CARRIED","NO_INTRINSIC_DAMAGE_SPREAD"])
def test_both_existing_spellings_accept_only_the_same_declared_semantics(flag):
    a=artifact()
    a["capability_declaration"]["consumer_annual_metrics"]["limitation_flags"]=[flag]
    before=deepcopy(a)
    VALIDATOR.validate_capability(a)
    assert a==before


@pytest.mark.parametrize("mutation",["emit_spread","annual_spread","annual_withheld"])
def test_a_flag_cannot_override_contradictory_or_withheld_capability(mutation):
    a=artifact();c=a["capability_declaration"]
    if mutation=="emit_spread":c["vulnerability_emit"]["curve_intrinsic_spread"]="carried"
    if mutation=="annual_spread":c["consumer_annual_metrics"]["vulnerability_uncertainty_distribution"]="supported_by_curve_emit"
    if mutation=="annual_withheld":c["consumer_annual_metrics"]["frequency_driven_annual_loss_distribution"]="withheld_no_runtime_curve"
    with pytest.raises(AssertionError):VALIDATOR.validate_capability(a)


@pytest.mark.parametrize("flags",[[],["NO_SPREAD"],["NO_INTRINSIC_DAMAGE_SPREAD_EXTRA"]])
def test_missing_or_lookalike_flags_are_rejected(flags):
    a=artifact();a["capability_declaration"]["consumer_annual_metrics"]["limitation_flags"]=flags
    with pytest.raises(AssertionError,match="limitation flag missing"):
        VALIDATOR.validate_capability(a)


def test_full_index_validates_current_identity_and_original_known_answers(capsys):
    VALIDATOR.main()
    output=json.loads(capsys.readouterr().out)
    index=json.loads(VALIDATOR.INDEX.read_text())
    assert output["status"]=="PASS"
    assert output["artifact_count"]==len(index["artifacts"])
    assert output["hail_runtime_kats"]>0 and output["wildfire_state_kats"]>0


def test_mismatched_changelog_pin_is_still_rejected(monkeypatch):
    original=VALIDATOR.load
    def load(path):
        data=original(path)
        if str(path).endswith("tropical_cyclone_wind_bess/CHANGELOG.json"):
            data["current_pin"]="incorrect"
        return data
    monkeypatch.setattr(VALIDATOR,"load",load)
    with pytest.raises(AssertionError,match="changelog pin mismatch"):
        VALIDATOR.main()
