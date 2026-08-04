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

  **And distinctness of identity is not independence.** Sophia falls by emanating ALONE and so
  cannot ascend by herself; her raiser is her son and yet stands as her father -- brought forth
  from below, but SENT from above. Origin may descend from the subject; AUTHORITY may not.
  Otherwise a subject mints a derived identity and has it attest on their behalf, and the +1 is
  the subject wearing another name. Hence `attestor_authority_chain`.

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


def check_authority_does_not_derive_from_the_subject(rite: dict) -> None:
    """Sophia's rule: the raiser may be BROUGHT FORTH from the one raised, but must not draw
    AUTHORITY from them.

    Sophia does not fall through ignorance — she falls by emanating ALONE, without her syzygy, and
    so she cannot ascend by herself; she is raised. Her raiser is her son and yet stands as her
    father: brought forth from below, but SENT from above. Origin descends from her; authority does
    not.

    That distinction is the security property. Refusing only `attestor == subject` leaves a sybil
    hole: a subject mints a derived identity and has it attest on their behalf. Distinctness of
    identity is not independence. So the attestor's AUTHORITY CHAIN must not contain the subject —
    while `attestor_origin` freely may, because being brought forth from the subject is not the
    defect.

    Fail-closed: where a crossing is at stake and the authority chain is unstated, the initiation is
    refused. Unknown provenance of authority is not evidence of independence.
    """
    if not rite.get("enables_threshold"):
        return
    subject = rite.get("subject")
    chain = rite.get("attestor_authority_chain")
    if not chain:
        raise InitiationError(
            "this initiation enables a crossing but states no `attestor_authority_chain` — where the "
            "attestor's authority comes from is exactly what must be shown, and unknown provenance is "
            "not independence"
        )
    if subject in chain:
        raise InitiationError(
            f"the attestor's authority derives from the subject ({subject!r} appears in its authority "
            "chain) — a raiser may be brought forth from the one it raises, but may not draw its "
            "authority from them; otherwise the +1 is the subject wearing another name"
        )


def check(rite: dict) -> None:
    if rite.get("operation") not in OPERATIONS:
        raise InitiationError(f"unknown operation {rite.get('operation')!r}; expected one of {list(OPERATIONS)}")
    check_operation_matches_the_names(rite)
    check_not_self_attested(rite)
    check_authority_does_not_derive_from_the_subject(rite)
