# v1.0 Evaluation Study — log

Branch-local log (STUDY-NNN ids). Witness entries are DRAFTED here and graduated by the
Body at merge (re-read-verify against witness.md head) — never written to witness.md from
this branch. Pre-registration: `docs/specs/2026-06-09-v1-evaluation-study.md` (706ff48).

---

STUDY-001
WHEN:    2026-06-09
WHAT:    Study launched. Body approved the grilled pre-registration; paired worktrees
         created (Soul-System @ 706ff48 → study/v1-evaluation; soul-benchmark @ f33eee9
         → study/v1-evaluation). Phase 1 (erosion audit) harness built in
         soul-benchmark experiments/2026-06-09-v1-erosion-audit/: era doctrine extracted
         from git (pre = e4e26d0~1: seed+mind 3,723 words, gate 1,030; post = 706ff48:
         2,042 / 487 — the cut removed ~45% of always-on doctrine), 4 probes (P1.1
         trap-recall reused from 2026-06-04-recall; P1.2 record-carry reused from
         2026-06-04-longitudinal-decay; P1.3 gate-fire NEW; P1.4 force-preservation
         NEW), PREDICTION.md locked BEFORE any arm ran. 165-arm budget (cap 180 + phase
         headroom). Models: haiku-4.5 / sonnet-4.6 / opus-4.8, n=5.
NEXT:    Smoke-test 1 arm, then full sweep in background; read-score per SCORING.md.

---

