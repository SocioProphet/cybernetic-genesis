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
]

INVALID_CASES = [
    ("artifact_record.schema.json", "artifact_record.invalid.missing_second_witness.json"),
    ("artifact_record.schema.json", "artifact_record.invalid.bad_boundary_stone.json"),
    ("twin.schema.json", "twin.invalid.ready_without_policy.json"),
]


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

    print()
    if failures:
        print(f"SELFTEST FAILED: {failures} case(s) wrong. Fail-closed: exiting non-zero.")
        return 1
    print("SELFTEST PASSED: all valids validate, all invalids rejected.")
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
