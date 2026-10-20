AMENDMENT ID:    SOUL-A029
DATE:            2026-10-19
WITNESS IDS:     SOUL-202 (the mining pass that triaged the note: an adopting
                 project's upstream note, SITE-WATCH, 2026-10-14, disposition IDEA,
                 captured as SOUL-I069); SOUL-205 (the Body's approval of the exact
                 sentence).
WHAT CHANGES:    Rule 6 gains one sentence: "After a context summary, re-read
                 `.soul/handoff.md` before acting." The citation (SOUL-I069) follows
                 it; the sentence is the Body's approved wording, verbatim.
WHERE IN SOUL:   operations/CLAUDE.md rule 6; the four eval cases' embedded copies
                 (evals/sync-contract.py).
QUESTION ONE:    Evidence — one upstream note: a context summary dropped the
                 cursor's standing facts and a rule they held was then broken. One
                 instance, one project.
QUESTION TWO:    Necessity — rule 6 said how to resume at session start; nothing
                 said the same cursor must be re-read when a summary replaces the
                 context mid-session, which is the moment its facts are lost.
QUESTION THREE:  Coherence — no new instrument, no new store; the cursor stays the
                 one source to resume from. Cost: one line of contract. Why the
                 contract and not elsewhere: the note named skills/soul-resume, but
                 a skill line is not in context after a summary unless invoked; the
                 triage's other option, a SessionStart hook re-injecting the cursor
                 on compaction, is a new instrument — the contract stays loaded
                 through a summary, so the sentence is where the moment arrives.
                 What would make this wrong: sessions re-reading the cursor after a
                 summary and still breaking what it held (the fix is then elsewhere),
                 or the re-read costing more than the facts it restores.
STATUS:          Accepted 2026-10-19 by the Body, who approved the exact sentence
                 (SOUL-205). Applied in v2.9.0.
