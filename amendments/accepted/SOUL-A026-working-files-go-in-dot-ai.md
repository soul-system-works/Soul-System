AMENDMENT ID:    SOUL-A026
DATE:            2026-10-19
WITNESS IDS:     SOUL-191 (ROUTER-LAB kept AI working files in one deletable
                 `.ai/` folder from 2026-09-28; this repo's own layout scan found
                 four non-record files living in `.soul/`).
WHAT CHANGES:    A Working-files paragraph beside Stores: plans, drafts, review
                 output, eval results and scratch go in `.ai/` (created on first
                 use, safe to delete), never in `docs/`, the root or source
                 folders; promoting one to project content is the owner's call;
                 project content never links into `.ai/`. Mirrored in AGENTS.md
                 (the public canonical layer) and docs/using-the-soul.md. The
                 instrument is `/soul-init` step 3e plus tools/layout-cleanup.py:
                 on an already-initialized project it lists misplaced working
                 files, asks per group, moves with `git mv`, and remembers a
                 decline.
WHERE IN SOUL:   operations/CLAUDE.md (the contract) — one paragraph after Stores.
QUESTION ONE:    Evidence — SOUL-191. One adopting project ran the convention for
                 three weeks and recommended it; this repo shows the failure it
                 prevents, the record store accumulating working material
                 (experiments/, vault/, a landscape review, a rendered graph)
                 because nothing said where else it goes. One project is thin;
                 ROUTER-LAB's own write-up said "document it, revisit after 2+
                 projects use `.ai/`". The owner chose to adopt now (2026-10-19).
QUESTION TWO:    Necessity — no rule covers it. Stores says where the durable
                 record lives and is silent on everything else an AI session
                 writes, so plans land in `docs/` and look like project content
                 at the end of a project. A docs-only note would not reach the
                 session that writes the plan; the contract is the always-on
                 layer, and the paragraph is four lines (85 → 90).
QUESTION THREE:  Coherence — it separates class 3 (disposable) from class 2 (the
                 record) rather than extending `.soul/`, so "delete the folder"
                 never needs judgment; `.soul/work/` was weighed and rejected for
                 that reason. No conflict with rule 1: decisions still go to the
                 code site or `docs/adr/`, which are project content. The
                 harness-neutral name matches the Codex direction (SOUL-I063).
STATUS:          Accepted 2026-10-19 — the owner approved the release of the
                 intake-2026-10-19 branch (v2.4.0).

---

**What would make this wrong.** If sessions start writing durable decisions into
`.ai/` because it is the one folder they are told about, the rule has pulled
records out of `.soul/` and ADRs out of `docs/adr/` — the opposite of its intent.
The check is the first milestone cleanup in an adopting project: anything in `.ai/`
the owner refuses to delete is a misfiled record.
