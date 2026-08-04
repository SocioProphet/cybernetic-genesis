# Legend registry — narrative, principle, mechanism

The narrative -> mechanism registry. Each entry carries a NARRATIVE (the explained story), a DESIGN_PRINCIPLE (the philosophy it yields), typed SOURCES (attested / tradition / interpretation / public-general / gap / boundary), the MECHANISM that implements it, page-anchored doc locations, and RELATED edges. The narrative and principle are separate fields precisely so retrieval can return either one alone.

*Generated from `registry/legends.v1.json` by `tools/legend_registry.py --emit`. Do not hand-edit; edit the registry.*

## The threshold: 22, and 21

`id: moses-threshold`

### Narrative

Moses is shown the land from Nebo and does not enter it. The shortfall is not failure of will and not disqualification from the work — he is the one who brought them there. He simply does not cross. Joshua does. And the mechanism of the handover is a letter: Moses renames Hoshea to Yehoshua, adding a yod. The man who cannot cross adds a letter to the name of the man who can.

### Design principle

Falling short is not a veto on the work. It is a demand that someone else cross with you. A threshold gate must therefore refuse quietly and name what is missing, never silently downgrade the actor.

### Sources

- **attested** — Deut 34:1-5 (Nebo)
- **attested** — Num 13:16 (Moses renames Hoshea to Yehoshua)

### Mechanism

`cybernetic-genesis` → `schemas/twin.schema.json`

> flow=bidirectional requires thresholds_crossed >= 22 AND consent.state=opted_in; 21 is refused

### Related

`initiation-rename`, `goose-carry`, `mosis-shortfall`

## The rename: initiation as a letter operation

`id: initiation-rename`

### Narrative

Renaming on initiation is a letter operation on a name: Abram gains a heh, Sarai trades a yod for a heh, Hoshea gains a yod — added by Moses — and Simon becomes Kephas, rock. The pentagrammaton sets a shin into the Name, which is why this pack's five phases are yod-heh-shin-vav-heh: the braid is named with a name that underwent the operation it describes.

### Design principle

You cannot rename yourself across a threshold. An initiation that buys passage requires an attestor distinct from the subject, and the declared operation must match what actually happened to the name.

### Sources

- **attested** — Gen 17:5; Gen 17:15; Num 13:16; John 1:42
- **tradition** — YHVH -> YHShVH is a Renaissance kabbalistic construction, not scripture

### Mechanism

`cybernetic-genesis` → `tools/initiation.py`

> enables_threshold requires an attestor != subject; insert must grow the name, swap must hold its length

### Related

`moses-threshold`, `sophia-authority`

## Sophia: origin may descend, authority may not

`id: sophia-authority`

### Narrative

Sophia's fall is specific — she emanates alone, without her syzygy. Acting alone IS the fall, so she cannot ascend alone either; she is raised. Her raiser is brought forth from below and sent from above: her son, standing as her father.

### Design principle

Distinctness of identity is not independence. A witness may descend from the subject in origin but never in authority — otherwise the second witness is the subject wearing another name. A distant shared root is fine; the defect is proximate.

### Sources

- **attested** — Pistis Sophia, Askew Codex, 3rd-4th c. Coptic
- **attested** — Jude 9 (Michael contends over the body of Moses); Dan 10:13, 12:1
- **interpretation** — Identifying Sophia's raiser WITH Michael is this estate's reading, not a claim about the Coptic text

### Mechanism

`cybernetic-genesis` → `tools/witness_independence.py`

> no witness may draw authority from the subject it witnesses, nor from the other witness; unstated authority is refused

### Related

`initiation-rename`, `feet-guarantors`, `quorum-independence`

## The goose: the carry, and why alignment beats a cap

`id: goose-carry`

### Narrative

The Game of the Goose is 63 spaces — 7x9, the grand climacteric, the most perilous year of a life — with geese every nine that carry you further than your own throw, and an exact-landing rule at the goal. There are no decisions; you roll and you move. The 9-chain arrives on 63 exactly in six uncapped carries; the 5-chain overshoots to 58, the death square. 21 and 22 are walked. 23 can only be carried.

### Design principle

A carry chain may be unbounded iff its step divides the distance to the goal. Alignment is the control; a cap truncates the aligned chain and fails to rescue the misaligned one, so a cap is the honest degraded mode and nothing more.

### Sources

- **attested** — Gioco dell'Oca / Jeu de l'Oie, documented from the late 1500s; rules printed on the boards themselves
- **attested** — Jeu du Juif Errant, 19th-c. French variant; Ahasuerus named in a 1602 German pamphlet, Cartaphilus in Matthew Paris

### Mechanism

`cybernetic-genesis` → `tools/genesis_braid.py`

> carry_is_aligned(step, distance): a chain needs no cap iff distance % step == 0

### Related

`moses-threshold`, `wanderer-no-arrival`, `guard-goose-gate`

## The wanderer: motion without arrival

`id: wanderer-no-arrival`

### Narrative

Ahasuerus is condemned to walk until the Second Coming — feet that carry and never deliver. That is the goose board's own losing condition. The seed of the structure is John 21:22-23, and it concerns the BELOVED DISCIPLE, not the Baptist; the evangelist corrects the rumour himself. John the Baptist carries a different structure: the forerunner who returns, identified with Elijah. One tarries, one returns.

### Design principle

Progress is not arrival. A process that advances forever without an exact-landing condition has not succeeded; it has only failed to stop.

### Sources

- **attested** — John 21:22-23; Matt 11:14, 17:12-13
- **attested** — Kurtze Beschreibung und Erzaehlung von einem Juden mit Namen Ahasverus, 1602

### Mechanism

`cybernetic-genesis` → `tools/genesis_braid.py`

> carry_terminus() reports where an unaligned chain actually ends, rather than that it moved

### Related

