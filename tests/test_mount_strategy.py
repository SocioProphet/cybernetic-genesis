"""Teeth for the InceptionMountStrategy contract (schema + verifier + podman projection).

Mirrors tools/verify_mount_strategy.py selftest as pytest so it runs under the repo's existing
`pytest tests/` CI step. Teeth both ways: admissible mounts admit, inadmissible mounts are rejected.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import verify_mount_strategy as vms  # noqa: E402


def _base(**over):
    m = {
        "context": "task_execution",
        "mount_type": "tmpfs",
        "scope_ref": "task:run-1",
        "durability": "ephemeral",
        "readonly": False,
        "symlink_safe": True,
        "destination": "/scratch",
    }
    m.update(over)
    return m


# --- mapping admits the right mount type ------------------------------------ #
def test_task_execution_tmpfs_admissible():
    assert vms.evaluate(_base()) == []


def test_userspace_volume_admissible():
    m = _base(context="userspace", mount_type="volume", scope_ref="user:cp",
              durability="durable", destination="/home/app")
    assert vms.evaluate(m) == []


def test_directory_bind_real_path_admissible():
    m = _base(context="directory", mount_type="bind", scope_ref="dir:src",
              readonly=True, source="schemas", destination="/src/schemas")
    assert vms.evaluate(m) == []


# --- teeth: task persistence ------------------------------------------------ #
def test_task_on_durable_volume_without_declaration_rejected():
    m = _base(mount_type="volume", durability="durable", destination="/artifacts")
    assert vms.evaluate(m), "task_execution on a durable volume without declared_durable must be REJECTED"


def test_task_durable_declared_admissible():
    m = _base(mount_type="volume", durability="durable", destination="/artifacts",
              declared_durable=True)
    assert vms.evaluate(m) == []


# --- teeth: durable-state on tmpfs = data loss ------------------------------ #
def test_durable_context_on_tmpfs_rejected():
    m = _base(context="userspace", mount_type="tmpfs", scope_ref="user:cp",
              durability="ephemeral", destination="/home/app")
    assert vms.evaluate(m), "a durable context on tmpfs must be REJECTED (data loss)"


# --- teeth: scope --------------------------------------------------------- #
def test_missing_scope_ref_rejected():
    m = _base(context="workspace", mount_type="volume", scope_ref="",
              durability="durable", destination="/data/ws")
    assert vms.evaluate(m), "empty scope_ref must be REJECTED"


def test_cross_scope_namespace_rejected():
    m = _base(context="chat", mount_type="volume", scope_ref="workspace:w-1",
              durability="durable", destination="/data/chat")
    assert vms.evaluate(m), "scope_ref namespace mismatching context must be REJECTED"


# --- teeth: bind through a symlink (real filesystem) ------------------------ #
def test_bind_through_symlink_rejected_and_projection_refused():
    with tempfile.TemporaryDirectory() as td:
        td = os.path.realpath(td)
        real_dir = Path(td) / "real"
        real_dir.mkdir()
        link_dir = Path(td) / "link"
        link_dir.symlink_to(real_dir, target_is_directory=True)

        clean = _base(context="directory", mount_type="bind", scope_ref="dir:src",
                      readonly=True, source=str(real_dir), destination="/src")
        tainted = {**clean, "source": str(link_dir / "sub")}

        assert vms.evaluate(clean) == []
        assert vms.evaluate(tainted), "a bind resolving through a symlink must be REJECTED"

        try:
            vms.project_to_podman(tainted)
            assert False, "project_to_podman must refuse an inadmissible mount"
        except ValueError:
            pass


# --- podman projection renders the right flags ------------------------------ #
def test_projection_renders_expected_flags():
    assert vms.project_to_podman(_base()).startswith("--mount=type=tmpfs,destination=/scratch")

    vol = _base(context="userspace", mount_type="volume", scope_ref="user:cp",
                durability="durable", destination="/home/app")
    flag = vms.project_to_podman(vol)
    assert flag.startswith("--mount=type=volume,source=incept-user-cp-")
    assert "destination=/home/app" in flag  # named volume, NOT a host path
