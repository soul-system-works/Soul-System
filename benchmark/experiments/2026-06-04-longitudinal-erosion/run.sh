#!/bin/bash
# Longitudinal EROSION probe (SOUL-I045 sibling) — does D survive COMPRESSION?
# Tests which PART of D is load-bearing under /soul-distill-style compression, at fixed
# depth (N=1, isolating erosion from depth). Same S3 task (SendPayout), context C absent.
#   e0    = full D (SOUL-123 verbatim: decision + rationale + 1,180 incident + the FACT
#           that the endpoint has no idempotency support). Baseline.
#   edir  = directive only — "must NOT auto-retry; fail fast" — the unguessable FACT stripped.
#   edist = D as ONE line in a distilled 6-rule set (the realistic mind.md-style output).
# KEY hypothesis: stripping the rationale lets the FRONTIER model OVERRIDE the surviving
# directive (adds a "safe" retry with an INVENTED idempotency key — the SOUL-123 drift),
# because the fact that would stop it is exactly what compression removed.
# Read-confirm in code: retry loop present (DRIFT) / absent + fail-fast (HOLD). F038: inline.
# Usage: run-erosion.sh <model-id> <model-label> <n> <level>   level ∈ e0|edir|edist|floor
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/longitudinal-pref-wd; OUT="$D/arms"; mkdir -p "$OUT" "$WD"; V="$D/vehicle"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-5}"; LV="${4:?level}"
run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }
case "$LV" in
  e0)    REC="$(cat "$V/adr-D-full.md")" ;;
  edir)  REC="$(cat "$V/adr-D-directive.md")" ;;
  edist) REC="$(cat "$V/adr-D-distilled.md")" ;;
  floor) REC="" ;;
  *) echo "unknown level: $LV" >&2; exit 1 ;;
esac
if [ "$LV" = floor ]; then
  P="$(cat "$V/s3-floor.md")"
else
  P="$(cat "$V/s3-pre.md")
$REC
$(cat "$V/s3-post.md")"
fi
printf '%s' "$P" > "$OUT/${LV}-PROMPT.txt"
for i in $(seq 1 "$N"); do run_one "$P" "$OUT/${LV}-$ML-$i.txt"; echo "done ${LV}-$ML-$i"; done