`goose-carry`, `feet-guarantors`

## The feet: a guarantor that cannot vouch for you

`id: feet-guarantors`

### Narrative

Solomon, learning the Angel of Death has been sent for his scribes, dispatches them to Luz where death has no dominion. They arrive, and die — they were wanted in that very place. The flight was the itinerary. The Aramaic arevin means guarantors: your feet stand surety and will deliver you. And at the threshold you uncover them (Ex 3:5, Moses at the bush, before he is sent).

### Design principle

Your feet are your guarantors, and that is exactly why they cannot be your witness. A thing's own claim about itself is not evidence about it: feet guarantee delivery to the threshold, never crossing it.

### Sources

- **attested** — Babylonian Talmud, Sukkah 53a — <https://www.sefaria.org/Sukkah.53a>
- **attested** — Ex 3:5

### Mechanism

`bearbrowser` → `scripts/bearbrowser-verify-bearfoot.py`

> the print is checked by something that is not the browser

### Related

`sophia-authority`, `wanderer-no-arrival`, `bearfoot-uniformity`

## Bearfoot: the print must be the same print

`id: bearfoot-uniformity`

### Narrative

A bear is plantigrade — whole sole, heel to toe, as we walk — so its hind track resembles a barefoot human print. That anatomical fact is why peoples across the northern hemisphere independently name the bear kin, the one who walks like a man. And the Lenape Mesingw, guardian of the game animals, is impersonated in the bear's own skin: a coat of bear skins to the toes, bearskin stockings, and the skin of the bear's head fastened to the mask with the ears projecting. The track makes the bear look like a man; the garb makes a man look like the bear. The kinship is not noticed, it is worn.

### Design principle

A print that distinguishes you is a print that betrays you. Anti-fingerprinting does not hide the track, it makes every track the same track — so profiles that flatten their print must flatten it identically, or the disagreement is itself a distinguishing bit.

### Sources

- **attested** — M. R. Harrington, Religion and Ceremonies of the Lenape (1921), pp. 34, 41 — <https://www.gutenberg.org/ebooks/72988>
- **attested** — David Brainerd's account of 1745, quoted in Harrington p.41
- **public-general** — Plantigrade gait and the resulting kinship motif belong to no single tradition
- **gap** — A Lenape 'returning god' tied to the bear could NOT be verified and is deliberately not supplied
- **gap** — The garb being shed during the ceremony is NOT attested in Harrington
- **gap** — A first-bear-hunt coming-of-age legend is NOT attested to the Lenape in what could be checked; the motif itself is widespread

### Mechanism

`bearbrowser` → `scripts/bearbrowser-verify-bearfoot.py`

> every profile claiming the bearfoot property must set every print-surface pref, and agree with its siblings on the value

### Related

`feet-guarantors`, `tamanend-reception`

## Tamanend: the king made by those who displaced him

`id: tamanend-reception`

### Narrative

Tamanend (c.1625-1701), Chief of Chiefs of the Turtle clan of the Lenni-Lenape, whose name means 'the Affable', treated with William Penn. After his death the colonists who had displaced his people elevated him to 'Saint Tammany' and 'King Tammany' — they wanted a native patron saint for a new American identity. His feast was set on May 1, displacing European May Day; Washington, Adams and Patrick Henry attended. The societies formed in his name became Tammany Hall.

### Design principle

Adoption is not consent, and veneration is not attribution. A name taken up by those it did not belong to acquires an authority its source never granted — which is exactly the provenance failure the witness rules refuse. NO PROPHECY OF HIS RETURN IS ATTESTED; the 'king' is a reception phenomenon, and saying so plainly is the point.

### Sources

- **attested** — Tamanend, c.1625-1701, Turtle clan, treated with William Penn — <https://en.wikipedia.org/wiki/Tamanend>
- **attested** — St. Tammany Day, May 1 — <https://www.delawarenation-nsn.gov/observing-st-tammany-day-friday-april-30-2021-2-2-2/>
- **gap** — No legend or prophecy of Tamanend's RETURN was found; the return-of-the-king framing is reception, not tradition

### Mechanism

`cybernetic-genesis` → `tools/witness_independence.py`

> authority must be traced to its source, not inherited by acclamation

### Related

`sophia-authority`, `bearfoot-uniformity`, `black-hills-return`

## The Black Hills: a return that is promised, and a boundary that is asked for

`id: black-hills-return`

### Narrative

White Buffalo Calf Woman (Ptesanwin) came to the Lakota in the sacred Black Hills — two scouts saw her approaching — brought the sacred pipe, and promised to return. Before departing she rolled upon the ground FOUR times, changing colour each time, and disappeared. The birth of a white buffalo calf is held as her sign.

### Design principle

REFERENCED, NOT OPERATIONALISED. This is living sacred tradition whose custodians have publicly objected to its appropriation, so it is recorded here as a documented return-prophecy alongside the others and is deliberately bound to NO mechanism in this estate. Documenting a boundary is itself a design act: the registry can hold an entry whose correct implementation is to implement nothing.

### Sources

- **attested** — White Buffalo Calf Woman brought the cannupa and promised to return; four rolls, four colours; the Black Hills (He Sapa) of South Dakota
- **gap** — 'Four crows' could NOT be verified. The attested four is the four rolls and four colours, not crows.
- **boundary** — Lakota custodians have publicly objected to appropriation of their spirituality; this entry is reference-only and binds to no code

### Mechanism

**None, deliberately.** This entry is referenced and not operationalised.

### Related

`tamanend-reception`, `bearfoot-uniformity`

## M.OS.ES: the shortfall that demands a companion

`id: mosis-shortfall`

### Narrative

A constrained device does not author on its own word. The covenant already made room for it: 'two OR THREE witnesses'. Two is the floor for a device that meets the bar; a device carrying a shortfall must reach three — the chart+method pair plus a +1 that makes up the difference.

