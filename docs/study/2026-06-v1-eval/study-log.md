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
