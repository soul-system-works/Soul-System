# SOUL-F061 — A handoff cursor's pointers are claims, not facts

```
FINDING ID:      SOUL-F061
DATE:            2026-07-09
KIND:            Instrument observation — how /soul-handoff and /soul-resume behaved in use
                 (operations/CLAUDE.md §Projects importing this contract: domain lessons stay
                 home; observations about the SYSTEM's gates and instruments come here).
REFERENCE PROJECT: RealisticSensors (UE 5.7 plugin; imports the contract via CLAUDE.md
                 @-include; register: plain).
WITNESS IDS:     RSENS-012 (project-local log; the anchoring instance. RSENS-009 is a prior
                 instance of the same shape not recognised as systemic at the time.)
STATUS:          Open — proposes an amendment to /soul-handoff + /soul-resume.

WHAT:            A cursor pointer that NAMES a location is treated by the resuming session as a
                 verified fact, but nothing in the cursor distinguishes a pointer that was
                 checked from one that was remembered. The claim then propagates into decisions
                 without ever being resolved.

ANCHORING INSTANCE:
                 The session-7 cursor for RealisticSensors stated that ADR-0024's design "lives
                 in the SEPARATE dains repo, not on disk in this tree." Session 8 resumed, read
                 the cursor, and repeated the claim to the Body inside a next-step
                 recommendation — annotating option B as "you'd be working from a site list,
                 not the real spec." The Body deferred that option.

                 The claim was false. `dains` is a sibling git repo at /mnt/d/UnrealProjects/dains
                 and the ADR was in it, fully written. Cost to check: one `ls`. It was found only
                 because a later completion-gate pass asked whether the cursor's own claims had
                 anchors — i.e. the instrument that caught it was the gate, NOT the resume.

                 Underneath the surface error sat a structural one the cursor could not have
                 seen: the plugin cited 20 distinct ADRs — 368 occurrences across 51 files — and
                 shipped no ADR store at all. Every citation was a dangling pointer into a repo
                 the plugin does not contain, and no check in the repo could detect it.

WHY THE INSTRUMENT PERMITS IT:
                 /soul-handoff §3 says the cursor must be "self-contained for correctness" and
                 that it should reference, not duplicate. /soul-resume §2 says "actually read
                 them so the durable state is in context; don't just glance at the cursor."
                 Both are right, and neither closes the hole:

                 - The cursor's POINTERS block mixes pointers the writing session USED (and so
                   implicitly verified) with pointers it merely BELIEVED. Nothing marks which.
                 - /soul-resume's "actually read them" silently succeeds when a pointer names a
                   path outside the tree: there is nothing to open, no error is raised, and the
                   unread pointer is carried forward as though read. A pointer that CANNOT be
                   resolved is exactly the one most in need of resolution.
                 - The failure is asymmetric and cheap to prevent: verifying a named path costs
                   a directory listing; propagating a false one costs a decision.

RELATION TO EXISTING FINDINGS:
                 - **F047 (asserted vs executed verification)** — this is F047's shape applied to
                   the handoff artifact rather than to a numeric claim. "The ADR is not on disk"
                   is a claim about reality, cheap to assert, cheap to execute, and never
                   executed. The cursor is a place where asserted-not-executed claims accumulate
                   and are then inherited with the authority of a durable record.
                 - **F039 (secondary-mention propagation evades drafter verify)** — closest kin.
                   The false claim rode in a *parenthetical* inside a NEXT-STEP option, not in a
                   headline assertion. Secondary mentions evade verification; a cursor is
                   almost entirely secondary mentions.
                 - **F057 (anchor validity hierarchy)** — the cursor is a low-tier anchor
                   (recollection of a prior session) that reads, typographically, like a
                   high-tier one (a durable record).

SECOND INSTANCE, SAME DAY, SAME CLASS (numeric variant):
                 The same session reported "367 citations across 166 files." The 166 was a
                 summing bug — per-ADR file lists added together, so a file citing three ADRs
                 counted three times. Before it was recomputed it had already propagated into a
                 checker's output line, a document's provenance note, and a commit message.
                 An unverified NUMBER spreads exactly like an unverified POINTER, through the
                 same mechanism: it is quoted forward rather than recomputed. Correct figures:
                 368 occurrences, 51 files.

PROPOSED AMENDMENT (for the Body's judgement, not yet applied):
                 (a) /soul-handoff: mark each POINTERS entry with provenance — `[read]` for a
                     path this session actually opened, `[inherited]` for one carried from a
                     prior cursor. Cheap to write, and it makes the unverified visible.
                 (b) /soul-resume: step 2 should RESOLVE every named path and report misses
                     explicitly ("cursor names X; X not found") rather than reading what exists
                     and silently skipping what doesn't. A miss is a finding, not a no-op.
                 (c) Where a cross-repo pointer is load-bearing, the durable fix is to remove
                     the seam, not to annotate it. In the anchoring instance the ADRs were moved
                     into the plugin and a red/green check (`tests/check_adr_references.py`) now
                     fails on any cited-but-absent ADR — the failure class became
                     machine-detectable instead of memory-dependent. This is F053's
                     force-at-the-temptation-site applied to a repo boundary.

WHAT WORKED (kept-because-it-fired):
                 The completion gate (F012 lineage) caught BOTH errors in this session, one turn
                 apart, and neither would have been caught by the resume or the handoff. Its
                 anchor-validity check surfaced the false cursor claim; its "absolute claims need
                 a valid external anchor" check forced a recompute of the citation counts and a
                 direct check of a link the session had *inferred* was already broken (it was —
                 but the inference was untested when it was written into an ADR). The gate is
                 currently the only instrument in the loop that treats the record's own claims as
                 claims.
```