### Design principle

Estimated shortfall handicaps direct authorship rather than forbidding the work. The +1 must be a different witness kind than the one the short device supplies; a re-signature by the same party is not a +1.

### Sources

- **attested** — Deut 19:15 (two or three witnesses)
- **interpretation** — M.OS.ES as Model-OS Estimated Shortfall is this estate's coinage

### Mechanism

`cybernetic-genesis` → `schemas/common.schema.json`

> estimated_shortfall > 0 forces authoring in {attested, refused}; attested requires plus_one; an ArtifactRecord from a short device needs 3 witnesses

### Related

`moses-threshold`, `sophia-authority`, `feet-guarantors`

## Guard Goose: the square that decides carried-forward or stopped

`id: guard-goose-gate`

### Narrative

On the board a goose is the square that decides whether you are carried forward or stopped. Guard Goose scans, classifies, redacts and stamps a marker — and until the gate was built, nothing refused. It labelled, and a label is not a control.

### Design principle

An unscanned artifact does not egress: absence of a classification is not permission, because Public means 'no detector fired', not 'reviewed and safe'. And nothing egresses above its destination's ceiling, which is a property of the destination binding rather than the protocol it speaks.

### Sources

- **interpretation** — Guard Goose as the board's goose is this estate's reading of its own component

### Mechanism

`goose-notes` → `crates/goose-guard/src/gate.rs`

> check_egress refuses an unscanned artifact and anything above the ceiling; GuardedAdapter is the only push path

### Related

`goose-carry`, `feet-guarantors`

## A quorum of one, where the one is the requester

`id: quorum-independence`

### Narrative

Counting signatures is not counting voices. A gateway gated its highest-danger operations on the NUMBER of quorum signatures and never asked who signed, so the actor requesting a grant could supply their own signature as the human quorum.

### Design principle

An approver must be independent of the subject, not merely distinct in name — and an unidentified signer is refused rather than skipped, because absence of identity cannot be shown independent.

### Sources

- **interpretation** — The generalisation of Sophia's rule to quorum is this estate's

### Mechanism

`prophet-platform` → `apps/compute-gateway/src/compute_gateway/grants.py`

> _check_quorum_independence refuses duplicate signers and the requester signing their own grant

### Related

`sophia-authority`, `mosis-shortfall`

## The Walking Purchase: the fraud was in the instrument

`id: walking-purchase-instrument`

### Narrative

In 1737 Thomas Penn — William's son, proprietor nineteen years after his father's death — produced a claimed 'lost' deed of 1686 ceding land as far as a man could walk in a day and a half. The Lenape understood a walk. Penn hired the three fastest men in the colony, Edward Marshall, James Yeates and Solomon Jennings, offered a prize to whoever covered the most ground, and had the path CLEARED IN ADVANCE. About 1,200 square miles were taken. Nutimus and other Lenape leaders protested precisely this: that the path had been artificially cleared and the pace was not the customary traverse the agreement assumed.

### Design principle

THE TERMS WERE KEPT AND THE MEASURE WAS RIGGED. A contract adjudicated by a measurement is only as honest as the instrument, and here the instrument was supplied, paid and prepared by one party to the agreement. That is the witness rule violated in a land treaty: the measurer's origin AND authority both came from the interested side, with no independent party to the measure. It is why a self-reported measurement is refused, why a signer must be independent of the subject, and why the estate recomputes rather than trusts a declared value.

### Sources

- **attested** — Walking Purchase, 25 August 1737; Thomas Penn (1702-1775); runners Marshall, Yeates, Jennings; pre-cleared path; ~1,200 sq mi — <https://www.britannica.com/event/Walking-Purchase>
- **attested** — Nutimus and other Lenape leaders protested the cleared path and the non-customary pace — <https://philadelphiaencyclopedia.org/essays/walking-purchase/>
- **attested** — The 1686 deed relied upon was itself of contested authenticity
- **interpretation** — Reading it as an INSTRUMENT failure rather than a terms failure is this estate's framing

### Mechanism

`cybernetic-genesis` → `tools/octonion_boundary.py`

> a declared norm is RECOMPUTED from the axes and a mismatch refused — a self-reported measurement is an instrument, and instruments lie

### Related

`penn-lawgiver-reception`, `feet-guarantors`, `sophia-authority`, `quorum-independence`

## Penn the lawgiver, and the son who used his name

`id: penn-lawgiver-reception`

### Narrative

Jefferson in 1825 called William Penn 'the greatest lawgiver the world has produced, being the first, in either ancient or modern times who has laid the foundation of government in the pure and unadulterated principles of peace, reason, and right.' Penn named Bucks County in 1682 for Buckinghamshire, his family's home in England. But the Walking Purchase was executed in 1737 by his SON Thomas, nineteen years after William's death, on a deed attributed to the father's era — the father's name carrying the credit, the son's runners taking the land.

### Design principle

A venerated name is not a warrant, and inherited authority is the weakest kind. The reception of William Penn as lawgiver is real and the fraud of 1737 is real, and holding both without letting either cancel the other is the discipline. Authority attaches to the act and the actor, never to the surname — which is exactly why an authority chain must be traced rather than assumed.

### Sources

- **attested** — Thomas Jefferson, 1825, on William Penn as 'the greatest lawgiver the world has produced'
- **attested** — Bucks County named 1682 for Buckinghamshire, the Penn family home — <https://en.wikipedia.org/wiki/Bucks_County,_Pennsylvania>
- **attested** — William Penn died 1718; the Walking Purchase was 1737, executed by Thomas Penn
- **gap** — A 'greatest lawgiver SINCE MOSES' formulation was not found; Jefferson's attested wording is 'the greatest lawgiver the world has produced'
- **gap** — A 'king's land' derivation for Buckingham/Bucks was not verified; the attested derivation is the Penn family's Buckinghamshire

