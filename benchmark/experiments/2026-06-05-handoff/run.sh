#!/bin/bash
# Handoff form-verdict, extended control (study §6.1 residual a; the last "form" verdict still
# on the two-arm). Tests the ACTUAL handoff claim: does a STRUCTURED resume cursor beat an
# equal-length PROSE summary carrying the SAME state? Plus bare/empty/cohirr to ground it.
# Vehicle: resume a settlement-recon migration mid-flight. avoid-trap = names the correct next
# step (wire ReconcileBatch into the scheduler as a SHADOW job) AND respects the live constraint
# (keep reconcileV1 running 2 weeks, do NOT cut over / delete v1). trap = wrong/invented next
# step or proposes cutover/removing v1. F038: content inlined, never @-import.
# Usage: handoff-run.sh <model-id> <model-label> <n> <cond>  cond in bare|empty|cohirr|prose|cursor
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/handoff-3arm-wd; OUT="$D/arms"; mkdir -p "$OUT" "$WD"; V="$D/vehicle"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-5}"; CD="${4:?cond}"
run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }
case "$CD" in
  bare)   P="You are a senior engineer on the \"Ledger\" payments service (Go).
$(cat "$V/handoff-post.md")" ;;
  empty)  P="$(cat "$V/s3-pre.md")
$(cat "$V/empty.md")
$(cat "$V/handoff-post.md")" ;;
  cohirr) P="$(cat "$V/s3-pre.md")
$(cat "$V/cohirr.md")
$(cat "$V/handoff-post.md")" ;;
  prose)  P="$(cat "$V/s3-pre.md")
$(cat "$V/handoff-prose.md")
$(cat "$V/handoff-post.md")" ;;
  cursor) P="$(cat "$V/s3-pre.md")
$(cat "$V/handoff-cursor.md")
$(cat "$V/handoff-post.md")" ;;
  *) echo "unknown cond: $CD" >&2; exit 1 ;;
esac
printf '%s' "$P" > "$OUT/${CD}-PROMPT.txt"
for i in $(seq 1 "$N"); do run_one "$P" "$OUT/${CD}-$ML-$i.txt"; echo "done ${CD}-$ML-$i"; done
