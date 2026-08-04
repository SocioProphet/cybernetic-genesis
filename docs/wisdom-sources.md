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

## Tamanend: the king made by those who displaced him

**Tamanend** (c. 1625–1701), Chief of Chiefs of the **Turtle clan** of the Lenni-Lenape, whose name
means *"the Affable"*, treated with William Penn in the Delaware Valley.

After his death, the colonists **who had displaced his people** raised him up as **"Saint Tammany"**
and **"King Tammany"** — they wanted a native patron saint for a new American identity, and took
one. His feast was fixed on **May 1**, displacing European May Day; Washington, Adams and Patrick
Henry attended the festivities. The societies formed in his name became **Tammany Hall**.

**No prophecy of his return is attested.** The "return of the king" is not a Lenape tradition — it
is a **reception**: a name lifted from the people it belonged to and given an authority they never
granted. Saying that plainly is the entire value of the entry, and it is the same failure the
witness rules refuse:

> **Adoption is not consent, and veneration is not attribution.** Authority must be traced to its
> source, never inherited by acclamation.

## The Black Hills: a return that is promised, and a boundary that is asked for

**White Buffalo Calf Woman** (*Ptesáŋwiŋ*) came to the Lakota in the sacred **Black Hills**
(*Ȟe Sápa*) — two scouts saw her approaching — brought the sacred pipe, and **promised to return**.
Before departing she **rolled upon the ground four times, changing colour each time**, and
disappeared. The birth of a white buffalo calf is held as her sign.

It belongs in this register because it is a **return-prophecy** standing beside the others here, and
because the shape rhymes: what is promised is not a resumption of what was, but a restoration
conditional on how people have kept faith.

**And it stops there, on purpose.** This is living sacred tradition whose custodians have **publicly
objected to its appropriation**. So the entry is **referenced and not operationalised** — it is
bound to **no mechanism in this estate**, and `tools/legend_registry.py` *enforces* that: an entry
carrying a `boundary` source and a mechanism is a registry error.

> **Documenting a boundary is itself a design act.** The registry can hold an entry whose correct
> implementation is to implement nothing — and can refuse the drift where such an entry quietly
> grows an implementation later.

**A gap, recorded as a gap:** "four crows" could not be verified. The attested four is the **four
rolls and four colours**, not crows. If a source turns up it can be added properly.

## The Walking Purchase: the fraud was in the instrument

In **1737** **Thomas Penn** — William's son, proprietor nineteen years after his father's death —
produced a claimed *lost* deed of **1686** ceding land as far as a man could **walk in a day and a
half**. The Lenape understood a walk.

Penn hired the three fastest men in the colony — **Edward Marshall, James Yeates, Solomon
Jennings** — offered a prize to whoever covered the most ground, and had **the path cleared in
advance**. About **1,200 square miles** were taken. **Nutimus** and other Lenape leaders protested
precisely this: that the path had been artificially cleared, and that the pace was not the customary
traverse the agreement assumed.

> **The terms were kept and the measure was rigged.**

A contract adjudicated by a measurement is only as honest as its instrument — and here the
instrument was **supplied, paid and prepared by one party to the agreement**. There was no
independent party to the measure. That is the witness rule violated in a land treaty: the measurer's
**origin and authority both came from the interested side.**

It is a contract settled by **feet**, and it is why this estate recomputes rather than trusts:
`tools/octonion_boundary.py` recomputes a declared norm from its axes and refuses a mismatch,
because *a self-reported measurement is an instrument, and instruments lie.*

## Penn the lawgiver, and the son who used his name

Jefferson, in **1825**, called William Penn *"the greatest lawgiver the world has produced, being
the first, in either ancient or modern times who has laid the foundation of government in the pure
and unadulterated principles of peace, reason, and right."* Penn named **Bucks County** in 1682 for
**Buckinghamshire**, his family's home in England.

And the Walking Purchase was executed by his **son Thomas**, in 1737, **nineteen years after
William's death**, on a deed attributed to the father's era. The father's name carried the credit;
the son's runners took the land.

> **A venerated name is not a warrant, and inherited authority is the weakest kind.**

Both things are true and neither cancels the other. Authority attaches to the act and the actor,
never to the surname — which is why an authority chain must be **traced**, not assumed.

