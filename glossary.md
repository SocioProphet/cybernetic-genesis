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
- **Membrane** — The twin bridge, stated correctly: not a pipe but a membrane. A single
  1-space system in which the AI connects to and **protects** the user's three-space system
  from the external three-space system. Carried on every Twin; declares `flow`,
  `thresholds_crossed`, `consent`, and `scale`.
- **ConsentGrant** — A purpose-bound opt-in (`opted_in | opted_out | not_asked`). The Ring /
  three-space serving-and-update stack governs **opted-in users only**; `not_asked` is the
  default posture and is never an implied yes.
- **AdapterDescriptor** — Declares an adapter (provider, organ, or surface bridge) the
  platform may bind — its capabilities, identity mode, policy hooks, audit surface,
  and rollback strategy. Contract frozen now; adapter build is Phase 1+.
- **InceptionMountStrategy** — The Podman mount-type contract: maps each execution context
  (userspace/task_execution/chat/workspace/project/directory) to the one admissible mount
  type — named **volume** (durable, sovereign-managed), **bind** (scoped host path, never
  through a symlink), or **tmpfs** (ephemeral). Carries `scope_ref` so cross-scope leakage
  is unrepresentable. See `docs/inception-mount-strategy.md`.

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

- **Threshold (22)** — The hermetically-sealed thresholds of the topic space. Bidirectional
  flow across the membrane — the only direction that lets the external three-space reach the
  protected user three-space — requires **all 22** crossed. **21 is short**: the land was seen,
  not entered. Enforced in `twin.schema.json`; fixture `twin.invalid.bidirectional_at_21.json`.
- **Scale (the repeating bridge)** — The INCEPTION→GENESYS bridge is not crossed once. It
  repeats at each frequency: stand up the **k3s quorum**, the twin bridge scales to **k8s**,
  and it repeats again for the **federated global mesh**. One bridge, three frequencies.
- **PATET / PETER** — The active-active LoRA-tuned foundation-model pair ("rock") behind model
  training and updates. *Active-active* is a liveness claim: exactly two live members, not a
  primary with a spare (`genesis_seed.model_profile`).

- **M.OS.ES (Model-OS Estimated Shortfall)** — A measured handicap on the *authoring device*:
  how far its assurance falls below what direct authorship demands. A constrained device
  (`mobile`, `ephemeral`) does not author on its own word. The covenant already allows for
  this — *"two **or three** witnesses"* — so a device carrying a shortfall must make it up
  with a **+1 attestation**: a third witness, independent of the chart+method pair. Shortfall
  `0` authors `direct`; shortfall `> 0` authors only `attested`; a shortfall that cannot be
  made up is `refused`. Same shape as the 22-threshold — **falling short is not a veto on the
  work, it is a demand that someone else cross with you.** Moses saw the land; Joshua crossed.
- **+1 attestation** — The third witness that discharges an M.OS.ES shortfall. Must be a
  different witness kind than the one the short device itself supplies; a re-signature by the
  same party is not a +1.

- **Octonion shell** — The outer governance boundary: eight non-negotiable axes (`legality` as
  the real unit, then containment, provenance, privacy, performance, reproducibility, licensing,
  governance as e1..e7). `‖b‖ ≥ 1` **halts**, and the shell has no discretion. The halting surface
  is the unit sphere in `𝕆 ≅ ℝ⁸` — that is `S⁷`, the **fiber** of the octonionic Hopf fibration
  `S⁷ → S¹⁵ → S⁸`. Governance is therefore attached over *every* point of the base, not a region
  you can stand outside of. See `docs/cognitive-fibrations.md`.
- **Evaluation order** — The recorded sequence in which the eight boundary axes were evaluated.
  Required and must be a complete permutation: octonions are non-associative, so `S⁷` is not a
  group and boundary constraints do **not** compose associatively — order can change the verdict,
  and an unrecorded order is not replayable.

- **The braid** — Four spaces (atzilut → beriah → yetzirah → assiah), five phases
  (**YHShVH**: yod-heh-shin-**vav**-heh), twelve contiguous steps `T0..T11`, and the 343-trit
  surface (7 × 49 = 7³). Counts are the contract; enforced by `tools/genesis_braid.py`.
- **Vav** — The fourth phase; the letter means *hook*. It is the connector/bridge phase. Renders
  that dropped it also dropped its steps — the join vanishing is how the braid silently loses its
  bridge. See `docs/genesis-braid.md`.
- **Carry (the goose)** — Advancement you did not walk. On the board a goose doubles your throw;
  21 and 22 are walked but **23 can only be carried**. The estate's forms are the +1 attestation
  (M.OS.ES) and Guard Goose. **A carry chain must be capped** — uncapped, it overshoots the goal
  and lands exactly on the restart square.

- **Initiation (the rename)** — A name change as a governed event: a letter inserted, swapped, or
  dropped. Abram→Abraham (heh in), Sarai→Sarah (yod for heh), Hoshea→**Ye**hoshua (yod added **by
  Moses**, Num 13:16), YHVH→YH**Sh**VH (shin set in — the braid's own five phases). **ADMN = Adam-N**
  is this operation applied to the naming space itself. It is the oldest form of the +1 attestation:
  the one who fell short adds a letter so another can cross.
- **You cannot rename yourself across a threshold** — An initiation carrying `enables_threshold`
  requires an attestor distinct from the subject. Hoshea did not add his own yod. Self-attested
  passage is refused for the same reason a re-signature by the same party is not a +1 (M.OS.ES).
- **AD4M** — A *third-party* project (Coasys: Agents/Languages/Perspectives). **Not** ADMN. Keep the
  names firewalled; they are unrelated.

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
