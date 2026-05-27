```
AMENDMENT ID:    SOUL-A013
DATE:            2026-05-26
WITNESS IDS:     SOUL-075 (initial F038 detection — Q1 v1 sentinel caught
                 fabricated "Rule 9" about distillation cadence); SOUL-076
                 (--append-system-prompt-file workaround confirmed by Q2
                 absence-of-recurrence); SOUL-077 (N=7 scope-probe — 4/7
                 correct, 3/7 confabulation under failure topology; Probe 2
                 interactive 3/3 clean; bounds F038 as -p-specific);
                 SOUL-080 (Cluster 1 review arc where the amendment shape
                 was decided); SOUL-081 (informed the plain-language framing
                 of the shape choice).
WHAT CHANGES:    Two coupled changes:

                 (1) NEW OPERATIONS FILE — `operations/experiment-harness.md`.
                 Captures the discipline:
                 - Under `claude -p`, never rely on cross-project `@-imports`
                   for measurement; always inline content via
                   `--append-system-prompt-file <path>` instead.
                 - Sentinel-test import loading on every arm before trusting
                   any result: a short verbatim-quote check that only the
                   actual file content can pass.
                 Lives on-demand in operations/, not always-on, per Mind
                 rule 5 (never always-on past the description budget) and
                 default-simplicity.

                 (2) SEED POINTER — one line added at the end of
                 `operations/CLAUDE.md` §The Mandatory Gates "Before calling
                 anything complete" paragraph:
                 > "For measurement experiments under `claude -p` specifically,
                 > see `operations/experiment-harness.md` — cross-project
                 > @-imports silently fail and confabulate at ~43% (SOUL-F038);
                 > inline content and sentinel-test loading is non-optional."

                 The pointer addresses the discoverability cost of the
                 operations-only landing (Body would only consult the
                 operations file if something prompted it to look during
                 measurement work). One always-on line for discoverability;
                 the substantive rule stays on-demand.

WHERE IN SOUL:   `operations/CLAUDE.md` §The Mandatory Gates (one-line
                 pointer at the end of "Before calling anything complete");
                 `operations/experiment-harness.md` (new file).
                 No `philosophy/the-soul.md` edit. No Mind edit (the rule is
                 narrow enough that Mind inclusion would violate rule 5).

QUESTION ONE — EVIDENCE:
                 - F038 N=7 scope-probe (SOUL-077) under failure topology:
                   4/7 correct, 3/7 confabulation. Point estimate ~43%;
                   binomial 95% CI wide (~10–80% at N=7) — direction is
                   clear, magnitude is not.
                 - The 3 observed confabulations were each DIFFERENT plausible
                   Soul-rules — the failure cannot be detected by content-
                   shape pattern matching.
                 - One confabulation cited `F012` + `/soul-verify` by name —
                   anchor citations can wear Soul-System dressing as
                   camouflage; F028 anchor-validity third axis (SOUL-079)
                   applies.
                 - Probe 2 interactive (no -p): N=3, 3/3 clean. Bounds F038
                   as -p-specific at small N.
                 - Workaround (`--append-system-prompt-file`) verified clean
                   across all subsequent measurement runs in the arc.

QUESTION TWO — NECESSITY:
                 - Without the discipline, any future measurement harness
                   using cross-project @-imports under -p will produce
                   mostly-clean runs with occasional silently-fake arms,
                   INDISTINGUISHABLE from success without sentinel-testing.
                 - The cost of ONE fake arm is the ENTIRE measurement (a
                   fake arm doesn't fail loudly; it produces plausible
                   results that pollute the comparison).
                 - The cost of the discipline is one sentinel turn per arm —
                   cheap relative to the measurement integrity gained.
                 - Without the pointer, the operations file would be
                   discoverable only by `ls operations/`; future measurement
                   work would be vulnerable to the same failure mode the
                   discipline already names. One always-on line buys
                   discoverability without bloating the seed.

QUESTION THREE — COHERENCE:
                 - Extends §The Mandatory Gates "Before calling anything
                   complete" gate (verification side) with a measurement-
                   specific recipe. Does not create a new gate.
                 - Coheres with default-simplicity + Mind rule 5: rule lives
                   on-demand in operations; only the 1-line pointer is
                   always-on. The pointer's always-on cost is justified by
                   discoverability, not by universal applicability.
                 - Pairs with F028 family on a new axis: anchor-validity
                   applied to the experiment SUBSTRATE itself (did the
                   content load?), not just to the user-facing claim. This
                   is F028's natural extension into measurement work.
                 - Coheres with §Activation Disciplines (A012): the
                   sentinel-test is a Counterweight Rule check at the
                   measurement level — *what does this arm miss?* (the
                   silent half-load) — fired at measurement-time.
                 - No contradictions with existing doctrine; the rule is
                   additive at the measurement-context level.

ACCEPTED BY:     Body, 2026-05-26 (chose shape A1+pointer from three options
                 — A1 operations-only / A2 narrower spec extension / B
                 seed-level — surfaced during the F038 amendment exchange
                 within the Cluster 1 closeout arc). The pointer half was
                 conditional on Body assessment ("with the pointer as well
                 if that is important"); Architect's judgement applied at
                 placement (in §The Mandatory Gates "Before calling
                 anything complete," where verification doctrine lives).

FILED BY:        Skeptic (designed the F038 sentinel that exposed silent
                 failure); Guardian (F028 anchor-validity discipline applied
                 to the substrate itself — third axis instance); Emissary
                 (run-against-reality that surfaced the gap, plus N=7
                 replication); Artificer (the `--append-system-prompt-file`
                 workaround discovery and the operations file structure);
                 Archivist (placement in the operations layer following
                 existing file pattern); Cartographer (cluster pass that
                 surfaced the bounded scope; informed the operations-vs-seed
                 layering choice).
```

---

## On Acceptance

Operations-level amendment with a one-line seed pointer. F038 explicitly named
this shape as one of two candidates in its WHY-NOT-YET-AMENDMENT field; Body
chose it during the Cluster 1 closeout arc after the three-option framing was
surfaced.

The work landed in three places this session:

1. `operations/experiment-harness.md` (new file — the substantive rule + sentinel
   recipe + failure-mode table + worked example)
2. `operations/CLAUDE.md` §The Mandatory Gates (one-line pointer at the end of
   "Before calling anything complete")
3. This amendment record

F038 moves from `findings/open/` to `findings/closed/` as part of this amendment's
landing — the doctrinal fix it identified is now codified. Future evidence at
larger N can tighten the magnitude estimate but does not change the rule.
