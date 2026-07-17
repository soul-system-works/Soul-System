# SOUL-F063 — The completion gate's firing rate is set by its cooldown, not by completions

```
FINDING ID:      SOUL-F063
DATE:            2026-07-16
KIND:            Instrument calibration — measured production behavior of the
                 SOUL-F012 completion gate reference implementation
                 (hooks/pre-completion-verify.py).
REFERENCE PROJECT: Cross-project — every Soul-governed project on the Body's
                 machine (Entergy_BOP, RealisticSensors/NeuroSiteWatch,
                 PageToPlate, dvs-nav, siggraph-2026-talk, Soul-System itself);
                 measured from ~/.claude Claude Code transcripts, 2026-04 →
                 2026-07.
WITNESS IDS:     SOUL-172 (the measurement); SOUL-026 (prior consecutive-turn
                 firing — the incident that introduced the cooldown).
STATUS:          Open — parameter retune applied to the reference implementation
                 this session; doctrine amendment not yet proposed.

WHAT:            The gate's trigger (ship + claim) is designed to mark genuine
                 completion moments, but _CLAIM_RE matched ordinary iterative
                 language — bare "done", "complete", "tests pass", "✓" anywhere
                 in turn text — so ship+claim was true on nearly every
                 substantive turn and the firing rate was governed entirely by
                 COOLDOWN_SECONDS. At 15 minutes against the Body's 8–10-hour
                 sessions this produced 8–20 fires per session (median ~10)
                 where genuine completion moments number ~1–3; each fire costs
                 one extra full-context inference pass at the most expensive
                 point of the session (300–700k cache-read tokens) plus the
                 ~450-token checklist.

MEASUREMENT:     225 firings across the window (avg 4.4/session in the Entergy
                 cluster; 20× max in one RealisticSensors session, 3c74f6c3);
                 ≈100–150M cache-read tokens of gate-induced extra turns ≈ 1–2%
                 of the machine's total volume. The dominant cost is flow —
                 10–20 interrupted stops per long session — more than tokens.
                 Scoping (_is_soul_project) behaved correctly everywhere
                 observed; this finding is about RATE, not scope.

RETUNE APPLIED (reference implementation only, this session):
                 - COOLDOWN_SECONDS 900 → 2700 (15 → 45 min): cuts fires/session
                   ≈3–4× while preserving end-of-session coverage. Rejected
                   alternative: a per-session firing latch — it exhausts on
                   early iterative noise and leaves the genuine final completion
                   unguarded, which is backwards.
                 - _CLAIM_RE tightened from word-presence to completion SHAPES
                   ("X is/are (now) complete/done/finished", "task/work/...
                   complete", "all done/set", "all tests pass(ed)", "tests
                   passed/passing", "ready to ship/merge/for review", "shipped",
                   a standalone "Done." line). Bare mid-sentence "done" /
                   "complete" / "✓" and imperatives like "make the tests pass"
                   no longer match.
                 - Unchanged: fail-open philosophy (a missed fire degrades to
                   the pre-hook status quo, per the hook's own design note);
                   turn-scoping; the stop_hook_active loop guard; the checklist
                   text (the expensive part is the extra inference pass, which
                   text length does not change).

WHY NOT YET AMENDMENT:
                 The retune is two constants in one reference implementation,
                 evidenced by one Body's usage pattern (very long sessions).
                 Whether the gate DOCTRINE (operations/completion-gate.md) needs
                 a rate-calibration clause — cooldown proportional to session
                 length, or a claim-precision requirement on implementations —
                 wants Council review, and ideally a second Body's data, before
                 it binds every implementation.

RELATED:         [[SOUL-F012]] (the gate this calibrates); SOUL-026 (introduced
                 the cooldown); [[SOUL-171]] (watch item (a): "gate FIRING
                 reliability is unmeasured" — this measures the over-firing half
                 on one machine); SOUL-I053 (deferred: Linux-FS runtime copy +
                 bash pre-gate for the per-stop spawn cost).
FILED BY:        Claude (Fable 5), Body-commissioned during the 2026-07-16
                 setup-diagnosis session; graduation to Finding explicitly
                 directed by the Body.
```
