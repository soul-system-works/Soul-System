# Structural Audit — Soul-Console v1

**Date:** 2026-05-27
**Driver:** SOUL-087 `/soul-council` convening, Thread 2 (reshape).
**Witness anchor:** SOUL-087.
**Criterion (locked at SOUL-087):** Stable Soul-Console v1 = each of three live structural seams (directory layout / record-type taxonomy / doctrine-layer boundaries) is either **RESOLVED** (decision committed to seed / mind / an ADR) or **EXPLICITLY DEFERRED** with criteria for resolution.

## What this audit is

**Architect-led per-boundary audit.** Per-boundary catches structural drift; per-item only catches surface bloat (SOUL-087 reshape from Steward per-item → Architect per-boundary).

**One-session output-only beat.** This document produces decisions; it does NOT delete or move anything. Retire-now and move-to-X decisions await **explicit per-item Body sign-off** in a follow-up beat.

**Decision shape per item:**
- **KEEP-IN-PLACE** — fits the rule.
- **MOVE-TO-X** — belongs elsewhere; destination flagged.
- **RETIRE-NOW** — propose deletion (Body sign-off required).
- **DEFER-WITH-CRITERIA** — known mismatch; resolution criteria documented.

**Roles in this audit:** Architect leads. Steward second voice. Cartographer keeps the map. Archaeologist guards against speedrun-deletion (the-commons.md verification at SOUL-087 was the dogfood example).

**What this audit does NOT do:**
- Edit the seed, mind.md, or philosophy text. Doctrine-text changes happen in a separate beat.
- Make calls requiring domain expertise outside the chamber (some items land DEFER-WITH-CRITERIA on purpose).
- Touch CONTRIBUTING.md / README.md content-discrepancies. Those are content updates, not structural; flagged here for separate beats.

---

## Section 1 — Directory layout

### The rule (proposed)

Each top-level location has a **single purpose** and a **rule for what belongs there**. Items that fit the rule KEEP-IN-PLACE; misfits get MOVE / RETIRE / DEFER markers.

### 1.1 Root-level live records (always-on doctrine + ratchet)

**Rule:** Files at the repo root are either (a) entry-point files the Claude Code harness loads (`CLAUDE.md`), (b) always-on auxiliary doctrine loaded by the seed (`mind.md`), or (c) live ratchet records the seed references by name (`witness.md`, `ideas.md`). No procedure, no specs, no on-demand depth at root.

