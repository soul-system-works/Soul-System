```
FINDING ID:      SOUL-F050
DATE:            2026-06-09
WITNESS IDS:     SOUL-154 (the bug + fix); the Body's dogfood test — fresh project (temp2) →
                 /soul-init → /soul-capture idea targeted the Soul System SOURCE repo's ideas.md
                 instead of temp2's own; verified fixed by re-test (capture now lands in temp2/).

WHAT:            **An adopting project's record must be local to THAT project, at its own root —
                 the capture/record instruments must never default to the Soul System source repo
                 (where the imported seed/skills physically live).** The record is per-project; the
                 source repo's record is its own. Two coupled gaps produced the bug: (1) `soul-init`
                 installed only the `@import` line and never scaffolded the project's local record
                 stores, so a fresh Soul project had NO local target; (2) no doctrine rule anchored
                 the record to the current project root, so with the local store missing the agent
                 resolved "ideas.md" to the only one it could see — the source repo's. The instrument
                 wrote (or tried to write) to the wrong record — ironic for a system whose first
                 discipline is "record where it happened."

                 FIX (both halves — scaffold + rule): (a) a **locality invariant** in the seed
                 §The Record + mirrored in AGENTS.md — *the record is THIS project's, at the project
                 root (the dir of the session's CLAUDE.md), create-on-first-use, NEVER the source
                 repo (exception: when this project IS that repo)*; inherited by all record commands.
                 (b) `soul-init` now SCAFFOLDS the local record (ideas.md, witness.md, findings/open
                 + closed; skips amendments/ — those go upstream) and is IDEMPOTENT (backfills an
                 already-imported project). (c) `soul-capture` carries an explicit "where it writes"
                 rule. The doctrine rule also protects projects initialized BEFORE the fix.

WHY THIS FILING (not an amendment):
                 Operational/instrument fix + a doctrine clarification (locality of the record), not
                 a new philosophy primitive — it sharpens the existing §The Record. The deeper
                 Soul-meta lesson is methodological: **the adopter flow is where the upstream is
                 structurally blind to its own gaps** — the Body running the real init→capture path
                 surfaced a bug no amount of in-repo testing would (in the repo, cwd IS the source,
                 so the ambiguity never fires). This is the Emissary/Advocate discipline (test as the
                 real external user) catching what internal coherence cannot — the longitudinal
                 in-vivo thesis (SOUL-144) on the adoption surface.

FILED BY:        Guardian (protects the source repo's record from adopter writes); Emissary/Advocate
                 (the real-adopter test that surfaced it); Craftsman (the fix).

RELATED:         [[SOUL-154]] (the catch + fix);
                 [[SOUL-144]] (longitudinal in-vivo payoff — this is its instance on the adoption
                 surface: the system's own use caught the system's own gap);
                 [[SOUL-F029]] (distribution model — the seed/skills live in one canonical repo and
                 are referenced/symlinked; this finding adds: the RECORD does NOT live there, it
                 lives with the adopter);
                 [[mind-rule-13]] (record the unguessable — here: record it in the right PLACE).

STATUS:          CLOSED (Body graduation, 2026-06-09). Fixed in doctrine + soul-init + soul-capture;
                 verified by the Body's temp2 re-test. Residual (non-blocking): read-commands
                 (next/resume/help) rely on the inherited doctrine rule rather than an explicit
                 per-command line — acceptable (kept lean).

                 UPSTREAM: this repo IS the Soul System (the upstream) — Soul-meta (instrument +
                 doctrine behavior), so it belongs in this findings/ stream.
```
