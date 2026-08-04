# The stories, told properly — and why they are the same story

`docs/wisdom-sources.md` maps each source to the mechanism it governs, in a table. That table is
useful and it is also a summary, and a summary is where a story goes to be forgotten. This file
tells them.

Read it as doctrine-with-provenance, in the discipline `docs/L0-genesis-covenant.md` set: the
sources are cited for **why a mechanism is shaped the way it is**, never as executable authority.
Attested history, living tradition, and this estate's own reading are marked apart throughout.

> **Images.** The plates below are public-domain works, linked to their institutional sources with
> attribution. If these docs are ever published, **vendor them** — the estate does not reference
> external hosts at runtime (`feedback_vendor_dont_reference_external_cdn`). They are references
> here, in a repo, deliberately.

---

## 1. Moses at Pisgah — the man who brought them there and did not arrive

**Deut 34:1–5.** Moses goes up from the plains of Moab to Nebo, to the top of **Pisgah**, opposite
Jericho. God shows him the whole land — Gilead to Dan, Naphtali, Ephraim and Manasseh, all Judah to
the western sea, the Negev, the plain of the valley of Jericho, the city of palm trees, as far as
Zoar. Then: *"I have caused thee to see it with thine eyes, but thou shalt not go over thither."*
He dies there, in the land of Moab, and no one knows his grave.

Read the arc whole. This is the man who argued God down from destroying the people, who carried
them forty years, who is called the meekest man on earth and the one God spoke to face to face. He
is not disqualified. He is not punished into irrelevance. **He simply does not cross.**

And what he does instead is the part that matters here. At **Num 13:16**, sending out the scouts,
*"Moses called Hoshea the son of Nun **Yehoshua**"* — he adds a **yod** to the man's name. It is a
small thing, one letter, done in passing, and the man it is done to is the one who enters.

> The one who falls short performs the act that lets another cross.

**→ `twin.schema.json`.** `flow: bidirectional` demands `thresholds_crossed >= 22` and refuses at
21. The refusal **names what is missing** rather than downgrading the actor. Falling short is not
disqualification; it is a demand for a companion.

