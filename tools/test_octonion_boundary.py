"""The shell refuses a lie even when the schema is satisfied."""
import math

import pytest

from octonion_boundary import AXES, BoundaryError, breaches, check, compute_norm

CLEAN = {a: 0.0 for a in AXES}


def _b(axes=None, **over):
    axes = {**CLEAN, **(axes or {})}
    b = {"axes": axes, "norm": compute_norm(axes), "state": "proceed",
         "evaluation_order": list(AXES)}
    b.update(over)
    return b


def test_clean_boundary_proceeds():
    assert check(_b()) == 0.0


def test_norm_is_euclidean_over_all_eight_axes():
    assert compute_norm({**CLEAN, "privacy": 0.3, "licensing": 0.4}) == pytest.approx(0.5)


def test_a_single_total_breach_halts():
    b = _b({"legality": 1.0}, state="halt")
    assert check(b) == pytest.approx(1.0)


def test_partial_pressures_compound_into_a_halt():
    """No single axis is breached, but together they reach the shell."""
    axes = {**CLEAN, "privacy": 0.6, "provenance": 0.6, "licensing": 0.6}
    assert compute_norm(axes) >= 1.0
    with pytest.raises(BoundaryError, match="no discretion"):
        check(_b(axes, norm=compute_norm(axes), state="proceed"))


def test_a_lied_about_norm_is_refused():
    """The schema would pass this: axes in range, norm < 1, state proceed. The arithmetic won't."""
    axes = {**CLEAN, "containment": 0.9, "governance": 0.9}
    with pytest.raises(BoundaryError, match="instruments lie"):
        check(_b(axes, norm=0.2, state="proceed"))


def test_incomplete_evaluation_order_is_refused():
    with pytest.raises(BoundaryError, match="non-associative"):
        check(_b(evaluation_order=list(AXES[:7])))


def test_duplicated_evaluation_order_is_refused():
    with pytest.raises(BoundaryError, match="non-associative"):
        check(_b(evaluation_order=[AXES[0]] + list(AXES[:7])))


def test_a_missing_axis_is_an_error_not_a_zero():
    with pytest.raises(BoundaryError, match="missing axes"):
        compute_norm({a: 0.0 for a in AXES[:6]})


@pytest.mark.parametrize("spelling", ["1/sqrt(2)", "sqrt(1/2)"])
def test_landing_exactly_on_the_shell_halts_in_either_spelling(spelling):
    """S^7 is the surface, and reaching it is a breach — regardless of the last bit of a float.

    `1/sqrt(2)` computes to 0.9999999999999999 (short of 1.0 by 1.1e-16) while `sqrt(1/2)` computes
    to exactly 1.0. Two spellings of the same number must not give opposite governance verdicts.
    """
    v = 1 / math.sqrt(2) if spelling == "1/sqrt(2)" else math.sqrt(0.5)
    axes = {**CLEAN, "legality": v, "privacy": v}
    assert breaches(compute_norm(axes)), f"{spelling} must be treated as ON the shell"
    with pytest.raises(BoundaryError, match="no discretion"):
        check(_b(axes, norm=compute_norm(axes), state="proceed"))


def test_the_epsilon_does_not_swallow_real_headroom():
    """Fail-closed slack is for float noise only — a genuinely sub-shell boundary still proceeds."""
    axes = {**CLEAN, "legality": 0.7, "privacy": 0.7}   # norm ~0.9899
    assert not breaches(compute_norm(axes))
    check(_b(axes, norm=compute_norm(axes), state="proceed"))
