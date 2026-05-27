---
description: Capture hard-won tool/procedure know-how into a governed, project-local Agent-Skills SKILL.md — AFTER a verified success. The thin governed layer over the skill engine: verify, attribute, retire. Use right after you got a tool/procedure working and confirmed it, so the know-how is not re-derived next session.
---

# /soul-skill — capture verified tool know-how as a governed skill

You just got something working — a tool invoked the right way, a procedure with
real gotchas, a workflow that took effort to discover — and you **verified** it.
This captures that know-how as an Agent-Skills `SKILL.md` so it survives the
session, scoped and attributed, and can float up to global with refinement.

**The verdict this is built on (SOUL-060):** do *not* reinvent the skill engine —
Agent Skills (`SKILL.md` + progressive disclosure) already *is* one. This command
adds only the part the field leaves open and the Soul owns: **governance** —
capture only *verified* know-how, stamp its provenance, and wire in retirement so
skills do not silently proliferate. It is `write-a-skill`'s discipline-wrapper for
the post-success moment, not a second authoring engine.

Manual-fire only. Auto-distillation from transcripts is deliberately deferred.

## What to do

1. **Gate the trigger — the two-part bar.** Do not draft until both hold:
   - **Verified, with an anchor (SOUL-F028).** Name the evidence it works and how
     it could be wrong (a measured result, a passing run, an observed fix — e.g.
     *"535s→38s, measured"*). If the only evidence is "it seemed to work," still
     capture, but at `soul-confidence: low` / `soul-status: under-review`, and say so.
   - **Playbook-sized, not note-sized.** A reusable multi-step procedure with
     gotchas worth not re-deriving. A one-liner is not a skill — stop, and suggest
     a witness note instead.

2. **Distill from what just happened — do not interview.** The post-success
   advantage is that the know-how was just *demonstrated*. Pull from the session:
   the tool · the goal · the steps that worked · the gotchas / dead-ends avoided ·
   the verification (the anchor). Reconstruct from the actual commands run, not
   from a `write-a-skill`-style questionnaire.

3. **Steward-check for overlap (SOUL-033 — generation couples with retirement).**
   Search existing skills (`~/.claude/skills/`, the project's `.claude/skills/`,
   and parents) for one that already covers this. If found → **update it** (refresh
   steps, bump `soul-last-verified`); do not create a duplicate. Also name any
   skill this one makes redundant and mark its `soul-status: deprecated`.

4. **Draft a SKILL.md (Agent-Skills standard) — a DRAFT for curation, never final.**
   Format to the open standard (agentskills.io/specification):
   - `name`: lowercase-hyphen, ≤64 chars, **must match the skill directory name**.
   - `description`: ≤1024 chars, keyword-rich *what + when* — this is the portable
     trigger and is always-on at discovery, so keep it tight.
   - `compatibility` (if env/tools are required): e.g.
     `Requires Dymola 2026x, Modelica/TRANSFORM, WSL` — the portable env signal.
   - `metadata:` provenance, `soul-`-prefixed (the spec asks for unique keys):
     `soul-source` (the verified run + anchor), `soul-captured`, `soul-last-verified`,
     `soul-confidence` (high|medium|low — CoALA procedural-confidence),
     `soul-status` (active|under-review|deprecated — the Steward handle).
   - `paths:` (OPTIONAL) to scope auto-load where it clearly helps (the Anthropic
     proliferation best-practice). Weigh it — a too-narrow glob can *suppress* a
     wanted activation (e.g. a Python-driven tool whose working files are not the
     tool's native extension). **Claude-Code-only — non-portable.**
   - **Body:** numbered procedure · gotchas · a **Verify** step (how to re-confirm
     it still works — the re-verification handle). Keep SKILL.md < 500 lines; push
     long reference material into `references/`.

5. **Write it.** A genuinely new skill goes **project-local first** —
   `<project>/.claude/skills/<name>/SKILL.md` — with the verification artifact (the
   measured run / log) in `references/`; global promotion is *earned*, not automatic.
   If step 3 found an existing skill to **update**, edit it **where it already lives**
   (it may already be global) — do not fork a project-local copy.

6. **Validate against the standard (an external anchor, not self-assertion).** Run
   `skills-ref validate ./<name>` if available; else the manual checklist
   (name == dir, description non-empty ≤1024, frontmatter parses).

7. **Present the draft for curation — do not commit it.** Show the SKILL.md; let
   the Body curate the *when/why* (auto-draft, then prune by hand — the Voyager
   pattern). State the promote ratchet and the retire cadence (below).

## The local→global promote ratchet (document; do not automate)

- Born **project-local** (`<project>/.claude/skills/`).
- Promotes to **global** (`~/.claude/skills/`), or into a Soul skills **plugin**
  (Anthropic's vehicle for distributing proven setups), only when **earned**:
  proven across repeated independent uses **and re-verified** (re-run the Verify
  step) — not merely old. Bump `soul-last-verified` on promotion.
- MVP is a manual promote (move/symlink + re-verify). Auto-promote and
  plugin-packaging are deferred.

## Retirement (Steward / never-always-on)

- Every skill carries `soul-status` + `soul-last-verified` so decay is visible.
- Review on **Anthropic's external cadence** — at each major Claude model
  release (historically ~every 3–6 months; defer to actual release rather than
  a fixed period): still used? still correct? superseded by native model
  capability? Move `active → under-review → deprecated`, and remove what is
  dead. This site uses calendar time because the external trigger is itself
  calendar-bound; the project-internal clock (e.g. soul-distill) is decoupled.
- The reason matters: a tool that gains AI integration makes its skill redundant;
  a tool that never will (e.g. Dymola) keeps its skill load-bearing.

## What not to do

- **Do not reinvent the skill engine.** Agent Skills already is one; this adds only
  governance. For elaborate multi-file skills, point the Body at `write-a-skill`.
- **Do not capture unverified know-how as if proven (SOUL-F028).** No anchor →
  `low` confidence / `under-review`, stated plainly.
- **Do not auto-commit or auto-finalize.** Draft for curation; the Body owns the
  when/why.
- **Do not duplicate an existing skill.** Update it (Steward).
- **Do not add a skill without its retire handle.** Generation couples with
  retirement (SOUL-033); every skill ships with `soul-status` + `soul-last-verified`.
- **Do not bloat.** Tight `description` (always-on at discovery), SKILL.md < 500
  lines, detail in `references/`.

---

**Source:** Built by the Artificer + Architect from the SOUL-I017 deep dive
(SOUL-060) and its grill/Council synthesis. Conforms to the **Agent Skills open
standard** (agentskills.io/specification — `metadata`/`compatibility` fields, the
`references/` convention, `skills-ref` validator) and the Anthropic
"How Claude Code works in large codebases" best practices (path-scoping;
3–6-month review cadence; plugins as the promotion vehicle). **Reinforced by:**
Voyager (generate→verify→store→reuse) and CoALA (procedural memory + confidence)
— `references/voyager-2023.md`, `references/coala-2023.md`. **Shapes:** the
verify-first trigger (F028/Anchor), the `metadata:` provenance, the Steward
retire cadence (SOUL-033). **Adopted:** 2026-05-22. **Status:** active — MVP;
auto-distillation, auto-promote, and plugin-packaging deferred.
