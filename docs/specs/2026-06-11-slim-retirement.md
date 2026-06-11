# SLIM retirement spec — DRAFT for Body review (item-by-item)

**Status:** DRAFT — nothing in this spec executes until the Body approves the item.
**Authority:** the SOUL-I049 verdict, rendered 2026-06-11: **SLIM, provisional**
(witness SOUL-162; rendered section in soul-benchmark
`experiments/2026-06-10-efficacy-program-VERDICT.md`).
**Provisionality:** the mediocre-CLAUDE.md floor discriminator
(`docs/specs/2026-06-11-floor-discriminator.md`, design) can revise any CUT back to
KEEP. Items marked ⏸ are recommended to WAIT for the floor result; the rest are safe
under any floor outcome.
**Discipline:** Rule 4 (generation couples with retirement) — every cut names its
retire handle and its resurrection path. No records are deleted anywhere in this spec.

Each item: disposition · evidence · action · `[ ]` Body approval checkbox.

---

## 1. KEEP — the measured core (no action beyond what is listed)

| # | Item | Evidence anchor |
|---|---|---|
| K1 | **Completion gate** `hooks/pre-completion-verify.py` (scope fix landed 2026-06-11, fence test `hooks/test_scope.py`) | v1.0 in-vivo 6/6 ship+GAP with broken code → v1.1 0/12 false-done (SOUL-159); discriminates where executors are absent (chain M obs.) |
| K2 | **Force-at-site doctrine** (Rule 14: negation at the code site, executable fences, pinned boundaries) | The twin-arm inversion: proposition mutated + taught the drift, force held (SOUL-155/F053); pin bounded damage to additive (SOUL-159) |
| K3 | **Record stores + cheap capture** — `witness.md`, `ideas.md`, `findings/`, `amendments/`, `/soul-capture` | Record-carry is the validated mechanism in BOTH arms of every efficacy chain; carry is depth-robust to N=20 (longitudinal); self-starts 2/3 chains (v1.0: 0/8) |
| K4 | **Continuity instruments** — `/soul-handoff`, `/soul-resume`, `/soul-next` | Carry points are the dominant mined class (c) at all 3 real projects; this verdict session itself resumed from the cursor |
| K5 | **Anchor discipline** (existence/validity/timing; Coherent Falsehood) | F015→F028→F040 chain; F054 (ungrounded invention RISES with capability); the program's own incidents were caught by it |
| K6 | **Rule-5 always-on budget + `/soul-distill`** | F055 (bloat splits quoting from obeying, 1/5→5/5); the instrument that makes SLIM itself safe to maintain |
| K7 | **Measurement/harness discipline** — `operations/experiment-harness.md`, locked-prediction protocol | Paid twice in one day (substring leak; zero-pad empty prompts, invisible to exit codes); five-fold calibration record |
| K8 | **Reference-project upstream obligation** (seed §Reference Projects, slimmed wording per R1) | Evolution fuel; orthogonal to the ceiling result; unchanged by the verdict |

`[ ]` K1 `[ ]` K2 `[ ]` K3 `[ ]` K4 `[ ]` K5 `[ ]` K6 `[ ]` K7 `[ ]` K8

---

## 2. REVISE — keep the function, shed the costume

**R1. The seed (`operations/CLAUDE.md`) shrinks to the behavioral core.**
Cut from always-on: §The Roles (the Council roster paragraph), the descriptive halves
of §Primary Failure Modes (keep the names as a one-line list — they are working
vocabulary in the record), §Reference Projects prose (compress to 3 lines + pointer).
Keep always-on: First Principle, the gates (completion gate pointer, change-fence,
witness line), Anchor Obligation, Activation Disciplines AS PLAIN SENTENCES (see C3),
Record section, Operating Notes. Target: ≤60% of current token count; sentinel-test
weak-model activation after the cut, per the Rule-5 precedent (the 1.0 CUT improved
activation — this is the same operation, second application).
Evidence: the efficacy comparator delivered ceiling quality on a 2,003-word plain
contract; F055.
`[ ]` approve R1 (execution via amendment + distill, weak-model re-test before commit)

**R2. The register becomes per-project plain/fluent (SOUL-I050).**
The spec exists (`docs/specs/2026-06-10-register-flag.md`, held for program close —
now unblocked). Under SLIM it is promoted from "interaction-quality feature" to the
REVISE bucket's main vehicle: plain register becomes the DEFAULT for new
`/soul-init` projects; fluent (mythological) register opt-in. Glossary mapping
(witness→decision log, gate→checkpoint, Body→owner…) lives in the register spec.
`[ ]` approve R2 (implement register flag per its spec, plain-default amendment)

