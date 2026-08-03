#!/usr/bin/env python3
"""InceptionMountStrategy verifier — the mount-type contract with teeth, plus the Podman projection.

The contract maps each agent-execution context to the ONE admissible Podman mount type:

    userspace / chat / workspace / project   -> named volume  (durable, sovereign-managed, NOT host-coupled)
    task_execution                           -> tmpfs         (ephemeral; MUST NOT persist)
    directory / project source               -> bind          (scoped host path; ro or scoped-write)

Two layers of teeth:
  1. STRUCTURAL — `schemas/inception_mount_strategy.schema.json` (enum coherence, required scope_ref,
     bind requires source, context->mount-type mapping, the task-persistence lock). Enforced here by
     validating every instance against that schema first.
  2. SEMANTIC — things JSON Schema cannot see:
       * a bind whose `source` resolves THROUGH A SYMLINK is REJECTED, proven against the real
         filesystem (never trust the symlink_safe claim — feedback_never_write_through_symlink);
       * `scope_ref`'s namespace MUST match the context (chat: -> chat, workspace: -> workspace, ...),
         so a mount cannot silently bind one scope's data into another (cross-scope leakage).

Fail-closed: `project_to_podman` REFUSES to render a mount that does not pass `evaluate`.

Usage:
    verify_mount_strategy.py selftest              # teeth both ways (valids pass, invalids rejected)
    verify_mount_strategy.py check <instance.json> # evaluate one mount; exit 0 iff admissible
    verify_mount_strategy.py project <instance.json>  # print the podman --mount flag for an admissible mount

MIT-licensed, part of SocioProphet/cybernetic-genesis. SHA-256 below is the FIPS 180-4 algorithm.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
EXAMPLE_DIR = ROOT / "examples"
SCHEMA_NAME = "inception_mount_strategy.schema.json"

# scope_ref namespace that each context REQUIRES — cross-scope leakage is unrepresentable.
SCOPE_PREFIX = {
    "userspace": "user:",
    "task_execution": "task:",
    "chat": "chat:",
    "workspace": "workspace:",
    "project": "project:",
    "directory": "dir:",
}


# --------------------------------------------------------------------------- #
# schema layer
# --------------------------------------------------------------------------- #
def _build_registry() -> Registry:
    registry = Registry()
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        registry = Resource.from_contents(json.loads(path.read_text())) @ registry
    return registry


_VALIDATOR = Draft202012Validator(
    json.loads((SCHEMA_DIR / SCHEMA_NAME).read_text()),
    registry=_build_registry(),
)


# --------------------------------------------------------------------------- #
# semantic layer (what JSON Schema cannot see)
# --------------------------------------------------------------------------- #
def _resolve(source: str) -> Path:
    """Resolve a bind source. Relative paths resolve against the repo root."""
    p = Path(source)
    return p if p.is_absolute() else (ROOT / p)


def _through_symlink(source: str) -> bool:
    """True iff the source resolves through a symlink on the real filesystem.

    Checks every existing path component (not just the leaf) AND compares the fully
    resolved realpath against the plainly normalised absolute path. Either signal => reject.
    """
    ap = _resolve(source)
    cur = Path(ap.anchor or "/")
    for part in ap.parts[1:]:
        cur = cur / part
        if cur.is_symlink():
            return True
        if not cur.exists():
            break  # can't resolve further; the existing prefix was symlink-free
    try:
        return os.path.realpath(ap) != os.path.abspath(ap)
    except OSError:
        return True  # cannot resolve => fail-closed


def evaluate(mount: dict) -> list[str]:
    """Return a list of violation messages. Empty list == admissible. Fail-closed."""
    violations = [e.message for e in _VALIDATOR.iter_errors(mount)]
    if violations:
        return violations  # structural teeth already tripped; stop here

    context = mount["context"]
    scope_ref = mount["scope_ref"]
    prefix = SCOPE_PREFIX[context]
    if not scope_ref.startswith(prefix):
        violations.append(
            f"scope_ref {scope_ref!r} does not match context {context!r} "
            f"(expected namespace {prefix!r}) — cross-scope leakage"
        )

    if mount["mount_type"] == "bind":
        if _through_symlink(mount["source"]):
            violations.append(
                f"bind source {mount['source']!r} resolves THROUGH A SYMLINK — REJECTED "
                f"(feedback_never_write_through_symlink); symlink_safe claim is false in fact"
            )
    return violations


# --------------------------------------------------------------------------- #
# Podman projection
# --------------------------------------------------------------------------- #
def _volume_name(scope_ref: str) -> str:
    """Deterministic sovereign-managed volume name derived from scope_ref.

    NOT a host path — Podman manages the volume. The suffix is a SHA-256 (FIPS 180-4)
    digest of the scope_ref so distinct scopes never collide onto one volume.
    """
    digest = hashlib.sha256(scope_ref.encode()).hexdigest()[:12]
    slug = re.sub(r"[^a-z0-9]+", "-", scope_ref.lower()).strip("-")
    return f"incept-{slug}-{digest}"


def project_to_podman(mount: dict) -> str:
    """Render an ADMISSIBLE mount to a single podman `--mount` argument. Fail-closed:
    refuses to project a mount that does not pass evaluate()."""
    problems = evaluate(mount)
    if problems:
        raise ValueError(f"refusing to project an inadmissible mount: {problems}")

    dest = mount["destination"]
    ro = "true" if mount["readonly"] else "false"
    mt = mount["mount_type"]

    if mt == "volume":
        # sovereign-managed named volume; source is the volume NAME, never a host path
        return f"--mount=type=volume,source={_volume_name(mount['scope_ref'])},destination={dest},ro={ro}"
    if mt == "bind":
        # bind the REAL resolved path (never a symlink), scoped ro/scoped-write
        real = os.path.realpath(_resolve(mount["source"]))
        return f"--mount=type=bind,source={real},destination={dest},ro={ro}"
    # tmpfs — memory only, ephemeral; no source
    return f"--mount=type=tmpfs,destination={dest},tmpfs-size=64m"


# --------------------------------------------------------------------------- #
# selftest — teeth both ways
# --------------------------------------------------------------------------- #
VALID_EXAMPLES = [
    "mount_strategy.task_tmpfs.valid.json",
    "mount_strategy.task_durable_declared.valid.json",
    "mount_strategy.userspace_volume.valid.json",
    "mount_strategy.chat_volume.valid.json",
    "mount_strategy.directory_bind.valid.json",
    # LIVE instances: the running Inception deploy declares its real mounts through the contract.
    "mount_strategy.inception_data.valid.json",  # /data durable log (PVC)  -> project volume
    "mount_strategy.inception_tmp.valid.json",   # /tmp task scratch        -> tmpfs (ephemeral)
]

INVALID_EXAMPLES = [
    "mount_strategy.invalid.task_persistent_no_declare.json",
    "mount_strategy.invalid.durable_on_tmpfs.json",
    "mount_strategy.invalid.no_scope.json",
    "mount_strategy.invalid.cross_scope.json",
]


def cmd_selftest() -> int:
    failures = 0

    print("== VALID mounts (must be ADMISSIBLE) ==")
    for name in VALID_EXAMPLES:
        mount = json.loads((EXAMPLE_DIR / name).read_text())
        errs = evaluate(mount)
        if errs:
            failures += 1
            print(f"  [X] {name}: expected ADMISSIBLE but got:")
            for m in errs:
                print(f"        - {m}")
        else:
            flag = project_to_podman(mount)
            print(f"  [ok] {name}  ->  {flag}")

    print("\n== INVALID mounts (must be REJECTED) ==")
    for name in INVALID_EXAMPLES:
        mount = json.loads((EXAMPLE_DIR / name).read_text())
        errs = evaluate(mount)
        if not errs:
            failures += 1
            print(f"  [X] {name}: expected REJECTION but it was admitted (TEETH MISSING)")
        else:
            print(f"  [ok] {name} rejected ({errs[0]})")

    print("\n== DYNAMIC teeth: bind through a symlink (real filesystem) ==")
    with tempfile.TemporaryDirectory() as td:
        td = os.path.realpath(td)  # resolve benign system ancestor symlinks (e.g. macOS /var -> /private/var)
        real_dir = Path(td) / "real_src"
        real_dir.mkdir()
        link_dir = Path(td) / "linked_src"
        link_dir.symlink_to(real_dir, target_is_directory=True)

        clean = {
            "context": "directory", "mount_type": "bind", "scope_ref": "dir:/src",
            "durability": "ephemeral", "readonly": True, "symlink_safe": True,
            "source": str(real_dir), "destination": "/src",
        }
        tainted = {**clean, "source": str(link_dir / "sub")}  # path goes through the symlink

        if evaluate(clean):
            failures += 1
            print(f"  [X] real (non-symlink) bind should be admissible: {evaluate(clean)}")
        else:
            print(f"  [ok] real (non-symlink) bind admitted  ->  {project_to_podman(clean)}")

        if not evaluate(tainted):
            failures += 1
            print("  [X] bind through a symlink was ADMITTED (symlink teeth MISSING)")
        else:
            print(f"  [ok] bind through a symlink REJECTED ({evaluate(tainted)[0]})")

        try:
            project_to_podman(tainted)
            failures += 1
            print("  [X] project_to_podman rendered an inadmissible (symlinked) mount")
        except ValueError:
            print("  [ok] project_to_podman refused the symlinked mount (fail-closed)")

    print()
    if failures:
        print(f"MOUNT-STRATEGY SELFTEST FAILED: {failures} case(s) wrong. Fail-closed: exiting non-zero.")
        return 1
    print("MOUNT-STRATEGY SELFTEST PASSED: mapping holds, teeth bite both ways.")
    return 0


def _cmd_one(path: str, project: bool) -> int:
    mount = json.loads(Path(path).read_text())
    errs = evaluate(mount)
    if errs:
        print(f"REJECTED  {path}")
        for m in errs:
            print(f"    - {m}")
        return 1
    if project:
        print(project_to_podman(mount))
    else:
        print(f"ADMISSIBLE  {path}")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    if argv[1] == "selftest":
        return cmd_selftest()
    if argv[1] == "project" and len(argv) == 3:
        return _cmd_one(argv[2], project=True)
    if argv[1] == "check" and len(argv) == 3:
        return _cmd_one(argv[2], project=False)
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