### Mechanism

`cybernetic-genesis` → `tools/witness_independence.py`

> an authority chain must be stated and traced; unstated provenance is not independence

### Related

`walking-purchase-instrument`, `tamanend-reception`, `sophia-authority`

## Pisgah in Pennsylvania: the place named for seeing and not entering

`id: pisgah-seeing-not-entering`

### Narrative

Pisgah is the summit from which Moses viewed the promised land and did not enter it (Deut 34:1-3). Central Pennsylvania has a Mount Pisgah Altar — a stone altar on Shade Mountain in Snyder County, at about 2,000 feet, looking out over the valley. It was built by Robert Cryan of Beaver Springs with Wilmer Shank doing the stonework, from May to October 1979, dedicated in June 1980, and it is used for Easter sunrise service. It is a modern altar, not an ancient one, and the people who built it are known by name.

### Design principle

A place is named for the vantage, not the crossing. That a viewpoint gets called Pisgah — repeatedly, by people who never met — says the shortfall at the threshold is the part worth marking, not the part to be hidden. Name the boundary you stopped at; it is more useful to whoever comes next than a claim of arrival.

### Sources

- **attested** — Deut 34:1-3 (Moses views the land from Pisgah)
- **attested** — Mount Pisgah Altar, Shade Mountain, Snyder County PA; built 1979 by Robert Cryan and Wilmer Shank, dedicated June 1980 — <https://www.interestingpennsylvania.com/2017/06/mt-pisgah-altar-atop-a-mountain.html>
- **attested** — The unhewn-altar law is real and citable: Ex 20:25 ('if thou lift up thy tool upon it, thou hast polluted it'), Deut 27:5-6, Josh 8:31
- **gap** — Whether the Snyder County altar was built unhewn / without iron tools is NOT attested in what could be checked; the sources describe concrete and mountain stone
- **gap** — No ANCIENT unhewn stone altar in central PA was verified; the Mount Pisgah altar is a documented 1979 construction

### Mechanism

`cybernetic-genesis` → `schemas/twin.schema.json`

> the threshold rule names what is missing (21 < 22) rather than silently downgrading the actor

### Related

`moses-threshold`, `walking-purchase-instrument`, `mosis-shortfall`

## The horse is the cheat: substituting the instrument voids the measure

`id: horse-substituted-instrument`

### Narrative

The Walking Purchase was settled by a walk, and the fraud was that they ran — trained runners on a cleared path, a faster conveyance put in place of the bodily measure the agreement named. The horse is that substitution's archetype: across Indo-European tradition it is the conveyance that crosses ground, and worlds, faster than a person can — Sleipnir carrying Odin between realms, and the horse sacrifices of the Vedic ashvamedha, the Roman October Equus, and Norse blot marking it as the animal set at the boundary between what a person may reach and what they may not.

### Design principle

WHEN A MEASURE IS DEFINED BY A HUMAN CAPACITY, SUBSTITUTING A SUPERIOR INSTRUMENT VOIDS IT. The terms can be kept perfectly while the measure is destroyed, because the agreement priced the capacity, not the distance. This is the general form of the Walking Purchase, of benchmark gaming, and of every proxy that gets optimised instead of traversed — and it is why a measure must name the instrument, not only the quantity, and why an instrument supplied by one party is not a measure at all.

### Sources

- **attested** — Walking Purchase 1737: hired runners on a pre-cleared path replaced the customary walk
- **attested** — Horse sacrifice is well attested across Indo-European traditions: Vedic ashvamedha, Roman October Equus, Norse blot
- **attested** — Sleipnir, Odin's eight-legged horse, carries its rider between worlds
- **interpretation** — Reading the horse as the ARCHETYPE OF THE SUBSTITUTED INSTRUMENT is this estate's framing, not a claim about any of those traditions
- **tradition** — The horse as the animal figuring human clairvoyance — and horse sacrifice as the marking of its loss — is discussed explicitly by Steiner per the author, who is writing the book this register serves. CITATION PENDING: the specific GA/lecture reference is still to be pinned. My own searches did not surface it, which is a fact about my searching and not about the corpus; the earlier note claiming it was 'not in Steiner' was an overreach and is withdrawn.

### Mechanism

`cybernetic-genesis` → `tools/octonion_boundary.py`

> the norm is recomputed from the axes rather than read from the declaration — the measure names its instrument and does not accept a substitute

### Related

`walking-purchase-instrument`, `feet-guarantors`, `foreknowledge-shortcut`

## Prophecy against the walked path

`id: foreknowledge-shortcut`

### Narrative

A walk-measured contract prices the traversal: how far a person can actually go, in a day and a half, over ground as it lies. Foreknowledge of the destination collapses that. If you already know where the line falls you do not need to walk to it — you clear the path to it in advance, which is precisely what was done in 1737. Seeing the end and walking to it are different acts, and only one of them is what the agreement bought.

### Design principle

FOREKNOWLEDGE IS THE LIMIT CASE OF INSTRUMENT SUBSTITUTION. Where a process is the thing being measured, any capacity that skips the process voids the measurement — however honestly the endpoint is reported. This is why a proof must carry its steps and not only its conclusion, why replay matters more than the answer, and why an evaluation that leaked its test set measured nothing.

### Sources

- **attested** — The 1737 path was cleared in advance — the endpoint was known before the walk
- **interpretation** — Framing foreknowledge as the limit case of instrument substitution is this estate's

### Mechanism

`cybernetic-genesis` → `tools/genesis_braid.py`

> carry_terminus() reports the path actually walked and where it actually ends, not the intended destination

### Related

`horse-substituted-instrument`, `walking-purchase-instrument`, `wanderer-no-arrival`

## Steiner on the mission of Abraham — recorded, typed, and bound to nothing

`id: steiner-abraham-mission`