**R3. `mind.md` re-distills against the verdict.**
Adds: the ceiling/floor distinction and the portability thesis (SOUL-161/162); the
calibration bias promoted from "residual" toward a rule-shaped lean (five-fold now).
Re-examines: Rule 6 wording (gate placement — confirmed by the program, keep), the
Tensions section under the slimmed role vocabulary. Runs under Rule 5 with the
salience re-check.
`[ ]` approve R3 (Body-invoked `/soul-distill` after R1/C1–C3 land)

**R4. `/soul-init` and `/soul-help` update to the slim shape.**
Init offers register choice + installs the slim seed; help text drops retired
ceremony. Mechanical, follows R1/R2.
`[ ]` approve R4

---

## 3. CUT — ceremony the data declined to defend

**C1. The nine-role Council as operating doctrine.** ⏸ *(wait for floor: the floor
arm tests whether role-machinery matters when the user/doctrine is weak)*
The roles (Witness, Skeptic, Accountant, Advocate, Steward, Emissary, Archaeologist,
Seer, Guardian, Hands) stop being normative always-on machinery; the postures they
name demonstrably occur without invocation (the comparator performed Skeptic- and
Witness-shaped work namelessly, every chain; the ablation study found forced roles
reproduced by filler). The role NAMES survive as record vocabulary (witness entries
TYPE lines keep meaning) and as a reading lens in the archive.
*Body refinement (2026-06-11, at spec review):* the roles are names for
perspectives that come into play naturally — and their remaining home may be the
HUMAN-facing layer, not AI doctrine at all: a person picking up the repo uses the
Council as an introspective lens. Roles need not appear in the record; where they
do (witness TYPE lines), they are mineable structured data for visuals/analytics
(precedent: soul-visual-test, registry). So C1 (always-on roster prose) and C4
(inspection instrument) may deserve different fates. See SOUL-I051.
*Retire handle:* `philosophy/the-soul.md` §roster marked ARCHIVE; seed §Roles removed
(R1); `/soul-explain council` retired (C4).
*Resurrection path:* un-archive the roster section; the record's TYPE vocabulary
never breaks.
`[ ]` approve C1

**C2. `philosophy/the-soul.md` becomes an archive document.** ⏸ *(revisit after
floor — Body, 2026-06-11)*
Header changes from "consult on demand" canon to ARCHIVE — the intellectual history
and the long-form rationale, no longer a governing layer sessions are pointed to.
"When in doubt, consult the-soul.md" leaves the seed (R1); governance lines repoint
to seed + mind + this spec's outcome. No content is deleted.
*Body refinement (2026-06-11):* the Body agrees the document as written no longer
reflects the system, but a third state exists besides canon/archive: a
HUMAN-FACING document — what a person reads to understand the system when they
pick up the repo, with the Council as their introspective lens. Different
audience, different budget: Rule 5 does not constrain a document only humans
read. Decision deferred to after the floor result (SOUL-I051).
*Resurrection path:* flip the header back.
`[ ]` approve C2 (archive)  `[ ]` or C2-alt: rewrite as the human-facing
understanding document

**C3. Named activation ceremonies collapse to plain sentences.**
- *Counterweight* (F014) → one seed sentence: "At any non-trivial scope decision,
  ask what this misses, what it could become, what already exists — and say if the
  answer is nothing."
- *Body-Input* (F037) → one seed sentence: "When a recommendation depends on
  knowledge only the owner has, ask — do not push harder on available evidence."
  **The ask-default SURVIVES — it is evidence-backed (F037, F054) independent of its
  ceremony; this item cuts the liturgy, not the behavior.**
- *"Name the Judge"* (urgency-override invariant) → kept in mind.md invariants as a
  plain sentence ("overrides are said out loud, never silent"), dropped as a named
  ritual.
`[ ]` approve C3

**C4. `/soul-explain` retires its `council` mode.** ⏸ *(falls with C1)*
The doctrine-explain path stays (it serves the register work, R2) or merges into
`/soul-help`. Steward's choice at implementation.
`[ ]` approve C4

---

## 4. Execution order (after Body approvals)

1. C2, C3, C4 + R1 in one amendment pass (the seed cut) → weak-model sentinel test
   (Rule 5 precedent) → commit.
2. R2 register flag implementation (its own spec).
3. R3 distill; salience re-check.
4. R4 init/help refresh.
5. C1 executes only after the floor discriminator reports (⏸ items).
6. Closing finding: the SLIM execution itself is a Soul-meta finding candidate
   (the system retiring its own ceremony on its own evidence — F044's promotion
   conditions met, carried queue item).

## 5. What this spec does NOT do (pinned, Rule 14)

- Deletes NO record file, finding, amendment, or witness entry — not one.
- Does not touch the hook beyond the already-landed scope fix.
- Does not weaken the reference-project upstream obligation.
- Does not retire the harness/measurement discipline.
- Does not pre-empt the floor discriminator: ⏸ items wait; a floor result showing
  the ceremony protects weak-doctrine users reverses those cuts by design, not by
  re-litigation.
