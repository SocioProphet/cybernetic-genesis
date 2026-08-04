# Cognitive Fibrations — the corrected tower, and why orientation is load-bearing

This records the geometry the octonion boundary rests on, and corrects a transposition that
appeared in the source diagrams. It is doctrine for `common.schema.json#/$defs/OctonionBoundary`
and `tools/octonion_boundary.py`.

## The four Hopf fibrations

Every Hopf fibration is built the same way from a normed division algebra `A`:

| | fiber = unit sphere **in** `A` | total = unit sphere in `A²` | base = `AP¹` |
|---|---|---|---|
| **ℝ** (dim 1) | `S⁰` | `S¹` | `S¹` |
| **ℂ** (dim 2) | `S¹` | `S³` | `S²` |
| **ℍ** (dim 4) | `S³` | `S⁷` | `S⁴` |
| **𝕆** (dim 8) | `S⁷` | `S¹⁵` | `S⁸` |

**The invariant that catches every transposition: the fiber index is always exactly one below the
base index.** `S⁰/S¹`, `S¹/S²`, `S³/S⁴`, `S⁷/S⁸`. A fiber that outranks its base is impossible —
the fiber is a sphere *inside* the algebra, the base is the projective line *over* it.

### The correction

The source diagrams wrote the quaternionic rung as `S⁴ → S⁷ → S³` and the octonionic rung as
`S⁸ → S¹⁵ → S⁷`. Both have **fiber and base transposed**. The correct forms are `S³ → S⁷ → S⁴`
and `S⁷ → S¹⁵ → S⁸`.

Two things about how that error survived, worth keeping:

1. **Dimension arithmetic cannot catch it.** `3 + 4 = 7` and `7 + 8 = 15` hold in either order.
   Only the construction fixes orientation.
2. **The only row that was right is the one where a swap is invisible** (`S⁰ → S¹ → S¹`, fiber and
   base both `S¹`). That is the signature of a systematic transposition rather than a typo.

## Why the orientation decides the governance semantics

The estate's octonion shell declares eight non-negotiable axes and halts at `‖b‖ ≥ 1`. So
`b ∈ 𝕆 ≅ ℝ⁸`, and the halting surface `‖b‖ = 1` is the unit sphere in `𝕆` — which is **`S⁷`, the
fiber** of the octonionic fibration.

That is a stronger and better claim than the transposed reading allows:

- **Governance is a fiber, not a region.** It sits over *every* point of the base. There is no
  position on the base from which you are outside it. Transposed, the shell becomes a place you
  could be beyond — exactly the wrong semantics for a boundary.
- **The tower terminates, so the eight axes are the top.** Hurwitz gives only ℝ, ℂ, ℍ, 𝕆; Adams
  (1960) proves Hopf invariant one exists only in dimensions 1, 2, 4, 8. There is no ninth axis and
  no rung above. The boundary is non-negotiable as a matter of fact, not preference.
- **Composition at the shell is non-associative.** Octonion multiplication is not associative, so
  `S⁷` is not a group and this is not a principal bundle. Boundary constraints therefore do not
  compose associatively: the order of evaluation can change the verdict. This is why
  `evaluation_order` is required and must be a complete permutation of the eight axes — without it
  the verdict is not replayable. Inside the shell, Ring-1's `U(k)` *is* associative and unitary;
  the outer shell is not. Unitary within, non-associative without.

## What the schema can and cannot enforce

JSON Schema can enforce the *shape* of the boundary — eight axes in range, a complete evaluation
order, halt-when-the-declared-norm-is-past-1. It **cannot compute a Euclidean norm**, so an object
may declare `norm: 0.2` over axes that actually norm to `1.27` and satisfy every schema check while
lying. `tools/octonion_boundary.py` recomputes it and refuses the mismatch. A self-reported
measurement is an instrument, and instruments lie.

### The fail-open bug this surfaced

The first implementation halted on `norm >= 1.0`. Landing *exactly* on the shell defeats it:

```
1/sqrt(2) on two axes  ->  0.9999999999999999   (short of 1.0 by 1.1e-16)  -> waved through
sqrt(1/2) on two axes  ->  1.0                                             -> halted
```

Two spellings of the same number, opposite governance verdicts, decided by the last bit of a
float. A control that must fail closed cannot be decided that way, so anything within
`HALT_EPSILON` (`1e-12`) of the surface is treated as **on** it. That is ~4 orders above
double-precision noise and ~9 orders below any meaningful pressure, so it swallows no real
headroom. Both spellings are pinned by test.
