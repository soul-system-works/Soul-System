# System Version

Current: **0.4.0**

This is the single source of system version. Per-file versions were removed in 0.2.0 — git history and Source footers (`Adopted` / `Status` fields in operations files) cover provenance at finer granularity.

---

## Changelog

| Version | Date | What Changed |
|---|---|---|
| 0.4.0 | 2026-05-21 | **A010 — Coherent Falsehood / Anchor Obligation.** Council synthesis (SOUL-048) over 12 open findings collapsed the verification cluster (F013/F015/F021/F023/F024 + F022 + this session's magnitude claim) into one named failure mode: **Coherent Falsehood** (the claim-level twin of Universe Collapse) with its discipline, the **Anchor Obligation** — any claim about reality (prediction, absence, magnitude, completion) needs an external anchor proportionate to its weight. Operationalized by sharpening the completion gate to name the anchor per claim (de-theaters F022). New: **F025** (second-adapter implementability test). Held: F014/F017 → experiment (SOUL-I011); F006 sharpened to an activation problem. |
| 0.3.0 | 2026-05-20 | **Post-dogfood amendment wave.** Four autonomous test runs (visual, markers, heat, REF-08) harvested into Findings SOUL-F001..F011. First philosophy-level amendments in the system. Accepted: **A003** (Universe Collapse failure mode + outward-reach completion obligation — counters "ratchet not engine"); **A004** (selective role visibility — name the Judge at gate-overrides); **A005** (Frame-as-check when pre-framed; global-invariant completion check — verification vs validation); **A006** (role-set scales to problem size; docstrings as a complementary honesty channel); **A007** (visual / non-automatable Witness → capture + inspect); **A008** (execution topology at the AL gate — single-agent default, multi-agent earns its place; self-contained handoff discipline); **A009** (handoff is self-contained for correctness, not hermetic — refined from the FANOUT multi-agent dogfood). Knowledge-graph memory deferred to a scale trigger (F011). |
| 0.2.0 | 2026-05-19 | Architect role added to Hands. Operations expanded: `code-markers.md`, `adr-format.md`, `AGENTS.md` at root, root `CLAUDE.md` for self-dogfood. New gate: Chesterton's Fence. New Council mode: Pre-Mortem. New conventions: Source Footers, Conventional Commits. External Skills mapping. `/soul-init` slash command. Per-file `Version 1.0/1.1` footers removed. |
| 0.1.2 | 2026-05-15 | Soul 1.2 — Adversary, Critic, Craftsman, The Hands added. Artificer moved to Hands. Versioned filenames removed. |
| 0.1.1 | 2026-05-15 | Soul 1.1 — Artificer role and pairing added |
| 0.1.0 | 2026-05-15 | Initial system — all founding documents |

---

## Identifying Versions

**`@`-import workflow (recommended):** the version is the current state of the source repo — `git log` and `git tag` are authoritative; sync via `git pull`.

**Snapshot install (`install.sh`):** the project carries a `.soul-version` file with the version at install time. Useful for findings to be traced back to the version that produced them.
