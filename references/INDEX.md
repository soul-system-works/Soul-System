# Reference Index

One line per saved source (like `MEMORY.md`). A claim that rests on outside work cites
a saved reference here, not a memory. The format every entry follows:

- `references.json` — the source's bibliographic record in CSL-JSON (the citation
  format Zotero and Pandoc read), keyed by a short slug `id`.
- `<id>.md` — a sidecar with the same slug. Front matter: `id`, `csl:
  references.json#<id>`, `access` (e.g. `public`), `retrieved` (date), `file` (a local
  copy's path, or `none`), `grounds` (the record IDs that cite it), optional
  `key-values` (each value with `defines`, `status` — `secondary-reading` until checked
  against the source itself — and `locus`), and `related`. Then a few lines on what
  the source is and what it does and does not establish.
- A line below, linking the sidecar.

First entries: the SOUL-I017 deep-dive prior-art pass (SOUL-060), all four verified
against the arXiv primary source on 2026-05-22.

- [voyager-2023](voyager-2023.md) — *Voyager* (Wang et al., 2023): the landmark LLM-agent **skill library** of executable, reusable code. The durable capture pattern. arXiv:2305.16291
- [coala-2023](coala-2023.md) — *Cognitive Architectures for Language Agents* (Sumers et al., 2023): the **procedural / episodic / semantic** memory taxonomy — I017's vocabulary. arXiv:2309.02427
- [agent-skills-survey-2026](agent-skills-survey-2026.md) — *Agent Skills for LLMs* survey (Xu & Yan, 2026): names "model-internal learning → portable, **auditable, governed** SKILL.md" as the open problem — **= I017's gap**. arXiv:2602.12430
- [agentic-skills-wild-2026](agentic-skills-wild-2026.md) — *How Well Do Agentic Skills Work in the Wild* (Liu et al., 2026): benchmark showing ungoverned skill proliferation **degrades selection** — validates never-always-on (SOUL-033). arXiv:2604.04323
- [bmad-method-v6-2026](bmad-method-v6-2026.md) — *BMAD Method documentation (V6)*: agent framework (Analyst / PM / Architect / SM / PO / Dev / QA / UX) shipped as fresh-chat skills with serial handoff — **the empirical ground for SOUL-F041** (seed §External Skills and Tools BMAD claim, partial). docs.bmad-method.org
