# The Reference Repository

The Archivist's instrument. Retrieved sources are saved locally — so results are
grounded in documents rather than memory, lookups are cheap, and a knowledge
graph can grow over time.

The Archaeologist and Emissary *surface* what the Universe holds. The Archivist
*places* it. Without a place to put what was found, research is re-done every
session and results rest on recollection — the failure that lets an unsourced
number ("the published value is 2474 K") survive until a reviewer asks for the
page it came from.

---

## The principle

**A claim that touches the Universe cites a saved source, not a memory.** When the
Emissary or Researcher retrieves a document, the *document itself* is saved — not
only a citation to it. The saved copy is what makes a claim re-verifiable later,
and what the [[completion-gate]] checks against.

---

## Structure (per project)

```
references/
  references.json   # bibliographic core for all entries — CSL-JSON (a standard)
  INDEX.md          # human manifest — one line per reference, like MEMORY.md
  <slug>.<ext>      # the document (pdf / txt / csv / ...)
  <slug>.md         # provenance sidecar (front-matter below)
```

The document, its sidecar, and its `references.json` entry share a slug `id`.
Large binaries may be stored out-of-tree with the sidecar recording the path; the
sidecar and `references.json` are always committed.

---

## Two layers: standard bibliographic core + provenance

Don't invent a citation format — one exists. The bibliographic identity of each
reference lives in `references.json` as **CSL-JSON** (the Citation Style Language
interchange format that Zotero, Pandoc, and citation processors read and write).
This makes every reference exportable to a real bibliography for free.

```json
{
  "id": "<slug>",
  "type": "article-journal | report | paper-conference | dataset | ...",
  "title": "...",
  "author": [{"family": "...", "given": "..."}],
  "issued": {"date-parts": [[2017]]},
  "container-title": "...", "volume": "...", "page": "...",
  "DOI": "...", "URL": "..."
}
```

The *provenance* — what is Soul-specific and has no home in a citation format —
lives in the markdown sidecar, designed so a knowledge graph can be *generated*
(the fields are the graph's edges), pointing at its CSL entry by `id`:

```yaml
---
id: <slug>
csl: references.json#<slug>        # bibliographic core (above)
access: public | paywall | institutional | provided-by-body | local-only | wanted
retrieved: <YYYY-MM-DD>            # "—" if not held (status wanted)
file: <local path, or none>
version-of-record: <citation of the published version, if this copy differs>
grounds: [<claim/result ids that cite this>]
key-values:                        # extracted numbers, each with provenance
  - value: <n unit>
    defines: <exact definition in the source>
    status: verified | figure-derived | derived-by-us
    locus: <table/figure/page>
supersedes: [<id>]
superseded-by: [<id>]
related: [[<other-ref>]]           # typed graph edges
---
<short prose: what this is, why it is held, what it does and does not establish>
```

The provenance fields map onto PROV / RO-Crate concepts (`grounds` ≈ `prov:used`,
`supersedes` ≈ `prov:wasRevisionOf`, `related` = typed edges), so the graph can
later be emitted as RO-Crate JSON-LD *if a consumer needs it*. We do not emit full
RO-Crate now — that is Premature Sophistication until something reads it. CSL-JSON
is adopted because citation processors already read it today.

A reference may be **held** or merely **wanted**: a `wanted` entry (access:
paywall/institutional, file: none) records a document the [[completion-gate]]'s
access-escalation check has handed to the Body. The repository tracks not only
what we have, but what we still need.

### Prefer the version of record

A document often exists in several forms: a journal or conference **version of
record**, and an open-repository copy (e.g. an OSTI report or a preprint) that may
be a draft. Cite the version of record in `references.json`; record the repository
copy as where the *file* was obtained (`access`, `URL`); when they differ
materially, note it in `version-of-record`. Repositories like OSTI are excellent
for *obtaining* documents — the published version is what you *cite*.

---

## Workflow

1. **Retrieve → place.** When the Emissary/Researcher pulls a source, save the
   document and write its sidecar; add a line to `INDEX.md`.
2. **Cite → ground.** When a result or paper uses a value, reference it by `id`.
   Source footers and memory `[[links]]` point into the repository.
3. **Escalate → wanted.** A source I cannot reach becomes a `wanted` entry, not a
   dead end. When the Body provides it, it flips to held — closing the loop.

---

## The knowledge graph

Nodes are references, claims, and extracted values. Edges are
`grounds` / `cites` / `supersedes` / `contradicts` / `derived-from`. Because each
edge already lives in a sidecar field, the graph is generated, not maintained by
hand. This composes with the existing Source-footer convention (provenance in
operations files) and the memory system's `[[name]]` links — one provenance fabric
across documents, operations, and memory.

---

## Stewardship — avoid the hoard (Archaeologist ↔ Steward)

The repository accumulates, so it must be pruned. Superseded references are
*marked* (`superseded-by`), not deleted — provenance outlives relevance. Genuinely
dead entries are retired. The standard is the Steward's: *does this still ground
something?* An Archivist who never prunes becomes a hoarder; the value is in
findability, not volume.

**Provenance, not redistribution.** Retrieved or paywalled documents are stored
for the project's own grounding and re-verification — not for redistribution. The
`access` field keeps that honest.

---

## Relationship to the Soul

Instrument of the **Archivist**; fed by the **Emissary** and **Researcher**;
pruned by the **Steward**; built and maintained by the **Artificer**. It is the
ground the [[completion-gate]] stands on: the gate asks "is this sourced?", the
repository is where the source lives.

**Proposed hook:** cited from [[completion-gate]] (access escalation → repository);
optionally a line in `CLAUDE.md` under Seeding.

---

**Source:** The Archivist role and the Archaeologist↔Steward tension
(`philosophy/the-soul.md`), plus the Source-footer provenance convention
(`operations/CLAUDE.md`), extended from citations-in-files to retrieved documents
after a project grounded a validation claim in an unsourced remembered number.
**Shapes:** entire file
**Adopted:** 2026-05-20
**Status:** active (per SOUL-090 audit — format spec for `references/`; `references/INDEX.md` delegates back to this file; KEEP-IN-PLACE confirmed 2026-05-27)

**Source:** Citation Style Language — CSL-JSON item schema,
https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html (and
https://github.com/citation-style-language/schema). Adopted for the bibliographic
core because it round-trips through Zotero, Pandoc, and other citation processors.
**Reinforced by:** RO-Crate 1.1 (https://www.researchobject.org/ro-crate/) and
W3C PROV-O — the provenance/graph layer maps onto these concepts; full RO-Crate
JSON-LD emission deferred until a consumer requires it.
**Shapes:** Two layers section
**Adopted:** 2026-05-20
**Status:** active (per SOUL-090 audit — format spec for `references/`; `references/INDEX.md` delegates back to this file; KEEP-IN-PLACE confirmed 2026-05-27)

*Refines as evidence accumulates.*
