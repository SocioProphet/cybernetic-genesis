#!/usr/bin/env python3
"""The Genesis braid spine — the counting, coverage and ordering JSON Schema cannot do.

Every corrupted render of the braid failed the same way: it dropped or duplicated a member of a
set whose size is fixed. A diagram is a witness, and a witness that miscounts is a false witness.
So the counts live here, as arithmetic, and the diagram becomes derivable from them instead of
hand-drawn beside them.

What this pins (each corresponds to an error actually found in a source render):

  FOUR SPACES   atzilut -> beriah -> yetzirah -> assiah, in emanation order, exactly four.
                A render titled "Four Spaces" listed three; beriah had been dropped.

  FIVE PHASES   yod, heh, shin, vav, heh  (YHShVH — the pentagrammaton: YHVH with shin set in).
                Two renders dropped VAV and repeated heh instead. Vav means "hook" — it is the
                connector, the bridge phase. Losing it silently deletes the join.

  TWELVE STEPS  T0..T11, contiguous, no gaps and no repeats, each bound to a space and a phase.
                One render skipped T9 and T10 while still calling itself twelve-step.

  343 TRITS     7 layers x 49 = 343, contiguous and non-overlapping, covering a0..a342 exactly.
                A render had layers overlapping and two ranges running BACKWARDS (end < start),
                and titled the array a0..a32.

  HARMONIC      111 = 1 + 10 + 100; 343 = 7^3; 777 + 111 = 888. (This one the renders got right;
                it is pinned so it stays right.)

stdlib only.
"""
from __future__ import annotations

# The four worlds, in order of emanation. Not a set — an ordered chain.
SPACES = ("atzilut", "beriah", "yetzirah", "assiah")

# YHShVH. `heh` legitimately appears twice (positions 2 and 5); `vav` exactly once.
PHASES = ("yod", "heh", "shin", "vav", "heh")

STEP_COUNT = 12
TRIT_LAYERS = 7
TRITS_PER_LAYER = 49
TRIT_TOTAL = TRIT_LAYERS * TRITS_PER_LAYER  # 343 = 7^3


class BraidError(ValueError):
    """A miscount in the spine. Never downgrade to a warning — the count IS the contract."""


def check_spaces(spaces: list) -> None:
    if tuple(spaces) != SPACES:
        missing = [s for s in SPACES if s not in spaces]
        extra = [s for s in spaces if s not in SPACES]
        detail = []
        if missing:
            detail.append(f"missing {missing}")
        if extra:
            detail.append(f"unknown {extra}")
        if not detail:
            detail.append("out of emanation order")
        raise BraidError(f"the four spaces must be exactly {list(SPACES)} in order — {'; '.join(detail)}")


def check_phases(phases: list) -> None:
    if tuple(phases) != PHASES:
        detail = "out of order"
        if "vav" not in phases:
            detail = ("VAV is missing — YHShVH is yod-heh-shin-vav-heh. Vav is the hook, the "
                      "connector; dropping it deletes the bridge phase")
        elif len(phases) != len(PHASES):
            detail = f"expected {len(PHASES)} phases, got {len(phases)}"
        raise BraidError(f"the five phases must be exactly {list(PHASES)} — {detail}")


def check_steps(steps: list) -> None:
    ids = [s.get("id") for s in steps]
    expected = [f"T{i}" for i in range(STEP_COUNT)]
    if len(ids) != STEP_COUNT:
        raise BraidError(f"the braid has exactly {STEP_COUNT} steps (T0..T{STEP_COUNT - 1}); got {len(ids)}")
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise BraidError(f"duplicate steps: {dupes}")
    if ids != expected:
        gaps = [e for e in expected if e not in ids]
        raise BraidError(f"steps must be contiguous T0..T{STEP_COUNT - 1} in order — missing {gaps or 'nothing, but out of order'}")
    for s in steps:
        if s.get("space") not in SPACES:
            raise BraidError(f"{s['id']} is bound to unknown space {s.get('space')!r}")
        if s.get("phase") not in PHASES:
            raise BraidError(f"{s['id']} is bound to unknown phase {s.get('phase')!r}")


