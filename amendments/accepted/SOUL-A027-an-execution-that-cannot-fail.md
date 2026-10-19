AMENDMENT ID:    SOUL-A027
DATE:            2026-10-19
WITNESS IDS:     SOUL-202 (mining pass 2: 37 upstream entries triaged; the Body
                 ruled "yes to all" on the eight recommendations). Finding
                 SOUL-F074 carries the rule-4 cluster: eight upstream entries,
                 five projects. The wording parts cite their own upstream entries
                 below.
WHAT CHANGES:    One record for the Body's 2026-10-19 rulings that touch doctrine:
                 (a) Rule 4 gains one clause. Verified by execution now reads "of
                     the property itself, read from the artifact, by an instrument
                     that did not make it", and the unrun-hand-forward sentence gains
                     "a partial run leaves the rest unrun".
                 (b) Completion-gate check 4 and the hook's checklist line 4 gain
                     "rendered is not true": an image backing a content claim is
                     checked against its source (the depicted system, a data
                     channel, or a feature-toggled A/B), or the gap is named.
                 (c) Rule 10 gains a third rider: a report of reviewed work says
                     what reached the artifact, not what review caught in drafts.
                     Its `— Bottom line:` line may use any dash, ASCII `-` included.
                 (d) Rule 6 names the instrument: resume with `/soul-resume`; write
                     the cursor with `/soul-handoff`, not by hand.
                 (e) operations/witness-log-format.md: a WHAT's fact about another
                     system is an as-of statement, not present fact. A history
                     rewrite gets one appended old → new SHA map entry, and earlier
                     citations resolve through it, never by editing them.
                 (f) The hook's first checklist line said "fires once". It now says
                     "fires at most once per 45 min in this project", computed from
                     COOLDOWN_SECONDS. Label only; the latch and fail-open paths are
                     unchanged.
WHERE IN SOUL:   operations/CLAUDE.md rules 4, 6 and 10 (90 → 93 lines);
                 operations/completion-gate.md check 4; hooks/pre-completion-verify.py
                 checklist text; operations/witness-log-format.md (WHAT field, Log
                 Location and Lifecycle).
QUESTION ONE:    Evidence.
                 (a) SOUL-F074: eight upstream entries, 2026-09-01 to 09-16, from
                     SENSOR-VIEW, PLANT-BOP, GAME-THERMAL, MODEL-TEST and SUB-K.
                     Each ran a check that could not have failed: a proxy, a
                     generator that never reached the failing inputs, a verdict read
                     through a pipe, a maker that checked itself, a one-sided run.
                 (b) PLANT-BOP (2026-09-10) and GAME-THERMAL (2026-09-01) reported
                     the check-4 defect independently: "rasterized and inspected"
                     passed while what the image showed was false.
                 (c) MODEL-TEST (2026-09-04) found a report of review rounds
                     that blurred what shipped with what was caught in drafts. An
                     adopting project's public blog (2026-09-02) hit a collision:
                     rule 10's em-dash against a harness's no-em-dash rule. (The
                     blog is public and intentionally unredacted in the registry;
                     it is cited without its name all the same.)
                 (d) MODEL-TEST (2026-09-25) found a cursor written by
                     hand. Rule 6 named `/soul-handoff` only in parentheses, and that
                     project's owner declined a local rule, so the contract is the
                     place.
                 (e) MODEL-TEST (2026-09-03) found a witness WHAT read later
                     as present fact about another system, after it had gone stale.
                     GAME-THERMAL (2026-09-02) found that an append-only witness plus
                     a history rewrite leaves cited SHAs dangling.
                 (f) GAME-THERMAL (2026-08-31): "fires once" did not hold across a
                     long autonomous session. SENSOR-FORGE had reported the same
                     mislabel earlier, in its closing note (SOUL-F062, item 5).
QUESTION TWO:    Necessity.
                 (a) Rule 4 asked that something run, and every F074 instance ran
                     something. The partial cover all sits outside the contract:
                     completion-gate check 0 (A019, "judge from content"), F047,
                     F071, and this repo's harness rules (SOUL-156, 160/161, 178,
                     mind items 3 and 6(d)). The gate rarely fires on current models
                     (mind item 5), so cover that lives only in the gate is cover
                     that rarely runs.
                 (b) Check 4 as written passes exactly the two reported failures.
                 (c) Rule 10's riders cover the action and the number of questions,
                     not provenance of reviewed work. The rule printed one dash and
                     was read as requiring it.
                 (d) A parenthesis read as optional, and nothing else in the
                     contract says the cursor comes from the instrument.
                 (e) The format said nothing about time-bound facts or rewritten
                     history. The append-only rule forbids the obvious repair,
                     editing old citations, and offered none in its place.
                 (f) The label was false as written. The code fires once per stop
                     and then cools down.
QUESTION THREE:  Coherence. No contradiction found.
                 (a) The clause narrows what counts as execution and adds no
                     obligation. Check 0 and the harness rules become applications of
                     rule 4 rather than separate doctrine. F071's candidate ("a
                     review is work") is partly absorbed: a reviewer who only
                     re-reasons the author's code is the same instrument twice.
                     F071 stays open on whether review needs its own sentence.
                     Known gap: the hook's checklist line 0 still asks only
                     whether a check's executor exists and runs. Rule 4's new
                     clause is enforced by the contract text and by checklist
                     line 4, not by a new hook check.
                 (c) The dash: the hook's `_VERDICT_RE` already accepts `—`, `–` or
                     `-`, but it parses the gate's `— Verify:` line, not
                     `— Bottom line:`. No code parses the Bottom line, so the change
                     loosens nothing that is checked.
                 (e) The as-of clause is the witness-side form of rule 3 and of
                     F067's ruling for cursor fields. The SHA map keeps append-only
                     intact.
                 Contract growth is three lines (90 → 93) on an always-on page
                 kept "within budget". No new rule numbers.
STATUS:          Accepted 2026-10-19 — the Body ruled "yes to all" on the mining-pass-2
                 recommendations (SOUL-202), then approved this exact wording
                 (SOUL-203). Applied in v2.8.0.

---

**What would make this wrong.** If sessions start meeting rule 4's clause with a
second run of the same instrument relabelled "independent", the clause has become a
formula. The same holds for an A/B whose toggle never changes the output. The check
is the next mining pass: an entry where a session named a second instrument, and that
instrument found something the first missed, is the evidence the clause works. A pass
with none means the clause is read and not used.