### Narrative

Rudolf Steiner, in GA 117 (Deeper Secrets of Human History in the Light of the Gospel of St. Matthew, 1909) and related cycles, holds that vestiges of an older atavistic clairvoyance survived into pre-Christian times among peoples generally, WITH THE ANCIENT HEBREW PEOPLE AS THE EXCEPTION: there its reappearance was not tolerated, and the capacity was set aside in favour of the development of rational thinking. Steiner's further claim is that seership must henceforth be reached THROUGH that thinking rather than around it — knowledge once had atavistically must now be attained by other methods.

### Design principle

A capacity that skips the process voids a measurement OF the process. Steiner's account — that an older atavistic seership was set aside in favour of thinking, and that seership must henceforth be reached THROUGH thinking rather than around it — is a claim about how a faculty is exchanged for a method, and it binds to the same mechanism as foreknowledge-shortcut: the walked path is the thing being priced, so a shortcut past it is not a faster measurement, it is a different and emptier one. Recorded with its citation and its scholarly contestation, and left for the author to work with on its own terms.

### Sources

- **tradition** — Rudolf Steiner, GA 117, 'Deeper Secrets of Human History in the Light of the Gospel of St. Matthew' (1909): atavistic clairvoyance not tolerated among the ancient Hebrew people; seership to be reached through rational thinking — <https://rsarchive.org/Lectures/DeepSecrets/19091109p01.html>
- **gap** — The 'mission fulfilled, reconciliation not yet' reading is the author's. CITATION PENDING: a specific passage to anchor it has not yet been pinned here.
- **tradition** — The horse as the animal figuring human clairvoyance — and horse sacrifice as the marking of its loss — is discussed explicitly by Steiner per the author, who is writing the book this register serves. CITATION PENDING: the specific GA/lecture reference is still to be pinned. My own searches did not surface it, which is a fact about my searching and not about the corpus; the earlier note claiming it was 'not in Steiner' was an overreach and is withdrawn.
- **tradition** — Steiner's writings on peoples, races and lineages are contested in scholarship — recorded so a reader can weigh the source, NOT as a bar on its use. Citing carefully is scholarship; refusing the binding was an editorial call this register withdraws.

### Mechanism

`cybernetic-genesis` → `tools/genesis_braid.py`

> carry_terminus() reports the path actually walked — a capacity that skips the process voids a measurement OF the process

### Related

`foreknowledge-shortcut`, `black-hills-return`, `horse-substituted-instrument`

## Martha measures, Mary raises — detection is not escalation

`id: martha-and-mary`

### Narrative

John 11. Lazarus is sick and his sisters send word, and the detail everyone skips is that he STAYED TWO MORE DAYS. By the time he comes it is four days. Martha goes out to meet him on the road, reasons with him, has the theological exchange, and at the tomb makes the measurement: 'Lord, by this time he stinketh: for he hath been dead four days' — observed, dated, quantified. Mary stays in the house until she is called; when she comes she falls at his feet and weeps. 'When Jesus saw her weeping... he groaned in the spirit.' Jesus wept. THEN: 'Where have ye laid him?'

### Design principle

MARTHA IS DETECTION; MARY IS ESCALATION. The report was accurate, complete, and followed by a two-day delay — information alone raised nothing. A finding must land on someone to move anything, so an alarm has to be an addressed, durable artifact that ESCALATES with the age of the silence, because the natural failure of monitoring is that an old alarm becomes furniture. And it must close itself when the thing lives again: an issue that outlives its cause is noise, and noise is what taught everyone to stop reading.

### Sources

- **attested** — John 11:1-44; the two-day delay at 11:6; Martha's measurement at 11:39; 'Jesus wept' at 11:35
- **interpretation** — Reading Martha as the detector and Mary as the escalation is this estate's framing

### Mechanism

`prophet-platform` → `tools/ci_liveness_escalate.py`

> severity rises with the age of the silence (P3->P2 at 30d, P1 at 60d, P0 at 90d; never-green outranks any age) and the issue closes itself when every workflow is green

### Related

`hellebore-dead-or-dormant`, `feet-guarantors`, `moses-threshold`

## Hellebore — how you tell dead from dormant

`id: hellebore-dead-or-dormant`

### Narrative

Melampus the seer-physician cures the daughters of Proetus of Argos of the madness Dionysus sent them, bringing them back with a brew of hellebore; his name is melas + pous, 'BLACK-FOOT', and Melampodium is the plant's old name for him. Two things make it the right emblem: it is poison and cure in ONE SUBSTANCE separated only by dose, so the measure decides which it is; and the Christmas rose, Helleborus niger, FLOWERS IN THE DEAD OF WINTER, in snow, when the whole garden looks finished. A winter garden and a dead garden look identical. The bloom is how you tell the ground is alive.

### Design principle

DEAD AND DORMANT ARE INDISTINGUISHABLE FROM OUTSIDE, and telling them apart is the whole difficulty. A repo emitting no signal may be dormant — manual, between phases, nobody pushing — or dead. Calling dormant things dead is how a checker gets muted; calling dead things dormant is how five weeks pass. So the verdicts must carry the distinction explicitly, and the benign verdict must be earned by evidence (a manual-only trigger) rather than assumed.

### Sources

- **attested** — Melampus cures the Proetides with hellebore; Melampodium = 'black-footed' — <https://www.theoi.com/Flora1.html>
- **attested** — Helleborus niger, the Christmas rose, flowers in December-January
- **gap** — The etymology of Helleborus is genuinely contested — heleîn 'injure' + borá 'food', álkē 'fawn' + borós 'food for fawns', or Graves (1948) 'food of Helle'. Scholars do not agree and this register does not pretend they do.
- **interpretation** — Reading the winter bloom as the dead/dormant discriminator is this estate's framing

### Mechanism

`prophet-platform` → `tools/ci_liveness_sweep.py`

