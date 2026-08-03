# L0 Genesis Covenant — the source-canon discipline the schemas enforce

This document is the **doctrinal source** for the Phase-0 schema pack. It records *why*
the schemas carry the constraints they carry. The verse references below are cited as a
**source of engineering doctrine and provenance — not as executable scripture**. Nothing
here runs; the enforcement lives in `schemas/*.schema.json` and `tools/validate.py`.

The through-line: a governed system must be **honest about what it knows, immutable about
what it has recorded, and closed when unsure**. Five disciplines make that concrete.

## The disciplines

### 1. Dual witness — a matter is established by two
A single attestation is not enough to make a world-changing claim true. Every
`ArtifactRecord`, and every world-changing `PolicyDecision` = `ALLOW`, must carry **two
witnesses of different kind**: a **chart** witness (a signer / identity attestation) AND
a **method** witness (a validator / verification attestation). One signer alone, or two
validators alone, does not establish the matter.
Enforced by: `common.schema.json#/$defs/WitnessesDualType` (`minItems: 2` + `contains`
chart + `contains` method), required on `ArtifactRecord.witnesses`.

### 2. Boundary stones — do not move the landmark
Content-address fields are immutable boundary markers. `digest` and `provenance_root`
must be real content hashes: `^(sha256|sha3-256):[0-9a-f]{64}$`. A record whose boundary
stone is malformed is rejected — you cannot quietly re-draw the line later.
Enforced by: `common.schema.json#/$defs/ContentHash`.

### 3. Weights and measures — a just weight states its terms
No naked numbers. Any metric/measurement declares `sample_size`, `snr` (a number, or an
explicit `"n/a"` when signal-to-noise does not apply), and `units`. A measurement that
hides its sample size or units is a false balance.
Enforced by: `common.schema.json#/$defs/Measurement`, used wherever metrics appear.

### 4. Fail-closed verdicts — absence of proof is denial
The policy plane's verdict enum is `ALLOW | DENY | REQUIRE_APPROVAL`; there is no
implicit allow. A `Twin` MUST NOT reach `READY` without `identity` + `policy_refs` +
`memory_refs` present and non-empty — it cannot go live blind. When in doubt, the system
denies or escalates.
Enforced by: `twin.schema.json` (`allOf` / `if READY then required + non-empty`),
`policy_decision.schema.json` (verdict enum + world-changing-ALLOW dual-witness gate).

### 5. Plumb-line — measure against the line, always
The schemas are the plumb-line; `tools/validate.py selftest` is the act of holding every
object against it in CI. Valids must validate and invalids must be rejected — teeth both
ways. Drift in names or shapes is caught at the gate, not discovered in production.
Enforced by: `.github/workflows/ci.yml` running the selftest on every push/PR.

## Never weaponize
This covenant governs **restraint**, not aggression. The disciplines exist to make the
platform auditable and fail-closed toward its own operators — to refuse unproven,
unwitnessed, or unbounded acts. They are not to be repurposed as offensive capability,
surveillance beyond declared purpose, or a pretext to bypass a human approval gate. A
Twin's power is bounded by its seed, its policy envelope, and these witnesses; that
boundary is the point.

## Verse → rule (condensed; doctrinal source, not executable scripture)

| Source (doctrine)        | Principle             | Schema rule enforced                                             |
| ------------------------ | --------------------- | --------------------------------------------------------------- |
| Deut 19:15               | Two-or-three witness  | `witnesses[]` `minItems: 2`, chart + method (`WitnessesDualType`) |
| Deut 19:14 / Prov 22:28  | Do not move landmarks | `ContentHash` on `digest` / `provenance_root`                    |
| Lev 19:35-36 / Prov 11:1 | Just weights & measures | `Measurement` requires `sample_size`, `snr`, `units`           |
| (fail-closed governance) | No implicit allow     | verdict enum; `Twin` READY requires identity+policy+memory       |
| Amos 7:7-8               | The plumb-line        | `validate.py selftest` as CI baseline                            |
| (never-weaponize)        | Restraint, not force  | bounded by seed + policy envelope + witnesses                    |

The rows are a **map from doctrine to mechanism**. The mechanism is the schema; the
doctrine is why. If a future change loosens a rule, it must be argued against this table.
