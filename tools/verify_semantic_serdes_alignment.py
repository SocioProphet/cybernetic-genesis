#!/usr/bin/env python3
"""Integration conformance: Genesis objects CONSUME the semantic-serdes contract, not fork it.

The estate lesson (from the TritRPC work): a new layer must be an *encoding/projection of* the
canonical contracts, not a competing schema. This gate proves it for cybernetic-genesis:

  * A `TwinEventEnvelope` PROJECTS to a valid `SocioProphet/semantic-serdes` **AgentMessage**
    (every AgentMessage-required field is derivable), and carries the estate `governance` block.
  * A `Hologram` aligns with a **SemanticCell**: it declares a canonical `truth_class` and a
    `governance` block, and its `provenance_root` is a boundary-stone content hash.
  * NO VOCABULARY DRIFT: the Genesis `admissibility_tier` / `review_status` / `truth_class`
    enums must EQUAL the semantic-serdes canonical_enums (pinned below; source of truth is
    `semantic-serdes/canonical_enums.yaml`). A Genesis object using an off-canon value is a fork.

Self-contained (the expected contract is pinned here with a pointer to the source), so it runs
in CI without cloning semantic-serdes. Teeth both ways in the selftest.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# --- pinned semantic-serdes contract (source: SocioProphet/semantic-serdes) ---------------- #
SS_AGENT_MESSAGE_REQUIRED = {
    "message_id", "sender", "recipient", "sent_at", "delivery_semantics",
    "subject", "payload_ref", "governance",
}
SS_ADMISSIBILITY_TIER = {"RAW", "VALIDATED", "GOVERNED", "CANONICAL"}
SS_REVIEW_STATUS = {"NOT_REQUIRED", "REQUIRED", "PENDING", "APPROVED", "REJECTED", "ESCALATED"}
SS_TRUTH_CLASS = {"OBSERVED", "ASSERTED", "INFERRED", "REPUTED"}
_HASH_OK = lambda s: isinstance(s, str) and (s.startswith("sha256:") or s.startswith("sha3-256:")) and len(s.split(":", 1)[-1]) == 64


def project_event_to_agent_message(env: dict) -> dict:
    """Project a TwinEventEnvelope onto the AgentMessage shape. This is the 'consume' contract:
    a Genesis event IS an AgentMessage under this mapping."""
    gov = env.get("governance") or {}
    return {
        "message_id": env.get("event_id"),
        "sender": env.get("actor_id"),
        "recipient": env.get("twin_id"),
        "sent_at": env.get("timestamp"),
        "delivery_semantics": "AT_LEAST_ONCE",           # twin events are at-least-once, replayable
        "subject": env.get("event_type"),
        "payload_ref": env.get("correlation_id") or env.get("event_id"),
        "governance": gov,
        "witness_refs": env.get("provenance_refs", []),
        "capability_tokens": [],
    }


def _check_governance(gov, where: str) -> list[str]:
    out = []
    if not isinstance(gov, dict):
        return [f"{where}: no governance block (fork — must carry the estate admission discipline)"]
    if gov.get("admissibility_tier") not in SS_ADMISSIBILITY_TIER:
        out.append(f"{where}: admissibility_tier {gov.get('admissibility_tier')!r} not a semantic-serdes canonical value")
    if gov.get("review_status") not in SS_REVIEW_STATUS:
        out.append(f"{where}: review_status {gov.get('review_status')!r} not a semantic-serdes canonical value")
    return out


def check_event_envelope(env: dict, where: str = "<envelope>") -> list[str]:
    out = _check_governance(env.get("governance"), where)
    am = project_event_to_agent_message(env)
    missing = [k for k in SS_AGENT_MESSAGE_REQUIRED if not am.get(k)]
    if missing:
        out.append(f"{where}: does not project to a valid AgentMessage — missing {sorted(missing)}")
    return out


def check_hologram(holo: dict, where: str = "<hologram>") -> list[str]:
    out = _check_governance(holo.get("governance"), where)
    if holo.get("truth_class") not in SS_TRUTH_CLASS:
        out.append(f"{where}: truth_class {holo.get('truth_class')!r} not a semantic-serdes canonical truth_class")
    if not _HASH_OK(holo.get("provenance_root", "")):
        out.append(f"{where}: provenance_root is not a boundary-stone content hash")
    return out


def check_file(path: Path) -> list[str]:
    doc = json.loads(path.read_text())
    n = path.name
    if "twin_event_envelope" in n:
        return check_event_envelope(doc, n)
    if n.startswith("hologram"):
        return check_hologram(doc, n)
    return []


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", help="genesis example json files (default: examples/*.valid.json)")
    args = ap.parse_args(argv)
    files = [Path(f) for f in args.files] or sorted(
        p for p in (ROOT / "examples").glob("*.json")
        if "invalid" not in p.name and (p.name.startswith("hologram") or "twin_event_envelope" in p.name)
    )
    problems = []
    for f in files:
        problems += check_file(f)
    if problems:
        print("semantic-serdes alignment FAILED (Genesis would fork the estate contract):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"OK: {len(files)} Genesis object(s) consume the semantic-serdes contract "
          f"(project to AgentMessage / align with SemanticCell; canonical enums; boundary-stone provenance).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
