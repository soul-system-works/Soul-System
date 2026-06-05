#!/usr/bin/env python3
"""Generate token-scale engineering-record contexts with the F038 needle at early/middle/late
positions, to test record recall against 'lost in the middle' [5] at token scale (vs the
original N=20-unit primacy-only depth probe). Deterministic (no RNG) so it is reproducible."""

# 80 plausible, DIVERSE, mutually-unrelated engineering findings (coherent-irrelevant at scale).
# None touch @-imports or non-interactive prompt loading EXCEPT the needle, inserted separately.
TOPICS = [
    ("connection pooling", "the Postgres pool max was set to 200 but the DB caps at 100 connections; the extra 100 sat in a perpetual wait queue and added p99 latency. Cap the pool below the server limit."),
    ("retry backoff", "the HTTP client retried with a fixed 100ms delay, synchronizing retries into a thundering herd after any blip. Switch to full-jitter exponential backoff."),
    ("cache stampede", "on cache expiry, every request recomputed the same value simultaneously. Add a per-key mutex / single-flight so only one recompute runs."),
    ("index bloat", "a partial index on a soft-deleted column doubled write amplification; most rows were deleted. Drop it and filter in the query instead."),
    ("clock skew", "two services compared wall-clock timestamps to order events; a 400ms NTP skew reordered them. Use a logical clock or the DB's commit order."),
    ("JSON precision", "large integer IDs were serialized to JSON numbers and lost precision in the JS client past 2^53. Serialize IDs as strings."),
    ("timezone drift", "a nightly job ran in server-local time; a DST transition skipped/duplicated a run. Pin all schedules to UTC."),
    ("N+1 query", "rendering an order list issued one query per line item. Batch with a single IN query or a join."),
    ("memory leak", "a per-request logger registered a global handler never removed; handlers accumulated until OOM. Scope the handler to the request."),
    ("flag default", "a new feature flag defaulted to ON in the absence of config, enabling it in environments that never set it. Default OFF; require explicit opt-in."),
    ("pagination", "an offset-based paginator skipped rows when items were inserted mid-scroll. Use keyset (seek) pagination on a stable sort key."),
    ("enum drift", "an enum stored as its ordinal broke when a new variant was inserted in the middle, shifting every later value. Store the name, not the ordinal."),
    ("double charge", "a payment retry without an idempotency key charged twice on a network timeout. Require a client-supplied idempotency key per charge."),
    ("log volume", "DEBUG logging left on in prod cost more than the service itself in egress. Gate verbosity behind a runtime-tunable level."),
    ("migration lock", "an ALTER TABLE took an ACCESS EXCLUSIVE lock and stalled all reads for 40s. Use the concurrent variant and add the column nullable-first."),
    ("float money", "amounts were summed as floats and drifted by cents over millions of rows. Use integer minor units (cents) end to end."),
    ("retry amplification", "each of three layers retried 3x, multiplying one failure into 27 downstream calls. Retry at one layer only; fail fast elsewhere."),
    ("header casing", "a proxy lowercased a custom header that the downstream compared case-sensitively. Compare headers case-insensitively."),
    ("queue ordering", "a 'FIFO' worker pool processed out of order because of per-worker prefetch. Set prefetch to 1 where order matters."),
    ("TTL units", "a cache TTL was set in seconds but the library expected milliseconds, expiring entries 1000x too fast. Assert units at the boundary."),
    ("partial write", "a crash mid-batch left the ledger with some rows written and some not. Wrap the batch in one transaction."),
    ("rate limit", "the limiter keyed on user-agent, so a shared UA throttled unrelated clients together. Key on an authenticated principal."),
    ("schema null", "a NOT NULL column added without a default failed the deploy on existing rows. Backfill, then add the constraint."),
    ("DNS caching", "the JVM cached a failed DNS lookup forever and never recovered after the endpoint came back. Set a finite networkaddress.cache.ttl."),
    ("signed overflow", "a duration in milliseconds overflowed a 32-bit int after 24 days of uptime. Use a 64-bit type for durations."),
    ("CORS wildcard", "an Access-Control-Allow-Origin wildcard plus credentials silently failed in browsers. Echo a specific allowed origin instead."),
    ("batch timeout", "a 'fast' batch endpoint had no per-item timeout; one slow item stalled the whole batch. Bound each item independently."),
    ("read replica lag", "a read-after-write hit a lagging replica and showed stale data. Route the immediate read to the primary."),
    ("compression bomb", "an upload endpoint decompressed user gzip without a size cap; a 1KB file expanded to 4GB. Cap the decompressed size."),
    ("UUID v1 leak", "UUID v1 embedded the MAC address and timestamp, leaking host identity in public IDs. Use v4 (random) for external IDs."),
    ("thread pool starve", "blocking I/O on the async event loop's pool starved CPU tasks. Move blocking calls to a dedicated pool."),
    ("metric cardinality", "a Prometheus label included the full URL path with IDs, exploding cardinality and OOMing the scraper. Template the path."),
    ("cookie scope", "a session cookie set without an explicit Domain defaulted to the host and broke across subdomains. Set the Domain explicitly."),
    ("lazy init race", "two threads lazily initialized a singleton and each built one; the second leaked. Use a thread-safe once-initializer."),
    ("retry on 4xx", "the client retried 400-class errors that could never succeed, wasting budget. Retry only idempotent 5xx/timeouts."),
    ("truncated UTF-8", "a fixed-byte varchar truncation split a multibyte character and corrupted the row. Truncate on character boundaries."),
    ("orphaned lock", "a process that crashed holding a Redis lock never released it; the TTL was infinite. Always set a lock expiry."),
    ("env precedence", "a config value set both in env and file used the file silently, ignoring the env override operators expected. Document and test precedence."),
    ("slow regex", "a backtracking regex on user input took seconds on a crafted string (ReDoS). Use a linear-time matcher or anchor the pattern."),
    ("stale feature gate", "a gate removed in code but left in the config store still showed in the admin UI as active. Reconcile gates on deploy."),
]


def render_record(i, topic, body):
    return f"F{i:03d} — {topic}: {body}"


def build(needle_pos, n_records=80):
    """needle_pos in {'early','middle','late'}. Returns the full context string."""
    needle = ("F038 — non-interactive doctrine loading: `@`-imports fail SILENTLY under "
              "`claude -p`. When a CLAUDE.md or system prompt uses an `@path/to/file.md` import "
              "and the model runs non-interactively (`claude -p`), the import is NOT resolved — "
              "the referenced file content never reaches the model, and instead of erroring the "
              "model CONFABULATES plausible content for the missing file ~43% of the time "
              "(measured, n=7). The fix is to inline the content or pass "
              "`--append-system-prompt-file`, and run a verbatim-quote sentinel load-test before "
              "trusting output.")
    # build n_records filler lines by cycling the topic table with index-varied IDs
    recs = []
    for k in range(n_records):
        topic, body = TOPICS[k % len(TOPICS)]
        recs.append(render_record(k + 1, topic, body))
    pos = {"early": int(n_records * 0.08), "middle": int(n_records * 0.5), "late": int(n_records * 0.92)}[needle_pos]
    recs.insert(pos, needle)
    header = ("Project engineering record — accumulated findings (read before infrastructure "
              "work). Entries are appended chronologically; each is an independent lesson.\n\n")
    return header + "\n".join(recs) + "\n"


if __name__ == "__main__":
    import sys
    pos = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    sys.stdout.write(build(pos, n))