def check_trit_surface(surface: dict) -> None:
    layers = surface.get("layers") or []
    if len(layers) != TRIT_LAYERS:
        raise BraidError(f"the holographic surface has exactly {TRIT_LAYERS} layers; got {len(layers)}")

    covered = []
    for layer in layers:
        start, end = layer.get("start"), layer.get("end")
        if start is None or end is None:
            raise BraidError(f"layer {layer.get('index')} has no range")
        if end < start:
            raise BraidError(
                f"layer {layer.get('index')} runs BACKWARDS (a{start}..a{end}) — an end before its start "
                "is not a range"
            )
        width = end - start + 1
        if width != TRITS_PER_LAYER:
            raise BraidError(
                f"layer {layer.get('index')} spans {width} trits (a{start}..a{end}); every layer is "
                f"exactly {TRITS_PER_LAYER}"
            )
        covered.append((start, end))

    covered.sort()
    for (s1, e1), (s2, e2) in zip(covered, covered[1:]):
        if s2 <= e1:
            raise BraidError(f"layers overlap: a{s1}..a{e1} and a{s2}..a{e2}")
        if s2 != e1 + 1:
            raise BraidError(f"gap between a{e1} and a{s2} — the surface must be contiguous")

    if covered[0][0] != 0 or covered[-1][1] != TRIT_TOTAL - 1:
        raise BraidError(
            f"the surface must cover a0..a{TRIT_TOTAL - 1} exactly; got a{covered[0][0]}..a{covered[-1][1]}"
        )


def check_harmonic(ladder: dict) -> None:
    """111 = 1+10+100, 343 = 7^3, 777 + 111 = 888."""
    seed, scaled, culmination, epoch = (ladder.get("seed"), ladder.get("scaled"),
                                        ladder.get("culmination"), ladder.get("epoch"))
    if seed != 1 + 10 + 100:
        raise BraidError(f"harmonic seed must be 111 (1+10+100); got {seed}")
    if scaled != TRIT_TOTAL:
        raise BraidError(f"harmonic scale must be 343 (7^3); got {scaled}")
    if culmination + seed != epoch:
        raise BraidError(f"{culmination} + {seed} != {epoch} — the ladder must close on the epoch step")


def check(braid: dict, *, strict: bool = False) -> list[str]:
    """Full spine check. Returns the list of steps whose label is unconfirmed.

    `strict` refuses any unconfirmed label — use it once the source spec is bound. By default the
    gaps are reported and counted rather than silently carried, because a label recovered from a
    corrupted render is not evidence.
    """
    check_spaces(braid.get("spaces") or [])
    check_phases(braid.get("phases") or [])
    check_steps(braid.get("steps") or [])
    check_trit_surface(braid.get("trit_surface") or {})
    check_harmonic(braid.get("harmonic_ladder") or {})

    unconfirmed = [s["id"] for s in braid["steps"] if s.get("unconfirmed")]
    if strict and unconfirmed:
        raise BraidError(
            f"{len(unconfirmed)} step label(s) still unconfirmed: {unconfirmed} — these were read off a "
            "corrupted render and must be bound to the source spec before the braid is canonical"
        )
    return unconfirmed


# --- The carry: when a chain may be unbounded -------------------------------------------------
#
# An earlier draft of docs/genesis-braid.md claimed the hop budget (CAP(K) / H_max) is what stops a
# carry cascade from overshooting. The board disproves that, and the correction matters:
#
#   the 9-chain  9 -> 18 -> 27 -> 36 -> 45 -> 54 -> 63   six carries, NO cap, arrives EXACTLY
#   the 5-chain  5 -> 14 -> 23 -> 32 -> 41 -> 50 -> 59 -> 68 -> bounces to 58 = death
#
# A cap would have TRUNCATED the first — cutting off a legitimate ascent — and would not have saved
# the second; it would only have relocated the failure. So a cap punishes the aligned chain and
# fails the misaligned one. It is a substitute for alignment, not the control itself.
#
# The real condition is arithmetic. 63 = 7 x 9: nine DIVIDES the goal, five does not.
#
#   A carry chain may be unbounded IFF its step divides the distance to the goal.
#
# That is "authority derived from above" — the step is anchored to the terminus rather than chosen
# locally. "Validated from below" is the exact-landing rule, applied at EVERY hop instead of only at
# the goal: the 5-chain fails precisely because nothing checks it until it has already overshot.
#
# A cap remains the honest DEGRADED MODE: where a chain cannot be shown aligned, bound it, and say
# that is what you are doing.

def carry_is_aligned(step: int, distance: int) -> bool:
    """True when a carry of `step` can reach `distance` exactly, so the chain needs no cap."""
    if step <= 0:
        raise BraidError("a carry step must be positive")
    return distance % step == 0


def carry_terminus(start: int, step: int, goal: int, *, goose: set[int] | None = None) -> tuple[int, list[int]]:
    """Walk an uncapped carry from `start` and report where it actually ends.

    Returns (final_position, path). Overshoot counts back from the goal, as on the board — which is
    how an unaligned chain lands somewhere it never chose.
    """
    pos, path = start, []
    while True:
        pos += step
        path.append(pos)
        if goose is not None and pos not in goose:
            break
        if goose is None and pos >= goal:
            break
        if len(path) > 1000:
            raise BraidError("carry did not terminate")
    final = pos if pos <= goal else goal - (pos - goal)
    return final, path
