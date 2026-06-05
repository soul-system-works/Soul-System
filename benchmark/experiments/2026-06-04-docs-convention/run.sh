#!/bin/bash
# Meta-doctrine ablation — DOCS-CONVENTION probe (derivable-convention class).
# Vehicle: a contributor proposes a top-level docs/architecture/ tree; the project's actual
# convention is docs-live-near-code. avoid-trap = REJECT the central tree citing co-location;
# fall-for-trap = ADOPT it (the trained-in "centralized docs are tidy" default).
# Four length-matched arms (~198-210w injected): bare (no context) / empty (lorem = pure
# compute) / cohirr (warehouse-ops prose = distraction) / substance (the project conventions
# incl. docs-near-code). Score by READING the recommendation, not keywords (SCORING.md §1).
# F038: every fragment is INLINED into -p, never @-imported.
#
# Usage: run.sh <model-id> <model-label> <n> <arm>     arm ∈ bare|empty|cohirr|substance
set -u
D="$(cd "$(dirname "$0")" && pwd)"; V="$D/vehicle"; WD=/tmp/docs-convention-wd; OUT="$D/arms"
mkdir -p "$OUT" "$WD"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-5}"; CD="${4:?arm}"
run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }
case "$CD" in
  bare)      P="You are a senior engineer on the \"Ledger\" payments service (Go).
$(cat "$V/task-post.md")" ;;
  empty)     P="$(cat "$V/s3-pre.md")
$(cat "$V/empty.md")
$(cat "$V/task-post.md")" ;;
  cohirr)    P="$(cat "$V/s3-pre.md")
$(cat "$V/cohirr.md")
$(cat "$V/task-post.md")" ;;
  substance) P="$(cat "$V/s3-pre.md")
$(cat "$V/substance.md")
$(cat "$V/task-post.md")" ;;
  *) echo "unknown arm: $CD" >&2; exit 1 ;;
esac
printf '%s' "$P" > "$OUT/${CD}-PROMPT.txt"
for i in $(seq 1 "$N"); do run_one "$P" "$OUT/${CD}-$ML-$i.txt"; echo "done ${CD}-$ML-$i"; done
