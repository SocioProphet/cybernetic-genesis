"""Teeth for Genesis -> tritrpc_envelope -> Q3 emission (end-to-end integration)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import emit_tritrpc as e  # noqa: E402
import tritpack_min as tp  # noqa: E402

EVENT = json.loads((ROOT / "examples/twin_event_envelope.valid.json").read_text())
_HASH = re.compile(r"^sha256:[0-9a-f]{64}$")


def test_emit_produces_valid_tritrpc_envelope():
    env = e.emit(EVENT)
    for k in ("envelope_id", "schema_id", "context_id", "encoding_mode",
              "numeral_system", "payload_trit_len", "payload_packed_hex", "payload_hash", "governance"):
        assert k in env, k
    assert env["encoding_mode"] == "B2_BINARY"
    assert env["numeral_system"] == "BALANCED_TERNARY"
    assert _HASH.match(env["schema_id"]) and _HASH.match(env["context_id"]) and _HASH.match(env["payload_hash"])
    # governance parity: the event's governance rides the frame
    assert env["governance"] == EVENT["governance"]


def test_payload_round_trips_to_the_agent_message():
    env = e.emit(EVENT)
    decoded = e.decode_payload(env)
    assert decoded == e.project_event_to_agent_message(EVENT)   # exact survive


def test_payload_hash_is_over_the_packed_bytes():
    env = e.emit(EVENT)
    assert env["payload_hash"] == tp.canonical_hash(bytes.fromhex(env["payload_packed_hex"]))


def test_q3_roundtrip_preserves_the_hash():
    env = e.emit(EVENT)
    r = e.q3_roundtrip(env)
    assert r["hash_preserved"] is True                          # audit doesn't fork on the Q3 leg


def test_tamper_is_detected():
    env = e.emit(EVENT)
    packed = bytearray(bytes.fromhex(env["payload_packed_hex"]))
    packed[0] = (packed[0] + 1) % 243                           # flip one trit-group
    tampered_hash = tp.canonical_hash(bytes(packed))
    assert tampered_hash != env["payload_hash"]                 # a changed frame changes the hash


def test_bytes_trit_round_trip_any_byte():
    for data in (b"", b"\x00", b"\xff", b"hello", bytes(range(256))):
        assert tp.wire_trits_to_bytes(tp.bytes_to_wire_trits(data)) == data