> UNUSED (dormant by design) never alarms; DEAD never once succeeded; SILENT is running and never winning — and UNUSED must be earned by a manual-only trigger, not assumed

### Related

`martha-and-mary`, `bearfoot-uniformity`, `feet-guarantors`

## Heller and Ahasuerus — the name in the record disagrees with itself

`id: heller-ahasuerus-nameline`

### Narrative

The Wandering Jew runs through the name this estate is written under. Seligmann Heller (1831-1890), the Austrian poet, published 'Ahasverus' — an epic on the Wandering Jew in three cantos, Leipzig 1866 — into which Andersen's own Ahasuerus feeds; the Germans took the legend up hard, and Schubart, Lenau, Chamisso, Schlegel and Mosen all worked it. AND THE RECORD DOES NOT AGREE ON HIS NAME: the 1911 Britannica calls him SIGISMUND Heller, Wikipedia and the Jewish Encyclopedia have SELIGMANN. Earlier, Jacob Heller, a Frankfurt merchant, commissioned from Durer the Heller Altarpiece — the 'Assumption of the Virgin' with the Apostles about her empty tomb, 1509, its centre panel lost to fire in 1729 and surviving only as Harrich's copy. And a Heller was a coin: a small denomination named for Hall, worth almost nothing on its own.

### Design principle

THE RECORD DISAGREES WITH ITSELF ABOUT A NAME, IN AN ENTRY ABOUT A MAN CONDEMNED TO WANDER UNDER A NAME HE WAS GIVEN. That is the whole discipline in one artifact: an identifier is not self-evidencing, provenance must be traced rather than assumed, and two sources naming the same person differently is a conflict to record rather than a detail to smooth. Note also what survives: the altarpiece's centre is GONE and we hold a copy, which is exactly why an anchor must resolve to a location and a copy must say that it is one.

### Sources

- **attested** — Seligmann Heller (1831-1890), Austrian poet; 'Ahasverus', epic on the Wandering Jew, Leipzig 1866 — <https://en.wikipedia.org/wiki/Seligmann_Heller>
- **attested** — 1911 Encyclopaedia Britannica, 'Jew, The Wandering': Heller developed the poem into three cantos; Andersen's Ahasuerus related — <https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Jew,_The_Wandering>
- **attested** — Jacob Heller of Frankfurt commissioned Durer's Heller Altarpiece, 'Assumption of the Virgin', 1509; centre panel destroyed by fire 1729, known through Jobst Harrich's copy
- **attested** — The Heller was a small German coin named for Hall (Schwabisch Hall)
- **gap** — SIGISMUND (1911 Britannica) vs SELIGMANN (Wikipedia, Jewish Encyclopedia) is an UNRESOLVED conflict in the record and is recorded as one rather than silently picked
- **interpretation** — Reading the name-line as this estate's own instance of the wanderer is Michael Heller's connection, not a scholarly claim

### Mechanism

`cybernetic-genesis` → `tools/witness_independence.py`

> an identifier is not self-evidencing; authority provenance must be stated and traced rather than inherited from a name

### Related

`wanderer-no-arrival`, `initiation-rename`, `tamanend-reception`, `sophia-authority`

## Mesingw — the guardian worn in the bear's own skin

`id: mesingw-guardian-of-the-game`

### Narrative

The Mesingw (Misingw, Misinghalikun, 'Living Solid Face') is the Lenape Mask Spirit: guardian and keeper of the game animals — deer, bear and the rest — a sacred medicine being who appears to men in dreams, and a focus of the Big House ceremony. He is impersonated in the bear's OWN SKIN. Harrington (1921) p.34: 'To the back of the mask is fastened the skin of the bear's head, which effectively conceals the head and neck of the impersonator, while the bear's ears, projecting, add to the uncanny effect.' And at p.41, quoting Brainerd's 1745 account — the earliest we have — 'a coat of bear skins, dressed with the hair on, and hanging down to his toes; a pair of bear skin stockings; and a great wooden face painted', red on the right and black on the left, with a stick, a turtle-shell rattle and a bearskin bag. His charge from the creator was to reconcile the people's need for meat with the resentment of the animals eaten.

### Design principle

THE GUARDIAN WEARS WHAT IT GUARDS. The kinship a bear's track only suggests is here PUT ON — a man in the animal's own hide, its ears still projecting. A keeper of the game is not outside the game; it is bound into the thing it protects, and its authority comes from that binding rather than from standing apart. Which is the counterweight to the independence rules elsewhere in this register: a witness must be independent of what it attests, but a GUARDIAN is precisely not — it is answerable to both sides at once, and that is what makes it a guardian rather than an inspector.

### Sources

- **attested** — M. R. Harrington, Religion and Ceremonies of the Lenape (1921), pp. 34, 41 — public domain — <https://www.gutenberg.org/ebooks/72988>
- **attested** — David Brainerd's 1745 account of the costume, quoted in Harrington p.41
- **attested** — Mesingw as Keeper/Master of the Game and focus of the Big House ceremony — <http://www.native-languages.org/mesingw.htm>
- **gap** — The garb being SHED during the ceremony is NOT attested in Harrington, who has the impersonator moving about the camp and following the hunters but never describes it coming off
- **gap** — A first-bear-hunt coming-of-age legend — a young man skinning his first bear and seeing how like a man it looks — is NOT attested to the Lenape in what could be checked. The MOTIF is real and widespread among northern hunting peoples; 'widespread motif' and 'this people's legend' are different claims
- **gap** — A Lenape returning-god tied to the bear could not be verified. Mesingw is a GUARDIAN, not a returner

### Mechanism

`bearbrowser` → `scripts/bearbrowser-verify-bearfoot.py`

> the kinship motif is public and general (plantigrade gait, human-like tracks); the ceremonial material is cited from published ethnography and claimed no further

