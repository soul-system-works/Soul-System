# Result — longitudinal-decay depth-burial probe (2026-06-04)

> **Reproduced 2026-06-05** (full rerun, n=5, read-scored): the headline result held. Full cross-experiment report: [`../../REPRODUCIBILITY.md`](../../REPRODUCIBILITY.md) (witness SOUL-143).

**Source of record:** witness `SOUL-125`. Pre-registration in `PREDICTION.md`. Depth-burial
variant of the carry probe; reuses the SOUL-123 FACT chain (D = ADR-001, no-auto-retry of
non-idempotent payment endpoints).

The headline: **no decay cliff through N=20** (≈20 sessions, ≈14k-char log) at **both**
capabilities. The carry is depth-robust — buried under 20 intervening ADRs with context C
gone, D still cites ADR-001 and fails fast.

## Outcome by depth (HOLD = no retry loop, fail-fast; DRIFT = retry loop)

| depth N | with-record (HOLD) | control, no D (DRIFT) | n |
|---|---|---|---|
| N=5  | 3/3 HOLD | DRIFT | n=3 (locate, Haiku) |
| N=10 | 3/3 HOLD | DRIFT | n=3 (locate, Haiku) |
| N=20 | 5/5 HOLD (both models) | 5/5 DRIFT (both models) | n=5 (confirm, Haiku + Sonnet) |

(N=1 = 5/5 HOLD both models, from SOUL-123.) with-record HOLDs at every depth; the
length-matched control DRIFTs at every depth.

## Findings

1. **No decay cliff through N=20.** Buried under 20 intervening ADRs with context C absent, D
   still cites ADR-001 and fails fast, 5/5 at the confirm depth on both models. The HOLD is
   **D-being-findable, not context volume** — the equal-length control (same length, no D)
   drifts at every depth, so generic long-context degradation is ruled out as the driver.

2. **Frontier replication at depth.** Sonnet control (no D), 5/5, builds a retry loop **and
   invents an `Idempotency-Key`** — reasoning that "the provider deduplicates, so retries are
   safe." This is the precise dangerous drift SOUL-123 found at the floor, now reproduced at
   burial depth 20; the provider has no such support (that fact lives in D, which the control
   lacks). With-record Sonnet often **explicitly rejects** this path.

3. **Placement.** Climbs the rung F044 named sharpest — decay over a long record. The
   accumulating record is depth-robust: the carry does not degrade with burial through 20
   sessions.

## Prediction scorecard (PREDICTION.md)

- Depth-robust carry → **confirmed**: with-record HOLDs at N=5 (3/3), N=10 (3/3), N=20 (5/5
  both models).
- Control DRIFTs at every depth → **confirmed**: equal-length, no-D control drifts including
  N=20 5/5 both models — isolating findability from generic degradation.
- Decay cliff (falsifier) → **did not occur** through N=20; the carry held.

## Verdict

Depth-burial rung **climbed** through N=20 at both capabilities. Resolved (decisive within
scope). The carry survives a long record; the HOLD tracks D's findability, not record volume.

## Bounds (Skeptic)

- D sits at the **primacy** position (oldest / first ADR — a privileged slot); **D-in-the-
  middle is untested**.
- Single linear log of short, uniform ADRs.
- N=20 was **deliberately not pushed deeper** — N=40–80 is a context-*capacity* test, a
  different question.
- Still open: **erosion** decay (D compressed by a later consolidation) and **many
  interacting decisions** (a later entry reinforcing or **contradicting** D) — neither tested
  here.
- The locate-ladder depths (N=5, N=10) are **n=3**; only the N=20 confirm is **n=5**.

**Raw arms gitignored** (`arms/` is regenerable via `run.sh`). Models:
claude-haiku-4-5-20251001, claude-sonnet-4-6.