| Item | Lines | Decision | Note |
|---|---|---|---|
| `CLAUDE.md` | (small) | KEEP-IN-PLACE | Seed entry. @-imports `operations/CLAUDE.md` + `mind.md`. |
| `mind.md` | ~190 | KEEP-IN-PLACE | Always-on project rules. Per `docs/specs/2026-05-26-the-mind-design.md`. |
| `witness.md` | 2961 | KEEP-IN-PLACE | Backward record (the ratchet's left-hand side). |
| `ideas.md` | 1078 | KEEP-IN-PLACE | Forward record (the ratchet's right-hand side). |

### 1.2 Root-level public docs (the contribution surface)

**Rule:** Each public-doc file at root has a single audience-purpose (orient newcomers, name governance, describe contribution shape, name the version, license).

| Item | Decision | Note |
|---|---|---|
| `LICENSE` | KEEP-IN-PLACE | Standard. |
| `README.md` | KEEP-IN-PLACE (structural) | **CONTENT DRIFT:** says "twelve symbolic voices"; actual chamber is 13 (8 Magistrates + 3 Tribunes + 2 Censors). Flag for content-update beat — not structural. |
| `AGENTS.md` | KEEP-IN-PLACE | Tool-agnostic entry point (agents.md cross-vendor convention). Explicitly named in operations/CLAUDE.md header as the rename target. |
| `CONTRIBUTING.md` | KEEP-IN-PLACE (structural) | **MAJOR CONTENT DRIFT:** taxonomy maps "Findings → logs/", "Skills → skills/", "Registry Entries → registry/" — all three are empty directories whose actual artifacts live elsewhere or don't yet exist (see 1.7). Flag for content-update beat synchronous with logs/skills/registry decisions. |
| `GOVERNANCE.md` | KEEP-IN-PLACE | References `operations/council-synthesis.md` as the amendment process. Confirms council-synthesis.md is doctrine, not retire candidate. |
| `SYSTEM-VERSION.md` | KEEP-IN-PLACE | Single source of system version (per-file versioning removed in 0.2.0). |

### 1.3 Root-level scaffolding (build/install/diagrams)

**Rule:** Tool scripts, diagrams, and other root-level scaffolding that serves the public-doc layer.

| Item | Decision | Note |
|---|---|---|
| `install.sh` | **DEFER-WITH-CRITERIA** | Claims `SYSTEM_VERSION="0.3.0"`; current is 0.5.1. Known-stale since 0.4.3 (2026-05-22). Original deferral: YAGNI multi-machine path. **Criteria to act:** (i) someone reports needing a multi-machine install → un-defer + update; (ii) script proves never-used over 6 more months → RETIRE-NOW. Currently neither. |
| `architecture.svg` | KEEP-IN-PLACE | Referenced from README.md; standalone diagram. |

### 1.4 `commands/` — Body-invoked instruments

**Rule:** `commands/<name>.md` per instrument. Each: (i) named `soul-X.md`, (ii) carries frontmatter `description:` ≤100 chars (per `/soul-help` cap), (iii) symlinked to `~/.claude/commands/<name>.md` (per F029 live-reference), (iv) executes a Soul-System obligation.

**Inventory (16 commands):** soul-ask-body, soul-council, soul-distill, soul-expand, soul-explain, soul-finding, soul-handoff, soul-help, soul-idea, soul-init, soul-resume, soul-roles, soul-skill, soul-tasks, soul-verify, soul-witness.

| Decision | Items |
|---|---|
| KEEP-IN-PLACE | All 16 fit the rule. |

**Per-instrument empirical use (deferred to a separate metrics beat):** SOUL-087 surfaced near-zero use of recent Cluster 1 instruments (`/soul-roles` 1× / `/soul-council` 2× counting SOUL-087 / `/soul-ask-body` 0×). Not a structural problem; dosage problem. Out of audit scope. **Surface this concern in a follow-up `/soul-distill` or a future `/soul-status` beat.**

### 1.5 `operations/` — on-demand doctrine + procedure + format specs

**Rule (currently fuzzy — this is a live seam).** Inspection shows three sub-classes living flat:

- **DOCTRINE-ABOVE-INSTRUMENT** — text the seed @-imports or directly references: `CLAUDE.md` (the seed itself), `council-synthesis.md`, `completion-gate.md`, `experiment-harness.md`.
- **FORMAT SPECS** — define record shapes used elsewhere: `witness-log-format.md`, `adr-format.md`, `code-markers.md`, `event-standard.md`.
- **PROCEDURE / SETUP** — how-to docs for specific situations: `autonomous-session-template.md`, `reference-repository.md`.

**Decision — propose RESOLVED via documented sub-classification, not via reorganization.** The flat structure works if the rule is named. Proposed rule: *operations/ holds on-demand DOCTRINE-ABOVE-INSTRUMENT, FORMAT SPECS, and PROCEDURE docs in a flat structure; each file's first paragraph names its sub-class.* This is cheaper than moving files into subdirectories and avoids URL/import churn.

| Item | Lines | Sub-class | Decision | Note |
|---|---|---|---|---|
| `CLAUDE.md` | 258 | DOCTRINE (seed) | KEEP-IN-PLACE | The seed. Header documents AGENTS.md-rename-deferred. |
| `adr-format.md` | 111 | FORMAT SPEC | KEEP-IN-PLACE | ADRs not yet in active use — but format defined; no harm. |
| `autonomous-session-template.md` | 269 | PROCEDURE | **DEFER-WITH-CRITERIA** | Likely pre-dates `/soul-handoff` + `/soul-resume`. **Criteria to act:** check `grep -r autonomous-session-template` across project. If zero references AND no instrument uses it AND the procedure-shape it describes is now in commands/, RETIRE-NOW (with Body sign-off). |
| `code-markers.md` | 93 | FORMAT SPEC | KEEP-IN-PLACE | Marker discipline (A011) referenced from doctrine. |
| `completion-gate.md` | 130 | DOCTRINE | **DEFER-WITH-CRITERIA** | Supersession question: is it now subsumed by `/soul-verify` + the pre-completion hook? **Criteria to act:** verify whether seed §Mandatory Gates still cites it vs the hook/command. If the runtime gate is the hook + command and the operations doc is only historical context, RETIRE-NOW or move to a "doctrine-superseded" subdirectory. |
| `council-synthesis.md` | 350 | DOCTRINE | KEEP-IN-PLACE | GOVERNANCE.md references this for the amendment process. Different layer from `/soul-council` (authority vs instrument). |
| `event-standard.md` | 202 | FORMAT SPEC | KEEP-IN-PLACE | `events.jsonl` is actively firing (gate.completion.flagged today). Format earns its keep. |
| `experiment-harness.md` | 123 | DOCTRINE | KEEP-IN-PLACE | Referenced from seed §Mandatory Gates (SOUL-F038-anchored). Active obligation. |
| `reference-repository.md` | 173 | PROCEDURE | **DEFER-WITH-CRITERIA** | Describes how `references/` is populated. **Criteria to act:** verify whether `references/INDEX.md` already documents the same procedure inline. If yes, RETIRE-NOW + consolidate to references/. If no, KEEP. |
| `witness-log-format.md` | 210 | FORMAT SPEC | KEEP-IN-PLACE | Witness format spec; cited from `/soul-witness` + record format. |

### 1.6 `philosophy/` — on-demand depth

**Rule:** Files that illuminate or carry the Soul's philosophy. Not procedure, not format specs, not instruments. Slow-growth, citation-heavy.

| Item | Lines | Decision | Note |
|---|---|---|---|
| `the-soul.md` | 707 | KEEP-IN-PLACE | The governing philosophy. On-demand per SOUL-033. |
| `the-commons.md` | 75 | KEEP-IN-PLACE | Outside wisdom. Verified at SOUL-087: Entry 001 sources mind rule 11 + seed §On This Document; Entry 002 shaped CLAUDE.md @-import design. Slow-growth by design. |

### 1.7 `docs/{experiments,plans,specs,audits}/` — design-doc records

**Rule:** Design-doc-shape artifacts. Build-once-then-stable (not live records). Each subdirectory holds one design-doc-kind.

| Subdir | Contents | Decision |
|---|---|---|
| `docs/specs/` (9 files) | Design specs for instruments (some Built, some Draft). | KEEP-IN-PLACE. |
| `docs/plans/` (1 file) | Implementation plans bridging spec → code. | KEEP-IN-PLACE. |
| `docs/experiments/` (2 files) | Measurement / empirical investigation records. | KEEP-IN-PLACE. |
| `docs/audits/` (1 file — this one) | **NEW: review-time audit records.** Fourth design-doc shape. | KEEP-IN-PLACE (new) — this audit itself instantiates the type. |

### 1.8 `councils/` — Council convening detail files

**Rule:** Each Council convening writes (a) a pointer entry in `witness.md` and (b) a detail file here under `councils/SOUL-CCC-<kebab-slug>.md`. The pointer keeps witness scannable; the detail keeps the convening reproducible (pointer+detail D4 shape).

| Item | Decision |
|---|---|
| SOUL-080-cluster-1-review-arc.md | KEEP-IN-PLACE. |
| SOUL-085-f014-confirmed-what-now.md | KEEP-IN-PLACE. |
| SOUL-087-stable-v1-and-consolidation.md | KEEP-IN-PLACE. |

**Relation to ratchet:** councils/ files sit **alongside** the ratchet, not within it. The ratchet (idea → witness → finding → amendment) is backward-observation graduating to doctrine. Council convenings are forward-deliberation events that PRODUCE witness pointers (and may produce finding/amendment graduations downstream), but the convening detail itself is not a ratchet record — it's a deliberation record. **This is the cleanest answer to SOUL-087's "where do councils/ files land?" question.**

### 1.9 `findings/{open,closed}/` and `amendments/{accepted,proposed,returned}/`

**Rule:** Ratchet records. Standardized IDs (`SOUL-F###`, `SOUL-A###`). Lifecycle directories.

| Subdir | Contents | Decision |
|---|---|---|
| `findings/open/` | 14 files | KEEP-IN-PLACE. |
| `findings/closed/` | 24 files | KEEP-IN-PLACE. |
| `amendments/accepted/` | 13 files | KEEP-IN-PLACE. |
| `amendments/proposed/` | 0 files | KEEP-IN-PLACE. Lifecycle scaffolding (empty is OK). |
| `amendments/returned/` | 0 files | KEEP-IN-PLACE. Lifecycle scaffolding. |

### 1.10 `logs/`, `skills/`, `registry/` — the empty triple (MAJOR SEAM)

**The seam:** CONTRIBUTING.md row 13–20 maps:
- Findings → `logs/`
- Skills → `skills/`
- Registry Entries → `registry/`

All three directories are EMPTY. Findings actually live in `findings/`. Skills produced by `/soul-skill` are project-local SKILL.md files, NOT here. Registry has never received a contribution.

**Reading 1: All three are stale aspiration. RETIRE-NOW + update CONTRIBUTING.md.**
**Reading 2: All three are public-facing contribution channels awaiting first external contribution.**
**Reading 3: Each has a different story; case-by-case.**

**Per-item decision:**

| Item | Decision | Note |
|---|---|---|
| `logs/` | **RETIRE-NOW (with Body sign-off)** | CONTRIBUTING.md "Findings" row points here, but actual findings live in `findings/`. CONTRIBUTING.md content is stale, not the structure. Delete `logs/` + update CONTRIBUTING.md row to point to `findings/` + `witness.md` (the actual raw-observation record). No information lost. |
| `skills/` | **DEFER-WITH-CRITERIA** | `/soul-skill` writes project-local SKILL.md (per the command file). This `skills/` directory is for *upstream-contributed* skills. **Criteria to act:** (i) first upstream skill contribution arrives → un-defer, keep + document; (ii) 6 months with no contribution → RETIRE-NOW + update CONTRIBUTING.md to remove the row. Sub-recommendation: add a `skills/README.md` explaining the intended use, so the empty directory isn't ambiguous. |
| `registry/` | **DEFER-WITH-CRITERIA — backfill candidate** | This is a real, not-yet-honored channel. Multiple dogfood projects exist (REF-09, REF-04, REF-03, REF-01, the blog, REF-02) that should have registry entries per CONTRIBUTING.md. **Criteria to act:** schedule a backfill beat (1 session) to write registry entries for the existing dogfood projects. Don't retire — populate. |

### 1.11 `references/` — Researcher workspace

**Rule:** Outside-knowledge artifacts gathered by Researcher beats. `INDEX.md` is the gate; surveys + JSON snapshots are the artifacts.

| Item | Decision | Note |
|---|---|---|
| `references/` (INDEX + 4 surveys + JSON) | KEEP-IN-PLACE. | Active. SOUL-I035 (BMAD Researcher beat) will add to it. |

### 1.12 `hooks/` and `.claude/` — harness wiring

| Item | Decision | Note |
|---|---|---|
| `hooks/pre-completion-verify.py` | KEEP-IN-PLACE | Firing actively (events.jsonl confirms gate.completion.flagged today). |
| `hooks/resume-cost.py` | KEEP-IN-PLACE | Resume-cost telemetry. |
| `.claude/settings.local.json` | KEEP-IN-PLACE | Harness-specific wiring. |

### 1.13 `.soul/` — runtime state

**Rule:** Volatile/runtime state. Gitignored. Read by instruments; written by hooks/commands.

| Item | Decision |
|---|---|
| `.soul/events.jsonl` | KEEP-IN-PLACE. |
| `.soul/handoff.md` | KEEP-IN-PLACE. |
| `.soul/role-queries.jsonl` | KEEP-IN-PLACE. |

### Section 1 summary

| Decision | Count | Items |
|---|---|---|
| KEEP-IN-PLACE | most | all-fits-rule majority |
| RETIRE-NOW (Body sign-off) | 1 | `logs/` |
| DEFER-WITH-CRITERIA | 5 | `install.sh`, `operations/autonomous-session-template.md`, `operations/completion-gate.md`, `operations/reference-repository.md`, `skills/`, `registry/` (registry as backfill, not retirement) |
| MOVE-TO-X | 0 | (no items currently misplaced) |
| Content-drift flags (not structural) | 2 | `README.md` "twelve voices" stale; `CONTRIBUTING.md` taxonomy stale |

---

## Section 2 — Record-type taxonomy

### The rule (proposed)

Every artifact the system writes belongs to one of **four record-kinds**. Each kind has an ID convention, a lifecycle, and a relationship to the ratchet.

### 2.1 Ratchet records (earned graduations)

The core spine: **idea (forward) → witness (backward) → finding (earned graduation) → amendment (doctrine change).**

| Kind | File(s) | ID | Lifecycle |
|---|---|---|---|
| Idea | `ideas.md` | `SOUL-I###` | Raw → Maturing → Graduated [to F###] / Dropped |
| Witness | `witness.md` | `SOUL-###` | Append-only, sequential, I027 re-read-verify |
| Finding | `findings/{open,closed}/SOUL-F###-*.md` | `SOUL-F###` | open → closed |
| Amendment | `amendments/{proposed,accepted,returned}/SOUL-A###-*.md` | `SOUL-A###` | proposed → accepted / returned |

### 2.2 Deliberation records (forward-deliberation, alongside ratchet)

Council convenings: events that may *produce* ratchet entries (witness pointer; downstream finding/amendment) but are themselves deliberation records.

| Kind | File(s) | Anchored by |
|---|---|---|
| Council convening detail | `councils/SOUL-CCC-<slug>.md` | Witness pointer (CCC = witness ID) |

**Relation:** alongside, not within. Each convening produces a witness pointer; the detail file is the deliberation's durable form. Mandatory both-outputs per `/soul-council` step 7.

### 2.3 Design-doc records (build-once-then-stable)

| Kind | File(s) | Purpose |
|---|---|---|
| Spec | `docs/specs/YYYY-MM-DD-*.md` | Design-spec for an instrument or feature |
| Plan | `docs/plans/YYYY-MM-DD-*.md` | Implementation plan bridging spec → build |
| Experiment | `docs/experiments/YYYY-MM-DD-*.md` | Empirical investigation record |
| Audit | `docs/audits/YYYY-MM-DD-*.md` | **NEW kind, this audit instantiates it.** Review-time structural assessment. |

**Relation to ratchet:** alongside. Design docs may anchor amendments (a spec cites the witness/finding that motivated it) but aren't ratchet records.

### 2.4 Doctrine records (the philosophy itself)

| Kind | File(s) | Activation |
|---|---|---|
| Seed | `CLAUDE.md` + @-import `operations/CLAUDE.md` + `mind.md` | Always-on |
| Mind | `mind.md` | Always-on (after seed) |
| Philosophy | `philosophy/the-soul.md`, `philosophy/the-commons.md` | On-demand depth |
| Process doctrine | `operations/{council-synthesis,completion-gate,experiment-harness}.md` | On-demand, cited from seed |
| Format spec | `operations/{witness-log-format,adr-format,code-markers,event-standard}.md` | On-demand, defines artifact shapes |
| Procedure | `operations/{autonomous-session-template,reference-repository}.md` | On-demand, situational |

### 2.5 Public-doc records (the contribution surface)

| Item | Purpose |
|---|---|
| `README.md` | Orient newcomers |
| `AGENTS.md` | Tool-agnostic entry point (cross-vendor convention) |
| `CONTRIBUTING.md` | Contribution shape |
| `GOVERNANCE.md` | Maintainer authority + amendment process |
| `SYSTEM-VERSION.md` | Version + changelog |
| `LICENSE` | Standard |

### 2.6 Reference/scaffolding records

| Kind | File(s) |
|---|---|
| Outside knowledge | `references/INDEX.md` + survey files + `references.json` |
| Registry entry | `registry/<project>.md` (none yet — see 1.10 deferred) |
| Upstream-contributed skill | `skills/<skill>.md` (none yet — see 1.10 deferred) |
| Hook | `hooks/<name>.py` |
| Diagram | `architecture.svg` |
| Installer | `install.sh` |

### 2.7 Runtime state

| Kind | File(s) |
|---|---|
| Handoff cursor | `.soul/handoff.md` |
| Event stream | `.soul/events.jsonl` |
| Role-query log | `.soul/role-queries.jsonl` |
| Harness settings | `.claude/settings.local.json` |

### Section 2 summary

**The record map is complete and consistent.** Each artifact has a kind; each kind has a rule and a relationship to the ratchet. The previously-ambiguous question — *where do councils/ files fit?* — has a clear answer: deliberation records alongside the ratchet. **Same answer for design-docs.** Both PRODUCE ratchet entries; neither IS one.

The only weakness: `skills/` and `registry/` are *named kinds* whose files don't exist. Section 1 already deferred these with criteria.

---

## Section 3 — Doctrine-layer boundaries

### The rule (proposed)

Doctrine sits at **three activation tiers**:

1. **ALWAYS-ON** — loaded every session before any problem is stated. Hard token budget. Universal doctrine (the seed) + project-specific doctrine (the Mind).
2. **ON-DEMAND DEPTH** — full philosophy + process doctrine + format specs. Read when needed.
3. **INVOKED** — commands the Body fires (`/soul-*`).

The boundary rules:

- **ALWAYS-ON gets only what must fire at every session.** SOUL-033 established the hard budget; mind rule 5 ("never always-on past description budget") encodes it.
- **ON-DEMAND DEPTH carries detail the always-on layer references.** If a process is described in always-on text but the *how* lives elsewhere, the elsewhere is on-demand depth.
- **INVOKED is the surface the Body actually drives.** Commands enact obligations; doctrine names them.

### 3.1 Assignments

| Layer | Where it lives | Files |
|---|---|---|
| ALWAYS-ON (universal) | seed | `CLAUDE.md` → @-imports `operations/CLAUDE.md` |
| ALWAYS-ON (project) | mind | `mind.md` |
| ON-DEMAND DEPTH (philosophy) | philosophy/ | `the-soul.md`, `the-commons.md` |
| ON-DEMAND DEPTH (process doctrine) | operations/ DOCTRINE-class | `council-synthesis.md`, `completion-gate.md`, `experiment-harness.md` |
| ON-DEMAND DEPTH (format specs) | operations/ FORMAT-SPEC-class | `witness-log-format.md`, `adr-format.md`, `code-markers.md`, `event-standard.md` |
| ON-DEMAND DEPTH (procedure) | operations/ PROCEDURE-class | `autonomous-session-template.md`, `reference-repository.md` |
| INVOKED | commands/ | 16 `/soul-*` commands |

### 3.2 Boundary blurs (and decisions)

**Blur 1: `operations/CLAUDE.md` IS the seed but lives in `operations/`.**
- Reading: the file is structurally always-on (it's @-imported by root `CLAUDE.md`), but lives in operations/ because of the framework's history (AGENTS.md convention came later).
- Decision: **DEFER-WITH-CRITERIA.** The header documents the rename-deferred state. Criteria to act: when AGENTS.md adoption matures across the broader ecosystem (criterion already named in the file), move the seed to root as `CLAUDE.md` or split-and-symlink. **No structural action this beat.**

**Blur 2: `operations/` mixes three sub-classes (doctrine / format-spec / procedure).**
- Section 1.5 proposed: **RESOLVED via documented sub-classification, not reorganization.** Each operations file's first paragraph names its sub-class. Flat structure stays; rule gets named.
- Decision: **propose this as an AMENDMENT** to seed §Source Footers — extend footers with a `Sub-class:` field for operations/ files. Cheap; respects the on-demand layer.

**Blur 3: `completion-gate.md` (operations, 130 lines) vs `/soul-verify` (commands, 67 lines) vs `hooks/pre-completion-verify.py`.**
- Same obligation, three artifacts at three layers (doctrine / instrument / automation).
- Decision: **DEFER-WITH-CRITERIA.** Investigate whether the operations doc has unique content not in the command + hook. If yes → KEEP-IN-PLACE. If no → RETIRE-NOW or condense to a pointer. Linked to Section 1.5 DEFER on this file.

**Blur 4: `philosophy/the-commons.md` is tended by Seer + Archaeologist; no instrument writes to it.**
- The file is slow-growth-by-design (verified at SOUL-087). Body-tended.
- Decision: **propose a soft-instrument** — `/soul-commons-entry` (low priority, captured-only-if-needed). Until then, manual edits are the channel. **Not retire-now.** No action this beat; captured as candidate idea if Body wants it.

### 3.3 Per-layer token budget (audit-time measurement)

Always-on at session start (the budget that matters):

| Layer | File | Lines | Approx tokens |
|---|---|---|---|
| Universal doctrine (the seed) | `operations/CLAUDE.md` | 258 | ~3000 |
| Project doctrine (the Mind) | `mind.md` | ~190 | ~2400 |
| **Subtotal — always-on doctrine** |  | **~448** | **~5400** |
| Skill descriptions (16 commands × ~100 chars) | various |  | ~1600 chars / ~400 tokens |
| **Approximate total always-on** |  |  | **~5800 tokens** |

**Reference points:**
- SOUL-033 retired `the-soul.md` (~700 lines / ~8500 tokens) from always-on because it was too heavy.
- Current ~5800 tokens is within budget but trending up. mind.md has grown since 0.5.0; seed has grown by A012/A013.
- **Soft cap recommendation:** 8000 tokens combined always-on. Beyond that, distill or retire.

### Section 3 summary

**Three boundary blurs documented:**
1. `operations/CLAUDE.md` location — DEFER (rename pending AGENTS.md adoption).
2. `operations/` sub-class mixing — RESOLVED via documented sub-classification (proposed amendment).
3. `completion-gate.md` triple-layer overlap — DEFER (investigate uniqueness).

**Token budget healthy** (~5800 always-on tokens; soft cap proposed 8000). No always-on bloat alarm yet, but mind.md is the growth-watch candidate.

---

## Closing — decisions, sign-offs, and follow-up beats

### Decisions requiring Body sign-off (per-item)

These four items the audit recommends acting on. **Per-audit-contract, each retire-now decision needs explicit Body confirmation.**

| Item | Recommended action | Risk if wrong |
|---|---|---|
| `logs/` (empty) | RETIRE-NOW + update CONTRIBUTING.md row to point to `findings/` + `witness.md` | Low — no information loss; CONTRIBUTING.md already mis-points |
| `operations/autonomous-session-template.md` | DEFER first; investigate references; if none, RETIRE-NOW in follow-up beat | Low — file is 269 lines but is likely doctrinally orphaned |
| `operations/completion-gate.md` | DEFER first; investigate uniqueness vs `/soul-verify` + hook; possibly RETIRE-NOW | Medium — risk losing doctrine-rationale if uniqueness exists |
| `operations/reference-repository.md` | DEFER first; verify against `references/INDEX.md`; possibly RETIRE-NOW or consolidate | Low |

### Decisions deferred with explicit criteria

| Item | Criteria to act |
|---|---|
| `install.sh` stale-version | Someone reports multi-machine need → un-defer + update; OR 6 more months no use → RETIRE-NOW |
| `skills/` empty | First upstream contribution → keep + document; OR 6 months no contribution → RETIRE-NOW + update CONTRIBUTING.md |
| `registry/` empty | **Backfill candidate** — schedule 1-session beat to write entries for existing dogfood projects (REF-09, REF-04, REF-03, REF-01, blog, REF-02) |
| `operations/CLAUDE.md` location | AGENTS.md ecosystem adoption matures → rename to root |

### Content-drift flags (not structural — separate beats)

| File | Drift |
|---|---|
| `README.md` | "twelve symbolic voices" — actual count 13. Update or anchor the count. |
| `CONTRIBUTING.md` | Taxonomy rows mis-point to empty dirs (`logs/`, `skills/`, `registry/`). Update synchronous with logs/skills/registry decisions. |

### Proposed amendments (chamber follow-ups)

1. **A014 candidate — Operations sub-classification footer field.** Extend seed §Source Footers with optional `Sub-class:` (DOCTRINE / FORMAT-SPEC / PROCEDURE) for operations/ files. Documents the boundary rule named in Section 1.5 / 3.2 Blur 2.
2. **A015 candidate — Audit as record-kind.** Acknowledge `docs/audits/` in the seed and mind.md as a fourth design-doc kind alongside specs/plans/experiments.

Both are low-controversy and can be batched into a single amendment beat after this audit lands.

### Discharges

- **SOUL-087 Thread 2 (reshape)** — discharged. Architect-led per-boundary audit produced output document with decisions.
- **SOUL-087 criterion (locked)** — each live seam either RESOLVED or DEFERRED-WITH-CRITERIA. Tally:
  - Directory layout: 95%+ KEEP-IN-PLACE; 1 RETIRE-NOW (logs/); 5 DEFER-WITH-CRITERIA. **RESOLVED for v1 criterion.**
  - Record-type taxonomy: complete map; councils/ + audits/ placed; skills/ + registry/ are named kinds awaiting first instances. **RESOLVED for v1 criterion.**
  - Doctrine-layer boundaries: three blurs each with decision (DEFER / RESOLVED-via-amendment / DEFER). **RESOLVED for v1 criterion** (all blurs have a decision, even if the decision is "defer with named criteria").
- **F039 discipline applied** — `wc -l` will anchor this audit document at write-time.

### What's NOT discharged

- **`/soul-status` re-evaluation (SOUL-087 Thread 3)** — contingent on this audit's evidence. The audit confirms three thin instruments (`/soul-tasks`, `/soul-roles`, `/soul-explain`) each carry distinct contracts; the structural case for aggregation is weak. **Provisional decision: keep separate.** Body confirms at follow-up.
- **Per-instrument dosage metric** — out of audit scope. Captured concern for a future `/soul-distill` or status beat.
- **Empirical activation (Skeptic's original criterion b)** — deferred at SOUL-087 in favor of structure-gate. Remains a useful metric to revisit at SOUL-150.

### Recommended next beats

1. **Body reviews this audit** (the immediate gate).
2. **Retire-now beat** — single session: delete `logs/`, update CONTRIBUTING.md (rows + reflecting registry/skills decisions), commit.
3. **Operations DEFER triple** — single session: investigate `autonomous-session-template.md`, `completion-gate.md`, `reference-repository.md` references; act on findings.
4. **Amendment batch** — single session: propose A014 (sub-class footers) + A015 (audits-as-record-kind).
5. **Registry backfill** — single session: write registry entries for existing dogfood projects.

Beats 2–5 are independent; can be sequenced however Body prefers. **Total estimated effort: ~3–4 sessions to reach v1-stable structure.**

---

**Source:** SOUL-087 `/soul-council` Thread 2 reshape. First instance of the `docs/audits/` record-kind. **Authored:** 2026-05-27. **Status:** Output-only; per-item Body sign-off required for retire-now / move actions.

---

## Section 4 — Beta phase: operations DEFER triple investigation

**Added:** 2026-05-27, same-day. **Witness anchor:** SOUL-090. **Driver:** Body authorization "investigate beta" after alpha (`logs/` retire) landed at SOUL-089. **Scope:** investigate uniqueness for the three DEFER-WITH-CRITERIA items in Section 1.5 — recommend KEEP / RETIRE-NOW / CONSOLIDATE per file.

### 4.1 `operations/autonomous-session-template.md` (269 lines)

**Method:** `grep -rn autonomous-session-template --include="*.md" .` across project.

**Result:** Zero live references. The only matches are:
- `witness.md` SOUL-087 + SOUL-088 (the audit's own retire-watch flag — descriptive).
- `docs/audits/2026-05-27-...` (this document — descriptive).
- `councils/SOUL-087-...` (the convening that flagged it — descriptive).

No operations file cites it. No command sources from it. No amendment names it. No finding references it. No spec uses it. The file IS what `grep -r "autonomous-session-template"` returned with the descriptive records filtered.

**Content analysis:** The file describes a 7-step Operating Sequence (Orient → Align → Plan → Execute → Convene → Stop → Output Package) for autonomous AI runs. Each step has a modern instrument that has subsumed it:

| Template step | Modern equivalent |
|---|---|
| Step 1 Orient — "Read CLAUDE.md in full" | Seed @-import on session start (automatic) |
| Step 2 Align — restate, AL gate, Cartographer, Accountant, Skeptic | Seed §Mandatory Gates + `/soul-expand` |
| Step 3 Plan — Prophet, Researcher | `writing-plans` skill (seed §External Skills) + `/soul-tasks` |
| Step 4 Execute — iterations, watch failure modes | The work itself; failure-mode list in seed |
| Step 5 Convene Council | `/soul-council` (instrument shipped 2026-05-26) |
| Step 6 Stop Conditions | `/soul-verify` + Body interrupts + `events.jsonl` |
| Step 7 Output Package | `/soul-handoff` (the cursor IS the output package) |

The template predates ALL of these instruments. Its content has been fully decomposed into the seed + commands/.

**Verdict: RETIRE-NOW (awaits Body sign-off).** Risk: low. Doctrinal content lives elsewhere (none orphaned); the procedure shape is now in instruments. Status footer says only "Adopted: 2026-05-20" with no Status field — never landed as "active."

**One residual concern (flagged for Body):** the Problem Slot template (lines 50–67) — `PROBLEM:`, `DOMAIN:`, `EPISTEMIC TYPE:`, `KNOWN CONSTRAINTS:`, `KNOWN ABSTRACTIONS:`, `SUCCESS LOOKS LIKE:` — is a useful framing prompt that has no modern equivalent. If Body wants to preserve it, can be lifted into a new lightweight `operations/problem-slot-template.md` (~20 lines) before retirement. Otherwise it's lost.

### 4.2 `operations/completion-gate.md` (130 lines)

**Method:** same grep.

**Result:** Heavily cited. Live references:
- `amendments/accepted/SOUL-A003-universe-collapse.md` (×2): completion gate as the "work's completion gate."
- `amendments/accepted/SOUL-A005-gate-refinements.md`: "completion gate was just modified by A003."
- `amendments/accepted/SOUL-A010-coherent-falsehood-anchor-obligation.md` (×4): **A010 explicitly states "Folded into completion-gate.md + the hook + soul-verify.md"** — names completion-gate.md as "the mechanism."
- `SYSTEM-VERSION.md` (×2): changelog entries 0.4.0 and 0.4.2 specifically cite completion-gate.md as the integration point for A010 and F028.
- `commands/soul-expand.md` row 12: "Unlike the completion gate (`/soul-verify`)..." — names the relationship.
- `commands/soul-tasks.md` (×2): "forward twin of the completion gate."
- `commands/soul-verify.md` description: "The pre-completion gate."
- `ideas.md` (×7): multiple captured ideas treat the completion gate as known doctrine; one (SOUL-055 graduation) named it as the integration target.
- `operations/reference-repository.md` row 20 + 147: "what the [[completion-gate]] checks against" + "the ground the [[completion-gate]] stands on."

**Comparison with `/soul-verify` + hook:**

| Layer | Artifact | Lines | Role |
|---|---|---|---|
| Doctrine | `operations/completion-gate.md` | 130 | The reasoning — why the gate exists, the four role-checks, the Gate↔Theatre tension, the A010 anchoring rule, the F022 tripwire. |
| Instrument | `commands/soul-verify.md` | 67 | The Body-invokable form — five numbered checks with concrete instructions. |
| Automation | `hooks/pre-completion-verify.py` | (Python) | The auto-firing form — emits `soul.gate.completion.flagged` events to `.soul/events.jsonl` (confirmed firing today). |

Three artifacts at three activation tiers, not three copies of the same content. A010 explicitly preserves this stack.

**Verdict: KEEP-IN-PLACE.** The audit's original suspicion (possible supersession) was wrong upon investigation. The doctrine layer is load-bearing — amendments cite it, the changelog cites it, two commands cross-reference it. Retiring it would orphan A010's "mechanism" reference and break the doctrine-layer rule (Section 3.2 Blur 3 also resolves: the triple-layering is intentional, not redundancy).

**Status-footer note:** "Status: proposed (pending Soul-System repo review)" is stale — A010's acceptance effectively reviewed it. **Minor follow-up:** update status to "active" in a future doctrine-text-cleanup beat. Not blocking.

### 4.3 `operations/reference-repository.md` (173 lines)

**Method:** same grep.

**Result:** Live references:
- `references/INDEX.md` row 5: **"See `operations/reference-repository.md` for the format."** — direct citation as the format spec.
- `operations/completion-gate.md` row 64: "Sources that come back land in the [[reference-repository]]."
- `operations/completion-gate.md` row 111: "It is fed by the [[reference-repository]] (where retrieved sources are grounded)."

**Comparison with `references/INDEX.md`:**

| File | Lines | Purpose |
|---|---|---|
| `operations/reference-repository.md` | 173 | FORMAT SPEC — CSL-JSON bibliographic core, provenance sidecar fields, workflow, knowledge graph edges, stewardship rules. |
| `references/INDEX.md` | 14 | MANIFEST — one line per held reference, pointing back to the spec for format detail. |

Not duplicates. INDEX is the catalog; reference-repository.md is the catalog's schema. Removing the spec orphans the catalog. The audit's original suspicion ("possible consolidation to references/INDEX.md") was wrong — INDEX explicitly delegates format documentation back to the spec.

**Verdict: KEEP-IN-PLACE.** The file is the FORMAT SPEC for the `references/` directory (per Section 1.5 sub-classification: FORMAT-SPEC class, like `witness-log-format.md` and `event-standard.md`).

**Status-footer note:** Same stale "proposed (pending Soul-System repo review)" status. Same minor follow-up.

### Section 4 summary

Investigation reverses the audit's original DEFER-WITH-CRITERIA tally on this triple:

| File | Original audit suspicion | Beta-phase verdict |
|---|---|---|
| `autonomous-session-template.md` | DEFER → likely retire | **RETIRE-NOW (Body sign-off)** |
| `completion-gate.md` | DEFER → possibly superseded | **KEEP-IN-PLACE** (heavily cited; A010-named) |
| `reference-repository.md` | DEFER → possibly consolidate | **KEEP-IN-PLACE** (format spec; INDEX-cited) |

**One retire-now candidate (autonomous-session-template.md); two preservation calls (completion-gate.md, reference-repository.md).** The audit's per-boundary reshape is vindicated: per-item grep + content analysis caught the doctrinal load-bearing of two files the chamber's intuition flagged as potential retire candidates.

**Decision needed from Body:**
1. RETIRE-NOW `operations/autonomous-session-template.md`? Preserve Problem Slot template separately or let it go?
2. Update status footers on completion-gate.md + reference-repository.md from "proposed (pending Soul-System repo review)" → "active"? (Non-blocking; bundle with another doctrine-text beat.)

### Audit-process lesson

**Two of three DEFER candidates were KEEPS upon investigation.** The chamber's surface-level Steward intuition ("looks like a retire candidate") was wrong twice and right once. **Per-boundary + per-item-grep is the discipline that catches the difference; per-item intuition alone would have produced two false retirements.** Validates the SOUL-087 reshape from Steward per-item → Architect per-boundary (with Steward second-voice).

Worth flagging as a candidate finding: SOUL-F040 candidate — *"surface-level retire intuitions need a uniqueness-investigation step before action; intuition alone produces ~67% false-retire rate (small N)."* Captured here; can graduate via `/soul-finding` when Body decides.
