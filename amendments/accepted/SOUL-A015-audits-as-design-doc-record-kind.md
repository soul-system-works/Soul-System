```
AMENDMENT ID:    SOUL-A015
DATE:            2026-05-27
WITNESS IDS:     SOUL-088 (Soul-Console v1 structural audit — the inaugural
                 `docs/audits/` instance; Section 2.3 enumerated the
                 four-kind design-doc taxonomy and Section 1.7 named the
                 new subdirectory's KEEP-IN-PLACE verdict).

WHAT CHANGES:    Formally recognize `docs/audits/YYYY-MM-DD-*.md` as the
                 FOURTH design-doc record-kind, alongside the three
                 existing kinds in `docs/`:

                 | Kind | Path | Purpose |
                 |---|---|---|
                 | Spec | `docs/specs/YYYY-MM-DD-*.md` | Design-spec for an instrument or feature |
                 | Plan | `docs/plans/YYYY-MM-DD-*.md` | Implementation plan bridging spec → build |
                 | Experiment | `docs/experiments/YYYY-MM-DD-*.md` | Empirical investigation record |
                 | **Audit** | `docs/audits/YYYY-MM-DD-*.md` | **NEW: Review-time structural assessment** |

                 An audit is a review-time record: it surveys some span of
                 the system (a directory, a record-kind, a doctrine layer,
                 a version boundary), names what is there, decides
                 KEEP / RETIRE / DEFER per item, and is dated to the moment
                 of the survey. Like specs/plans/experiments, audits are
                 build-once-then-stable — they are not living records and
                 do not graduate through a ratchet.

                 An audit may anchor downstream graduations: a witness
                 entry that cites the audit; a finding promoted from a
                 pattern the audit surfaced; an amendment that codifies a
                 rule the audit named. The audit itself is the immutable
                 anchor, not a ratchet record.

WHERE IN SOUL:   No `operations/CLAUDE.md` seed edit (the seed does not
                 currently enumerate design-doc kinds; adding an
                 enumeration would grow the always-on budget against
                 mind-rule-5). No `philosophy/the-soul.md` edit. No
                 `mind.md` edit (taxonomy, not doctrine).

                 The recognition lives in:
                 1. This amendment (the formal record).
                 2. The audit document itself
                    (`docs/audits/2026-05-27-soul-console-v1-structure.md`
                    §1.7 + §2.3) — already in place; back-anchors this
                    amendment.
                 3. Future audits follow the same date-prefixed naming and
                    file under `docs/audits/`; the convention propagates
                    by example.

QUESTION ONE — EVIDENCE:
                 - SOUL-088 produced the first audit-shape artifact:
                   531-line review-time structural assessment of every
                   top-level location in the Soul-System repo. Same shape
                   as a spec (build-once, dated) but different content
                   class (survey-and-decide vs. design-spec).
                 - The audit's §1.7 named the kind explicitly: "review-time
                   audit records. Fourth design-doc shape. KEEP-IN-PLACE
                   (new) — this audit itself instantiates the type."
                 - Section 2.3's taxonomy table places audits alongside
                   specs/plans/experiments at the same layer (design-doc
                   records, build-once-then-stable, alongside-not-within
                   the ratchet).
                 - The audit's per-boundary investigation discipline (the
                   SOUL-087 Thread 2 reshape: Architect per-boundary, not
                   Steward per-item) IS the audit-kind's distinguishing
                   shape — broader scope than a spec, retrospective rather
                   than forward-looking.

QUESTION TWO — NECESSITY:
                 - Audits will recur. Structural review on a v1 boundary
                   (this one); periodic state-of-the-record audit; per-
                   system-version audits at minor releases — all are
                   plausible future cadences.
                 - Without the kind formally recognized, the next audit
                   author has to choose: file under `docs/specs/`
                   (wrong — audits don't spec), `docs/experiments/`
                   (wrong — audits don't measure), `docs/plans/`
                   (wrong — audits don't plan), or invent a location.
                   The kind makes the placement non-ambiguous.
                 - The cost of the kind is zero — the subdirectory already
                   exists, the inaugural file already lives there, the
                   date-prefixed naming already matches the sibling kinds.
                 - The cost of NOT recognizing the kind is taxonomy churn:
                   future audits land in the wrong directory or pollute an
                   existing kind's coherence.

QUESTION THREE — COHERENCE:
                 - Parallel structure to the existing three kinds: same
                   `docs/<kind>/` path; same `YYYY-MM-DD-<slug>.md`
                   naming; same build-once-then-stable lifecycle; same
                   "alongside, not within the ratchet" relation.
                 - Coheres with `mind-rule-10` (docs live near the code)
                   — audits live in the docs directory with the other
                   design-doc kinds, not bolted onto the ratchet or the
                   philosophy.
                 - Coheres with `mind-rule-2` (default simplicity) — uses
                   the existing pattern rather than inventing a new shape.
                 - Coheres with `mind-rule-5` (never always-on past the
                   description budget) — the kind's recognition does NOT
                   require a seed edit; the amendment record + the audit
                   document carry the formal recognition without growing
                   the always-on context.
                 - No contradictions with existing doctrine. Distinct
                   enough from specs (specs design, audits survey) and
                   experiments (experiments measure, audits decide) that
                   the kind is not a duplicate.

ACCEPTED BY:     Body, 2026-05-27 (within the b→c→a beat following the
                 Soul-Console v1 audit close — SOUL-088 explicitly flagged
                 A015 as a candidate amendment in its closing section, and
                 the Body authorized the batch).

FILED BY:        Archivist (record-kind recognition is the Archivist's
                 instrument — the kind defines where future audit-shaped
                 contributions land); Cartographer (Section 2.3's taxonomy
                 map is the cartographic move — kinds laid down so the
                 territory stays legible); Architect (the boundary between
                 spec/plan/experiment/audit is structural; naming the
                 kinds at the same layer preserves the cleanness of the
                 `docs/` tree); Seer (the audit-shape was implicit in
                 SOUL-088's own production — Seer reads what the record
                 means; the kind is what the audit was always going to be
                 once it existed).
```

---

## On Acceptance

Lightweight design-doc taxonomy amendment. The kind already exists in practice (SOUL-088's audit document lives at `docs/audits/2026-05-27-soul-console-v1-structure.md`); this amendment formalizes the recognition so the next audit-shaped contribution has a non-ambiguous home.

The work landed in three places (already in place; no new edits this beat):

1. `docs/audits/2026-05-27-soul-console-v1-structure.md` §1.7 + §2.3 — the inaugural instance and the taxonomy table that named the kind.
2. This amendment record — the formal recognition.
3. Sibling directories (`docs/specs/`, `docs/plans/`, `docs/experiments/`) — unchanged; the parallel structure is the precedent.

No findings closed by this amendment — it formalizes a taxonomy extension named in an audit. Future audits follow `docs/audits/YYYY-MM-DD-<slug>.md` by example.