### Related

`bearfoot-uniformity`, `guard-goose-gate`, `tamanend-reception`

## INCEPTION → ADMN → GENESYS → SYSTEM, and ADMN is Adam-N

`id: genesys-space-stack`

### Narrative

The four spaces run idea → identity → admission → runtime. INCEPTION is the seed; ADMN is the user/identity space; GENESYS is admission and provenance (never 'Genesis' — a doc that spells it so is misspelled); SYSTEM is the runtime. ADMN is a play on ADAM-N, not on ADMIN: Adam is the first human whose primordial act is NAMING (Gen 2:19 — the original I-AM), and N is the instance index, the Nth user. It reads as ADMIN and means Adam-N, and it is bijective through angelic chains, each Adam-N paired with a guardian.

### Design principle

IDENTITY IS A NAMING SPACE, NOT AN ACCOUNT TABLE. Putting the user space between the seed and the admission plane says that WHO is asking is resolved before WHAT is admitted — identity is upstream of provenance, not a field on it. And the pun is doing work: the first act of the first user is to name, so the naming operation and the identity operation are the same operation, which is why initiation (a letter changed in a name) belongs to this layer and not to a settings page.

### Sources

- **attested** — Gen 2:19 — the naming of the animals
- **interpretation** — The INCEPTION→ADMN→GENESYS→SYSTEM stack and the Adam-N reading are Michael Heller's own framework, stated by him and recorded verbatim
- **tradition** — The angelic-chain pairing, with Michael as guardian, is the author's framework

### Mechanism

`cybernetic-genesis` → `schemas/initiation.schema.json`

> a rename is a first-class governed event at the identity layer, with an attestor distinct from the subject

### Related

`initiation-rename`, `braid-yhshvh`, `membrane-twin-bridge`

## The four Hopf fibrations — and the tower stops at the octonions

`id: hopf-tower-terminates`

### Narrative

Every Hopf fibration is built the same way from a normed division algebra A: the fiber is the unit sphere IN A, the base is the projective line AP¹, the total space is the unit sphere in A². So S⁰→S¹→S¹ (ℝ), S¹→S³→S² (ℂ), S³→S⁷→S⁴ (ℍ), S⁷→S¹⁵→S⁸ (𝕆) — and the fiber index is ALWAYS exactly one below the base index. The source diagrams wrote the quaternionic and octonionic rungs backwards (S⁴→S⁷→S³, S⁸→S¹⁵→S⁷): fiber and base transposed. Dimension arithmetic cannot catch it — 3+4=7 and 7+8=15 hold either way — and the only rung drawn correctly was the one where fiber and base are both S¹ and a swap is invisible.

### Design principle

THE GOVERNANCE BOUNDARY IS A FIBER, NOT A REGION. The octonion shell's halting surface ‖b‖=1 is the unit sphere in 𝕆≅ℝ⁸ — that is S⁷, the FIBER — so governance sits over every point of the base and there is no position from which one is outside it. Transposed, the shell becomes somewhere you could stand beyond. And the tower TERMINATES: Hurwitz gives only ℝ,ℂ,ℍ,𝕆 and Adams (1960) proves Hopf invariant one exists only in dimensions 1,2,4,8, so the eight axes are provably the top rung — non-negotiable as a matter of fact rather than preference.

### Sources

- **attested** — The four Hopf fibrations and their construction from the normed division algebras
- **attested** — Hurwitz's theorem (only ℝ,ℂ,ℍ,𝕆) and Adams (1960) on Hopf invariant one in dims 1,2,4,8
- **attested** — Octonion multiplication is non-associative, so S⁷ is not a group and the octonionic fibration is not a principal bundle
- **gap** — The source diagrams also labelled S¹² twice and placed S¹³ in a Klein-bottle figure; neither has a place in the tower

### Mechanism

`cybernetic-genesis` → `schemas/common.schema.json`

> OctonionBoundary: eight axes, ‖b‖>=1 halts, evaluation_order required in full because composition at a non-associative boundary is order-dependent

### Related

`braid-yhshvh`, `membrane-twin-bridge`, `walking-purchase-instrument`

## The braid — four spaces, five phases, twelve steps, 343 trits

`id: braid-yhshvh`

### Narrative

Four spaces in emanation order: atzilut → beriah → yetzirah → assiah. Five phases spelling YHShVH — yod, heh, SHIN, VAV, heh — the Tetragrammaton with a shin set into it. Twelve contiguous steps T0..T11. And a 343-trit holographic surface: seven layers of forty-nine, 7³, contiguous and non-overlapping across a0..a342, with a harmonic ladder where 111 = 1+10+100, 343 = 7³, and 777+111 = 888. Renders of it dropped beriah from the four spaces, dropped VAV from the phases, skipped T9 and T10 while still calling itself twelve-step, and had trit layers that overlapped and ran backwards.

### Design principle

COUNTS ARE THE CONTRACT, AND VAV IS THE TELL. Every corrupted render failed the same way — dropping a member of a fixed-size set — so the counts live as arithmetic and the diagram is generated from them rather than drawn beside them. And the deletions correlate: the renders that lost VAV also lost T9/T10, which are the vav phase. Vav means HOOK — it is the connector — so the join vanished from both places at once, which is how a braid silently loses its bridge.

### Sources

- **attested** — The four worlds of Kabbalistic cosmology in emanation order
- **tradition** — YHShVH, the pentagrammaton — a Renaissance kabbalistic construction, not scripture
- **attested** — 343 = 7³; the harmonic ladder arithmetic checks (111 = 1+10+100, 777+111 = 888)
- **gap** — T9 and T10 appear in NO source render; their labels are carried as unconfirmed and check(strict=True) refuses them

### Mechanism

`cybernetic-genesis` → `tools/genesis_braid.py`

