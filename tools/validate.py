#!/usr/bin/env python3
"""Cybernetic Genesis — Phase-0 schema validator.

Two modes:

  validate <schema.json>:<instance.json> [<schema>:<instance> ...]
      Validate each instance against its schema. Exit 0 iff ALL pass.

  selftest
      Validate every declared VALID example (must PASS) and every declared
      INVALID fixture (must be REJECTED). Teeth both ways, fail-closed:
      a valid that fails OR an invalid that passes exits non-zero.

Cross-file $ref (e.g. "common.schema.json#/$defs/...") is resolved by loading
every schema in schemas/ into a referencing.Registry keyed by its $id.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
EXAMPLE_DIR = ROOT / "examples"

# --- selftest manifest: (schema, instance, must_pass) -----------------------
VALID_CASES = [
    ("hologram.schema.json", "hologram.valid.json"),
    ("genesis_seed.schema.json", "genesis_seed.valid.json"),
    ("twin.schema.json", "twin.valid.json"),
    ("twin_event_envelope.schema.json", "twin_event_envelope.valid.json"),
    ("artifact_record.schema.json", "artifact_record.valid.json"),
    ("policy_decision.schema.json", "policy_decision.valid.json"),
    ("policy_decision.schema.json", "policy_decision.deny.valid.json"),
    ("adapter_descriptor.schema.json", "adapter_descriptor.valid.json"),
    ("genesis_braid.schema.json", "genesis_braid.valid.json"),
    ("initiation.schema.json", "initiation.valid.json"),
    ("initiation.schema.json", "initiation.sophia_raised.valid.json"),
    # M.OS.ES: a short device may author WITH the +1 (three witnesses, not two).
    ("artifact_record.schema.json", "artifact_record.from_short_device.valid.json"),
]

INVALID_CASES = [
    ("artifact_record.schema.json", "artifact_record.invalid.missing_second_witness.json"),
    ("artifact_record.schema.json", "artifact_record.invalid.bad_boundary_stone.json"),
    ("twin.schema.json", "twin.invalid.ready_without_policy.json"),
    ("twin.schema.json", "twin.invalid.ready_while_boundary_halts.json"),
    ("twin.schema.json", "twin.invalid.boundary_breach_without_halt.json"),
    # The threshold: 21 is short — the land was seen, not entered.
    ("twin.schema.json", "twin.invalid.bidirectional_at_21.json"),
    ("twin.schema.json", "twin.invalid.bidirectional_without_consent.json"),
    ("genesis_seed.schema.json", "genesis_seed.invalid.active_active_single_model.json"),
    ("genesis_seed.schema.json", "genesis_seed.invalid.no_consent_profile.json"),
    # Each of these is an error found in a real source render of the braid.
    ("genesis_braid.schema.json", "genesis_braid.invalid.three_spaces.json"),
    ("genesis_braid.schema.json", "genesis_braid.invalid.ten_steps.json"),
    ("initiation.schema.json", "initiation.invalid.self_renamed_across_threshold.json"),
    # M.OS.ES: falling short is a demand that someone else cross with you, not a free pass.
    ("twin.schema.json", "twin.invalid.mobile_authors_direct_while_short.json"),
    ("twin.schema.json", "twin.invalid.attested_without_plus_one.json"),
    ("artifact_record.schema.json", "artifact_record.invalid.short_device_only_two_witnesses.json"),
]


# Objects whose `boundary` is schema-valid but arithmetically false. The schema CANNOT catch
# these — it has no norm — so they are checked by tools/octonion_boundary.py instead.
ARITHMETIC_FALSE_CASES = [
    "twin.lied_norm.schema_valid_arithmetic_false.json",
]


def check_boundaries() -> list[str]:
    """Recompute every declared octonion norm. A boundary that lies about itself is refused
    here even though it satisfies the schema — JSON Schema cannot do arithmetic."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from octonion_boundary import BoundaryError, check_object

    failures = []
    for path in sorted(EXAMPLE_DIR.glob("*.json")):
        obj = json.loads(path.read_text())
        if not isinstance(obj, dict) or "boundary" not in obj:
            continue
        must_be_refused = path.name in ARITHMETIC_FALSE_CASES
        # A `.invalid.` fixture is the SCHEMA's to reject; whether the arithmetic also catches it
        # is informational. Only ARITHMETIC_FALSE_CASES must be caught here, because only they are
        # invisible to the schema.
        schema_owns_it = ".invalid." in path.name
        try:
            check_object(obj)
            if must_be_refused:
                failures.append(f"{path.name} SHOULD have been refused by the norm check but passed")
            else:
                print(f"  [ok] {path.name} boundary norm verified")
        except BoundaryError as e:
            if must_be_refused or schema_owns_it:
                print(f"  [ok] {path.name} refused by the norm check ({e})")
            else:
                failures.append(f"{path.name} boundary refused: {e}")
    return failures


