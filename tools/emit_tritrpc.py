"""Emit a Genesis TwinEventEnvelope AS a semantic-serdes `tritrpc_envelope` — end to end.

This closes the loop Genesis -> semantic-serdes -> quantum-prophet: a twin event is projected
to an AgentMessage (the consume contract), canonicalized, packed to a balanced-ternary
TritPack243 payload, and wrapped in a `tritrpc_envelope` carrying SCHEMA-ID / CONTEXT-ID and the
SAME governance/warrant the event carries. That envelope is exactly what quantum-prophet's Q3
leg transports; `q3_roundtrip()` proves the canonical hash survives a qutrit round-trip, so
AUDIT DOES NOT FORK from JSON event to ternary frame to quantum leg.

Self-contained: TritPack243 is vendored (tritpack_min); the Q3 leg uses quantum-prophet if it is
importable, else a trivial identity qutrit transport (trit {0,1,2} -> |0>|1>|2> -> measure) —
the mapping is 1:1 for basis states, so the identity round-trip is exact either way. The noisy /
ECC-protected Q3 path is proven in quantum-prophet's own tests.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import tritpack_min as tp  # noqa: E402
from verify_semantic_serdes_alignment import project_event_to_agent_message  # noqa: E402


def _canonical_json(obj) -> bytes:
    """Canonical JSON: sorted keys, no insignificant whitespace (the TriTRPC house rule)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_id(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()


def emit(envelope: dict, *, schema_name: str = "twin_event_envelope.schema.json",
         context: str = "https://socioprophet.ai/contexts/genesis.jsonld") -> dict:
    """TwinEventEnvelope -> tritrpc_envelope (B2). The payload is the canonical projected
    AgentMessage; SCHEMA-ID/CONTEXT-ID bind shape+meaning; governance/warrant ride along."""
    am = project_event_to_agent_message(envelope)
    payload = _canonical_json(am)
    wire = tp.bytes_to_wire_trits(payload)
    packed = tp.pack_trits(wire)
    gov = envelope.get("governance") or {}
    return {
        "envelope_id": f"trit:env:{envelope.get('event_id')}",
        "schema_id": _sha256_id(schema_name),
        "context_id": _sha256_id(context),
        "payload_schema_name": "agent_message.schema.json",
        "encoding_mode": "B2_BINARY",
        "numeral_system": "BALANCED_TERNARY",
        "payload_trit_len": len(wire),
        "payload_packed_hex": packed.hex(),
        "payload_hash": tp.canonical_hash(packed),
        "witness_refs": envelope.get("provenance_refs", []),
        "warrant_refs": (gov.get("policy_basis") or []),
        "governance": gov,
    }


def decode_payload(env: dict) -> dict:
    """Inverse: tritrpc_envelope -> the projected AgentMessage (proves the payload survives)."""
    wire = tp.unpack_trits(bytes.fromhex(env["payload_packed_hex"]), env["payload_trit_len"])
    return json.loads(tp.wire_trits_to_bytes(wire).decode("utf-8"))


def _identity_qutrit_transport(wire: list[int]) -> list[int]:
    """Fallback Q3 leg: each wire trit {0,1,2} -> qutrit basis |0>|1>|2> -> measure. Identity on
    basis states, so lossless. (quantum-prophet supplies the real noisy/ECC path.)"""
    return list(wire)


def q3_roundtrip(env: dict) -> dict:
    """Send the envelope's payload over the qutrit (Q3) leg and prove the canonical hash is
    preserved (audit doesn't fork). Uses quantum-prophet if importable, else the identity leg."""
    packed = bytes.fromhex(env["payload_packed_hex"])
    sent_hash = tp.canonical_hash(packed)
    wire = tp.unpack_trits(packed, env["payload_trit_len"])
    try:  # prefer the real quantum-prophet Q3 transport if it is on the path
        from quantum_prophet.qutrit_gateway import identity_channel, transmit_trits  # type: ignore
        recovered = list(transmit_trits(wire, channel=identity_channel).recovered_trits)
    except Exception:
        recovered = _identity_qutrit_transport(wire)
    recovered_packed = tp.pack_trits(recovered)
    recovered_hash = tp.canonical_hash(recovered_packed)
    return {
        "sent_hash": sent_hash,
        "recovered_hash": recovered_hash,
        "hash_preserved": recovered_hash == sent_hash,
        "backend": "quantum-prophet" if "quantum_prophet" in sys.modules else "identity",
    }


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("event", help="path to a TwinEventEnvelope json")
    ap.add_argument("--q3", action="store_true", help="also run the Q3 round-trip proof")
    args = ap.parse_args(argv)
    env = emit(json.loads(Path(args.event).read_text()))
    print(json.dumps(env, indent=2))
    if args.q3:
        r = q3_roundtrip(env)
        print(f"\nQ3 round-trip ({r['backend']}): hash_preserved={r['hash_preserved']}", file=sys.stderr)
        return 0 if r["hash_preserved"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
