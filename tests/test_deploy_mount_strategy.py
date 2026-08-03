"""Teeth for the LIVE WIRING: the real Inception Deployment declares its mounts through the
InceptionMountStrategy contract, and the coherence verifier REJECTS a manifest that does not.

Teeth both ways: the real manifests pass; every way to break the wiring is caught.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import verify_deploy_mount_strategy as vdm  # noqa: E402


def _load(name: str) -> dict:
    docs = [d for d in yaml.safe_load_all((ROOT / "deploy" / name).read_text()) if isinstance(d, dict)]
    return next(d for d in docs if d.get("kind") == "Deployment")


def _real_deployment() -> dict:
    return _load("base/deployment.yaml")


def _config_env() -> dict:
    cm = yaml.safe_load((ROOT / "deploy/base-support/configmap.yaml").read_text())
    return cm.get("data", {})


STRAT = vdm.load_strategies()


# --- the real manifests are coherent ---------------------------------------- #
def test_real_deploy_is_coherent():
    assert vdm.check(_real_deployment(), _config_env(), STRAT) == []


def test_verifier_main_passes_on_repo():
    assert vdm.main() == 0


def test_data_is_a_named_volume_and_tmp_is_tmpfs():
    # /data -> project volume -> PVC ; /tmp -> task_execution tmpfs -> emptyDir{medium: Memory}
    dep = _real_deployment()
    vols = {v["name"]: v for v in dep["spec"]["template"]["spec"]["volumes"]}
    assert vdm._k8s_volume_kind(vols["data"]) == "pvc"
    assert vdm._k8s_volume_kind(vols["tmp"]) == "tmpfs"


# --- teeth: every way to break the wiring is REJECTED ----------------------- #
def test_undeclared_mount_rejected():
    dep = copy.deepcopy(_real_deployment())
    spec = dep["spec"]["template"]["spec"]
    spec["volumes"].append({"name": "rogue", "emptyDir": {}})
    spec["containers"][0]["volumeMounts"].append({"name": "rogue", "mountPath": "/rogue"})
    problems = vdm.check(dep, _config_env(), STRAT)
    assert any("not declared through any InceptionMountStrategy" in p.lower() or
               "undeclared mount" in p.lower() for p in problems), problems


def test_durable_context_on_ephemeral_storage_rejected():
    # /data is declared as a durable named volume, but back it with node-disk emptyDir -> INCOHERENT.
    dep = copy.deepcopy(_real_deployment())
    for v in dep["spec"]["template"]["spec"]["volumes"]:
        if v["name"] == "data":
            v.pop("persistentVolumeClaim")
            v["emptyDir"] = {}
    problems = vdm.check(dep, _config_env(), STRAT)
    assert any("INCOHERENT" in p for p in problems), problems


def test_task_scratch_on_durable_pvc_rejected():
    # /tmp is task_execution -> tmpfs; backing it with a PVC (durable) must be REJECTED
    # (this is the invariant that keeps task-scratch off the /data volume).
    dep = copy.deepcopy(_real_deployment())
    for v in dep["spec"]["template"]["spec"]["volumes"]:
        if v["name"] == "tmp":
            v.pop("emptyDir")
            v["persistentVolumeClaim"] = {"claimName": "inception-data"}
    problems = vdm.check(dep, _config_env(), STRAT)
    assert any("INCOHERENT" in p for p in problems), problems


def test_plain_emptydir_tmp_is_not_tmpfs_rejected():
    # medium: Memory is what makes /tmp a real tmpfs; a plain emptyDir is node disk, NOT tmpfs.
    dep = copy.deepcopy(_real_deployment())
    for v in dep["spec"]["template"]["spec"]["volumes"]:
        if v["name"] == "tmp":
            v["emptyDir"] = {}
    problems = vdm.check(dep, _config_env(), STRAT)
    assert any("INCOHERENT" in p for p in problems), problems


def test_durable_log_pointed_at_tmpfs_rejected():
    # Repoint the append-only log onto the ephemeral /tmp tmpfs -> the log would not survive.
    problems = vdm.check(_real_deployment(), {"INCEPTION_LOG": "/tmp/events.jsonl"}, STRAT)
    assert any("would NOT survive" in p for p in problems), problems


def test_readonly_mismatch_rejected():
    dep = copy.deepcopy(_real_deployment())
    for vm in dep["spec"]["template"]["spec"]["containers"][0]["volumeMounts"]:
        if vm["mountPath"] == "/data":
            vm["readOnly"] = True  # strategy declares readonly=false
    problems = vdm.check(dep, _config_env(), STRAT)
    assert any("readonly mismatch" in p for p in problems), problems
