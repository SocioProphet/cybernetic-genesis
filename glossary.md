# Cybernetic Genesis — Phase-0 Canonical Glossary

The frozen vocabulary for Phase 0. Names here are the contract; downstream code and
schemas MUST use these terms and no synonyms. Each entry is one or two lines.

## Core objects

- **Hologram** — The semantic-hologram base object: a multi-projection representation
  of an entity (dense/sparse vectors, memories, relations, affordances) bound to a
  policy envelope and a boundary-stone provenance root.
- **GenesisSeed** — The declarative seed from which a Twin is inceived: ontology slice,
  goal schema, allowed organs, and retrieval/memory/policy/provider/federation profiles.
- **Twin** — The runtime verified twin inceived from a GenesisSeed. Lifecycle states:
  SEEDED → VERIFYING → READY → PAUSED → REVOKED → ARCHIVED.
- **TwinEventEnvelope** — Canonical envelope for every twin-emitted event, carrying
  identity, correlation/trace context, and policy/memory/provenance references.
- **ArtifactRecord** — A world-changing output produced by a Twin; boundary-stone
  addressed and dual-witnessed.
- **PolicyDecision** — A verdict from the policy plane: ALLOW | DENY | REQUIRE_APPROVAL.
- **AdapterDescriptor** — Declares an adapter (provider, organ, or surface bridge) the
  platform may bind — its capabilities, identity mode, policy hooks, audit surface,
  and rollback strategy. Contract frozen now; adapter build is Phase 1+.

## Process concepts

- **Genesis** — The generative phase: authoring seeds and holograms that define what a
  Twin can become.
- **Inception** — The act of instantiating a Twin from a GenesisSeed and verifying it
  into READY.
- **K3 bridge** — The verification/attestation bridge crossed during Inception that
  binds a Twin's chart (identity) and method (validation) witnesses before it may act.
- **Organ** — A bounded capability unit a Twin may operate (e.g. retriever, planner,
  composer); a Twin may only use organs its seed's `organs_allowed` permits.
- **Mission** — A scoped objective a Twin pursues; every event carries its `mission_id`.
- **Archetype** — A reusable pattern a hologram/seed instantiates (e.g. cartographer).
- **Affordance** — An action a hologram exposes as available to a Twin.

## L0 source-canon discipline (see `docs/L0-genesis-covenant.md`)

- **Dual witness** — A world-changing record is established only by two or more
  witnesses of different kind: a **chart** (signer/identity) witness AND a **method**
  (validator) witness. Never one. (`witnesses[]`, `minItems: 2`.)
- **Boundary stone** — An immutable content-address field (`digest`, `provenance_root`)
  matching `^(sha256|sha3-256):[0-9a-f]{64}$`. Do not move the landmark.
- **Weights & measures** — Any metric object declares `sample_size`, `snr` (a number or
  explicit `"n/a"`), and `units`. A just weight states its terms.
- **Fail-closed** — Absence of proof is denial, not permission. A Twin is not READY
  without identity + policy + memory refs; a world-changing ALLOW needs dual witnesses.
- **Plumb-line** — The CI baseline (`tools/validate.py selftest`) that measures every
  object against the frozen schemas; drift is caught, not tolerated.
