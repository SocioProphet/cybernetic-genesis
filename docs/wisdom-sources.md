# Wisdom sources — the legends behind the mechanisms, and the mechanisms they became

`docs/L0-genesis-covenant.md` established the practice: cite the source as **provenance for
engineering doctrine, not as executable scripture**, and keep a table mapping doctrine to mechanism.
This document does the same for the wisdom-literature and legend material the rest of the pack draws
on, and holds to the same discipline — **attested history and interpretation are marked apart**, and
every entry ends in code that runs.

## 1. The threshold: 22, and 21

The braid's `thresholds_crossed` gate demands **all 22** before the membrane opens both ways, and
refuses at **21**.

Moses is shown the land from Nebo and does not enter it (Deut 34:1–5). The shortfall is not failure
of will and not disqualification from the work — he is the one who brought them there. He simply
does not cross. **Joshua does.**

And the mechanism of that handover is a letter: at Num 13:16 **Moses renames Hoshea to Yehoshua**,
adding a *yod*. The man who cannot cross adds a letter to the name of the man who can.

→ `twin.schema.json` (the threshold rule), `initiation.schema.json`, `tools/initiation.py`.
**21 is refused with `21 is less than the minimum of 22`.**

## 2. The rename: initiation as a letter operation

| before | after | operation | attested at |
|---|---|---|---|
| Abram | Abra**ha**m | *heh* inserted | Gen 17:5 |
| Sarai | Sarah | *yod* → *heh* | Gen 17:15 |
| Hoshea | **Ye**hoshua | *yod* added, **by Moses** | Num 13:16 |
| Simon | Kephas / Peter, *rock* | renamed | John 1:42 |
| YHVH | YH**Sh**VH | *shin* set in | pentagrammaton, a Renaissance kabbalistic construction — **tradition, not scripture** |

The last row is why this pack's five phases are `yod · heh · shin · vav · heh`: the braid is named
with a name that itself underwent the operation it describes.

→ `tools/initiation.py` checks the declared operation against what actually happened to the name
(`insert` must grow it, `swap` must hold its length), and enforces the rule that falls out of the
Hoshea case: **you cannot rename yourself across a threshold.**

## 3. Sophia: origin may descend, authority may not

In the Gnostic account — *Pistis Sophia*, Askew Codex, 3rd–4th c. Coptic — Sophia is the last aeon,
and her fall is specific: she **emanates alone**, without her syzygy. Acting alone *is* the fall.
Therefore she cannot ascend alone either; she repents from the chaos and is **raised**.

Her raiser is **brought forth from below and sent from above** — her son, standing as her father.
That paradox is the load-bearing part, because it separates two things that look alike:

> **Origin may descend from the subject. Authority may not.**

Distinctness of identity is not independence. A witness derived from the subject is fine; a witness
whose *authority* comes from the subject is the subject wearing another name.

*(Michael as the guardian who contends is his own thread — Jude 9 has him disputing over the body of
Moses, the guardian attesting for the one who fell short. Dan 10:13 and 12:1 give him as the prince
who stands. The identification of Sophia's raiser **with** Michael is this estate's reading, not a
claim about the Coptic text.)*

→ `tools/witness_independence.py`: no witness may draw authority from the subject it witnesses, nor
from the other witness. **A distant shared root is allowed** — two attestations under one
organisational CA are still two attestations, and demanding disjoint chains to the top would refuse
every real PKI. The defect is proximate.

## 4. The goose: the carry

The **Game of the Goose** (*Gioco dell'Oca*, *Jeu de l'Oie*), documented from the late 1500s: 63
spaces — **7 × 9, the grand climacteric**, the most perilous year of a life — with geese every nine
that **carry** you further than your own throw, hazards, and an **exact-landing** rule at the goal.
No decisions; you roll and you move.

Its **Jeu du Juif Errant** variant puts **Ahasuerus** on the board — named in a 1602 German pamphlet,
called **Cartaphilus** in Matthew Paris a century earlier — condemned to walk until the Second
Coming: **motion without arrival**, which is precisely the board's losing condition.

**A distinction worth keeping:** the seed of the deathless-tarrier is **John 21:22–23** and concerns
the *beloved disciple* — **not** John the Baptist — and the evangelist explicitly corrects the rumour
that grew from it. **John the Baptist** carries a different structure: the forerunner who *returns*,
identified with Elijah (Matt 11:14; 17:12–13). One tarries, one returns. They are routinely
conflated; they are not the same mechanism.

And **Mother Goose** — *Contes de ma Mère l'Oye*, Perrault 1697 — is wisdom as the one who **hands
the tales down**, the same office Sophia holds in Prov 8. *That the wisdom-mother and the goose are
one figure is this estate's reading, not attested history*; the folkloric Berthe *la reine Pédauque*
thread is real scholarship but contested.

→ `tools/genesis_braid.py`: `carry_is_aligned` / `carry_terminus`. The arithmetic is exact and it
settled a design question: the 9-chain arrives on 63 in **six uncapped carries** (9 divides 63) while
the 5-chain overshoots to the death square (5 does not). So **a carry chain may be unbounded iff its
step divides the distance to the goal.** A cap truncates the aligned chain and fails to rescue the
misaligned one; **alignment is the control, a cap is the degraded mode.**

## 5. The one rule underneath

Every entry above is the same rule seen from a different side:

| | cannot | is carried by |
|---|---|---|
| Sophia | ascend alone — she *fell* by acting alone | one sent from above |
| Moses | cross at 21 | adds the *yod*; Joshua enters |
| Ahasuerus | arrive by walking | — he never is; that is the condemnation |
| the board | walk to 23 | the goose doubles the throw |
| M.OS.ES | author on its own word | the **+1** — a third witness |
| initiation | rename yourself across | an attestor with independent authority |

> **Falling short is not a veto on the work. It is a demand that someone else cross with you.**

## Never weaponise

The `L0` covenant's closing clause governs this document too. These sources are cited to make the
platform **auditable and fail-closed toward its own operators** — to refuse unproven, unwitnessed,
or unbounded acts. They are not a warrant for anything, not a claim about anyone's tradition, and
not a licence to bypass a human gate. Several of the readings here are this estate's own synthesis
and are labelled as such; a reader is free to take the mechanism and leave the reading.

---

*Doctrinal source, not executable scripture. Nothing here runs — enforcement lives in `schemas/` and
`tools/`, and `tools/validate.py selftest` is what actually holds. Where this document and the code
disagree, the code ships; fix the document.*
