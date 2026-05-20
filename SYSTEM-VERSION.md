# System Version

Current: **0.3.0**

This is the single source of system version. Per-file versions were removed in 0.2.0 — git history and Source footers (`Adopted` / `Status` fields in operations files) cover provenance at finer granularity.

---

## Changelog

| Version | Date | What Changed |
|---|---|---|
| 0.3.0 | 2026-05-20 | **Post-dogfood amendment wave.** Four autonomous test runs (visual, markers, heat, REF-08) harvested into Findings SOUL-F001..F011. First philosophy-level amendments in the system. Accepted: **A003** (Universe Collapse failure mode + outward-reach completion obligation — counters "ratchet not engine"); **A004** (selective role visibility — name the Judge at gate-overrides); **A005** (Frame-as-check when pre-framed; global-invariant completion check — verification vs validation). |
| 0.2.0 | 2026-05-19 | Architect role added to Hands. Operations expanded: `code-markers.md`, `adr-format.md`, `AGENTS.md` at root, root `CLAUDE.md` for self-dogfood. New gate: Chesterton's Fence. New Council mode: Pre-Mortem. New conventions: Source Footers, Conventional Commits. External Skills mapping. `/soul-init` slash command. Per-file `Version 1.0/1.1` footers removed. |
| 0.1.2 | 2026-05-15 | Soul 1.2 — Adversary, Critic, Craftsman, The Hands added. Artificer moved to Hands. Versioned filenames removed. |
| 0.1.1 | 2026-05-15 | Soul 1.1 — Artificer role and pairing added |
| 0.1.0 | 2026-05-15 | Initial system — all founding documents |

---

## Identifying Versions

**`@`-import workflow (recommended):** the version is the current state of the source repo — `git log` and `git tag` are authoritative; sync via `git pull`.

**Snapshot install (`install.sh`):** the project carries a `.soul-version` file with the version at install time. Useful for findings to be traced back to the version that produced them.
