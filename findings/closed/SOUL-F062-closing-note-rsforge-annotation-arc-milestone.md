# SOUL-F062 — Closing note: rsforge bbox-annotation arc (v2 + cross/strip milestones)

```
FINDING ID:      SOUL-F062
DATE:            2026-07-10
KIND:            Closing Note — the milestone reflection an importing project owes upstream
                 (operations/CLAUDE.md §Projects importing this contract). Domain lessons
                 (join keys, OBB math, tile layouts, capture quirks) stay home in the
                 project's witness.md and mind.md; this note carries only how the SYSTEM's
                 gates and instruments behaved.
REFERENCE PROJECT: RealisticSensorsForge / rsforge (standalone Python analysis repo;
                 imports the contract via CLAUDE.md @-include; register: plain).
WITNESS IDS:     SENSA-023..029 (project-local log; the annotation arc v1→v2→cross/strip,
                 all shipped as of this note). Covers two owed milestones in one note:
                 bbox-annotation v2 (SENSA-027, 2026-07-10) and cross/strip annotation on
                 the first lane api surface (SENSA-029, 2026-07-10), plus the same-day
                 Mind redistill.

WHAT WORKED (kept-because-it-fired):

(1) **Stop-on-discrepancy subagent execution audits the RECORD, not just the code.** Across
    the two builds, FIVE defects in committed plans (an unsatisfiable test bound, a stale
    suite-count, a git-add omission, a mid-plan count gone stale from the plan's own earlier
    task, and one plan demanding contradictory behavior from a single raise site) were caught
    by executors refusing to improvise, and each was fixed in the committed plan BEFORE code
    shipped. The plan files now match what was actually built. System-level lesson: execution
    is a verifier of plans — the discipline turns executors into record auditors, and the
    "fix the record first" ordering is what makes the record stay trustworthy.

(2) **Counter-default fence carriage held across a session boundary AND across agent
    boundaries (F053 lineage).** The piped-exit-code fence (incident: a commit rode "exit 0"
    over two collection errors, SENSA-028) traveled in the cursor's COUNTER-DEFAULT FENCES
    with its incident attached, was restated in every executor prompt, and every executor
    reported printed pass-counts verbatim. Zero recurrence across four subagent tasks. The
    force (incident + explicit negation), not the bare rule, is what survived the two hops:
    session → orchestrator → subagent.

(3) **The visual-witness check fired with teeth for a third project instance (F030/F031,
    F060(2) lineage).** The executor eyeballed the stitched-overlay PNG and diagnosed a
    cosmetic wireframe bleed; the completion gate then forced the ORCHESTRATOR's independent
    look at the same artifact, which confirmed both the correctness claims and the cosmetic
    finding. The named-residual discipline (the strip view deliberately un-eyeballed, named
    as such) gave the Body a crisp accept-or-extend decision instead of a hidden gap. The
    interactive witness-draft-hold (draft shown → Body's "go" → append) also ran cleanly this
    arc — the tension F060(3) flagged is specific to autonomous mode, not the mechanism.

(4) **The Mind's default-deny growth check turned silent bloat into a priced decision.**
    The redistill wanted 84→115 lines after the record grew 19→29 entries; the growth check
    forced an explicit "consciously expanding because…" ask with the honest merges already
    taken and a cut-list priced. The Body signed off with the delta-first review (SOUL-055
    gap-only shape) in one exchange. The check's value was not blocking growth — it was
    making growth a decision the Body actually saw.

TENSIONS / FLAGGED (not graduated — the Body's call, A022):

(5) **The completion gate's "fires once" label does not match its behavior.** The
    pre-completion-verify Stop hook announces "fires once" but fired on three separate
    turns of one session (each turn that shipped-and-claimed). Each firing was answerable
    in one gap-only line, so the cost stayed low (F032 compression held) — but a label that
    says "once" and means "once per shipping turn" invites the reader to dismiss later
    firings as spurious. Candidate fix: reword the label, or gate repeat firings on new
    unverified claims only.
```