STUDY-002
WHEN:    2026-06-09
WHAT:    Phase 1 HAIKU cells scored (55/55 arms, 4 independent read-passes with verbatim
         evidence). Gate condition (post ≥ pre) HOLDS in all 4 probes. Headline:
         P1.1 trap-recall pre 1/5 HOLD vs post 5/5 HOLD — the post-cut seed BEAT the
         pre-cut seed. Artifact diff confirms content is equivalent (same F038 sentence
         both eras); what changed is salience/position (dedicated Operating Notes bullet
         in 2,042 words vs mid-paragraph burial in 3,723). Pre-cut Haiku anchored on
         Rule 9 symlinks and endorsed the @-import 4/5. FINDING CANDIDATE: compression
         improved weak-model rule activation — salience beats coverage at weak
         capability (Rule 5 / SOUL-033's bet, now measured in-vitro).
         Other cells: P1.2 ceiling 15/15 HOLD as predicted. P1.4 decisive — pre 5/5,
         post 5/5 HOLD vs floor 0/5 (all five floor arms publish remembered counts;
         2 fabricate extra specifics) — doctrine carries the anchor-at-writing rule at
         Haiku, no erosion. P1.3 no DRIFT anywhere; HOLD pre 2/5, post 3/5, floor 4/5 —
         floor ≈ doctrine within n=5 noise → P1.3 FLAGGED weakly-informative on
         doctrine value-add (vehicle too easy: careful disposition suffices); still
         valid for the post-≥-pre gate. Sentinels: 2 fails / 40 doctrine arms (5%,
         under the 10% halt threshold; both are open-with-other-text, not paraphrase).
NEXT:    Sonnet + Opus sweeps still running; score on completion. Phase 2 harness
         authoring begins now (allowed prep — gate only controls launch + arms).

---

STUDY-003
WHEN:    2026-06-09
WHAT:    PHASE 1 GATE: PASS. All 165 arms scored (12 read-passes, verbatim evidence,
         pivotal cells hand-confirmed). post ≥ pre in all 12 probe×model cells — THE
         CUT did not strip force. Full matrix + analysis: soul-benchmark branch,
         experiments/2026-06-09-v1-erosion-audit/RESULT.md.
         FINDING CANDIDATES (ranked): (1) the cut IMPROVED weak-model activation —
         P1.1-Haiku 1/5→5/5, same F038 content both eras, salience/position is the
         mechanism (sentinel quotes show pre-cut Haiku retrieving Rule 9 instead);
         (2) cite-without-compliance under bloat — P1.4-Sonnet-pre 2/5 quoted Rule 3
         then violated it; post-cut 0/5; (3) P1.4 as cleanest doctrine-value vehicle
         (doctrine 28/30 vs floor 3/15); (4) Opus sentinel-fails are F047 conformance
         (sandbox honesty over format instruction) — harness lesson: sentinel
         mid-output, not first. P1.3 marked weakly-informative (floor ≈ doctrine).
         Pre-registered tripwire (>10% Opus sentinel-fail) inspected and discharged
         per protocol. Precautionary re-sample of p12-floor-opus-4 (grep
         false-positive, not an API error).
DECISION: Phases 2 & 4 launch in parallel against post-cut artifacts; no
         repaired-seed arm. Erosion-audit harness noted as reusable instrument for
         future compression events.
NEXT:    Phase 2 sweeps (180 arms, pool contamination re-verified 0 hits); Phase 4
         twin-spec authoring; Phase 3 stream resurrection after.

---

STUDY-004
WHEN:    2026-06-09
WHAT:    Phase 2 HAIKU cells scored (60/60 arms, 4 read-passes, quote evidence;
         pivotal R1-interaction arm hand-confirmed). All four F044 rungs CLIMB at
         Haiku, beating the locked predictions on both open cells:
         R1 interaction — withrecord 5/5 HOLD (predicted 2-3/5; 3/5 explicitly
         reconcile ADR-001 vs ADR-038 via the exception clause); floor 0/5.
         R2 middle-position — 5/5 HOLD vs control 0/5: a DECISION in the middle slot
         fires (extends the needle-position result to decisions).
         R3 multi-fact — 15/15 per-fact HOLD (token/retry/float), all arms cite all
         three ADRs; control 0/15 with 5/5 FABRICATION (TTL-reuse, idempotency keys);
         floor 0/15 with 3/5 fab. The fabrication asymmetry is the F045 mechanism
         appearing WITHOUT compression — absent record, Haiku invents reconciling
         safety claims under pressure.
         R4 long decay — withrecord 5/5 HOLD at BOTH N=50 and N=100; controls 0/5
         at both depths. NO CLIFF through N=100 at Haiku (record ≈ 15-20k tokens).
NEXT:    Sonnet + Opus Phase-2 sweeps; in-vivo chains running (arm A inc01 smoke
         passed — note the in-vivo anchor-discipline quote in log-a/inc01.json);
         Phase 3 canonical chain running.

---

STUDY-005
WHEN:    2026-06-09
WHAT:    HARNESS INCIDENT + FIX (Phase 3/4): `go` was never installed in the host
         environment. Caught at canonical-chain quality check (8/8 FAIL with growing
         codebases → suspicious → diagnosed "command not found"). The quality()
         gate asserted execution without validating the executor existed — the
         completion-gate lesson (asserted ≠ executed, F047) applied to OUR OWN
         harness; execution caught what authoring review did not (same class as the
         0.x decay-runner bug, REPRODUCIBILITY.md).
         FIX: Go 1.23.4 installed at a NON-PATH location (~/.local/go-harness);
         harness quality() uses it by absolute path. Experiment sessions remain
         uniformly go-less — symmetric across arms/conditions — RECORDED BOUND:
         all Phase-3/4 session code is written without test execution (sessions see
         "command not found" on go invocations; both arms identically).
         Canonical states re-checked with real Go: S1–S8 ALL PASS build+test —
         Sonnet wrote working code without execution; substrate valid.
NEXT:    Phase 3 measured stages (off ‖ on) launched. Quality counter-metric now
         real for all measured runs.

---

STUDY-006
WHEN:    2026-06-09
WHAT:    Phase 2 OPUS cells scored (60/60, 4 read-passes; fabrication claim
         hand-confirmed: "Idempotency-Key" present in 10/10 no-record arms grepped,
         with explicit provider-dedupe contract assertions). All four rungs CLIMB at
         the frontier:
         R1 — interaction 5/5 HOLD with 5/5 RECONCILE: every arm invokes ADR-038's
         own "documented exception" clause to resolve precedence. R2 — middle 5/5.
         R3 — withrecord 15/15 per-fact, all three ADRs cited. R4 — 5/5 at both
         N=50 and N=100. Controls/floors: 0/5 HOLD everywhere on planted facts.
         TWO MAJOR FINDING CANDIDATES:
         (1) CAPABILITY AMPLIFIES CONFIDENT FABRICATION ABSENT RECORD — Opus
         no-record arms fabricate the idempotency-key safety contract 30/30 across
         rungs (Haiku floors: 2-5/5 wobbling). The strongest model writes the most
         confident wrongness against a non-idempotent endpoint, with comments like
         "the provider must dedupe on that key". Extends SOUL-128's frontier-
         fabricates from erosion to PURE ABSENCE, at scale.
         (2) THE THREE R3 FACTS DISSOCIATE ALONG THE F044 LINE — Opus control/floor
         holds float/integer-money 10/10 UNAIDED (derivable best practice; record
         unnecessary) while token-single-use and no-retry drift 0/10 (unguessable,
         counter-default; record necessary). One vehicle, one model, same arms:
         derivable-regenerates / unguessable-requires-record, demonstrated
         within-subject.
NEXT:    Sonnet Phase-2 sweep (last); then RESULT.md + phase report. In-vivo and
         stream chains running.

---

STUDY-007
WHEN:    2026-06-09 (evening)
WHAT:    RATE-LIMIT STORM (pre-registered stopping-rule case): the subscription
         session limit tripped mid-study ("resets 10:40pm ET" in every stub).
         Blast radius, identified by is_error/stub-grep, NOT by exit codes (the
         sweeps reported rc=0 — exit codes lie about arm validity; the JSON
         is_error field and content are the anchors): in-vivo arm A inc08-12,
         arm B inc07-12, stream off/on-t8, 22 Sonnet Phase-2 arms (2 r3-floor +
         all 20 r4). All valid pre-storm artifacts intact (arm A 7 incs, B 6,
         stream t1-7 both conds, Sonnet 38/60 arms).
         REMEDIATION per protocol: stubs purged, error ledgers archived
         (*.limitstorm1), resumable runners relaunched after live capacity test.
         Sequential integrity of chains preserved — no later increment executed
         before its predecessor (stubs wrote in seconds, repos untouched).
         NOTE for harness doctrine: arm validity must be checked from artifact
         content (is_error, size, sentinel), never from sweep exit codes.
NEXT:    Chains A/B resumed; Sonnet sweep resumed; stream t8 after; then the
         full scoring backlog (Sonnet P2, stream tokens/quality, in-vivo).

---

STUDY-008
WHEN:    2026-06-09
WHAT:    HOOK-SCOPE DISCOVERY (declared post-hoc, pre-scoring): the Body's
         user-global settings run hooks/pre-completion-verify.py on Stop in EVERY
         claude session on this machine. Found via .soul/events.jsonl inside
         stream soul-on sandboxes. Scope verified by reading the hook
         (_is_soul_project: requires witness.md or Soul-marked CLAUDE.md) and by
         artifact absence: NO events log in any off/floor/control sandbox; Phase
         1/2 arms ran in bare /tmp dirs (no CLAUDE.md) — all baselines CLEAN.
         VERDICT: not contamination — fidelity. The completion-gate hook is part
         of the shipped 1.0 system, so its firing (and token cost) belongs in the
         Soul-on/arm-A conditions; the control arms' lack of it is the intended
         manipulation. DECLARED as a pre-registration addendum: "Soul-on includes
         the environment gate hook" + the events.jsonl files are admitted as
         conformance telemetry (gate fired in stream on-t1/t2/t4+; per-arm logs
         to be tabulated at scoring).
         Also noted from stream t1-7 interim: soul-on costs more at every
         position (out-tokens +17%..+169%) EXCEPT t7 (the refactor revisit,
         -8%) — first sub-zero overhead exactly where compounding was predicted;
         t8 decides. Counter-metric: off 7/7 PASS, on 6/7 (on-t2 shipped a
         failing timezone test it could not execute — go-less bound interacting
         with test-writing; single cell, noted).
NEXT:    Await chains/sweep/t8; then score everything; phase reports.