*Two gaps:* a *"greatest lawgiver **since Moses**"* formulation was not found — Jefferson's attested
wording is *"the greatest lawgiver the world has produced."* And a *"king's land"* derivation for
Buckingham was not verified; the attested derivation is the Penn family's Buckinghamshire.

## Pisgah in Pennsylvania: the place named for seeing and not entering

**Pisgah** is the summit from which Moses viewed the promised land **and did not enter it**
(Deut 34:1–3).

Central Pennsylvania has a **Mount Pisgah Altar** — a stone altar on **Shade Mountain, Snyder
County**, at about 2,000 feet, looking out over the valley. It was built by **Robert Cryan** of
Beaver Springs, with **Wilmer Shank** doing the stonework, **May–October 1979**, dedicated June
1980, and it is used for Easter sunrise service. **It is modern, not ancient, and the people who
built it are known by name.**

> **A place is named for the vantage, not the crossing.**

That viewpoints keep getting called Pisgah — repeatedly, by people who never met — says the
shortfall at the threshold is the part worth **marking**, not the part to hide. Name the boundary
you stopped at; it serves whoever comes next better than a claim of arrival.

*Two gaps:* whether this altar was built **unhewn / without iron tools** is **not attested** — the
sources describe concrete and mountain stone. The unhewn-altar law itself is real and citable
(**Ex 20:25** — *"if thou lift up thy tool upon it, thou hast polluted it"* — **Deut 27:5–6**,
**Josh 8:31**), but no *ancient* unhewn altar in central PA was verified.

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


## The feet: a guarantor that cannot vouch for you

> **"The feet of a person are responsible for him; to the place where he is in demand, there they
> lead him."** — Babylonian Talmud, *Sukkah* 53a

Solomon sees the Angel of Death grieving, and learns he has been sent for two of his scribes,
Elihoreph and Ahijah. Solomon sends them away to **Luz** — the city where death has no dominion.
*"When they arrived at the district of Luz, they died."* The next day the Angel is happy: they were
wanted **in that very place**. The flight was the itinerary.

The Aramaic is **`arevin`** — not merely "responsible" but **guarantors, sureties**: the ones who
stand for you and make good on the obligation. And that is the same office as the **+1**. Which
makes the maxim say something precise, and something the whole pack turns on:

> **A man's feet are his guarantors — and that is exactly why they cannot be his +1.**

A guarantor must be **independent of the subject**. Your feet are not. They are yours; their
authority is entirely derived from you. So by Sophia's rule they are the textbook self-attestation
case: origin *and* authority both descending from the one they would vouch for. They can carry you.
They cannot **witness** for you.

That is why the guarantee is real but bounded:

- **Feet guarantee delivery.** Sukkah's scribes could not outwalk their appointment; the routing
  meant to save them performed it. You will arrive somewhere, and your own effort decides that.
- **Feet do not guarantee crossing.** Delivery to the threshold is not entry. Moses walks to Nebo
  and sees; he does not enter. 21 and 22 are walked; **23 can only be carried.**

### And Ahasuerus is the same law with the sign flipped

The Wandering Jew is condemned to walk **until the Second Coming** — feet that carry and never
deliver. Where Sukkah shows a guarantee you cannot escape, the legend shows the **guarantee
suspended**: the one man whose feet are no longer his guarantors.

Read together they say one thing from both sides:

> **Walking is not the agency.** In Sukkah it delivers you regardless of your intent; in the legend
> it delivers you never. Either way, arrival is not something walking achieves.

Which is precisely the goose board, where there are **no decisions at all** — you roll and you move,
and only a goose carries you past what your own throw could reach. It is also why the estate's
controls are shaped the way they are: a short device's own effort is bounded by its shortfall
(M.OS.ES), a subject cannot rename itself across a threshold, and a witness may descend from the
subject in **origin** but never in **authority**.

*Attribution note: this maxim was raised from the SocioProphet account, and is identified here as
Sukkah 53a. If the intended quote is a different one, swap the epigraph — the argument stands on the
`arevin`/guarantor reading either way.*

---

*Doctrinal source, not executable scripture. Nothing here runs — enforcement lives in `schemas/` and
`tools/`, and `tools/validate.py selftest` is what actually holds. Where this document and the code
disagree, the code ships; fix the document.*
