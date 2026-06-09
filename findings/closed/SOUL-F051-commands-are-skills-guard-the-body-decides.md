```
FINDING ID:      SOUL-F051
DATE:            2026-06-09
WITNESS IDS:     SOUL-153 (commands → skills migration); SOUL-152 / SOUL-I047 (the cross-tool +
                 convergence research that prompted it).

WHAT:            **In current Claude Code, slash commands and skills are the same mechanism in two
                 file layouts — "loaded identically; the only difference is file layout" (commands/
                 is the LEGACY layout; skills/<name>/SKILL.md is canonical). So the carrier is not
                 the design question; the INVOCATION SEMANTICS are.** Both can be invoked by the user
                 (`/name`) AND programmatically by the model (the SlashCommand tool), gated by the
                 frontmatter flag `disable-model-invocation`. The load-bearing consequence for the
                 Soul: the capture / distill / graduation instruments are DELIBERATELY Body-invoked
                 (Rule 7 — graduation is the Body's call, never auto-fired), yet they shipped WITHOUT
                 the guard — so only DOCTRINE prevented the model programmatically firing
                 /soul-capture or /soul-distill. Setting `disable-model-invocation: true` on the
                 Body-decides instruments makes the **Body-decides invariant STRUCTURAL, not merely
                 doctrinal** — the F031 family: an instrument backs the posture so the failure can't
                 occur, rather than relying on the model to remember the rule.

WHY THIS FILING (not an amendment):
                 Operational (instrument format + a frontmatter guard), not a new primitive — but it
                 carries a reusable doctrine: **wherever a rule says "the Body decides X, never
                 auto-fire," prefer a structural guard over a doctrinal one when the platform offers
                 it.** Generalizes F031 ("the recipe IS the activation; instrument over posture")
                 from the visual gate to invocation control.

FILED BY:        Steward (retired the legacy command layout); Architect (invocation semantics);
                 Guardian (the structural guard on the Body-decides invariant).

RELATED:         [[SOUL-153]] (the migration); [[SOUL-I047]] (cross-tool + the Codex/Claude
                 commands→skills convergence that motivated canonical-format adoption);
                 [[SOUL-F031]] (instrument-over-posture — the parent pattern this extends);
                 [[mind-rule-6]] (the gate fires where the failure happens — here, model-invocation
                 is the failure surface, and the guard sits exactly there);
                 [[SOUL-F042]] (the cut measured form-vs-substance — the format move is form;
                 the guard is the substance).

STATUS:          CLOSED (Body graduation, 2026-06-09). 8 commands migrated to skills/<name>/SKILL.md
                 with `disable-model-invocation: true`; behavior preserved (user-invoked-only);
                 plugin validates --strict. Residual (non-blocking): a few instruments (e.g.
                 soul-help) could justifiably be model-invocable later — a per-instrument decision,
                 deferred; all are manual for now (behavior-preserving migration).

                 UPSTREAM: this repo IS the Soul System (the upstream) — Soul-meta (instrument design
                 + the structural-guard doctrine), so it belongs in this findings/ stream.
```
