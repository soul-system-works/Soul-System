#!/bin/bash
# Token-scale + position depth test (study §6.1 #4; against 'lost in the middle' [5]).
# The F038 needle (the recorded fact that @-imports fail silently under `claude -p`) is buried
# in a ~6.6k-token engineering record at 8% / 50% / 92% depth. Task = the recall trap (endorse
# @-import under -p?). Avoid-trap = uses the buried fact (reject @-import / inline / sentinel).
# Tests whether MIDDLE placement degrades recall vs EARLY/LATE at token scale — the original
# depth probe (SOUL-134 neighborhood) was primacy-only at ~20 record UNITS.
# F038: the record is INLINED into -p (never @-import — that is the very fact under test).
# Usage: depth-run.sh <model-id> <model-label> <n> <pos>   pos in early|middle|late
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/depth-pos-wd; OUT="$D/arms"; mkdir -p "$OUT" "$WD"; V="$D/vehicle"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-5}"; POS="${4:?pos}"
case "$POS" in early|middle|late) ;; *) echo "bad pos: $POS" >&2; exit 1;; esac
run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }
P="$(cat "$V/s3-pre.md")
$(cat "$V/context-$POS.md")
$(cat "$V/recall-post.md")"
printf '%s' "$P" > "$OUT/${POS}-PROMPT.txt"
for i in $(seq 1 "$N"); do run_one "$P" "$OUT/${POS}-$ML-$i.txt"; echo "done ${POS}-$ML-$i"; done
