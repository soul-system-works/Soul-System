#!/bin/bash
# Longitudinal PREFERENCE probe (sibling of longitudinal-drift-v2 / SOUL-123).
# D = expected business failures are signalled by returning a Result type, NOT by raising
#     exceptions. A reasoning-PREFERENCE (both paths valid), counter-default 6/6 at both
#     models in the floor-check. Tests deference-vs-override at the frontier: does the
#     frontier model defer to a recorded arbitrary convention, or override it with its
#     own (equally-valid) idiom?
# Chain is a PIPELINE; arms fork at S3. Records inlined directly into -p (NOT @-import, F038).
# Each S3 arm's exact prompt saved for read-confirm.
# Usage: run.sh <model-id> <model-label> <n> <arm>   arm ∈ s1|s2|withrecord|control|floor
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/longitudinal-pref-wd; OUT="$D/arms"; mkdir -p "$OUT" "$WD"; V="$D/vehicle"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-5}"; ARM="${4:?arm}"
run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }
case "$ARM" in
  s1) run_one "$(cat "$V/s1.md")" "$OUT/record_1.txt"; echo "done s1" ;;
  s2) P="$(cat "$V/s2-pre.md")
$(cat "$OUT/record_1.txt")
$(cat "$V/s2-post.md")"
      run_one "$P" "$OUT/record_2-delta.txt"; echo "done s2" ;;
  withrecord)
      REC="$(cat "$OUT/record_1.txt"; echo; echo; cat "$OUT/record_2-delta.txt")"
      P="$(cat "$V/s3-pre.md")
$REC
$(cat "$V/s3-post.md")"
      printf '%s' "$P" > "$OUT/s3-withrecord-PROMPT.txt"
      for i in $(seq 1 "$N"); do run_one "$P" "$OUT/s3-withrecord-$ML-$i.txt"; echo "done wr-$ML-$i"; done ;;
  control)
      REC="$(cat "$V/filler.txt")"
      P="$(cat "$V/s3-pre.md")
$REC
$(cat "$V/s3-post.md")"
      printf '%s' "$P" > "$OUT/s3-control-PROMPT.txt"
      for i in $(seq 1 "$N"); do run_one "$P" "$OUT/s3-control-$ML-$i.txt"; echo "done ctl-$ML-$i"; done ;;
  floor)
      P="$(cat "$V/s3-floor.md")"
      printf '%s' "$P" > "$OUT/s3-floor-PROMPT.txt"
      for i in $(seq 1 "$N"); do run_one "$P" "$OUT/s3-floor-$ML-$i.txt"; echo "done fl-$ML-$i"; done ;;
  *) echo "unknown arm: $ARM" >&2; exit 1 ;;
esac