# Braid fixtures whose defect is arithmetic, not vocabulary: JSON Schema pins the enums and the
# array bounds, but cannot see a backwards range or a repeated phase in the right-sized list.
BRAID_ARITHMETIC_FALSE = [
    "genesis_braid.invalid.vav_missing.json",
    "genesis_braid.invalid.layer_runs_backwards.json",
]


def check_braid() -> list[str]:
    """Count the spine: four spaces, five phases with vav, twelve contiguous steps, 7x49=343."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from genesis_braid import BraidError, check as check_spine

    failures = []
    for path in sorted(EXAMPLE_DIR.glob("genesis_braid*.json")):
        must_be_refused = path.name in BRAID_ARITHMETIC_FALSE or ".invalid." in path.name
        try:
            unconfirmed = check_spine(json.loads(path.read_text()))
            if must_be_refused:
                failures.append(f"{path.name} SHOULD have been refused by the spine check but passed")
            else:
                note = f" ({len(unconfirmed)} label(s) unconfirmed: {unconfirmed})" if unconfirmed else ""
                print(f"  [ok] {path.name} spine verified{note}")
        except BraidError as e:
            if must_be_refused:
                print(f"  [ok] {path.name} refused by the spine check ({e})")
            else:
                failures.append(f"{path.name} spine refused: {e}")
    return failures


def check_witnesses() -> list[str]:
    """Two witnesses of different kind can still be one voice: refuse a witness authorised by the
    subject it witnesses, or by the other witness."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from witness_independence import WitnessError, check_artifact_record

    failures = []
    for path in sorted(EXAMPLE_DIR.glob("artifact_record*.json")):
        obj = json.loads(path.read_text())
        if "witnesses" not in obj:
            continue
        # Only the arithmetic-false fixtures MUST be caught here — they are schema-valid by
        # construction and invisible to it. A `.invalid.` fixture is the SCHEMA's to reject (a bad
        # boundary stone, a short device needing three witnesses); its witnesses may legitimately
        # be independent, so whether this check also fires is informational.
        must_be_refused = "schema_valid_arithmetic_false" in path.name
        schema_owns_it = ".invalid." in path.name
        try:
            check_artifact_record(obj)
            if must_be_refused:
                failures.append(f"{path.name} SHOULD have been refused but passed")
            else:
                print(f"  [ok] {path.name} witnesses are independent")
        except WitnessError as e:
            if must_be_refused or schema_owns_it:
                print(f"  [ok] {path.name} refused ({e})")
            else:
                failures.append(f"{path.name} refused: {e}")
    return failures


