Project engineering record — selected findings (read before infra work):

F038 — `@`-imports fail SILENTLY under `claude -p`. When a `CLAUDE.md` or system prompt uses an `@path/to/file.md` import and the model runs non-interactively (`claude -p`), the import is NOT resolved — the referenced file content never reaches the model. Worse, instead of erroring, the model CONFABULATES plausible-but-fabricated content for the missing file roughly 43% of the time (measured, n=7); the runs look completely successful. The fix is to inline the file content directly, or pass it via `--append-system-prompt-file <path>`, and to run a sentinel load-test — a short verbatim-quote check that only the real file's content can pass — on every run before trusting any output.

F022 — the Prometheus metrics endpoint binds to the internal port `:9090` only, never the public API gateway; exposing it publicly is a standing incident.

F031 — rasterize generated geometry and visually inspect it before committing; a self-intersecting turbine polygon shipped once because the visual gate was skipped.

F040 — before claiming a retire is safe, investigate uniqueness; an "unused" helper had one caller behind a feature flag.
