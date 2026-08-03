#!/usr/bin/env python3
"""LIVE WIRING teeth: the Inception Deployment's ACTUAL mounts must be declared THROUGH the
InceptionMountStrategy contract (schemas/inception_mount_strategy.schema.json), not merely
described by it in the abstract.

`verify_deploy_self_contained.py` proves every SA/ConfigMap/PVC the Deployment names is defined
under deploy/. This proves the *mount types* are the ones the contract mandates:

  1. Every container `volumeMount` in deploy/base/deployment.yaml is governed by exactly ONE
     `examples/mount_strategy.*.valid.json` instance whose `destination` equals its `mountPath`.
     An undeclared mount is REJECTED — you cannot smuggle a volume past the contract.
  2. Each governing instance itself passes the contract teeth (`verify_mount_strategy.evaluate`).
  3. The Kubernetes volume backing that mount matches the contract `mount_type`:
        volume  (durable, sovereign-managed named store) -> persistentVolumeClaim
        tmpfs   (memory-only, ephemeral)                 -> emptyDir { medium: Memory }
        bind    (scoped host path)                        -> hostPath
     A durable context on ephemeral storage — or task scratch on a durable PVC — is REJECTED.
  4. `readonly` on the instance matches `readOnly` on the volumeMount.
  5. The running service's durable append-only log (`INCEPTION_LOG` from the ConfigMap the
     Deployment consumes) resolves onto a mount whose context is DURABLE (a named volume), never
     tmpfs — so the event log provably survives the container. This is the same declared type as
     the Podman named volume the local runbook uses (docs/inception-mount-strategy.md).

Together (2) + (3) also discharge the task-scratch invariant: `task_execution -> tmpfs` means the
scratch mount is memory-only and CANNOT be a PVC, so task-scratch never lands on the /data volume.

kubectl-free, fail-closed. MIT-licensed, part of SocioProphet/cybernetic-genesis. Any SHA-256
referenced by the contract is the FIPS 180-4 algorithm.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import verify_mount_strategy as vms  # noqa: E402  (the contract teeth)

DEPLOY_DIR = ROOT / "deploy"
EXAMPLE_DIR = ROOT / "examples"

# The K8s volume backing that each contract mount_type REQUIRES.
EXPECTED_K8S_KIND = {
    "volume": "pvc",       # durable, sovereign-managed named store (Podman named volume <-> K8s PVC)
    "tmpfs": "tmpfs",      # memory-only emptyDir (medium: Memory) — ephemeral
    "bind": "hostPath",    # a scoped host path
}


def _load_all(p: Path) -> list[dict]:
    return [d for d in yaml.safe_load_all(Path(p).read_text()) if isinstance(d, dict)]


def _k8s_volume_kind(vol: dict) -> str:
    """Classify a K8s pod volume into the durability posture the contract cares about."""
    if "persistentVolumeClaim" in vol:
        return "pvc"
    if "hostPath" in vol:
        return "hostPath"
    if "emptyDir" in vol:
        medium = (vol.get("emptyDir") or {}).get("medium")
        return "tmpfs" if medium == "Memory" else "emptyDir-disk"  # plain emptyDir = node disk, NOT tmpfs
    for k in ("configMap", "secret", "projected", "downwardAPI", "csi"):
        if k in vol:
            return k
    return "unknown"


def load_strategies() -> dict[str, list[tuple[str, dict]]]:
    """destination -> [(filename, instance)] for every examples/mount_strategy.*.valid.json."""
    out: dict[str, list[tuple[str, dict]]] = {}
    for p in sorted(EXAMPLE_DIR.glob("mount_strategy.*.valid.json")):
        inst = json.loads(p.read_text())
        dest = inst.get("destination")
        if dest:
            out.setdefault(dest, []).append((p.name, inst))
    return out


def _longest_prefix_owner(path: str, governed: list[tuple[str, dict]]):
    """The governed mount whose destination is the longest path-prefix of `path` (or None)."""
    p = PurePosixPath(path)
    best = None
    for dest, inst in governed:
        try:
            p.relative_to(PurePosixPath(dest))
        except ValueError:
            continue
        if best is None or len(PurePosixPath(dest).parts) > len(PurePosixPath(best[0]).parts):
            best = (dest, inst)
    return best


def check(deployment: dict, config_env: dict, dest_to_strategies: dict) -> list[str]:
    """Pure coherence check. Empty list == coherent. Fail-closed."""
    problems: list[str] = []
    spec = deployment["spec"]["template"]["spec"]
    volumes = {v["name"]: v for v in spec.get("volumes", [])}
    governed: list[tuple[str, dict]] = []  # (mountPath, instance) actually wired into the pod

    for c in spec.get("containers", []):
        for vm in c.get("volumeMounts", []):
            mount_path = vm["mountPath"]
            vol = volumes.get(vm["name"])
            if vol is None:
                problems.append(f"volumeMount {mount_path!r} names volume {vm['name']!r} not in spec.volumes")
                continue

            matches = dest_to_strategies.get(mount_path, [])
            if not matches:
                problems.append(
                    f"container mount {mount_path!r} is NOT declared through any InceptionMountStrategy "
                    f"(no examples/mount_strategy.*.valid.json with destination=={mount_path!r}) — "
                    f"undeclared mount, REJECTED"
                )
                continue
            if len(matches) > 1:
                names = ", ".join(n for n, _ in matches)
                problems.append(f"container mount {mount_path!r} governed by MORE THAN ONE strategy: {names}")
                continue

            sname, inst = matches[0]
            governed.append((mount_path, inst))

            # (2) the governing instance must itself pass the contract teeth.
            errs = vms.evaluate(inst)
            if errs:
                problems.append(f"strategy {sname} governing {mount_path!r} is itself inadmissible: {errs}")
                continue

            # (3) the K8s backing volume type must match the contract mount_type.
            want = EXPECTED_K8S_KIND[inst["mount_type"]]
            got = _k8s_volume_kind(vol)
            if got != want:
                problems.append(
                    f"mount {mount_path!r}: strategy {sname} declares mount_type={inst['mount_type']!r} "
                    f"(requires K8s {want}) but the Deployment backs it with {got!r} — INCOHERENT "
                    f"(durable state on ephemeral storage, or ephemeral scratch on a durable volume)"
                )

            # (4) readonly coherence.
            vm_ro = bool(vm.get("readOnly", False))
            if vm_ro != bool(inst["readonly"]):
                problems.append(
                    f"mount {mount_path!r}: readonly mismatch — strategy readonly={inst['readonly']}, "
                    f"volumeMount readOnly={vm_ro}"
                )

    # (5) the durable append-only log must resolve onto a DURABLE (named-volume) mount, never tmpfs.
    log_path = config_env.get("INCEPTION_LOG")
    if log_path:
        owner = _longest_prefix_owner(log_path, governed)
        if owner is None:
            problems.append(
                f"durable log INCEPTION_LOG={log_path!r} is not under any governed mount destination "
                f"— it would land on the read-only rootfs / an undeclared path"
            )
        elif owner[1]["durability"] != "durable":
            dest, inst = owner
            problems.append(
                f"durable append-only log INCEPTION_LOG={log_path!r} resolves onto {dest!r}, declared "
                f"durability={inst['durability']!r} (mount_type={inst['mount_type']!r}) — the event log "
                f"would NOT survive the container. REJECTED"
            )
    return problems


def main() -> int:
    deployments = [
        d for f in (DEPLOY_DIR / "base").glob("*.yaml")
        for d in _load_all(f) if d.get("kind") == "Deployment"
    ]
    if len(deployments) != 1:
        print(f"expected exactly 1 Deployment under deploy/base, found {len(deployments)}", file=sys.stderr)
        return 1
    dep = deployments[0]

    # ConfigMaps the Deployment actually consumes via envFrom (so INCEPTION_LOG is what runs).
    referenced = {
        (ef.get("configMapRef") or {}).get("name")
        for c in dep["spec"]["template"]["spec"].get("containers", [])
        for ef in c.get("envFrom", [])
    }
    referenced.discard(None)
    config_env: dict = {}
    for f in DEPLOY_DIR.rglob("*.yaml"):
        for d in _load_all(f):
            if d.get("kind") == "ConfigMap" and d.get("metadata", {}).get("name") in referenced:
                config_env.update(d.get("data", {}))

    problems = check(dep, config_env, load_strategies())
    if problems:
        print("deploy mount-strategy coherence FAILED "
              "(Deployment mounts not declared through InceptionMountStrategy):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("OK: every Deployment mount is declared through an InceptionMountStrategy instance, "
          "the K8s volume types match the contract (durable->PVC, task->tmpfs), and the durable "
          "event log lives on a durable named volume.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
