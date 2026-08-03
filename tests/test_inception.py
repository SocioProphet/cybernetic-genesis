"""Teeth for the Inception runtime — it actually RUNS, fail-closed, durable, replayable."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from inception.engine import InceptionEngine  # noqa: E402
from inception.organs import ReadOnlyAdapter, RetrieverOrgan  # noqa: E402

SEED = json.loads((ROOT / "examples/genesis_seed.valid.json").read_text())


def _engine(tmp_path) -> InceptionEngine:
    return InceptionEngine(tmp_path / "events.jsonl")


def test_seed_becomes_verified_twin_end_to_end(tmp_path):
    st = _engine(tmp_path).incept(SEED)
    assert st["status"] == "READY"
    assert st["twin_id"].startswith("twin:")
    assert st["capabilities"] == ["dry_run", "status"]


def test_events_are_emitted_as_trit_frames(tmp_path):
    eng = _engine(tmp_path); eng.incept(SEED)
    frame = eng.read_log()[0]["trit_frame"]
    assert frame["encoding_mode"] == "B2_BINARY"
    assert frame["payload_trit_len"] > 0
    assert frame["payload_hash"].startswith("sha256:")
    assert frame["governance"]["admissibility_tier"] in ("GOVERNED", "VALIDATED", "CANONICAL")


def test_durable_and_replayable(tmp_path):
    eng = _engine(tmp_path); st = eng.incept(SEED)
    assert eng.log_path.exists()
    # a fresh engine rehydrates + replay reconstructs from the log alone
    eng2 = InceptionEngine(eng.log_path)
    assert eng2.twins[st["twin_id"]]["status"] == "READY"
    assert eng2.replay(st["twin_id"])["replayed_status"] == "READY"


def test_receipt_chain_intact_then_tamper_detected(tmp_path):
    eng = _engine(tmp_path); eng.incept(SEED)
    assert eng.verify_chain() == (True, None)
    lines = eng.log_path.read_text().splitlines()
    rec = json.loads(lines[1]); rec["event"]["payload"]["status"] = "HACKED"
    lines[1] = json.dumps(rec, sort_keys=True); eng.log_path.write_text("\n".join(lines) + "\n")
    ok, broken = InceptionEngine(eng.log_path).verify_chain()
    assert not ok and broken == 1


def test_fail_closed_no_ready_without_policy(tmp_path):
    bad = dict(SEED); bad["seed_id"] = "seed:nopolicy/1"; bad["policy_profile"] = []
    st = _engine(tmp_path).incept(bad)
    assert st["status"] == "BLOCKED" and "policy" in st["missing"]


def test_revoke_closes_the_actuation_gate(tmp_path):
    eng = _engine(tmp_path); st = eng.incept(SEED)
    assert eng.can_actuate(st["twin_id"]) is True
    eng.revoke(st["twin_id"])
    assert eng.can_actuate(st["twin_id"]) is False


def test_read_only_adapter_is_gated_and_effectless(tmp_path):
    eng = _engine(tmp_path); st = eng.incept(SEED)
    adapter = ReadOnlyAdapter(eng)
    dr = adapter.dry_run(st["twin_id"], "deploy")
    assert dr["ok"] and dr["plan"]["effect"] == "NONE (dry-run)"
    eng.revoke(st["twin_id"])
    assert adapter.dry_run(st["twin_id"], "deploy")["ok"] is False   # gate closed after revoke


def test_retriever_is_read_only(tmp_path):
    eng = _engine(tmp_path); st = eng.incept(SEED)
    evs = RetrieverOrgan(eng).events_for(st["twin_id"])
    assert len(evs) >= 3 and all(e["twin_id"] == st["twin_id"] for e in evs)


# --- HTTP surface -------------------------------------------------------- #
def test_http_service_incept_status_replay_revoke(tmp_path, monkeypatch):
    fastapi_testclient = pytest.importorskip("fastapi.testclient")
    monkeypatch.setenv("INCEPTION_LOG", str(tmp_path / "svc.jsonl"))
    import importlib
    import inception.service as svc
    importlib.reload(svc)
    client = fastapi_testclient.TestClient(svc.app)

    r = client.post("/twins/incept", json=SEED)
    assert r.status_code == 200 and r.json()["state"]["status"] == "READY"
    tid = r.json()["state"]["twin_id"]
    assert client.get(f"/twins/{tid}").json()["can_actuate"] is True
    assert client.get(f"/twins/{tid}/replay").json()["replayed_status"] == "READY"
    # dry-run allowed while READY, refused after revoke
    assert client.post(f"/twins/{tid}/dry-run", json={"action": "x"}).status_code == 200
    assert client.post(f"/twins/{tid}/revoke").json()["status"] == "REVOKED"
    assert client.post(f"/twins/{tid}/dry-run", json={"action": "x"}).status_code == 409
