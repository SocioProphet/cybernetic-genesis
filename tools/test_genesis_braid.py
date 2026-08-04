"""Each test corresponds to an error actually found in a source render of the braid."""
import copy
import json
from pathlib import Path

import pytest

from genesis_braid import (PHASES, SPACES, BraidError, check, check_harmonic, check_phases,
                           check_spaces, check_steps, check_trit_surface)

CANON = json.loads((Path(__file__).resolve().parents[1] / "examples/genesis_braid.valid.json").read_text())


def test_the_canonical_braid_passes():
    assert check(copy.deepcopy(CANON)) == ["T9", "T10"]


def test_dropping_beriah_is_refused():
    """A render titled 'Four Spaces' listed three."""
    with pytest.raises(BraidError, match="missing \\['beriah'\\]"):
        check_spaces(["atzilut", "yetzirah", "assiah"])


def test_spaces_out_of_emanation_order_are_refused():
    with pytest.raises(BraidError, match="out of emanation order"):
        check_spaces(["beriah", "atzilut", "yetzirah", "assiah"])


def test_dropping_vav_is_refused_and_named():
    """Two renders spelled the phases yod-heh-heh-shin-heh. Vav is the hook — the bridge."""
    with pytest.raises(BraidError, match="VAV is missing"):
        check_phases(["yod", "heh", "heh", "shin", "heh"])


def test_heh_may_repeat_but_vav_may_not_vanish():
    check_phases(list(PHASES))                       # heh twice is correct
    assert PHASES.count("heh") == 2 and PHASES.count("vav") == 1


def test_a_ten_step_braid_cannot_call_itself_twelve():
    steps = [s for s in CANON["steps"] if s["id"] not in ("T9", "T10")]
    with pytest.raises(BraidError, match="exactly 12 steps"):
        check_steps(steps)


def test_a_gap_in_the_middle_is_refused():
    steps = copy.deepcopy(CANON["steps"])
    steps[9]["id"] = "T12"
    with pytest.raises(BraidError, match="contiguous"):
        check_steps(steps)


def test_duplicate_steps_are_refused():
    steps = copy.deepcopy(CANON["steps"])
    steps[9]["id"] = "T8"
    with pytest.raises(BraidError, match="duplicate steps"):
        check_steps(steps)


def test_a_layer_running_backwards_is_refused():
    """A render had a145..a128 — an end before its start."""
    s = copy.deepcopy(CANON["trit_surface"])
    s["layers"][3] = {"index": 4, "start": 145, "end": 128, "role": "x"}
    with pytest.raises(BraidError, match="BACKWARDS"):
        check_trit_surface(s)


def test_overlapping_layers_are_refused():
    s = copy.deepcopy(CANON["trit_surface"])
    s["layers"][1] = {"index": 2, "start": 39, "end": 87, "role": "x"}   # 49 wide, but overlaps layer 1
    with pytest.raises(BraidError, match="overlap"):
        check_trit_surface(s)


def test_the_surface_must_cover_343_exactly():
    s = copy.deepcopy(CANON["trit_surface"])
    s["layers"] = s["layers"][:6]
    with pytest.raises(BraidError, match="exactly 7 layers"):
        check_trit_surface(s)


def test_seven_times_fortynine_is_343():
    total = sum(l["end"] - l["start"] + 1 for l in CANON["trit_surface"]["layers"])
    assert total == 343 == 7 ** 3


def test_the_harmonic_ladder_must_close():
    check_harmonic({"seed": 111, "scaled": 343, "culmination": 777, "epoch": 888})
    with pytest.raises(BraidError, match="must close"):
        check_harmonic({"seed": 111, "scaled": 343, "culmination": 777, "epoch": 900})


def test_strict_refuses_labels_recovered_from_a_corrupted_render():
    """T9/T10 appear in no source render. The count proves they exist; the labels are not evidence."""
    with pytest.raises(BraidError, match="unconfirmed"):
        check(copy.deepcopy(CANON), strict=True)


def test_the_two_missing_steps_are_the_vav_phase():
    """The renders dropped vav from the phases AND T9/T10 from the steps — one deletion, two symptoms."""
    unconfirmed = [s for s in CANON["steps"] if s.get("unconfirmed")]
    assert [s["id"] for s in unconfirmed] == ["T9", "T10"]
    assert {s["phase"] for s in unconfirmed} == {"vav"}
