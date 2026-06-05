#!/bin/bash
# Reasoning-PREFERENCE probe — floor-check counter-default-ness BEFORE building the chain
# (the SOUL-122 method lesson, reused from longitudinal-drift-v2).
# For each candidate preference D, run the S3-equivalent task FRESH (no record) and read
# what the model does BY DEFAULT. We want D where the default is reliably the NON-preferred
# (counter-default) path AT BOTH MODELS — Sonnet counter-default is the binding constraint,
# since the whole question is what the FRONTIER model does.
#   P1 errstyle:   default=raise exceptions     | preferred=return Result/(value,error)
#   P2 validation: default=guard in process_fn  | preferred=validate at construction
#   P3 repository: default=inline SQL in the fn  | preferred=route through a repository
# Usage: floorcheck.sh <model-id> <model-label> <n>
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/longitudinal-pref-wd; OUT="$D/floorcheck"; mkdir -p "$WD"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-3}"
for cand in P1-errstyle P2-validation P3-repository; do
  for i in $(seq 1 "$N"); do
    ( cd "$WD" && claude -p "$(cat "$D/floorcheck/$cand.md")" --model "$MODEL" < /dev/null ) > "$OUT/floor-$cand-$ML-$i.txt" 2>&1
    echo "done floor-$cand-$ML-$i"
  done
done
