# SOUL-F070 — Rule 3 is read as a rule about numbers, so a result someone else produced passes unanchored

```
FINDING ID:      SOUL-F070
DATE:            2026-08-28
KIND:            Doctrine gap — a rule whose scope is narrower in practice than
                 its text, in the one direction that matters most now that
                 sessions routinely delegate.
REFERENCE PROJECT: Nine instances across six projects. Five came from the first
                 upstream mining pass; (5) and (6) were separated out by hand
                 afterwards, from a store whose six observations shared one heading;
                 (8) and (9) came from the second pass (claim type C, below).
                 Instance (1) is itself two occurrences, so the occurrence count is
                 ten:
                 (1) SENSOR-FORGE — an agent-produced artifact stated stale repo
                     facts with confidence; two instances, one claiming "all line
                     references from the working tree" while four of nine items
                     were the previous day's, unchanged.
                 (2) NOTE-VAULT — the completion gate's check 0 caught the session
                     having committed on a SUBAGENT's reported test counts.
                 (3) GAME-THERMAL — a primitive reported `captured=true` from a
                     function whose success does not imply the file exists.
                 (4) GAME-THERMAL — "agent self-verification has a measurable
                     ceiling": two confident assertions, both surviving the
                     session's own checking, both falling to one skeptical
                     question from the owner.
                 (5) SENSOR-VIEW — a scripted edit whose anchor did not match
                     wrote nothing and REPORTED SUCCESS.
                 (6) SENSOR-VIEW — a green test can be a statement about the
                     machine rather than about the code.
                 (7) PLANT-BOP — the session told the owner three times that their
                     application held an export licence; the instrument that
                     measures it was one command away and showed the session's own
                     processes holding it.
                 (8) MODEL-TEST — a correction is a new claim (2026-09-04).
                 (9) MODEL-TEST — a reviewer's suggested fix carries the finding's
                     authority, not its verification (2026-09-04).
WITNESS IDS:     SOUL-184 (the mining pass); SOUL-202 (mining pass 2 — claim
                 type C, instances (8) and (9)).
STATUS:          Open — graduated by the Body 2026-08-28.
RELATED:         Contract rule 3 (absolute claims need an external anchor), rule 4
                 (nothing is done until verified by execution), SOUL-F047
                 (asserted vs executed verification), SOUL-F063.
```

## The gap

Rule 3: *absolute claims need an external anchor. Say why the anchor is trusted and
what would make it wrong.* Nothing in it is restricted to quantities — but every
example that made it into the record is a measurement, so that is how it reads, and
sessions apply it to numbers and not to the two claim types below.

**Claim type A — "someone else verified it."** A subagent reports 12/12 passing; a
tool returns `captured=true`; a helper's brief says "all line references from the
working tree." The session repeats these as its own results. Under rule 4 the work
LOOKS verified: something executed and something reported. But the main session ran
nothing, and delegation makes the appearance of rule 4 cheap to satisfy — instance
(2) is the completion gate catching exactly this, and it is currently the only thing
that asks whether the session itself ran anything.

**Claim type B — "X is blocking."** Instance (7) is the sharpest in the whole pass:
three separate reports to the owner naming their application as the licence holder,
while the measuring command sat one invocation away and showed the opposite. A
statement about who or what is blocking is an absolute claim about the world, made
at the moment the session most wants it to be true — and rule 3 was never read as
covering it.

## Why these are one finding

Both are the same failure: **a claim that entered the session already formed, and was
passed on without the session acquiring its own anchor.** In type A the source is a
tool or an agent; in type B it is the session's own inference about causes. Rule 3's
existing machinery — name the anchor, say why it is trusted, say what would make it
wrong — answers both, and applying it costs one sentence: *the subagent reported it,
I did not run it* or *`lmstat` says otherwise.*

Instance (5) is worth keeping visible for a reason beyond the cluster: the tool
reported success **because it had been asked to do something it did not do.** A green
signal is only evidence about what the check actually measured, which is also
instances (3) and (6).

## Candidate wording

Rule 3 gains a scope clause: *this covers any claim the session did not verify
itself — a result reported by a tool or an agent, and a statement about what is
blocking — not only quantities. Name who or what produced it.*

## Cost of leaving it

Five projects independently hit this in **eight days** (2026-08-21 to 2026-08-28).
**Two of the seven reached the owner as a confident statement** — instance (4), where
one skeptical question overturned two assertions that had survived the session's own
checking, and instance (7), where it reached them three times. The other five were
caught inside the session, by a gate, a fact-check or a later test; that they were
caught is not evidence the rule covered them, only that something else did.

*Correction, 2026-08-28:* this paragraph first said "four of the seven" reached the
owner. Two do. The overstatement is the same class of defect as the one a
fresh-context review caught in SOUL-F065 the same day — and it happened here, in the
finding whose subject is passing on claims the session did not verify.

## Claim type C — a correction, or a reviewer's suggested fix (added 2026-10-19, SOUL-202)

The second upstream mining pass found two more claims that arrived already formed,
both from MODEL-TEST, both dated 2026-09-04. The Body
ruled that they join this finding rather than open a new one (SOUL-202):

- **(8) A correction is a new claim.** A correction overturns an earlier statement
  and is then trusted because it is a correction. It needs its own anchor under rule
  3, and a batch of corrections sent for review is labelled as such.
- **(9) A reviewer's suggested fix carries the finding's authority, not its
  verification.** A remedy proposed alongside a verified finding is a separate,
  unverified claim. It is checked by testing the property it should establish, not by
  the review that found the defect.

Both are the mechanism above. The source here is a corrector or a reviewer rather
than a tool or the session's own inference, and the claim passes on the credit of
what came with it. Type A, "someone else verified it", is the near neighbour. The
difference is that here the verification was real, but of something else: the defect,
not the fix. The count is now nine instances across six projects (ten occurrences,
counting instance (1) as two).

Candidate wording, if rule 3's scope clause is ever adopted: add *a correction, and a
fix someone suggested*. Not adopted. The ruling placed the instances; it did not
change the contract.
