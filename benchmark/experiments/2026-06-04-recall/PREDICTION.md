# Pre-registration — recall / F038 three-arm filler control

**Reconstructed from:** witness `SOUL-134` (pre-registration locked before outputs in the
original run; the standalone-file shape did not yet exist). Faithful to the rule and
prediction recorded there; no fresh lock timestamp (see `../../SCORING.md` §provenance).

**Probe class:** unguessable fact. This is the **clean substance vehicle** — the pair to
`2026-06-04-docs-convention`. The docs probe failed to isolate substance because its answer
was derivable; this probe was designed so generic reasoning gets the trap *confidently
wrong*, so neither re-derivation nor a primed disposition can rescue it.

## Vehicle
The team is standing up batched non-interactive eval runs (`claude -p "<task>" < /dev/null`),
each needing the same shared 1,800-line doctrine file in context. The team lead proposes the
DRY fix: put `@shared/ledger-doctrine.md` in each run's `CLAUDE.md` so the doctrine is
imported by reference. The substance arm carries the recorded fact **F038**: `@`-imports fail
**silently** under `claude -p` — the file never reaches the model, which confabulates
plausible content ~43% of the time; the fix is to inline the content (or
`--append-system-prompt-file`) and run a sentinel quote-back check.

- **avoid-trap** = reject the `@`-import under `-p`; inline / `--append-system-prompt-file`
  / sentinel-verify (the F038 behavior).
- **fall-for-trap** = endorse the `@`-import as a DRY way to load the shared doctrine (the
  generically-plausible default).

## Scoring rule
Read the actual recommendation, NOT keywords — "inline" and "won't resolve" can appear for
the *wrong* reason (path-relativity, a generic fallback) without the F038 silent-fail
knowledge. Score `avoid-trap` iff the recommendation rejects the `@`-import under `-p` on
grounds consistent with the silent-fail behavior. Distinguish path-relativity hedging from
actual F038 knowledge in the read.

## Prediction (as recorded in SOUL-134)
This is the vehicle where the three-arm control should show a **clean isolation**, unlike the
docs probe:

1. **substance (F038 record) ≫ {bare ≈ empty ≈ cohirr ≈ 0}** — the fact is unguessable, so
   the controls cannot reach it; coherent-irrelevant filler is **harmless here** (≈ bare),
   the *opposite* of the docs probe where it primed the answer.
2. **cohirr ≈ bare** — with no derivable answer to prime, the distraction has nothing to push
   toward; its sign should flip to ~neutral.
3. **The frontier may FABRICATE the wrong fact** — without F038, a capable model is expected
   to *confidently assert* that `@`-imports resolve under `-p` like interactive (the
   confident-fabrication signature; watch for it specifically).

## Falsifier
If `bare`/`cohirr`/`empty` reach avoid-trap at a meaningful rate, the fact is *not*
unguessable (the control would show the docs-style derivability instead), and the clean-
isolation claim fails. A `cohirr` that primed avoid-trap (as it did on docs) would mean the
distraction sign is not content-dependent.

## Design
n=5 × {Haiku-4.5 (claude-haiku-4-5-20251001), Sonnet-4.6 (claude-sonnet-4-6)} × 4 arms = 40.
Length-matched injected context (empty 198w / cohirr 198w / substance 184w). Reuses the docs
probe's `empty`/`cohirr` arms. F038: inlined, no `@`-import (the very fact under test).
