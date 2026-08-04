# cybernetic-genesis

Contract baseline for the **Cybernetic agentic Genesis & Inception** platform:
a semantic-hologram base, Genesis seeds, and verified twins (Inception + K3 bridge),
governed by the **L0 dual-witness / boundary-stone** discipline.

This repo is **Phase 0**: the schema pack, shipped **first**, before any broad adapter
work. It is the frozen vocabulary and the JSON Schemas that everything downstream
consumes. Private-first.

> **Phase-0 rule (from the plan):** *Build the schema pack FIRST. Do not begin broad
> adapter work before the vocabulary and schemas are stable.*
> **Exit criteria (met):** names stop drifting, schemas validate, example objects
> compile, repo structure frozen.

## What's here

| Path | What it is |
| --- | --- |
| `glossary.md` | The frozen Phase-0 vocabulary. Names here are the contract. |
| `schemas/common.schema.json` | Shared `$defs`: `ContentHash`, `Witness(es)`, `WitnessesDualType`, `Measurement`, `Ref`. |
| `schemas/hologram.schema.json` | The semantic-hologram base object. |
| `schemas/genesis_seed.schema.json` | The seed a Twin is inceived from. |
| `schemas/twin.schema.json` | The runtime twin + fail-closed READY gate + the membrane threshold gate. |
| `schemas/twin_event_envelope.schema.json` | Canonical envelope for twin events. |
| `schemas/artifact_record.schema.json` | Dual-witnessed, boundary-stone-addressed outputs. |
| `schemas/policy_decision.schema.json` | Fail-closed verdicts (ALLOW/DENY/REQUIRE_APPROVAL). |
| `schemas/adapter_descriptor.schema.json` | Adapter contract (frozen now; built Phase 1+). |
| `schemas/inception_mount_strategy.schema.json` | Podman mount-type contract per execution context (volume/bind/tmpfs). |
| `examples/*.valid.json` | Valid sample objects (must validate). |
| `examples/*.invalid.*.json` | Fixtures that MUST be rejected (teeth). |
| `tools/validate.py` | jsonschema validator + `selftest` (valids pass, invalids fail). |
| `tools/verify_mount_strategy.py` | Mount-strategy verifier (symlink + scope teeth) + Podman `--mount` projection. |
| `docs/inception-mount-strategy.md` | The mount-type mapping, the teeth, and the Podman projection. |
| `docs/L0-genesis-covenant.md` | The source-canon doctrine the schemas enforce. |
| `.github/workflows/ci.yml` | Installs jsonschema, runs the selftest, fail-closed. |

All schemas are **JSON Schema draft 2020-12**, `additionalProperties: false`, with the
L0 primitives shared from `common.schema.json`.

## The L0 covenant (baked in, not decoration)

The schemas enforce five disciplines — see `docs/L0-genesis-covenant.md` for the full
doctrine and the verse→rule table (cited as *doctrinal source, not executable scripture*):

1. **Dual witness** — `ArtifactRecord` and world-changing `ALLOW` need ≥2 witnesses of
   different kind: a **chart** (signer) witness AND a **method** (validator) witness.
2. **Boundary stones** — `digest` / `provenance_root` must match
   `^(sha256|sha3-256):[0-9a-f]{64}$`.
3. **Weights & measures** — every metric declares `sample_size`, `snr` (or `"n/a"`), `units`.
4. **Fail-closed verdicts** — no implicit allow; a Twin is not `READY` without
   identity + policy + memory refs.
5. **Plumb-line** — `validate.py selftest` is the CI baseline; drift is caught at the gate.
6. **The threshold** — the membrane opens both ways only on a full crossing of the 22 sealed
   thresholds **and** an explicit purpose-bound opt-in. 21 is short; the Ring stack serves
   opted-in users only.

## Run the checks locally

```bash
pip install jsonschema
python tools/validate.py selftest          # valids validate, invalids rejected; exit 0
python tools/validate.py hologram.schema.json:hologram.valid.json   # one-off pair
python tools/verify_mount_strategy.py selftest   # mount-strategy teeth both ways; exit 0
make check                                  # every fail-closed gate the CI runs
```

## The 7-phase plan

- **Phase 0 — Schema pack (SHIPPED, this repo).** Glossary + schemas + fixtures + CI.
  Contract baseline consumed downstream.
- **Phase 1 — Adapters.** Bind providers/organs/surfaces via `AdapterDescriptor`.
- **Phase 2 — Genesis.** Author holograms + seeds against the frozen schemas.
- **Phase 3 — Inception + K3 bridge.** Instantiate and verify Twins (chart+method) to READY.
- **Phase 4 — Missions & organs.** Run Twins under bounded organ sets; emit envelopes.
- **Phase 5 — Policy plane.** Enforce fail-closed `PolicyDecision`s on world-changing acts.
- **Phase 6 — Federation & provenance.** Cross-peer twins with sealed `ArtifactRecord` lineage.

Phases 1–6 are tracked downstream and MUST consume the contracts frozen here.

## License

MIT © 2026 SocioProphet. See `LICENSE`.

## Integrations landed
- **Consumes semantic-serdes** (governance + truth_class; alignment gate proves a TwinEventEnvelope projects to a valid AgentMessage). No enum drift (`tools/check_enum_alignment.py` vs `vendor/semantic_serdes_canonical_enums.yaml`).
- **Genesis → TritRPC → Q3 end-to-end** (`tools/emit_tritrpc.py`): a twin event emits AS a `tritrpc_envelope` (TritPack243), and `q3_roundtrip()` proves the canonical hash survives the qutrit leg (audit doesn't fork). Uses quantum-prophet if importable, else an identity qutrit leg.
- **Multiscript / SBS-10T** alphabet layer given a home (`docs/multiscript-sbs10t.md` + `schemas/glyph.schema.json`, v0.1 sketch — needs the manuscript).

## Running runtime (Inception)
Not just schemas — a running service. `src/inception/` drives a GenesisSeed through the K3 twin lifecycle (SEEDED→VERIFYING→READY, fail-closed), emits each governed `TwinEventEnvelope` **as a `tritrpc_envelope` over the trit rail**, persists to a durable append-only log with hash-chained receipts, and supports replay + revoke (revoke closes the actuation gate).

```bash
pip install -e '.[runtime]'
PYTHONPATH=src uvicorn inception.service:app --port 8731
curl -X POST localhost:8731/twins/incept -d @examples/genesis_seed.valid.json  # -> twin READY
curl localhost:8731/twins/<twin_id>/replay   # reconstructs the lifecycle from the log
```

Read-only only: a `ReadOnlyAdapter.dry_run` returns a PLAN with **effect NONE** and is refused once the twin is revoked. No world-changing adapter runs yet (plan Phases 4-6).
