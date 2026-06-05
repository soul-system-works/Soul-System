Project engineering record — accumulated findings (read before infrastructure work). Entries are appended chronologically; each is an independent lesson.

F001 — connection pooling: the Postgres pool max was set to 200 but the DB caps at 100 connections; the extra 100 sat in a perpetual wait queue and added p99 latency. Cap the pool below the server limit.
F002 — retry backoff: the HTTP client retried with a fixed 100ms delay, synchronizing retries into a thundering herd after any blip. Switch to full-jitter exponential backoff.
F003 — cache stampede: on cache expiry, every request recomputed the same value simultaneously. Add a per-key mutex / single-flight so only one recompute runs.
F004 — index bloat: a partial index on a soft-deleted column doubled write amplification; most rows were deleted. Drop it and filter in the query instead.
F005 — clock skew: two services compared wall-clock timestamps to order events; a 400ms NTP skew reordered them. Use a logical clock or the DB's commit order.
F006 — JSON precision: large integer IDs were serialized to JSON numbers and lost precision in the JS client past 2^53. Serialize IDs as strings.
F007 — timezone drift: a nightly job ran in server-local time; a DST transition skipped/duplicated a run. Pin all schedules to UTC.
F008 — N+1 query: rendering an order list issued one query per line item. Batch with a single IN query or a join.
F009 — memory leak: a per-request logger registered a global handler never removed; handlers accumulated until OOM. Scope the handler to the request.
F010 — flag default: a new feature flag defaulted to ON in the absence of config, enabling it in environments that never set it. Default OFF; require explicit opt-in.
F011 — pagination: an offset-based paginator skipped rows when items were inserted mid-scroll. Use keyset (seek) pagination on a stable sort key.
F012 — enum drift: an enum stored as its ordinal broke when a new variant was inserted in the middle, shifting every later value. Store the name, not the ordinal.
F013 — double charge: a payment retry without an idempotency key charged twice on a network timeout. Require a client-supplied idempotency key per charge.
F014 — log volume: DEBUG logging left on in prod cost more than the service itself in egress. Gate verbosity behind a runtime-tunable level.
F015 — migration lock: an ALTER TABLE took an ACCESS EXCLUSIVE lock and stalled all reads for 40s. Use the concurrent variant and add the column nullable-first.
F016 — float money: amounts were summed as floats and drifted by cents over millions of rows. Use integer minor units (cents) end to end.
F017 — retry amplification: each of three layers retried 3x, multiplying one failure into 27 downstream calls. Retry at one layer only; fail fast elsewhere.
F018 — header casing: a proxy lowercased a custom header that the downstream compared case-sensitively. Compare headers case-insensitively.
F019 — queue ordering: a 'FIFO' worker pool processed out of order because of per-worker prefetch. Set prefetch to 1 where order matters.
F020 — TTL units: a cache TTL was set in seconds but the library expected milliseconds, expiring entries 1000x too fast. Assert units at the boundary.
F021 — partial write: a crash mid-batch left the ledger with some rows written and some not. Wrap the batch in one transaction.
F022 — rate limit: the limiter keyed on user-agent, so a shared UA throttled unrelated clients together. Key on an authenticated principal.
F023 — schema null: a NOT NULL column added without a default failed the deploy on existing rows. Backfill, then add the constraint.
F024 — DNS caching: the JVM cached a failed DNS lookup forever and never recovered after the endpoint came back. Set a finite networkaddress.cache.ttl.
F025 — signed overflow: a duration in milliseconds overflowed a 32-bit int after 24 days of uptime. Use a 64-bit type for durations.
F026 — CORS wildcard: an Access-Control-Allow-Origin wildcard plus credentials silently failed in browsers. Echo a specific allowed origin instead.
F027 — batch timeout: a 'fast' batch endpoint had no per-item timeout; one slow item stalled the whole batch. Bound each item independently.
F028 — read replica lag: a read-after-write hit a lagging replica and showed stale data. Route the immediate read to the primary.
F029 — compression bomb: an upload endpoint decompressed user gzip without a size cap; a 1KB file expanded to 4GB. Cap the decompressed size.
F030 — UUID v1 leak: UUID v1 embedded the MAC address and timestamp, leaking host identity in public IDs. Use v4 (random) for external IDs.
F031 — thread pool starve: blocking I/O on the async event loop's pool starved CPU tasks. Move blocking calls to a dedicated pool.
F032 — metric cardinality: a Prometheus label included the full URL path with IDs, exploding cardinality and OOMing the scraper. Template the path.
F033 — cookie scope: a session cookie set without an explicit Domain defaulted to the host and broke across subdomains. Set the Domain explicitly.
F034 — lazy init race: two threads lazily initialized a singleton and each built one; the second leaked. Use a thread-safe once-initializer.
F035 — retry on 4xx: the client retried 400-class errors that could never succeed, wasting budget. Retry only idempotent 5xx/timeouts.
F036 — truncated UTF-8: a fixed-byte varchar truncation split a multibyte character and corrupted the row. Truncate on character boundaries.
F037 — orphaned lock: a process that crashed holding a Redis lock never released it; the TTL was infinite. Always set a lock expiry.
F038 — env precedence: a config value set both in env and file used the file silently, ignoring the env override operators expected. Document and test precedence.
F039 — slow regex: a backtracking regex on user input took seconds on a crafted string (ReDoS). Use a linear-time matcher or anchor the pattern.
F040 — stale feature gate: a gate removed in code but left in the config store still showed in the admin UI as active. Reconcile gates on deploy.
F041 — connection pooling: the Postgres pool max was set to 200 but the DB caps at 100 connections; the extra 100 sat in a perpetual wait queue and added p99 latency. Cap the pool below the server limit.
F042 — retry backoff: the HTTP client retried with a fixed 100ms delay, synchronizing retries into a thundering herd after any blip. Switch to full-jitter exponential backoff.
F043 — cache stampede: on cache expiry, every request recomputed the same value simultaneously. Add a per-key mutex / single-flight so only one recompute runs.
F044 — index bloat: a partial index on a soft-deleted column doubled write amplification; most rows were deleted. Drop it and filter in the query instead.
F045 — clock skew: two services compared wall-clock timestamps to order events; a 400ms NTP skew reordered them. Use a logical clock or the DB's commit order.
F046 — JSON precision: large integer IDs were serialized to JSON numbers and lost precision in the JS client past 2^53. Serialize IDs as strings.
F047 — timezone drift: a nightly job ran in server-local time; a DST transition skipped/duplicated a run. Pin all schedules to UTC.
F048 — N+1 query: rendering an order list issued one query per line item. Batch with a single IN query or a join.
F049 — memory leak: a per-request logger registered a global handler never removed; handlers accumulated until OOM. Scope the handler to the request.
F050 — flag default: a new feature flag defaulted to ON in the absence of config, enabling it in environments that never set it. Default OFF; require explicit opt-in.
F051 — pagination: an offset-based paginator skipped rows when items were inserted mid-scroll. Use keyset (seek) pagination on a stable sort key.
F052 — enum drift: an enum stored as its ordinal broke when a new variant was inserted in the middle, shifting every later value. Store the name, not the ordinal.
F053 — double charge: a payment retry without an idempotency key charged twice on a network timeout. Require a client-supplied idempotency key per charge.
F054 — log volume: DEBUG logging left on in prod cost more than the service itself in egress. Gate verbosity behind a runtime-tunable level.
F055 — migration lock: an ALTER TABLE took an ACCESS EXCLUSIVE lock and stalled all reads for 40s. Use the concurrent variant and add the column nullable-first.
F056 — float money: amounts were summed as floats and drifted by cents over millions of rows. Use integer minor units (cents) end to end.
F057 — retry amplification: each of three layers retried 3x, multiplying one failure into 27 downstream calls. Retry at one layer only; fail fast elsewhere.
F058 — header casing: a proxy lowercased a custom header that the downstream compared case-sensitively. Compare headers case-insensitively.
F059 — queue ordering: a 'FIFO' worker pool processed out of order because of per-worker prefetch. Set prefetch to 1 where order matters.
F060 — TTL units: a cache TTL was set in seconds but the library expected milliseconds, expiring entries 1000x too fast. Assert units at the boundary.
F061 — partial write: a crash mid-batch left the ledger with some rows written and some not. Wrap the batch in one transaction.
F062 — rate limit: the limiter keyed on user-agent, so a shared UA throttled unrelated clients together. Key on an authenticated principal.
F063 — schema null: a NOT NULL column added without a default failed the deploy on existing rows. Backfill, then add the constraint.
F064 — DNS caching: the JVM cached a failed DNS lookup forever and never recovered after the endpoint came back. Set a finite networkaddress.cache.ttl.
F065 — signed overflow: a duration in milliseconds overflowed a 32-bit int after 24 days of uptime. Use a 64-bit type for durations.
F066 — CORS wildcard: an Access-Control-Allow-Origin wildcard plus credentials silently failed in browsers. Echo a specific allowed origin instead.
F067 — batch timeout: a 'fast' batch endpoint had no per-item timeout; one slow item stalled the whole batch. Bound each item independently.
F068 — read replica lag: a read-after-write hit a lagging replica and showed stale data. Route the immediate read to the primary.
F069 — compression bomb: an upload endpoint decompressed user gzip without a size cap; a 1KB file expanded to 4GB. Cap the decompressed size.
F070 — UUID v1 leak: UUID v1 embedded the MAC address and timestamp, leaking host identity in public IDs. Use v4 (random) for external IDs.
F071 — thread pool starve: blocking I/O on the async event loop's pool starved CPU tasks. Move blocking calls to a dedicated pool.
F072 — metric cardinality: a Prometheus label included the full URL path with IDs, exploding cardinality and OOMing the scraper. Template the path.
F073 — cookie scope: a session cookie set without an explicit Domain defaulted to the host and broke across subdomains. Set the Domain explicitly.
F074 — lazy init race: two threads lazily initialized a singleton and each built one; the second leaked. Use a thread-safe once-initializer.
F075 — retry on 4xx: the client retried 400-class errors that could never succeed, wasting budget. Retry only idempotent 5xx/timeouts.
F076 — truncated UTF-8: a fixed-byte varchar truncation split a multibyte character and corrupted the row. Truncate on character boundaries.
F077 — orphaned lock: a process that crashed holding a Redis lock never released it; the TTL was infinite. Always set a lock expiry.
F078 — env precedence: a config value set both in env and file used the file silently, ignoring the env override operators expected. Document and test precedence.
F079 — slow regex: a backtracking regex on user input took seconds on a crafted string (ReDoS). Use a linear-time matcher or anchor the pattern.
F080 — stale feature gate: a gate removed in code but left in the config store still showed in the admin UI as active. Reconcile gates on deploy.
F081 — connection pooling: the Postgres pool max was set to 200 but the DB caps at 100 connections; the extra 100 sat in a perpetual wait queue and added p99 latency. Cap the pool below the server limit.
F082 — retry backoff: the HTTP client retried with a fixed 100ms delay, synchronizing retries into a thundering herd after any blip. Switch to full-jitter exponential backoff.
F083 — cache stampede: on cache expiry, every request recomputed the same value simultaneously. Add a per-key mutex / single-flight so only one recompute runs.
F084 — index bloat: a partial index on a soft-deleted column doubled write amplification; most rows were deleted. Drop it and filter in the query instead.
F085 — clock skew: two services compared wall-clock timestamps to order events; a 400ms NTP skew reordered them. Use a logical clock or the DB's commit order.
F086 — JSON precision: large integer IDs were serialized to JSON numbers and lost precision in the JS client past 2^53. Serialize IDs as strings.
F087 — timezone drift: a nightly job ran in server-local time; a DST transition skipped/duplicated a run. Pin all schedules to UTC.
F088 — N+1 query: rendering an order list issued one query per line item. Batch with a single IN query or a join.
F089 — memory leak: a per-request logger registered a global handler never removed; handlers accumulated until OOM. Scope the handler to the request.
F090 — flag default: a new feature flag defaulted to ON in the absence of config, enabling it in environments that never set it. Default OFF; require explicit opt-in.
F091 — pagination: an offset-based paginator skipped rows when items were inserted mid-scroll. Use keyset (seek) pagination on a stable sort key.
F092 — enum drift: an enum stored as its ordinal broke when a new variant was inserted in the middle, shifting every later value. Store the name, not the ordinal.
F093 — double charge: a payment retry without an idempotency key charged twice on a network timeout. Require a client-supplied idempotency key per charge.
F094 — log volume: DEBUG logging left on in prod cost more than the service itself in egress. Gate verbosity behind a runtime-tunable level.
F095 — migration lock: an ALTER TABLE took an ACCESS EXCLUSIVE lock and stalled all reads for 40s. Use the concurrent variant and add the column nullable-first.
F096 — float money: amounts were summed as floats and drifted by cents over millions of rows. Use integer minor units (cents) end to end.
F097 — retry amplification: each of three layers retried 3x, multiplying one failure into 27 downstream calls. Retry at one layer only; fail fast elsewhere.
F098 — header casing: a proxy lowercased a custom header that the downstream compared case-sensitively. Compare headers case-insensitively.
F099 — queue ordering: a 'FIFO' worker pool processed out of order because of per-worker prefetch. Set prefetch to 1 where order matters.
F100 — TTL units: a cache TTL was set in seconds but the library expected milliseconds, expiring entries 1000x too fast. Assert units at the boundary.
F101 — partial write: a crash mid-batch left the ledger with some rows written and some not. Wrap the batch in one transaction.
F102 — rate limit: the limiter keyed on user-agent, so a shared UA throttled unrelated clients together. Key on an authenticated principal.
F103 — schema null: a NOT NULL column added without a default failed the deploy on existing rows. Backfill, then add the constraint.
F104 — DNS caching: the JVM cached a failed DNS lookup forever and never recovered after the endpoint came back. Set a finite networkaddress.cache.ttl.
F105 — signed overflow: a duration in milliseconds overflowed a 32-bit int after 24 days of uptime. Use a 64-bit type for durations.
F106 — CORS wildcard: an Access-Control-Allow-Origin wildcard plus credentials silently failed in browsers. Echo a specific allowed origin instead.
F107 — batch timeout: a 'fast' batch endpoint had no per-item timeout; one slow item stalled the whole batch. Bound each item independently.
F108 — read replica lag: a read-after-write hit a lagging replica and showed stale data. Route the immediate read to the primary.
F109 — compression bomb: an upload endpoint decompressed user gzip without a size cap; a 1KB file expanded to 4GB. Cap the decompressed size.
F110 — UUID v1 leak: UUID v1 embedded the MAC address and timestamp, leaking host identity in public IDs. Use v4 (random) for external IDs.
F111 — thread pool starve: blocking I/O on the async event loop's pool starved CPU tasks. Move blocking calls to a dedicated pool.
F112 — metric cardinality: a Prometheus label included the full URL path with IDs, exploding cardinality and OOMing the scraper. Template the path.
F113 — cookie scope: a session cookie set without an explicit Domain defaulted to the host and broke across subdomains. Set the Domain explicitly.
F114 — lazy init race: two threads lazily initialized a singleton and each built one; the second leaked. Use a thread-safe once-initializer.
F115 — retry on 4xx: the client retried 400-class errors that could never succeed, wasting budget. Retry only idempotent 5xx/timeouts.
F116 — truncated UTF-8: a fixed-byte varchar truncation split a multibyte character and corrupted the row. Truncate on character boundaries.
F117 — orphaned lock: a process that crashed holding a Redis lock never released it; the TTL was infinite. Always set a lock expiry.
F118 — env precedence: a config value set both in env and file used the file silently, ignoring the env override operators expected. Document and test precedence.
F119 — slow regex: a backtracking regex on user input took seconds on a crafted string (ReDoS). Use a linear-time matcher or anchor the pattern.
F120 — stale feature gate: a gate removed in code but left in the config store still showed in the admin UI as active. Reconcile gates on deploy.
F121 — connection pooling: the Postgres pool max was set to 200 but the DB caps at 100 connections; the extra 100 sat in a perpetual wait queue and added p99 latency. Cap the pool below the server limit.
F122 — retry backoff: the HTTP client retried with a fixed 100ms delay, synchronizing retries into a thundering herd after any blip. Switch to full-jitter exponential backoff.
F123 — cache stampede: on cache expiry, every request recomputed the same value simultaneously. Add a per-key mutex / single-flight so only one recompute runs.
F124 — index bloat: a partial index on a soft-deleted column doubled write amplification; most rows were deleted. Drop it and filter in the query instead.
F125 — clock skew: two services compared wall-clock timestamps to order events; a 400ms NTP skew reordered them. Use a logical clock or the DB's commit order.
F126 — JSON precision: large integer IDs were serialized to JSON numbers and lost precision in the JS client past 2^53. Serialize IDs as strings.
F127 — timezone drift: a nightly job ran in server-local time; a DST transition skipped/duplicated a run. Pin all schedules to UTC.
F128 — N+1 query: rendering an order list issued one query per line item. Batch with a single IN query or a join.
F129 — memory leak: a per-request logger registered a global handler never removed; handlers accumulated until OOM. Scope the handler to the request.
F130 — flag default: a new feature flag defaulted to ON in the absence of config, enabling it in environments that never set it. Default OFF; require explicit opt-in.
F131 — pagination: an offset-based paginator skipped rows when items were inserted mid-scroll. Use keyset (seek) pagination on a stable sort key.
F132 — enum drift: an enum stored as its ordinal broke when a new variant was inserted in the middle, shifting every later value. Store the name, not the ordinal.
F133 — double charge: a payment retry without an idempotency key charged twice on a network timeout. Require a client-supplied idempotency key per charge.
F134 — log volume: DEBUG logging left on in prod cost more than the service itself in egress. Gate verbosity behind a runtime-tunable level.
F135 — migration lock: an ALTER TABLE took an ACCESS EXCLUSIVE lock and stalled all reads for 40s. Use the concurrent variant and add the column nullable-first.
F136 — float money: amounts were summed as floats and drifted by cents over millions of rows. Use integer minor units (cents) end to end.
F137 — retry amplification: each of three layers retried 3x, multiplying one failure into 27 downstream calls. Retry at one layer only; fail fast elsewhere.
F138 — header casing: a proxy lowercased a custom header that the downstream compared case-sensitively. Compare headers case-insensitively.
F139 — queue ordering: a 'FIFO' worker pool processed out of order because of per-worker prefetch. Set prefetch to 1 where order matters.
F140 — TTL units: a cache TTL was set in seconds but the library expected milliseconds, expiring entries 1000x too fast. Assert units at the boundary.
F141 — partial write: a crash mid-batch left the ledger with some rows written and some not. Wrap the batch in one transaction.
F142 — rate limit: the limiter keyed on user-agent, so a shared UA throttled unrelated clients together. Key on an authenticated principal.
F143 — schema null: a NOT NULL column added without a default failed the deploy on existing rows. Backfill, then add the constraint.
F144 — DNS caching: the JVM cached a failed DNS lookup forever and never recovered after the endpoint came back. Set a finite networkaddress.cache.ttl.
F145 — signed overflow: a duration in milliseconds overflowed a 32-bit int after 24 days of uptime. Use a 64-bit type for durations.
F146 — CORS wildcard: an Access-Control-Allow-Origin wildcard plus credentials silently failed in browsers. Echo a specific allowed origin instead.
F147 — batch timeout: a 'fast' batch endpoint had no per-item timeout; one slow item stalled the whole batch. Bound each item independently.
F148 — read replica lag: a read-after-write hit a lagging replica and showed stale data. Route the immediate read to the primary.
F149 — compression bomb: an upload endpoint decompressed user gzip without a size cap; a 1KB file expanded to 4GB. Cap the decompressed size.
F150 — UUID v1 leak: UUID v1 embedded the MAC address and timestamp, leaking host identity in public IDs. Use v4 (random) for external IDs.
F151 — thread pool starve: blocking I/O on the async event loop's pool starved CPU tasks. Move blocking calls to a dedicated pool.
F152 — metric cardinality: a Prometheus label included the full URL path with IDs, exploding cardinality and OOMing the scraper. Template the path.
F153 — cookie scope: a session cookie set without an explicit Domain defaulted to the host and broke across subdomains. Set the Domain explicitly.
F154 — lazy init race: two threads lazily initialized a singleton and each built one; the second leaked. Use a thread-safe once-initializer.
F155 — retry on 4xx: the client retried 400-class errors that could never succeed, wasting budget. Retry only idempotent 5xx/timeouts.
F156 — truncated UTF-8: a fixed-byte varchar truncation split a multibyte character and corrupted the row. Truncate on character boundaries.
F157 — orphaned lock: a process that crashed holding a Redis lock never released it; the TTL was infinite. Always set a lock expiry.
F158 — env precedence: a config value set both in env and file used the file silently, ignoring the env override operators expected. Document and test precedence.
F159 — slow regex: a backtracking regex on user input took seconds on a crafted string (ReDoS). Use a linear-time matcher or anchor the pattern.
F160 — stale feature gate: a gate removed in code but left in the config store still showed in the admin UI as active. Reconcile gates on deploy.
F161 — connection pooling: the Postgres pool max was set to 200 but the DB caps at 100 connections; the extra 100 sat in a perpetual wait queue and added p99 latency. Cap the pool below the server limit.
F162 — retry backoff: the HTTP client retried with a fixed 100ms delay, synchronizing retries into a thundering herd after any blip. Switch to full-jitter exponential backoff.
F163 — cache stampede: on cache expiry, every request recomputed the same value simultaneously. Add a per-key mutex / single-flight so only one recompute runs.
F164 — index bloat: a partial index on a soft-deleted column doubled write amplification; most rows were deleted. Drop it and filter in the query instead.
F165 — clock skew: two services compared wall-clock timestamps to order events; a 400ms NTP skew reordered them. Use a logical clock or the DB's commit order.
F166 — JSON precision: large integer IDs were serialized to JSON numbers and lost precision in the JS client past 2^53. Serialize IDs as strings.
F167 — timezone drift: a nightly job ran in server-local time; a DST transition skipped/duplicated a run. Pin all schedules to UTC.
F168 — N+1 query: rendering an order list issued one query per line item. Batch with a single IN query or a join.
F169 — memory leak: a per-request logger registered a global handler never removed; handlers accumulated until OOM. Scope the handler to the request.
F170 — flag default: a new feature flag defaulted to ON in the absence of config, enabling it in environments that never set it. Default OFF; require explicit opt-in.
F171 — pagination: an offset-based paginator skipped rows when items were inserted mid-scroll. Use keyset (seek) pagination on a stable sort key.
F172 — enum drift: an enum stored as its ordinal broke when a new variant was inserted in the middle, shifting every later value. Store the name, not the ordinal.
F173 — double charge: a payment retry without an idempotency key charged twice on a network timeout. Require a client-supplied idempotency key per charge.
F174 — log volume: DEBUG logging left on in prod cost more than the service itself in egress. Gate verbosity behind a runtime-tunable level.
F175 — migration lock: an ALTER TABLE took an ACCESS EXCLUSIVE lock and stalled all reads for 40s. Use the concurrent variant and add the column nullable-first.
F176 — float money: amounts were summed as floats and drifted by cents over millions of rows. Use integer minor units (cents) end to end.
F177 — retry amplification: each of three layers retried 3x, multiplying one failure into 27 downstream calls. Retry at one layer only; fail fast elsewhere.
F178 — header casing: a proxy lowercased a custom header that the downstream compared case-sensitively. Compare headers case-insensitively.
F179 — queue ordering: a 'FIFO' worker pool processed out of order because of per-worker prefetch. Set prefetch to 1 where order matters.
F180 — TTL units: a cache TTL was set in seconds but the library expected milliseconds, expiring entries 1000x too fast. Assert units at the boundary.
F181 — partial write: a crash mid-batch left the ledger with some rows written and some not. Wrap the batch in one transaction.
F182 — rate limit: the limiter keyed on user-agent, so a shared UA throttled unrelated clients together. Key on an authenticated principal.
F183 — schema null: a NOT NULL column added without a default failed the deploy on existing rows. Backfill, then add the constraint.
F184 — DNS caching: the JVM cached a failed DNS lookup forever and never recovered after the endpoint came back. Set a finite networkaddress.cache.ttl.
F038 — non-interactive doctrine loading: `@`-imports fail SILENTLY under `claude -p`. When a CLAUDE.md or system prompt uses an `@path/to/file.md` import and the model runs non-interactively (`claude -p`), the import is NOT resolved — the referenced file content never reaches the model, and instead of erroring the model CONFABULATES plausible content for the missing file ~43% of the time (measured, n=7). The fix is to inline the content or pass `--append-system-prompt-file`, and run a verbatim-quote sentinel load-test before trusting output.
F185 — signed overflow: a duration in milliseconds overflowed a 32-bit int after 24 days of uptime. Use a 64-bit type for durations.
F186 — CORS wildcard: an Access-Control-Allow-Origin wildcard plus credentials silently failed in browsers. Echo a specific allowed origin instead.
F187 — batch timeout: a 'fast' batch endpoint had no per-item timeout; one slow item stalled the whole batch. Bound each item independently.
F188 — read replica lag: a read-after-write hit a lagging replica and showed stale data. Route the immediate read to the primary.
F189 — compression bomb: an upload endpoint decompressed user gzip without a size cap; a 1KB file expanded to 4GB. Cap the decompressed size.
F190 — UUID v1 leak: UUID v1 embedded the MAC address and timestamp, leaking host identity in public IDs. Use v4 (random) for external IDs.
F191 — thread pool starve: blocking I/O on the async event loop's pool starved CPU tasks. Move blocking calls to a dedicated pool.
F192 — metric cardinality: a Prometheus label included the full URL path with IDs, exploding cardinality and OOMing the scraper. Template the path.
F193 — cookie scope: a session cookie set without an explicit Domain defaulted to the host and broke across subdomains. Set the Domain explicitly.
F194 — lazy init race: two threads lazily initialized a singleton and each built one; the second leaked. Use a thread-safe once-initializer.
F195 — retry on 4xx: the client retried 400-class errors that could never succeed, wasting budget. Retry only idempotent 5xx/timeouts.
F196 — truncated UTF-8: a fixed-byte varchar truncation split a multibyte character and corrupted the row. Truncate on character boundaries.
F197 — orphaned lock: a process that crashed holding a Redis lock never released it; the TTL was infinite. Always set a lock expiry.
F198 — env precedence: a config value set both in env and file used the file silently, ignoring the env override operators expected. Document and test precedence.
F199 — slow regex: a backtracking regex on user input took seconds on a crafted string (ReDoS). Use a linear-time matcher or anchor the pattern.
F200 — stale feature gate: a gate removed in code but left in the config store still showed in the admin UI as active. Reconcile gates on deploy.
