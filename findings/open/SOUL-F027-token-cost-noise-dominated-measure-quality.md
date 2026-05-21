```
FINDING ID:      SOUL-F027
DATE:            2026-05-21
WITNESS IDS:     SOUL-053 (run 1), SOUL-054 (run 2 + quality check).
WHAT:            METHODOLOGICAL finding from running the stream experiment twice. At
                 n=1 per cell, per-task token cost is NOISE-DOMINATED: a single agent's
                 thrash (one off run spent +10k re-discovering a CLI it had let drift
                 across two files) exceeded the entire systematic on/off gap (~1-2k).
                 Run 1 reported on +8.4%; run 2 (thin cursor) reported on -8.2% — but
                 -1% (parity) once that one outlier is removed. Two runs, opposite
                 headlines: the treatment effect is within the variance. The MORE
                 TELLING axis was quality/drift, not tokens — the no-structure (off)
                 path drifted into a dual-entry-point mess AND shipped a real defect (a
                 `convert` command unreachable via the standard entry point), while the
                 cursor-guided (on) path stayed consistent and functional.
WHY NOT YET AMENDMENT:  A measurement-method lesson, not a doctrine change. It says:
                 (a) any token-economics claim needs n>1 per cell (replication) to rise
                 above per-run variance; (b) score QUALITY / drift / defects, not only
                 tokens — the bet's real mechanism is drift-prevention, which shows in
                 quality before cost; (c) the research's variance/reproducibility
                 warnings bind here. Gate any future token claim on it; feeds the
                 measurement spec and SOUL-I011.
FILED BY:        Archivist (from the token-economics experiment)
RELATED:         [[SOUL-F026]] (the retrieval-mode finding it qualifies), [[SOUL-I005]],
                 [[SOUL-I011]], the measurement spec
STATUS:          Open — binds future runs (n>1 + quality scoring before any token claim).
```