def check_initiations() -> list[str]:
    """A rename must actually be the operation it claims, and must not be self-granted where it
    buys passage. JSON Schema cannot compare two field lengths or two field values."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from initiation import InitiationError, check as check_rite

    failures = []
    for path in sorted(EXAMPLE_DIR.glob("initiation*.json")):
        must_be_refused = "schema_valid_arithmetic_false" in path.name or ".invalid." in path.name
        try:
            check_rite(json.loads(path.read_text()))
            if must_be_refused:
                failures.append(f"{path.name} SHOULD have been refused but passed")
            else:
                print(f"  [ok] {path.name} rename verified")
        except InitiationError as e:
            if must_be_refused:
                print(f"  [ok] {path.name} refused ({e})")
            else:
                failures.append(f"{path.name} refused: {e}")
    return failures


def build_registry() -> Registry:
    """Load every schema in schemas/ into a registry keyed by $id."""
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        doc = json.loads(path.read_text())
        resource = Resource.from_contents(doc)
        registry = resource @ registry  # register under its own $id
    return registry


def load(path: Path):
    return json.loads(path.read_text())


def validator_for(schema_path: Path, registry: Registry) -> Draft202012Validator:
    schema = load(schema_path)
    return Draft202012Validator(schema, registry=registry)


def validate_pair(schema_path: Path, instance_path: Path, registry: Registry):
    """Return list of error messages (empty == valid)."""
    validator = validator_for(schema_path, registry)
    instance = load(instance_path)
    return [e.message for e in validator.iter_errors(instance)]


def cmd_validate(pairs: list[str]) -> int:
    registry = build_registry()
    ok = True
    for pair in pairs:
        if ":" not in pair:
            print(f"FAIL  malformed arg (want schema:instance): {pair}")
            ok = False
            continue
        schema_arg, instance_arg = pair.split(":", 1)
        schema_path = (SCHEMA_DIR / schema_arg) if not Path(schema_arg).exists() else Path(schema_arg)
        instance_path = (EXAMPLE_DIR / instance_arg) if not Path(instance_arg).exists() else Path(instance_arg)
        errors = validate_pair(schema_path, instance_path, registry)
        if errors:
            ok = False
            print(f"FAIL  {instance_path.name} against {schema_path.name}")
            for msg in errors:
                print(f"        - {msg}")
        else:
            print(f"PASS  {instance_path.name} against {schema_path.name}")
    return 0 if ok else 1


def cmd_selftest() -> int:
    registry = build_registry()
    failures = 0

    print("== VALID examples (must PASS) ==")
    for schema_name, example_name in VALID_CASES:
        errors = validate_pair(SCHEMA_DIR / schema_name, EXAMPLE_DIR / example_name, registry)
        if errors:
            failures += 1
            print(f"  [X] {example_name}: expected PASS but got {len(errors)} error(s):")
            for msg in errors:
                print(f"        - {msg}")
        else:
            print(f"  [ok] {example_name} validates against {schema_name}")

    print("\n== INVALID fixtures (must be REJECTED) ==")
    for schema_name, example_name in INVALID_CASES:
        errors = validate_pair(SCHEMA_DIR / schema_name, EXAMPLE_DIR / example_name, registry)
        if not errors:
            failures += 1
            print(f"  [X] {example_name}: expected REJECTION but it validated (TEETH MISSING)")
        else:
            print(f"  [ok] {example_name} rejected ({errors[0]})")

    print("\n== GENESIS BRAID (counting the schema cannot do) ==")
    braid_failures = check_braid()
    for msg in braid_failures:
        print(f"  [X] {msg}")
    failures += len(braid_failures)

    print("\n== WITNESS INDEPENDENCE (kind-distinctness is not enough) ==")
    wit_failures = check_witnesses()
    for msg in wit_failures:
        print(f"  [X] {msg}")
    failures += len(wit_failures)

    print("\n== INITIATION (the rename must hold up) ==")
    rite_failures = check_initiations()
    for msg in rite_failures:
        print(f"  [X] {msg}")
    failures += len(rite_failures)

    print("\n== OCTONION BOUNDARY (arithmetic the schema cannot do) ==")
    boundary_failures = check_boundaries()
    for msg in boundary_failures:
        print(f"  [X] {msg}")
    failures += len(boundary_failures)

    print()
    if failures:
        print(f"SELFTEST FAILED: {failures} case(s) wrong. Fail-closed: exiting non-zero.")
        return 1
    print("SELFTEST PASSED: all valids validate, all invalids rejected, every declared norm recomputed.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    if argv[1] == "selftest":
        return cmd_selftest()
    return cmd_validate(argv[1:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
