#!/usr/bin/env python3
"""Initiation — a name change as a governed event, and the arithmetic that keeps it honest.

Renaming on initiation is a letter operation on a name: a letter inserted, swapped, or dropped.
It is the oldest form of the +1 attestation, and the pattern is consistent:

    Abram    -> Abraham    a HEH inserted
    Sarai    -> Sarah      a YOD swapped for a HEH
    Hoshea   -> Yehoshua   a YOD added -- and MOSES is the one who adds it (Num 13:16)
    YHVH     -> YHShVH     a SHIN set into the Name (the five phases of the braid)

The Hoshea case is the load-bearing one. Moses cannot cross; what he can do is add a letter to
another's name so that other crosses. So:

  **You cannot rename yourself across a threshold.** An initiation that enables a crossing needs
  an attestor who is not the subject. Hoshea did not add his own yod. Abram was not renamed by
  Abram. Self-attested initiation into a crossing is refused -- it is the same defect as a device
  with a shortfall signing its own +1 (see M.OS.ES: a re-signature by the same party is not a +1).

JSON Schema pins the vocabulary; it cannot compare two field lengths, so the operation/name
consistency is checked here.

stdlib only.
"""
from __future__ import annotations

# The braid letters, plus room for any script's letters.
BRAID_LETTERS = ("yod", "heh", "shin", "vav")
OPERATIONS = ("insert", "swap", "drop", "replace")


class InitiationError(ValueError):
    """A rename that does not hold up. The name IS the identity; do not wave these through."""


def _norm(name: str) -> str:
    return "".join(name.split()).lower()


def check_operation_matches_the_names(rite: dict) -> None:
    """The declared operation must be consistent with what actually happened to the name."""
    prior, new = _norm(rite.get("prior_name") or ""), _norm(rite.get("new_name") or "")
    if not prior or not new:
        raise InitiationError("an initiation needs both a prior_name and a new_name")
    if prior == new:
        raise InitiationError(f"{rite.get('prior_name')!r} is unchanged — an initiation that renames nothing is not one")

    op = rite.get("operation")
    dl = len(new) - len(prior)
    if op == "insert" and dl <= 0:
        raise InitiationError(f"operation 'insert' but the name did not grow ({len(prior)} -> {len(new)})")
    if op == "drop" and dl >= 0:
        raise InitiationError(f"operation 'drop' but the name did not shrink ({len(prior)} -> {len(new)})")
    if op == "swap" and dl != 0:
        raise InitiationError(
            f"operation 'swap' but the length changed ({len(prior)} -> {len(new)}) — a swap trades one "
            "letter for another; use 'insert' or 'drop' if the length moves"
        )


def check_not_self_attested(rite: dict) -> None:
    """You cannot rename yourself across a threshold.

    Moses added the yod to Hoshea's name; Hoshea did not. An initiation that ENABLES a crossing
    requires an attestor distinct from the subject. Without a crossing at stake a self-chosen name
    is fine — the rule binds only where the rename buys passage.
    """
    if not rite.get("enables_threshold"):
        return
    attestor, subject = rite.get("attestor"), rite.get("subject")
    if not attestor:
        raise InitiationError(
            "this initiation enables a threshold crossing, so it requires an attestor — "
            "you cannot rename yourself across a threshold"
        )
    if attestor == subject:
        raise InitiationError(
            f"attestor and subject are both {subject!r} — a self-attested initiation is not a +1, "
            "for the same reason a re-signature by the same party is not one (M.OS.ES)"
        )


def check(rite: dict) -> None:
    if rite.get("operation") not in OPERATIONS:
        raise InitiationError(f"unknown operation {rite.get('operation')!r}; expected one of {list(OPERATIONS)}")
    check_operation_matches_the_names(rite)
    check_not_self_attested(rite)