[*Moses Views the Holy Land*, Gustave Doré, 1866 — public domain](https://commons.wikimedia.org/wiki/File:059.Moses_Views_the_Holy_Land.jpg)

---

## 2. The renamings — initiation is a letter operation

The pattern is remarkably consistent, and it is always **one letter**.

| before | after | operation | where |
|---|---|---|---|
| Abram | Abra**h**am | a **heh** inserted | Gen 17:5 |
| Sarai | Sara**h** | a **yod** traded for a **heh** | Gen 17:15 |
| Hoshea | **Ye**hoshua | a **yod** added, **by Moses** | Num 13:16 |
| Simon | Kephas / Peter, *rock* | renamed outright | John 1:42 |

Abram is ninety-nine when it happens, and the covenant and the letter arrive together — the name
changes *at* the threshold, not before and not after. Sarai's case is the tidiest: a yod goes out
and a heh comes in, the length unchanged, the person entirely changed.

**And the pattern recurses.** `YHVH → YHShVH` — a **shin** set into the Name — is the
pentagrammaton, a Renaissance kabbalistic construction (*tradition, not scripture,* and marked so).
That is why this pack's five phases are `yod · heh · shin · vav · heh`: **the braid is named with a
name that underwent the operation the braid describes.**

**→ `tools/initiation.py`.** The declared operation must match what happened to the name — `insert`
must grow it, `swap` must hold its length. And the rule that falls straight out of Hoshea:
**you cannot rename yourself across a threshold.** Hoshea did not add his own yod.

---

## 3. Sophia — the fall is acting alone, so the rising cannot be alone either

In the Valentinian and Sethian accounts, and at length in the Coptic **Pistis Sophia** (Askew
Codex, 3rd–4th c.), Sophia is the last and lowest of the aeons of the Pleroma. Her fall is not
disobedience and it is not ignorance. **She emanates alone** — without her syzygy, her paired
consort — reaching beyond her measure by herself. What she brings forth alone is defective, and she
falls out of the fullness into the chaos.

From there she cries out. The *Pistis Sophia* gives her **thirteen repentances**, one after
another, from the deficiency. She cannot climb back. The very thing that would be required —
acting under her own power — is the thing that put her there.

She is **raised**. And her raiser is the figure the whole distinction turns on: **brought forth
from below, and sent from above** — her son, standing to her as her father.

> Origin may descend from the subject. **Authority may not.**

*(That her raiser is **Michael** specifically is this estate's reading, not a claim about the Coptic
text. Michael's own warrant is elsewhere and is real: **Jude 9**, contending with the devil over
the body of Moses — the guardian attesting for the one who fell short — and **Dan 10:13, 12:1**,
the prince who stands.)*

**→ `tools/witness_independence.py`.** No witness may draw authority from the subject it witnesses,
nor from the other witness. `Witness.origin` is unconstrained; `Witness.authority_chain` is not. A
distant shared root is fine — two attestations under one org CA are still two attestations — because
**the defect is proximate**, one party standing behind the other.

---

## 4. The Game of the Goose — a life in sixty-three squares, and no decisions

The *Gioco dell'Oca* / *Jeu de l'Oie* is documented from the late 1500s — a set sent by Francesco I
de' Medici to Philip II of Spain — and spreads across Europe with its shape fixed.

Sixty-three squares, spiralling inward. **63 = 7 × 9**, which in Renaissance reckoning is the
**grand climacteric**: the year of a life when both critical cycles fall together, held to be the
most perilous a person survives. The board's goal is the year you are least likely to reach.

Along the way: a **bridge** at 6, an **inn** at 19 where you pay and wait, a **well** at 31 where
you sit until another player frees you, a **labyrinth** at 42 that sends you back to 30, a
**prison** at 52, and **death at 58** — five short of home — which sends you back to the beginning.

And **geese every nine**: 5, 9, 14, 18, 23, 27, 32, 36, 41, 45, 50, 54, 59. Land on a goose and you
**advance again by the same throw**, and again if you land on another. The goose is the only thing
on the board that moves you further than your own roll.

You must land on 63 **exactly**. Overshoot and you count the excess backward from the goal.

**And there are no decisions.** You roll; you move. Whatever the game models, it is not skill.

### The two chains

| chain | path | outcome |
|---|---|---|
| **the 9-chain** | 9 → 18 → 27 → 36 → 45 → 54 → **63** | arrives **exactly**, six uncapped carries |
| **the 5-chain** | 5 → 14 → 23 → 32 → 41 → 50 → 59 → 68 | overshoots by five → bounces to **58, death** |

**Nine divides 63. Five does not.** That one arithmetic fact decides which chain saves and which
kills.

**21 and 22 are plain squares. 23 is a goose.** You *walk* 21 and 22. You reach 23 only by being
**doubled** — carried past what your own throw could reach. And 23 sits on the **fatal** chain.

Every square on the fatal chain is exactly **5 above** a square on the saving one, and 4 below the
next — **and 5 + 4 = 9, the throw itself**. Descend five, or ascend four. The two escapes are the
two parts of the roll.

### The optimal is forbidden

A **9 on the first throw** carries you 9 → 18 → 27 → 36 → 45 → 54 → 63: exact arrival, first throw,
no decisions. **The rules printed on the board forbid it** — a first-throw 9 is sent to 26 or 53
instead. And the two ways of making 9 land **27 squares apart** (6+3 → 26, 5+4 → 53): the same sum,
decomposed differently, is a different fate. Both punishments leave you exactly **one short** of a
saving square.

**→ `tools/genesis_braid.py`.** `carry_is_aligned(step, distance)`: a carry chain may be unbounded
**iff its step divides the distance to the goal**. Alignment is the control; a cap truncates the
good chain and does not rescue the bad one.

[*Jeu de l'Oie*, 19th c. French board — public domain](https://commons.wikimedia.org/wiki/Category:Game_of_the_Goose)

---

## 5. Ahasuerus — motion without arrival

The **Wandering Jew** enters the record with Roger of Wendover and Matthew Paris in the 13th
century as **Cartaphilus**, Pilate's doorkeeper, and is named **Ahasuerus** in a 1602 German
pamphlet. He taunts Christ on the road to Calvary and is answered: *you will walk until I return.*

Not killed. Not stopped. **Made to keep going.** His condemnation is the removal of arrival, and the
19th-century French **Jeu du Juif Errant** puts him on the goose board — where motion without
landing is precisely the losing condition.

**Two Johns, routinely conflated, and the difference matters.** The seed of the deathless-tarrier is
**John 21:22–23**, and it concerns the **beloved disciple** — *"If I will that he tarry till I come,
what is that to thee?"* — with the evangelist immediately correcting the rumour that grew from it.
**John the Baptist** carries a different structure entirely: the forerunner who *returns*, identified
with Elijah (Matt 11:14, 17:12–13). One tarries; one returns. Different men, different mechanisms.

**→ `carry_terminus()`** reports where a chain actually *ends*, not that it moved. Progress is not
arrival.

### The name-line, and a record that disagrees with itself

The legend runs through the name this estate is written under. **Seligmann Heller** (1831–1890), the
Austrian poet, published ***Ahasverus*** — an epic on the Wandering Jew in **three cantos**, Leipzig
**1866**. Germans took the legend up hard: Schubart, Lenau, Chamisso, Schlegel and Mosen all worked
it, and Andersen's own *Ahasuerus* feeds into the same stream.

**And the record does not agree on his name.** The 1911 *Britannica* calls him **Sigismund** Heller;
Wikipedia and the *Jewish Encyclopedia* have **Seligmann**. Two sources, one man, two names —
**in an entry about a man condemned to wander under a name he was given.**

Earlier still, **Jacob Heller**, a Frankfurt merchant, commissioned from **Dürer** the *Heller
Altarpiece* — the **Assumption of the Virgin**, the Apostles gathered about her **empty tomb**, 1509.
Its centre panel **burned in 1729**. What survives is Jobst Harrich's **copy**. And a *Heller* was a
coin: a small denomination named for Hall, worth almost nothing by itself.

> An identifier is not self-evidencing. Two sources naming the same person differently is a
> **conflict to record**, not a detail to smooth — and a surviving copy must say that it is one.

*(The name-line as this estate's own instance of the wanderer is Michael Heller's connection, not a
scholarly claim, and is marked so.)*

---

## 6. The feet — Sukkah 53a, and a guarantor who cannot vouch for you

Solomon sees the **Angel of Death** grieving and asks why. He has been sent for two of Solomon's
scribes, **Elihoreph and Ahijah**, and cannot reach them. So Solomon sends the two men away — to
**Luz**, the city where death has no dominion.

*"When they arrived at the district of Luz, they died."*

The next day the Angel is cheerful. They were wanted **in that very place**. And Solomon says:

> *"The feet of a person are responsible for him; to the place where he is in demand, there they
> lead him."* (Sukkah 53a)

The Aramaic is **`arevin`** — not "responsible" but **guarantors, sureties**: the parties who stand
for you and make good the obligation. **The flight was the itinerary.**

And that word is the same office as the **+1**. Which makes the maxim say something exact:

> **A man's feet are his guarantors — and that is exactly why they cannot be his witness.**

A guarantor must be **independent of the subject**. Your feet are not; their authority derives
wholly from you. They are the textbook self-attestation case. **They carry you to the threshold.
They cannot vouch for you at it.**

The other half is **Ex 3:5**, at the bush: *"Put off thy shoes from off thy feet, for the place
whereon thou standest is holy ground."* At the threshold you **uncover** the guarantor — said to
Moses, before he is sent, long before Nebo.

**→ `bearbrowser/scripts/bearbrowser-verify-bearfoot.py`.** A thing's own claim about itself is not
evidence about it; the print is checked by something that is not the browser.

---

## 7. The Walking Purchase — the terms were kept and the measure was rigged

**1737.** **Thomas Penn** — William's son, proprietor nineteen years after his father's death —
produces a claimed *lost* deed of 1686 ceding land as far as a man can **walk in a day and a half**.
The Lenape understood a walk: a customary traverse, at a customary pace, over the ground as it lies.

Penn hires the three fastest men in the colony — **Edward Marshall, James Yeates, Solomon Jennings**
— offers a prize to whoever covers the most ground, and **has the path cleared in advance**. Marshall
runs. About **1,200 square miles** are taken. **Nutimus** and other Lenape leaders protest exactly
this: that the path was artificially cleared, and that the pace was not a walk.

**Nothing in the terms was broken.** A man walked for a day and a half. **The instrument was
corrupted** — supplied, paid and prepared by one party to the agreement, with no independent party
to the measure.

> The measurer's **origin and authority both came from the interested side.** That is Sophia's rule
> violated in a land treaty.

And it is a contract settled by **feet** — the guarantor that cannot be independent, made to
adjudicate.

**→ `tools/octonion_boundary.py`** recomputes a declared norm from its axes and refuses a mismatch.
*A self-reported measurement is an instrument, and instruments lie.*

*(And the reception is its own lesson: Jefferson in 1825 called **William** Penn "the greatest
lawgiver the world has produced." The fraud was his son's, on a deed attributed to the father's era.
The father's name carried the credit; the son's runners took the land.)*

---

## 8. The horse — substituting the instrument

The Walking Purchase was settled by a walk and the fraud was that **they ran**. The horse is that
substitution's archetype: across Indo-European tradition it is the thing that crosses ground — and
worlds — faster than a person can. **Sleipnir** carries Odin between realms. The horse sacrifices —
Vedic **ashvamedha**, Roman **October Equus**, Norse **blót** — mark it as the animal set at the
boundary of what a person may reach unaided.

> **When a measure is defined by a human capacity, substituting a superior instrument voids it.**

The terms survive; the measure does not, because the agreement priced **the capacity, not the
distance**. Benchmark gaming is the same move. So is every proxy metric that gets optimised rather
than traversed.

**Foreknowledge is the limit case.** If you already know where the line falls, you do not walk to it
— you clear the path to it in advance, which is literally what was done in 1737.

*(That the horse figures human clairvoyance, and horse sacrifice its loss, is discussed explicitly
by Steiner per the author of the work this register serves; the specific GA/lecture citation is
**pending** and marked as such rather than guessed. Steiner's own related claim — GA 117, 1909, that
atavistic clairvoyance did not survive among the ancient Hebrew people and that seership must
henceforth be reached through rational thinking — is recorded in the registry, typed `tradition`,
carrying a `boundary`, and **bound to no mechanism**. Steiner's doctrines concerning peoples and
lineages are substantially and continuingly contested; recording a doctrine and adopting it are
different acts.)*

---

## 9. Lazarus — Martha measures, Mary raises

**John 11.** Lazarus is sick at Bethany and his sisters send word: *"Lord, he whom thou lovest is
sick."* And the response is the detail everyone skips: **he stayed two more days where he was.**

By the time he comes, Lazarus has been in the tomb four days. **Martha** goes out to meet him on the
road. She reasons: *"Lord, if thou hadst been here, my brother had not died. But I know that even
now, whatsoever thou wilt ask of God, God will give it thee."* She has the theological exchange —
*"I am the resurrection and the life"* — and later, at the tomb, she makes **the measurement**:
*"Lord, by this time he stinketh: for he hath been dead four days."* Observed. Dated. Quantified.

**Mary** stays in the house until she is called. When she comes she falls at his feet and **weeps**.
And then: *"When Jesus therefore saw her weeping, and the Jews also weeping which came with her, he
groaned in the spirit, and was troubled."* **Jesus wept.** *Then*: **"Where have ye laid him?"**

> **Martha is detection. Mary is escalation.**
> The report was accurate and complete, and it was followed by a two-day delay. What moved the
> action was grief that landed on someone.

**→ `tools/ci_liveness_sweep.py` is Martha; `tools/ci_liveness_escalate.py` is Mary.** The sweep
measures and prints. The escalation files a durable, addressed issue that **gets louder with the
age of the silence** and **closes itself when the pipeline is green again** — the mourning ends at
the raising.

[*The Raising of Lazarus*, Rembrandt, c. 1630–32 — public domain](https://commons.wikimedia.org/wiki/File:Rembrandt_Harmenszoon_van_Rijn_-_The_Raising_of_Lazarus,_c._1630-1632.jpg)

---

## 10. Hellebore — how you tell dead from dormant

**Melampus**, the seer-physician, cures the daughters of **Proetus of Argos** of the madness
Dionysus sent them — they had run wild, and he brings them back with a brew of **hellebore**. His
name is **melas** + **pous**: **"black-foot."** The old name for the plant, **Melampodium**, is his.

*(The etymology of `Helleborus` itself is genuinely contested — `heleîn` "to injure" + `borá` "food",
or `álkē` "fawn" + `borós`, "food for fawns"; Graves (1948) proposed "food of Helle." Scholars do
not agree, and the doc should not pretend they do.)*

Two things make it the right emblem here.

**It is poison and cure in one substance**, separated only by dose. The measure decides which it is
— which is the Walking Purchase again, from the other side.

**And it flowers in the dead of winter.** The Christmas rose, *Helleborus niger*, blooms in
December and January, in snow, when the whole garden looks finished. **A winter garden and a dead
garden look identical.** The bloom is how you tell the ground is alive.

That is exactly the problem the liveness sweep solves. A repo emitting no signal may be **dormant**
— manual, between phases, nobody pushing — or it may be **dead**, and from outside the two are
indistinguishable. The estate spent five weeks unable to tell.

> Calling dormant things dead is how a checker gets muted.
> Calling dead things dormant is how five weeks pass.

**→ the verdicts.** `UNUSED` is dormant, by design, and **never alarms**. `DEAD` never once
succeeded. `SILENT` is the deceptive middle: running, therefore apparently alive, and never winning.
`UNUSED` exists because this tool's first draft flagged three never-invoked dispatch workflows as
dead — it made exactly the first mistake.

[*Helleborus*, Sibthorp, *Flora Graeca* vol. 6, c. 1840s — public domain](https://commons.wikimedia.org/wiki/Category:Flora_Graeca)

---

## And why it is one story

Every entry above is the same shape seen from a different side. Not by analogy — by **structure**:

| | cannot | what carries them |
|---|---|---|
| **Moses** | cross at 21 | adds the yod; **Joshua** enters |
| **Sophia** | ascend — she *fell by* acting alone | one **sent from above** |
| **Ahasuerus** | arrive by walking | *nothing* — that is the condemnation |
| **the board** | walk to 23 | the **goose** doubles the throw |
| **the scribes** | outwalk the appointment | their feet deliver them **to** it |
| **a short device** | author on its own word | the **+1**, a third witness |
| **Lazarus** | rise | Martha reports; **Mary** weeps; he is called out |

> **Falling short is not a veto on the work. It is a demand that someone else cross with you.**

And the second law, which is the first one turned around:

> **Nothing may vouch for itself.** Not your feet, not your own name, not a party's own measurer,
> not a witness the subject authorised, not a browser's own claim about its print, and not a
> pipeline's own silence.

Every control in this estate is one of those two sentences, made refusable.

---

*Doctrinal source, not executable scripture. Nothing here runs; enforcement lives in `schemas/` and
`tools/`, and `tools/validate.py selftest` is what actually holds. Where this document and the code
disagree, the code ships — fix the document.*
