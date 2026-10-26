AMENDMENT ID:    SOUL-A030
DATE:            2026-10-26
WITNESS IDS:     SOUL-220 (no adopting project set `fluent`; the Body never used
                 it and chose to drop it).
WHAT CHANGES:    The contract's Register paragraph loses its override sentence
                 ("A `**Register: fluent**` line in the project's CLAUDE.md switches
                 to full Soul vocabulary.") and reads "plain" instead of "`plain` by
                 default". /soul-init stops asking plain-or-fluent; the Codex
                 procedure stops writing a fluent override; /soul-resume drops its
                 "under a plain register" condition.
WHERE IN SOUL:   operations/CLAUDE.md (Register); operations/contract-reasons.md;
                 skills/soul-init, skills/soul-resume, operations/codex.md; the four
                 eval cases' embedded copies (evals/sync-contract.py).
QUESTION ONE:    Evidence — SOUL-220: zero adopting projects carried the override
                 across every project under /mnt/d/Projects; the author ran plain.
QUESTION TWO:    Necessity — the override bought nothing anyone used and cost a
                 question at every fresh init (I082 is removing questions that do
                 not earn their place) plus always-on contract text in every
                 session of every project.
QUESTION THREE:  Coherence — plain stays exactly as it was; nothing else in the
                 Soul depends on fluent. A project that wants terse Soul vocabulary
                 can still say so in its own CLAUDE.md; the Soul just stops
                 offering and maintaining the switch. What would make this wrong: an
                 adopter who relied on fluent (none found; a Codex trial folder was
                 not swept), or plain measurably costing expert readers time.
STATUS:          Accepted 2026-10-26 by the Body ("yes to your recommendations",
                 answering the drop-fluent lean). Applied in v3.6.0.
