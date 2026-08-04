#!/usr/bin/env python3
"""The octonion shell — the arithmetic JSON Schema cannot do.

`common.schema.json#/$defs/OctonionBoundary` can enforce the SHAPE of the boundary (eight axes in
range, a complete evaluation order, halt-when-declared-past-1). It cannot enforce the TRUTH of it,
because JSON Schema cannot compute a Euclidean norm. So an object can declare `norm: 0.2` over axes
that actually norm to 1.4 and pass every schema check while lying.

That gap is the whole point of this module: a self-reported measurement is an instrument, and
instruments lie. The norm is RECOMPUTED from the axes and a mismatch is refused.

Geometry (corrected 2026-08-04). The halting surface ||b|| = 1 is the unit sphere in O = R^8, i.e.
S^7 — the FIBER of the octonionic Hopf fibration S^7 -> S^15 -> S^8, not its base. Governance sits
over every point of the base; it is not a region you can stand outside of. And because octonion
multiplication is non-associative, S^7 is not a group, this is not a principal bundle, and boundary
constraints do not compose associatively — hence `evaluation_order` must be recorded in full or the
verdict is not replayable.

stdlib only.
"""
from __future__ import annotations

import math

# `legality` is the real unit (1); the rest are the imaginary units e1..e7.
AXES = ("legality", "containment", "provenance", "privacy",
        "performance", "reproducibility", "licensing", "governance")

# Floating-point slack for the declared-vs-computed norm comparison.
NORM_TOLERANCE = 1e-9

# Fail-closed slack AT the shell. Exactly on the surface, floating point can land just under 1:
# two axes at 1/sqrt(2) compute to 0.9999999999999999 — short of 1.0 by 1.1e-16 — so a naive
# `>= 1.0` waves a real breach through. Worse, `1/sqrt(2)` and `sqrt(1/2)` differ by one ULP and
# would give OPPOSITE verdicts on the same boundary. A control that must fail closed cannot be
# decided by the last bit of a float, so anything within EPSILON of the surface is ON it.
# 1e-12 is ~4 orders above double-precision noise and ~9 orders below any meaningful pressure.
HALT_EPSILON = 1e-12


def breaches(norm: float) -> bool:
    """True when `norm` is at or past the shell — inclusive of the surface, fail-closed."""
    return norm >= 1.0 - HALT_EPSILON


class BoundaryError(ValueError):
    """The shell was misreported. Never downgrade this to a warning."""


def compute_norm(axes: dict) -> float:
    """||b|| over the eight axes. A missing axis is an error, not a zero."""
    missing = [a for a in AXES if a not in axes]
    if missing:
        raise BoundaryError(f"boundary is missing axes: {', '.join(missing)}")
    return math.sqrt(sum(float(axes[a]) ** 2 for a in AXES))


def check(boundary: dict) -> float:
    """Verify a boundary object end to end; return the computed norm.

    Refuses, in order: an incomplete/duplicated evaluation order, a declared norm that does not
    match the axes, and a shell breach that does not halt.
    """
    order = boundary.get("evaluation_order") or []
    if sorted(order) != sorted(AXES):
        raise BoundaryError(
            "evaluation_order must be a complete permutation of the eight axes — composition at "
            f"the shell is non-associative, so an incomplete order is not replayable (got {order})"
        )

    computed = compute_norm(boundary.get("axes") or {})
    declared = boundary.get("norm")
    if declared is None:
        raise BoundaryError("boundary declares no norm")
    if abs(float(declared) - computed) > NORM_TOLERANCE:
        raise BoundaryError(
            f"declared norm {declared!r} does not match the axes (computed {computed:.6f}) — "
            "a self-reported measurement is an instrument, and instruments lie"
        )

    if breaches(computed) and boundary.get("state") != "halt":
        raise BoundaryError(
            f"||b|| = {computed:.6f} >= 1 but state is {boundary.get('state')!r} — the shell has no discretion"
        )
    return computed


def check_object(obj: dict) -> float | None:
    """Check the `boundary` on any object that carries one. Returns None when there is none."""
    return check(obj["boundary"]) if isinstance(obj.get("boundary"), dict) else None
