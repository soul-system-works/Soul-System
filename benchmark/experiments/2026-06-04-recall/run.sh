#!/bin/bash
# Three-arm filler control on the RECALL probe (the clean substance vehicle — generic reasoning
# gets the trap CONFIDENTLY WRONG, so disposition can't rescue it). Trap: endorse the @-import
# to load shared doctrine under `-p` (DRY, looks right). Avoid-trap = inline / --append-system-
# prompt-file (the F038 finding). Conditions length-matched (~190w): bare / empty (lorem=compute)
# / cohirr (warehouse=distraction) / rsub (the F038 record=substance). F038: content inlined.
# Usage: recall-run.sh <model-id> <model-label> <n> <cond>   cond in bare|empty|cohirr|rsub
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/three-arm-wd; OUT="$D/arms"; mkdir -p "$OUT" "$WD"; V="$D/vehicle"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-5}"; CD="${4:?cond}"
run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }
case "$CD" in
  bare)   P="You are a senior engineer on the \"Ledger\" payments service (Go).
$(cat "$V/recall-post.md")" ;;
  empty)  P="$(cat "$V/s3-pre.md")
$(cat "$V/empty.md")
$(cat "$V/recall-post.md")" ;;
  cohirr) P="$(cat "$V/s3-pre.md")
$(cat "$V/cohirr.md")
$(cat "$V/recall-post.md")" ;;
  rsub)   P="$(cat "$V/s3-pre.md")
$(cat "$V/recall-substance.md")
$(cat "$V/recall-post.md")" ;;
  *) echo "unknown cond: $CD" >&2; exit 1 ;;
esac
printf '%s' "$P" > "$OUT/recall-${CD}-PROMPT.txt"
for i in $(seq 1 "$N"); do run_one "$P" "$OUT/recall-${CD}-$ML-$i.txt"; echo "done recall-${CD}-$ML-$i"; done
