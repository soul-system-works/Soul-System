# SOUL-F075 — An owner quote is not tied to an owner turn

```
FINDING ID:      SOUL-F075
DATE:            2026-11-06
KIND:            Doctrine gap — a record says "the Body said …" or "approved by the
                 Body", and nothing checks that an owner turn holds those words.
REFERENCE PROJECT: SUB-OS, upstream note 2026-10-30 ("an owner quote is attributed
                 by label, not by mechanism"), read in the third upstream mining
                 pass (triage .ai/mining/2026-11-06-triage.md, row Q1). The note
                 carries a team contributor's measured failure as a risk, not an
                 instance in that project: in the contributor's logs, 59 of 88
                 answers recorded as a person's came from models, and 90 approvals
                 of irreversible actions were answered in about 2 s by an
                 autopilot script. Their fix: decide an answer's source by
                 mechanism (who ran it, from where), not by label (that
                 project's witness SUB-OS-012).
WITNESS IDS:     SOUL-203 (A027/A028 claimed approval of contract wording the Body
                 had not seen) and SOUL-205 (an amendment quoted an approval no
                 record held): this repo's own instances, both caught by
                 fresh-context review, not by any check. SOUL-234 (the Body's
                 ruling).
WHY NOT YET AMENDMENT:  the fix needs a design and a test. The note's mechanism
                 (the `unconfirmed — owner to ratify` mark) was retired in v3.9.0
                 (SOUL-A031), after the note was written, so no existing
                 mechanism even partly covers it.
FILED BY:        the mining-pass-3 triage (a read-only Claude agent) proposed it;
                 the Body graduated it ("yes", 2026-11-06).
STATUS:          Open.
RELATED:         contract rule 1 (record the owner's words) and rule 2 (never
                 invent history); SOUL-F056 (the fabrication axis); SOUL-F070;
                 mind item 7 (a transcript's subagent and notification turns are
                 not the owner's).
```

## The gap

Rule 1 asks a session to record the owner's incident "in their words", and the
skills quote the Body in witness entries, amendments and release rows. Every one of
those quotes is written by the model. Nothing ties it to a user turn, so a
paraphrase, a quote from a subagent's report, or an approval inferred from a nearby
"yes" reads exactly like the Body's own words. SOUL-203 and SOUL-205 are this repo's
two caught cases; both were caught by a reviewer reading the record against the
conversation, which only happens when someone thinks to look.

## One shape a fix could take (from the note; not designed)

A capture that quotes the owner checks the quoted text against the user turns of
the session's transcript, excluding subagent reports and task notifications (mind
item 7's traps), and writes the quote as a paraphrase when it is not found.
