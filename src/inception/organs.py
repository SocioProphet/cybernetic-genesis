"""Organs (plan Phase 4, minimal): a read-only retriever + a read-only adapter.

Organs are the twin's operating modes. These two are strictly read-only — no world-changing
action runs until a real adapter with dry-run/rollback lands behind the actuation gate. The
adapter's `dry_run` produces a PLAN and never an effect; `apply` is deliberately absent here.
"""
from __future__ import annotations
from .engine import InceptionEngine


class RetrieverOrgan:
    """Read-only retrieval over the durable event log (the memory the twin can see)."""
    def __init__(self, engine: InceptionEngine):
        self.engine = engine

    def events_for(self, twin_id: str) -> list[dict]:
        return [r["event"] for r in self.engine.read_log() if r["event"]["twin_id"] == twin_id]

    def twins_by_status(self, status: str) -> list[str]:
        return [tid for tid, t in self.engine.twins.items() if t.get("status") == status]


class ReadOnlyAdapter:
    """A read-only adapter: dry_run(action) returns a plan (no effect); status() is read-only.
    Gated behind the actuation gate — a non-READY twin cannot even dry-run an actuation."""
    adapter_id = "adapter:readonly/v1"
    capabilities = ("dry_run", "status")

    def __init__(self, engine: InceptionEngine):
        self.engine = engine

    def dry_run(self, twin_id: str, action: str) -> dict:
        if not self.engine.can_actuate(twin_id):
            return {"ok": False, "reason": "twin not READY — actuation gate closed", "twin_id": twin_id}
        return {"ok": True, "plan": {"twin_id": twin_id, "action": action, "effect": "NONE (dry-run)"},
                "would_apply": action, "rollback": "n/a (read-only adapter)"}

    def status(self, twin_id: str) -> dict:
        t = self.engine.twins.get(twin_id, {})
        return {"twin_id": twin_id, "status": t.get("status", "UNKNOWN"),
                "can_actuate": self.engine.can_actuate(twin_id)}
