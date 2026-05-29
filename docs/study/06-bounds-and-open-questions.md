# Bounds & open questions — what this study did *not* settle, and why

A study that measures "does the system change the work" is only honest if it is
equally explicit about what it could *not* measure. This is the deliberate failure
of the method: the harness is single-shot / single-resume, so any claim that is
intrinsically *longitudinal* or *multi-task* cannot be closed here — and faking a
single-shot proxy for one would be the precise Coherent Falsehood the study exists
to catch. The line below is **measurable-by-this-method vs not**, not
important-vs-unimportant. Several of the biggest bets sit on the unmeasurable side.

## The ledger

| Open end | Measurable single-shot here? | Status / why open | Value if closed |
|---|---|---|---|
| **Longitudinal accumulation** — does the record across *many* sessions prevent drift? | **First rung climbed** (SOUL-123; see [`07`](07-longitudinal.md)) | The system's strongest claim — now measured for the first time. A self-generated session chain (S1 records a counter-default decision → S2 buries it → S3 faces a new task with the original context gone) **flipped a dangerous default 5/5 → 0/5 drift** in the later session, with a length-matched filler drifting exactly like having no record (equal-compute control passes). Decisively, it **does not dissolve at the frontier** — the strong model drifts too (it invents an idempotency key that doesn't exist), because the substance is a *fact it cannot derive*. The v1 pilot (SOUL-122) validated the mechanism but its decision wasn't counter-default (C2-null, caught by the floor check); v2 floor-checked first and landed the result. **Still open:** many sessions (N>3), many interacting facts, and record-*decay* over a long/eroding record — and whether a *reasoning-preference* record (vs a fact) would dissolve at the frontier like the rest of the study. | High — the core promise of an accumulating record, now shown real for fact-carrying records at both capabilities. Scaling is widening a built instrument, not building one. |
| **Multi-task what/when routing** — does curation compound across a *distribution* of tasks? | **No** (cross-task) | Skill-routing (SOUL-120) measured one task in the win-cell. Whether a tested catalog pays off across the project's whole task mix is the longitudinal twin of routing. | Medium-high — it is the real shape of the catalog's value over time. |
| **A *built* router** (vs the oracle) — can a real router approach perfect routing better than the model's own pick? | **Partly** (but it's a *build*, not an ablation) | SOUL-120's oracle is the *upper bound*; it proved the value exists. Whether a built router captures it is a product spike, justified now but not yet done. | High — decides whether the catalog needs a routing *mechanism* or just a curated index. |
| **Tool-skills** (vs procedure-knowledge) | **No** in this harness | Headless arms can't be granted *differential real tools* (web-search, execution). The routing probe used procedure-knowledge as a faithful proxy for the *selection* kernel; tool-skill routing is unmeasured. | Medium — extends routing from knowledge to capabilities. |
| **Retrieval** — does a curated index/handoff beat find-it-yourself in a *large* repo? | **Yes** | Held constant in the handoff probe (all arms got a pre-curated slice). Genuinely closeable; deferred as **low marginal value** — predicted to re-confirm "the record carries the value." Bears on the handoff/Mind KEEP rows. | Low-medium — would firm the handoff/Mind decisions, unlikely to move the thesis. |
| **Depth-bottleneck agentic** — does multi-agent help when one agent's *context* is the limit (not breadth)? | **Attempted; ceilinged** | The honest steelman for Path B. **Closed this session** (SOUL-121): a 36-item audit packet could not *create* a bottleneck — single / careful / mapreduce all caught 6/6 at both capabilities (C2 failure). It does NOT show map-reduce can't help on depth; it shows the bottleneck isn't creatable at tractable single-shot scale with recognizable issues. The genuine lost-in-the-middle regime needs large inputs — where chunked map-reduce is an established *generic* technique, not Soul-specific. | The fork is airtight on the testable side: even agentic's best-case depth niche is generic map-reduce, not the Soul role-engine. |
| **Legibility's downstream payoff** for a *human* reader over time | **No** (human, longitudinal) | Asserted throughout (A017: "roles = legibility"); the *value* of that legibility to the inheriting human/session is not measured, only its existence. | Medium — it is the standing justification for keeping the record readable. |

## What "closing" honestly means here

For the **measurable** rows, closure is a probe (depth-bottleneck is closed; retrieval
is deferred-by-choice). For the **unmeasurable** rows, closure is *this ledger* — naming
them precisely, with why each resists single-shot measurement and what it would take
to measure properly. That is the Cartographer's closure: an honest map of covered /
adjacent / unmeasurable territory. The study does not claim the unmeasured ground;
it marks it.

## The shape of the open ground

Three of the heaviest open ends — longitudinal accumulation, multi-task routing,
legibility-over-time — share a structure: they are all about **value that compounds
across sessions/tasks**, which is exactly where the surviving substance (counter-default
knowledge: have / compress / deploy) is *supposed* to pay off, and exactly what a
single-shot harness cannot reach. The study's confident half (what dissolves under
equal compute in one shot) is real; its humble half (what the accumulating record buys
over a project's life) was, until now, named rather than claimed. A longitudinal harness
was the one instrument that could move the thesis rather than re-confirm it — and as of
**SOUL-123 ([`07`](07-longitudinal.md)) it did**: a self-accumulated record carried a
counter-default fact across a session boundary and prevented a dangerous drift 5/5 → 0/5,
at *both* capabilities, with the equal-compute control passing. This is the **first win
that does not dissolve at the frontier** — because it carries a fact the model cannot
derive, not a reasoning skill it can. The humble half is no longer wholly unmeasured: its
first rung is climbed. What remains genuinely open is *scale* (many sessions, many facts,
record-decay over a long record) and whether a reasoning-*preference* record would dissolve
at the frontier like the rest of the study — both now widenings of a built instrument.
