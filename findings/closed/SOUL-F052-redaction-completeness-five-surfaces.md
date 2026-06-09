```
FINDING ID:      SOUL-F052
DATE:            2026-06-09
WITNESS IDS:     SOUL-150 (the pre-public redaction — names/paths in content); SOUL-151 (the
                 secret/PII sweep that found the work-email-in-commit-metadata catch).

WHAT:            **A confidentiality scrub of a repo going public has at least FIVE distinct
                 surfaces, and redacting one (file CONTENT) leaves the other four leaking. The
                 surfaces: (1) content — names/identifiers in files; (2) paths — directory names
                 and absolute paths (e.g. an absolute path whose folder name leaks both the
                 directory layout and a project's domain); (3)
                 commit METADATA — author/committer name+email and TAGGER identity (a work email
                 hid here, invisible to every content sweep); (4) BINARIES — blobs git-grep can't
                 read (verify via their text source, e.g. a figure's generating .py); (5)
                 CREDENTIALS — API keys/tokens/private keys (entropy + known-pattern scan, e.g.
                 detect-secrets, over working tree AND history).** Each surface is structurally
                 invisible to the tools that catch the others — a name-grep never sees a tagger
                 email; a content scan never reads a PNG; entropy scanners don't flag a project
                 name. Completeness = sweeping all five, over the FULL history, not just HEAD.

                 This is the Partial-Domain-Coverage failure mode (it "feels complete" after the
                 obvious content pass) specialized to confidentiality — and the in-vivo proof was
                 that two of the five (commit-metadata, and an incomplete content pass missing
                 a capitalized variant of a project token's witness-ID prefix) were caught only by
                 the explicit per-surface sweep, AND
                 the redaction's own record-entry initially re-leaked a name (caught by a pre-commit
                 leak-check). The leak-check on every write is itself the sixth discipline.

WHY THIS FILING (not an amendment):
                 Operational doctrine — a reusable CHECKLIST, not a new primitive. It sharpens the
                 Steward/Guardian "going public" obligation with a concrete five-surface sweep. The
                 anchoring force here is the incident (an institutional/national-lab work email that
                 would have gone public on the author/committer fields of 13 commits) — preserve
                 that, per F045: the
                 fact "metadata leaks separately from content" loses its force as a bare proposition.

FILED BY:        Guardian (third-party + self confidentiality); Skeptic (drove the completeness bar —
                 a missed surface is a leak); Emissary (used real scanners, not just internal grep).

RELATED:         [[SOUL-150]] (content/path redaction); [[SOUL-151]] (the sweep + metadata catch);
                 [[SOUL-F048]] (mechanical sweep catches the reasoning pass's residual — sibling:
                 there a deletion sweep, here a redaction sweep; both = mechanical coverage beats
                 "thought carefully");
                 [[SOUL-F045]] (preserve the incident's FORCE, not just the proposition);
                 [[the Primary Failure Modes: Partial Domain Coverage]] (this is its
                 confidentiality specialization).

STATUS:          CLOSED (Body graduation, 2026-06-09). Applied to make the Soul-System + Soul-
                 Benchmark repos public-safe (verified 0 sensitive across all history on all five
                 surfaces). Reusable as the "going-public" redaction checklist. Residual
                 (non-blocking): force-push leaves pre-rewrite commits SHA-retrievable on the host
                 briefly — delete+recreate the remote is the zero-retention path (used here).

                 UPSTREAM: this repo IS the Soul System (the upstream) — Soul-meta (the going-public
                 discipline), so it belongs in this findings/ stream.
```
