# Multiscript / SBS-10T — letters as semantic projections (v0.1, needs manuscript)

> **Status: home established, content thin.** The source (`0.2_Multiscript_Genesis_Framework.md`)
> is a stub — "a universal semantic alphabet layer; letters as semantic projections". This doc
> gives the idea a home in the Genesis platform and a defensible v0.1 shape, **flagged as needing
> the full manuscript** before it hardens. It is doctrine-plus-sketch, not a frozen contract.

## The idea
**SBS-10T** ("Symbol-Base-System, 10-trit") is the **alphabet layer** of the Genesis platform: a
system of **agent knowledge projection and reconstruction** in which a written **glyph** (a
letter, across scripts) is a **semantic projection of a trit-tuple** — i.e. of an ASu / balanced-
ternary structure. It sits between the ternary substrate and human-legible script:

```
trit-tuple / ASu (Ghostspace)  --project-->  Glyph (a letter in some script)  --reconstruct-->  trit-tuple / ASu
```

So the same knowledge can be **projected** to a readable multiscript form and **reconstructed**
back to its trit/ASu structure without loss — the "letters as semantic projections" claim. This
is why it is *multiscript*: many surface scripts, one ternary meaning underneath, exactly as
TritRPC keeps one canonical stream across many transports.

## Minimal shape (v0.1, see `schemas/glyph.schema.json`)
A **Glyph** carries: `glyph_id`; the `script` it renders in; the `trit_tuple` it projects (its
ternary content); an optional `asu_ref` (the Ghostspace ASu it came from); a `semantic_role`;
and a `reconstruction` note asserting the projection is invertible. Projection is lossless iff
`reconstruct(project(x)) == x` on the trit-tuple — the property a future test must enforce.

## Alignment
- **trit_tuple** ↔ semantic-serdes TritRPC balanced-ternary; a Glyph is a *rendering* of the same
  trits Genesis emits over the Q3 rail.
- **asu_ref** ↔ Ghostspace ASu / `asa-triune` — a Glyph is the legible face of an ASu.
- Projection/reconstruction ↔ Ghostspace projection/collapse.

## What's needed to harden
- The actual SBS-10T alphabet table (which glyphs ↔ which trit-tuples) from the manuscript.
- A `project`/`reconstruct` reference implementation + a lossless round-trip test (the real teeth).
- Whether "10-T" fixes tuple width at 10 trits (a specific encoding) — unconfirmed; flagged.
