#!/usr/bin/env python3
"""Witness independence — Sophia's rule generalised to every place two witnesses are accepted.

The L0 covenant demands two witnesses of different KIND: a chart (signer) and a method (validator).
`WitnessesDualType` enforces that, and it is enforceable in JSON Schema because it is a statement
about types.

It is not enough. Two witnesses of different kind can still be **one voice**:

  * a witness whose authority derives from the SUBJECT it is witnessing — the artifact's own
    producing twin authorised its own attestors, so the record witnesses itself; or
  * a witness whose authority derives from the OTHER WITNESS — if the chart signer issued the
    method validator's authority, then "two witnesses" is one witness wearing two names, and the
    dual-witness rule has been satisfied in form while defeated in substance.

This is Pistis Sophia's distinction, generalised. Sophia falls by emanating ALONE and cannot
ascend by herself; her raiser is her son and yet stands as her father — brought forth from below,
but SENT from above. **Origin may descend from the subject; authority may not.** So a witness's
`origin` is unconstrained — being produced by the thing you witness is not the defect — while its
`authority_chain` is.

Deliberately NOT enforced: sharing a distant common root. Two attestations under one organisational
root CA are still two attestations; demanding disjoint chains all the way up would refuse every
real PKI. The defect is PROXIMATE — one party standing behind the other, or behind the subject.

JSON Schema cannot test whether one field's value appears inside another field's array, so this
lives here alongside the octonion norm, the braid counts and the initiation checks.

stdlib only.
"""
from __future__ import annotations


class WitnessError(ValueError):
    """Two witnesses that are one voice. Never downgrade — the whole point is independence."""


def _chain(w: dict) -> list:
    return list(w.get("authority_chain") or [])


def _name(w: dict) -> str:
    return w.get("name") or w.get("role") or w.get("hash", "<unnamed>")


def check_not_authorised_by_subject(witnesses: list, subject) -> None:
    """No witness may draw authority from the thing it witnesses."""
    if subject is None:
        return
    for w in witnesses:
        if subject in _chain(w):
            raise WitnessError(
                f"witness {_name(w)!r} draws authority from the subject it witnesses ({subject!r} is "
                "in its authority chain) — the record would be witnessing itself"
            )


def check_witnesses_do_not_authorise_each_other(witnesses: list) -> None:
    """No witness may stand behind another. If A authorised B, A and B are one voice."""
    identities = {}
    for w in witnesses:
        for key in ("id", "name", "role"):
            if w.get(key):
                identities[w[key]] = w
    for w in witnesses:
        for link in _chain(w):
            other = identities.get(link)
            if other is not None and other is not w:
                raise WitnessError(
                    f"witness {_name(w)!r} draws its authority from witness {_name(other)!r} — two "
                    "witnesses with one behind the other are one witness wearing two names, and the "
                    "dual-witness rule is satisfied in form but defeated in substance"
                )


def check_authority_is_stated(witnesses: list) -> None:
    """Fail-closed: an unstated authority chain is not evidence of independence."""
    for w in witnesses:
        if not _chain(w):
            raise WitnessError(
                f"witness {_name(w)!r} states no authority_chain — where a witness's authority comes "
                "from is exactly what independence turns on, and unknown provenance is not independence"
            )


def check(witnesses: list, *, subject=None) -> None:
    if len(witnesses) < 2:
        raise WitnessError(f"a matter is established by two or three witnesses; got {len(witnesses)}")
    check_authority_is_stated(witnesses)
    check_not_authorised_by_subject(witnesses, subject)
    check_witnesses_do_not_authorise_each_other(witnesses)


def check_artifact_record(record: dict) -> None:
    """The subject of an ArtifactRecord's witnesses is the twin that produced it."""
    check(record.get("witnesses") or [], subject=record.get("produced_by_twin"))