> four spaces in order, five phases with vav present, twelve contiguous steps, seven contiguous 49-trit layers covering a0..a342 exactly

### Related

`genesys-space-stack`, `hopf-tower-terminates`, `initiation-rename`

## The twin bridge is a membrane, and the bridge repeats at every scale

`id: membrane-twin-bridge`

### Narrative

The Ring/three-space stack governs model serving and updates for OPTED-IN users only, not universally. The twin bridge is a single 1-space system in which the AI connects to and PROTECTS the user's three-space system from the external three-space system — a membrane, not a pipe. Bidirectional flow, the only direction that lets the external space reach the protected one, requires all 22 hermetically-sealed thresholds crossed plus an explicit purpose-bound opt-in; 21 is short. And the INCEPTION→GENESYS bridge is not crossed once: it repeats as the k3s quorum is stood up, again as the twin bridge scales to k8s, and again for the federated global mesh. One bridge, three frequencies.

### Design principle

A PROTECTIVE BOUNDARY MUST DECLARE ITS DIRECTION. Flow direction is stated, not assumed, and the permissive direction costs more than the restrictive one. Consent is purpose-bound and 'not_asked' is never an implied yes. And because the bridge recurs at each scale rather than being crossed once, the same gate must hold at quorum, cluster and mesh — a control that only holds at one frequency is not a control.

### Sources

- **interpretation** — The membrane reading, the 22/21 threshold and the repeating bridge are Michael Heller's framework, stated by him and recorded
- **attested** — Deut 34 — Moses sees from Pisgah and does not enter, the source of the 21/22 shortfall reading

### Mechanism

`cybernetic-genesis` → `schemas/twin.schema.json`

> flow=bidirectional requires thresholds_crossed>=22 AND consent.state=opted_in; scale is k3s_quorum|k8s|federated_mesh

### Related

`moses-threshold`, `patet-peter-active-active`, `genesys-space-stack`

## PATET / PETER — the active-active pair, and 'active' is a liveness claim

`id: patet-peter-active-active`

### Narrative

Model training and updates run as an ACTIVE-ACTIVE pair of LoRA-tuned foundation models: PATET and PETER. Peter is Kephas, the rock — Simon renamed at John 1:42, which puts the pair inside the same renaming operation the rest of this register turns on. Active-active means both members are live, not a primary with a spare waiting.

### Design principle

'ACTIVE-ACTIVE' IS A CLAIM ABOUT LIVENESS AND MUST BE CHECKABLE. A pair declared active-active with one member idle is the same defect as a quorum satisfied by one repeated signer, or two witnesses with one standing behind the other: the form is satisfied and the substance is not. So the schema demands exactly two live members when the mode is active_active — a claim about redundancy that cannot be verified is a claim about nothing.

### Sources

- **interpretation** — PATET/PETER as the active-active LoRA pair is Michael Heller's framework, stated by him
- **attested** — John 1:42 — Simon renamed Kephas, 'rock'

### Mechanism

`cybernetic-genesis` → `schemas/genesis_seed.schema.json`

> model_profile.mode=active_active requires exactly two members in pair

### Related

`membrane-twin-bridge`, `initiation-rename`, `quorum-independence`

## The allowlist that killed a pipeline without a red mark

`id: silent-workflow-death`

### Narrative

goose-notes CI reported startup_failure in 0s on every branch from 2026-07-01 to 2026-08-04. The YAML was valid. The repo's Actions policy is `selected` — GitHub-owned and verified-creator actions only — and the workflow used dtolnay/rust-toolchain, which is neither. A disallowed action does not fail a step; it stops the WHOLE WORKFLOW from starting, and GitHub reports it as 'likely a workflow file issue', pointing at the wrong thing. main did not compile for five weeks. check-ui.sh — added precisely because CI had missed a JS syntax error that left the entire capture layer inert in a running app — had never run either.

### Design principle

A CONTROL CAN BE DISABLED BY CONFIGURATION WITHOUT LEAVING A RED MARK. The failure was not in the code, not in the workflow, and not in any test — it was in a policy that silently withdrew permission to start, and its symptom was ABSENCE. So the guard has to run where a human looks: a check that refuses a disallowed `uses:` AT REVIEW TIME, before the pipeline it would disable is the thing meant to catch it.

### Sources

- **attested** — goose-notes CI startup_failure 2026-07-01 to 2026-08-04; repo Actions policy allowed_actions=selected; consent-plane-surface.yml using only actions/* succeeded on the same pushes

### Mechanism

`goose-notes` → `scripts/check-workflow-actions.sh`

> refuses any `uses:` outside the Actions allowlist, in the one job that can still start

### Related

`martha-and-mary`, `hellebore-dead-or-dormant`, `guard-goose-gate`

## Consent decides the act; the gate decides the departure

`id: consent-versus-gate`

### Narrative

goose-guard now carries four parts — two that observe and two that refuse. `scan` classifies and redacts; `receipt` emits the evidence record; `consent` is the decision engine that admits or denies a tool invocation fail-closed, in-process, before it happens; `gate` refuses egress of an already-classified artifact above a destination's ceiling. The two enforcement halves arrived from different directions and were kept apart rather than merged.

### Design principle

PERMISSION TO ACT IS NOT PERMISSION TO SEND. An act can be entirely legitimate and its payload still be too sensitive for the destination it was headed to — so the two questions need two gates, asked at two moments, against two different facts. Collapsing them into one check would make each answer stand in for the other, which is how a control ends up approving something it never examined.

### Sources

- **interpretation** — The act/artifact split is this estate's reading of two independently-built modules

### Mechanism

`goose-notes` → `crates/goose-guard/src/gate.rs`

> consent gates the invocation; gate gates the artifact's departure by destination ceiling, and refuses an unscanned artifact outright

### Related

`guard-goose-gate`, `feet-guarantors`, `silent-workflow-death`

