# Integration: Genesis **consumes** semantic-serdes (does not fork it)

The estate's canonical contract layer is `SocioProphet/semantic-serdes` (SemanticCell,
AgentMessage, canonical_enums, governance). Cybernetic Genesis is a layer **on top of** it, so
its objects must be *projections of* those contracts — the same discipline TritRPC follows
(an encoding profile of the contracts, never a competing schema). This is enforced by
`tools/verify_semantic_serdes_alignment.py` (in CI), fail-closed and teeth both ways.

## Object mapping

| Genesis object | semantic-serdes contract | How they align |
|---|---|---|
| **TwinEventEnvelope** | **AgentMessage** | `project_event_to_agent_message()` maps every AgentMessage-required field: `event_id→message_id`, `actor_id→sender`, `twin_id→recipient`, `timestamp→sent_at`, `event_type→subject`, `correlation_id→payload_ref`, `provenance_refs→witness_refs`, and `governance→governance` (identical block). A twin event **is** an AgentMessage under this mapping. |
| **Hologram** | **SemanticCell** | Both are governed semantic objects: Hologram now carries a canonical `truth_class` (OBSERVED/ASSERTED/INFERRED/REPUTED) and a `governance` block; `provenance_root` is a boundary-stone content hash (≈ SemanticCell `provenance` + `governance`). |
| **PolicyDecision.verdict** | **decision_outcome / review_status** | ALLOW/DENY/REQUIRE_APPROVAL are the fail-closed verdict family; a world-changing ALLOW additionally requires dual-witness. |
| **governance** block | **semantic-serdes governance** | `admissibility_tier` (RAW/VALIDATED/GOVERNED/CANONICAL) + `review_status` are reused **verbatim** from `semantic-serdes/canonical_enums.yaml`. |

## No vocabulary drift
`common.schema.json`'s `Governance` and `TruthClass` `$defs` use the semantic-serdes canonical
enum values. `verify_semantic_serdes_alignment.py` pins those values and **rejects** any Genesis
object that uses an off-canon `admissibility_tier` / `review_status` / `truth_class` — so the
two packs cannot silently diverge. (Source of truth: `semantic-serdes/canonical_enums.yaml`; a
future step may generate these `$defs` from it directly.)

## What this buys
- A Genesis `TwinEventEnvelope` can ride the same TritRPC/AgentMessage rail, carry the same
  governance/warrant/consent (governance-parity, semantic-serdes#17), and be audited by the
  same tooling — across binary/ternary/qutrit transports.
- A Genesis `Hologram` is a `SemanticCell` archetype, so it inherits truth-class + governance
  discipline rather than reinventing it.
- The L0 dual-witness / boundary-stone covenant composes with the estate's existing
  governance-parity and digest-pinning — one discipline, two names.

## Follow-on
- Generate `Governance`/`TruthClass` `$defs` from `semantic-serdes/canonical_enums.yaml` in CI
  (kill the pin duplication).
- Emit a Genesis event AS a `tritrpc_envelope` (B2/B3/Q3) end-to-end and prove the canonical
  hash survives (ties into quantum-prophet's Q3 leg).
