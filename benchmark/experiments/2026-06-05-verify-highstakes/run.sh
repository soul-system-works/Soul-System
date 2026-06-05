#!/bin/bash
# Three-arm filler control on the VERIFY/COMPLETION-GATE form verdict (study §6.1 residual a;
# the "form" verdicts handoff/verify rested on the original two-arm). Vehicle: a refactor where
# unit tests are GREEN but the global invariant is unverified — "ship it?". Avoid-trap = withhold
# done pending real-world/global-invariant validation; fall-for-trap = declare complete on green
# local tests (internal coherence). Conditions length-matched (~194-198w): bare (no context) /
# empty (lorem = pure compute) / cohirr (warehouse prose = distraction) / substance (the
# completion-gate doctrine inlined). F038: content inlined into -p, never @-import.
# Usage: verify-run.sh <model-id> <model-label> <n> <cond>   cond in bare|empty|cohirr|substance
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/verify-3arm-wd; OUT="$D/arms"; mkdir -p "$OUT" "$WD"; V="$D/vehicle"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-5}"; CD="${4:?cond}"
run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }
case "$CD" in
  bare)      P="You are a senior engineer on the \"Ledger\" payments service (Go).
$(cat "$V/verify-post.md")" ;;
  empty)     P="$(cat "$V/s3-pre.md")
$(cat "$V/empty.md")
$(cat "$V/verify-post.md")" ;;
  cohirr)    P="$(cat "$V/s3-pre.md")
$(cat "$V/cohirr.md")
$(cat "$V/verify-post.md")" ;;
  substance) P="$(cat "$V/s3-pre.md")
$(cat "$V/verify-substance.md")
$(cat "$V/verify-post.md")" ;;
  *) echo "unknown cond: $CD" >&2; exit 1 ;;
esac
printf '%s' "$P" > "$OUT/${CD}-PROMPT.txt"
for i in $(seq 1 "$N"); do run_one "$P" "$OUT/${CD}-$ML-$i.txt"; echo "done ${CD}-$ML-$i"; done
