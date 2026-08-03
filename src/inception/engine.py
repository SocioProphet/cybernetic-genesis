"""Inception runtime — turns a GenesisSeed into a verified Twin, for real.

This is the first RUNNING piece of the platform (plan Phase 1 + the K3 twin bridge): not a schema,
a process. It ingests a GenesisSeed, drives the twin lifecycle SEEDED -> VERIFYING -> READY under
fail-closed verification, emits a governed `TwinEventEnvelope` for every transition ENCODED AS a
semantic-serdes `tritrpc_envelope` (the same trit rail quantum-prophet transports), persists the
stream to a durable append-only log with hash-chained receipts, and can replay the whole lifecycle
and revoke a twin (blocking further actuation). No world-changing adapter runs here — actuation is
gated behind READY + policy, per the plan's actuation gate.

Runs on stdlib + the repo's own `emit_tritrpc`; the HTTP surface (service.py) is a thin wrapper.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sys
_TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(_TOOLS))
import emit_tritrpc as _rail  # emit a TwinEventEnvelope AS a tritrpc_envelope  # noqa: E402

READY = "READY"
_RECEIPT_ROOT = "genesis:inception:receipt-root:v0"


def _gov(tier: str = "GOVERNED", status: str = "APPROVED", basis=None) -> dict:
    return {"admissibility_tier": tier, "review_status": status, "policy_basis": basis or []}


def _content_hash(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass
class InceptionEngine:
    """The durable runtime. `log_path` is an append-only JSONL event log — the source of truth;
    twin state is a projection of it (replayable)."""
    log_path: Path
    _clock: int = 0
    twins: dict[str, dict] = field(default_factory=dict)
    receipt_head: str = _RECEIPT_ROOT

    def __post_init__(self):
        self.log_path = Path(self.log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if self.log_path.exists():
            self._rehydrate()

    # --- durable append with a hash-chained receipt --------------------- #
    def _append(self, record: dict) -> dict:
        eh = _content_hash(record["event"])
        receipt = "sha256:" + hashlib.sha256(f"{self.receipt_head}␟{eh}".encode()).hexdigest()
        record["receipt"] = {"prev": self.receipt_head, "event_hash": eh, "receipt": receipt}
        self.receipt_head = receipt
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
        return record

    def _emit(self, twin_id: str, event_type: str, payload: dict, seed_id: str,
              policy_refs, memory_refs) -> dict:
        self._clock += 1
        env = {
            "event_id": f"evt:{twin_id}:{self._clock}",
            "event_type": event_type,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(0)),  # deterministic for replay parity
            "actor_id": "inception-engine",
            "twin_id": twin_id,
            "mission_id": f"mission:inception:{twin_id}",
            "project_id": "project:inception",
            "correlation_id": f"corr:{twin_id}:{self._clock}",
            "trace_id": f"trace:{twin_id}",
            "policy_refs": list(policy_refs),
            "memory_refs": list(memory_refs),
            "provenance_refs": [f"prov:seed:{seed_id}"],
            "payload": payload,
            "governance": _gov(basis=list(policy_refs)),
        }
        trit_frame = _rail.emit(env)          # <-- the twin event AS a tritrpc_envelope (trit rail)
        return self._append({"clock": self._clock, "event": env, "trit_frame": trit_frame})

    # --- the K3 lifecycle: seed -> verified twin ------------------------ #
    def incept(self, seed: dict) -> dict:
        """Drive SEEDED -> VERIFYING -> READY. Fail-closed: no READY without identity + policy +
        memory. Returns the twin's final state (a projection of the emitted, persisted events)."""
        seed_id = seed["seed_id"]
        twin_id = f"twin:{seed_id.split(':',1)[-1]}"
        policy_refs = seed.get("policy_profile", [])
        memory_refs = [f"mem:{k}" for k in (seed.get("memory_profile") or {})]
        identity = {"workload_identity": twin_id}

        self._emit(twin_id, "twin.seeded", {"status": "SEEDED"}, seed_id, policy_refs, memory_refs)
        self._emit(twin_id, "twin.verifying", {"status": "VERIFYING",
                   "checks": ["identity", "policy", "memory"]}, seed_id, policy_refs, memory_refs)

        # VERIFICATION GATE (fail-closed):
        missing = []
        if not identity.get("workload_identity"): missing.append("identity")
        if not policy_refs: missing.append("policy")
        if not memory_refs: missing.append("memory")
        if missing:
            self._emit(twin_id, "twin.blocked", {"status": "BLOCKED", "missing": missing},
                       seed_id, policy_refs, memory_refs)
            state = {"twin_id": twin_id, "seed_id": seed_id, "status": "BLOCKED",
                     "missing": missing, "identity": identity}
        else:
            self._emit(twin_id, "twin.verified", {"status": READY, "capabilities": ["dry_run", "status"]},
                       seed_id, policy_refs, memory_refs)
            state = {"twin_id": twin_id, "seed_id": seed_id, "status": READY,
                     "identity": identity, "policy_refs": policy_refs, "memory_refs": memory_refs,
                     "capabilities": ["dry_run", "status"]}
        self.twins[twin_id] = state
        return state

    def revoke(self, twin_id: str) -> dict:
        t = self.twins.get(twin_id)
        if not t:
            raise KeyError(twin_id)
        self._emit(twin_id, "twin.revoked", {"status": "REVOKED"}, t["seed_id"],
                   t.get("policy_refs", []), t.get("memory_refs", []))
        t["status"] = "REVOKED"
        return t

    def can_actuate(self, twin_id: str) -> bool:
        """Actuation gate: only a READY (never REVOKED/BLOCKED) twin may act."""
        return self.twins.get(twin_id, {}).get("status") == READY

    # --- replay + verification ------------------------------------------ #
    def read_log(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        return [json.loads(l) for l in self.log_path.read_text().splitlines() if l.strip()]

    def verify_chain(self) -> tuple[bool, int | None]:
        """Recompute the receipt chain over the persisted log; return (ok, first_broken_index)."""
        prev = _RECEIPT_ROOT
        for i, rec in enumerate(self.read_log()):
            eh = _content_hash(rec["event"])
            expect = "sha256:" + hashlib.sha256(f"{prev}␟{eh}".encode()).hexdigest()
            r = rec.get("receipt", {})
            if r.get("event_hash") != eh or r.get("prev") != prev or r.get("receipt") != expect:
                return False, i
            prev = r["receipt"]
        return True, None

    def replay(self, twin_id: str) -> dict:
        """Reconstruct a twin's final status purely from the event log (no in-memory state)."""
        status = None
        for rec in self.read_log():
            ev = rec["event"]
            if ev["twin_id"] == twin_id:
                status = ev["payload"].get("status", status)
        return {"twin_id": twin_id, "replayed_status": status}

    def _rehydrate(self):
        """Rebuild engine state from the durable log on startup (crash-safe)."""
        for rec in self.read_log():
            self._clock = max(self._clock, rec.get("clock", 0))
            self.receipt_head = rec.get("receipt", {}).get("receipt", self.receipt_head)
            ev = rec["event"]
            tid = ev["twin_id"]
            st = ev["payload"].get("status")
            if st:
                self.twins.setdefault(tid, {"twin_id": tid, "seed_id": ev["provenance_refs"][0].split(":")[-1]})
                self.twins[tid]["status"] = st
