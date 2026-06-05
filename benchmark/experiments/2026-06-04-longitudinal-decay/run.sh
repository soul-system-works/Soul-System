#!/bin/bash
# Longitudinal DECAY probe (SOUL-I045) — does the carry survive a LONG record?
# KNOB: record DEPTH N = # of intervening ADRs between D (ADR-001, the FACT no-retry
# decision, REUSED from SOUL-123) and the S3 fork task. "Many sessions" ≡ deeper burial.
# N=1 is already measured (SOUL-123 = 5/5 HOLD both models); this extends the ladder.
#
# ARMS at depth N (all share the S3 task = SendPayout, context C absent):
#   withrecord: [ADR-001 = no-retry D] + [N burial ADRs]              → does D still fire?
#   control:    [ADR-030 filler-anchor, length-matched to D] + [N burial ADRs]  (NO D)
#   floor:      no record (N-independent — run once)
# The control isolates POSITION/volume decay from generic long-context degradation:
# it is the SAME length as with-record, differing ONLY in whether the anchor ADR is the
# no-retry decision. If withrecord HOLD falls to meet control DRIFT at large N, the cliff
# is D-becoming-unfindable, not "long context degrades everything".
#
# Records inlined into -p (NEVER @-import — F038). Each arm's exact prompt saved.
# Usage: run-decay.sh <model-id> <model-label> <n> <arm> <N>   arm ∈ withrecord|control|floor
set -u
D="$(cd "$(dirname "$0")" && pwd)"; WD=/tmp/longitudinal-pref-wd; OUT="$D/arms"; POOL="$OUT/pool"; V="$D/vehicle"
mkdir -p "$WD" "$POOL"
MODEL="${1:?model id}"; ML="${2:?model label}"; N="${3:-3}"; ARM="${4:?arm}"; DEPTH="${5:-0}"

# Split the pool once (idempotent): p0..p20 from pool-raw.txt on ===ADR===
if [ ! -f "$POOL/p0.md" ]; then
  awk -v out="$POOL" 'BEGIN{i=0} /^===ADR===/{i++; next} {print >> (out"/p"i".md")}' "$V/pool-raw.txt"
  echo "split pool → $(ls "$POOL" | wc -l) files"
fi

run_one(){ ( cd "$WD" && claude -p "$1" --model "$MODEL" < /dev/null ) > "$2" 2>&1; }

build_record(){  # $1=arm $2=N  → echoes the record block
  local arm="$1" n="$2" i
  if [ "$arm" = withrecord ]; then cat "$V/adr-D.md"; else cat "$POOL/p20.md"; fi
  for i in $(seq 0 $((n-1))); do echo; echo; cat "$POOL/p$i.md"; done
}

case "$ARM" in
  withrecord|control)
      REC="$(build_record "$ARM" "$DEPTH")"
      P="$(cat "$V/s3-pre.md")
$REC
$(cat "$V/s3-post.md")"
      printf '%s' "$P" > "$OUT/${ARM}-N${DEPTH}-PROMPT.txt"
      for i in $(seq 1 "$N"); do run_one "$P" "$OUT/${ARM}-N${DEPTH}-$ML-$i.txt"; echo "done ${ARM}-N${DEPTH}-$ML-$i"; done ;;
  floor)
      P="$(cat "$V/s3-floor.md")"
      printf '%s' "$P" > "$OUT/floor-PROMPT.txt"
      for i in $(seq 1 "$N"); do run_one "$P" "$OUT/floor-$ML-$i.txt"; echo "done floor-$ML-$i"; done ;;
  *) echo "unknown arm: $ARM" >&2; exit 1 ;;
esac
