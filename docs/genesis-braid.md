# The Genesis braid — correction record and spine

Every corrupted render of the braid failed the same way: it dropped or duplicated a member of a
set whose size is fixed. A diagram is a witness, and a witness that miscounts is a false witness.
So the counts now live in `tools/genesis_braid.py` as arithmetic, and the diagram becomes
derivable from the spine instead of hand-drawn beside it.

## Errors found in the source renders

| Where | Error | Now refused by |
|---|---|---|
| "Four Spaces" | Listed **three** — atzilut, yetzirah, assiah. **Beriah dropped.** | `check_spaces` |
| Five-phase / 12-step | Rendered `yod·heh·heh·shin·heh` and `yod·heh·shin·heh`. **Vav missing in both.** | `check_phases` |
| 12-step braid | Titled twelve; one render showed ten (**T9, T10 absent**), another ~seven. | `check_steps` |
| 12-step braid | One render had three space-rows, not four. | `check_spaces` |
| 343-trit encoding | `A = a₀…a₃₂` — should be **a₃₄₂**. | schema `total: 343` |
| 343-trit encoding | Layers overlapped; two ran **backwards** (`a₁₄₅–a₁₂₈`, `a₂₄₁–a₂₂₃`). | `check_trit_surface` |
| 11-part table | Ten rows for "eleven parts"; **B₄ twice, B₂ and B₁₀ missing.** | (pending — needs the source part-list) |
| Klein bottle in S¹⁵ | `S¹²` labelled twice; `S¹³`/`S¹²` have no place in the tower. | `docs/cognitive-fibrations.md` |

What the renders got **right**, now pinned so it stays right: `111 = 1+10+100`, `343 = 7³`,
`777 + 111 = 888`.

## VAV — one deletion, two symptoms

`YHShVH` is yod-heh-**shin**-**vav**-heh: the Tetragrammaton with shin set in. **Vav means
"hook"** — it is the connector, the join. Two renders dropped it and repeated `heh` instead.

The same renders dropped **T9 and T10** from the twelve steps. Those two steps are the **vav
phase**. The connector was deleted from the phase list and its steps were deleted from the braid:
one deletion, two symptoms. That the two steps are absent is *observed*; that vav spans exactly
those two is a *reading* of the span, and both labels are carried as `unconfirmed: true` until
bound to the source spec. A label recovered from a corrupted render is not evidence — run
`check(braid, strict=True)` to refuse them.

## The goose: carry, and why the carry must be capped

The Game of the Goose (`Jeu de l'Oie`) is the mechanism, and its arithmetic is exact.

- **Goal 63 = 7 × 9**, geese every nine: `5, 9, 14, 18, 23, 27, 32, 36, 41, 45, 50, 54, 59`.
- **21 and 22 are plain squares. 23 is a goose.** You *walk* 21 and 22; you reach 23 only by being
  doubled. The crossing is not a step, it is a **carry** — the same principle as M.OS.ES and the
  +1 attestation: falling short is not a veto, it is a demand that someone else cross with you.
- **Exact landing.** You must hit 63 exactly; overshoot counts back from the goal. The membrane's
  `thresholds_crossed` is capped at 22 and the bidirectional rule demands ≥ 22, so it is exactly
  22 by construction — overshoot is unrepresentable.
- **THE OPTIMAL IS FORBIDDEN.** A 9 on the first throw carries `9 → 18 → 27 → 36 → 45 → 54 → 63`
  — exact arrival, first throw, no decisions. The board's own printed legend bars it: rolling 9
  first sends you to 26 or 53 instead. And the two ways of making 9 land 27 squares apart
  (`6+3 → 26`, `5+4 → 53`) — **same sum, different decomposition, different fate**, which is the
  octonion non-associativity again: magnitude is insufficient, composition is load-bearing. Both
  punishments leave you exactly **one short** of a saving square (27, 54).

- **Two chains, opposite fates — and 23 is on the fatal one.**
  `9,18,27,36,45,54 → 63` arrives exactly. `5,14,23,32,41,50,59 → 68` overshoots and bounces to
  **58, the death square.** Every fatal square sits exactly **5 above** a saving square (and 4
  below the next), and `5 + 4 = 9` — the two escapes are the two parts of the throw. **Descend
  before ascend:** from 23, down 5 to 18, and the carry then runs clean to the goal.

- **⚠️ CORRECTION — a cap is NOT the control.** An earlier draft of this document claimed `CAP(K)`
  / `H_max` is what stops the cascade. The board disproves it: the 9-chain runs **six uncapped
  carries and arrives exactly** (a cap would have truncated a legitimate ascent), while the 5-chain
  dies at seven (a cap would not save it, only relocate the failure). A cap **punishes the aligned
  chain and fails the misaligned one.**

  The real condition is arithmetic — **63 = 7 × 9**: nine divides the goal, five does not.

  > **A carry chain may be unbounded iff its step divides the distance to the goal.**

  That is *authority derived from above* — the step is anchored to the terminus rather than chosen
  locally. *Validated from below* is the exact-landing rule applied at **every hop** rather than
  only at the goal; the 5-chain fails precisely because nothing checks it until it has already
  overshot. A cap remains the honest **degraded mode**: where a chain cannot be shown aligned,
  bound it — and say that is what you are doing. See `carry_is_aligned` / `carry_terminus`.

**Guard Goose** (the goose-notes security layer — scan, classify `public→restricted`, redact,
stamp `policyRefs`, emit a receipt, and gate sync so restricted content does not leave) is the
estate's goose already built: the square that decides whether you are carried forward or stopped.
Its classification lattice is the same `public | internal | restricted` the BERESHIT catalog uses.
**Open question for that repo: does the carry have a cap?** An ungated chain of promotions has the
same overshoot property as the board.
