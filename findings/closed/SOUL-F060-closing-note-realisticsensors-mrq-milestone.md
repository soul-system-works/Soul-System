# SOUL-F060 — Closing note: RealisticSensors MRQ-consolidation milestone

```
FINDING ID:      SOUL-F060
DATE:            2026-07-06
KIND:            Closing Note — the milestone reflection an importing project owes upstream
                 (operations/CLAUDE.md §Projects importing this contract). Domain lessons
                 (MRQ behavior, alpha propagation, frame counting) stay home in the project's
                 witness.md; this note carries only how the SYSTEM's gates and instruments
                 behaved.
REFERENCE PROJECT: RealisticSensors (UE 5.7 plugin; imports the contract via CLAUDE.md
                 @-include; register: plain).
WITNESS IDS:     RSENS-001..005 (project-local log; all five Resolved as of this note).
COVERS:          The MRQ-consolidation arc across three sessions: an 8-task plan collapsing
                 two render paths to one behind a live parity gate; the sensor-alpha fix;
                 two follow-up fixes; all merged to the project's 5.7 branch 2026-07-06.

WHAT WORKED (kept-because-it-fired):

(1) **The handoff→resume cycle carried the arc with zero re-derivation, twice.** Session 2's
    cursor named the ONE load-bearing unknown (does the legacy renderer run headless — the
    parity gate's precondition) and session 2 resolved it first, before spending anything on
    dependent work. Session 3 resumed from the cursor + durable records alone, restated state
    in three lines, and went straight to the recorded next step (owner merge decision →
    follow-ups). No prior conversation was re-read; nothing recorded was re-derived.

(2) **The completion gate produced two real catches, one session apart, same failure mode.**
    Session 2: a post-deletion render frame had been counted but never eyeballed — the gate's
    visual-witness check (F030/F031 lineage) forced the look. Session 3: the same check fired
    on knob-verification renders that had been verified by sentinel, filename, and frame
    count — every check EXCEPT looking at the image; the forced eyeball confirmed real scene
    content (and visibly confirmed the AA knob's effect). Twice in-vivo, the gap between
    "all metadata checks pass" and "a human-meaningful artifact was inspected" was where the
    residual risk actually lived.

TENSIONS / FLAGGED (not graduated — the Body's call, A022):

(3) **Witness-draft-hold vs autonomous operation.** soul-capture's idea/witness mode says:
    draft the entry, hold for the Body's confirmation before appending. An autonomous session
    (Body absent mid-run) can hold nothing — nothing is appendable until the Body returns, so
    candidate entries either die with the session or bypass the hold. In this arc the handoff
    absorbed the tension (candidates traveled in the cursor's VOLATILE DELTA / next-step
    sections and were confirmed-or-dropped at resume), which worked but is undocumented as
    the sanctioned path. Candidate resolution for the Body: bless "the handoff IS the hold"
    as the autonomous-mode rule (mirroring the existing headless rule that force-comments +
    handoff ARE the record), or name a better mechanism.

(4) **The plain register applies to QUESTIONS, not just prose — and the cursor's own
    vocabulary is what needs glossing.** At resume, a decision was put to the Body using the
    cursor's shorthand (witness IDs, branch names, "milestone note") and the Body could not
    answer it — the context had to be re-explained in plain terms first, with a
    recommendation, before the decision could be made. soul-resume step 3 already says
    "plain language throughout" for the restatement; this instance says the same rule binds
    any DECISION SURFACE shown to the Body (options, questions, previews). The record is
    written for session continuity; the Body reads it cold. Possible soul-resume/soul-handoff
    refinement: cursor NEXT STEP entries should carry a one-line plain gloss alongside IDs.
```
