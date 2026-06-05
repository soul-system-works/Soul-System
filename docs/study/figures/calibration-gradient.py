#!/usr/bin/env python3
"""Calibration, two runs (SOUL-137 original + SOUL-142 reproducibility rerun). Across a
capability ladder Haiku->Sonnet->Opus, the hidden fact (F038's '@-imports fail silently
under -p') is NEVER spontaneously recalled at any tier (flat, robust). The rate of
CONFIDENTLY asserting the false '-p == interactive' mechanism is SCORING-FRAGILE: two
independent runs/readings diverge sharply at the top tier (Opus ~12/15 -> 0/15), because
Opus tends to assert the falsehood AND then recommend a verify-it-loaded canary (and often
rejects the @-import outright). So there is NO reliable capability gradient; the surviving
claim is non-elimination, not 'stronger => more confident'. Deterministic; regenerates the PNG.
Data: recall/F038 no-fact arms, n=15/tier (3 arms x 5)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

tiers = ["Haiku 4.5\n(weak)", "Sonnet 4.6\n(mid)", "Opus 4.8\n(frontier)"]
x = [0, 1, 2]

# Never recalls the hidden fact (Grade A knowledge axis): ~flat near 100%, both runs.
# No tier states the F038 mechanism; Opus's safe cells on rerun avoid the trap by GENERIC
# caution + a verify step, not by recalling the fact -> recall stays ~floor.
recall_fail = [100, 100, 100]

# Confidently asserts the falsehood (Grade B), two independent runs:
gradeB_run1 = [3/15*100, 6/15*100, 12/15*100]   # SOUL-137 original (lenient reading)
gradeB_run2 = [1/15*100, 9/15*100,  0/15*100]   # SOUL-142 rerun (strict: verify-step disqualifies)

fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.plot(x, recall_fail, "o-", color="#b02418", lw=2.4, ms=9,
        label="Never recalls the hidden fact (flat — robust, both runs)")
ax.plot(x, gradeB_run1, "s--", color="#1f5fb0", lw=2.2, ms=8,
        label="Confidently asserts the falsehood — run 1 (lenient)")
ax.plot(x, gradeB_run2, "D:", color="#5fa83a", lw=2.2, ms=8,
        label="Confidently asserts the falsehood — run 2 (strict rerun)")

ax.set_xticks(x); ax.set_xticklabels(tiers)
ax.set_ylim(0, 105); ax.set_ylabel("% of no-fact cells  (n = 15 / tier)")
ax.set_title("The fact is unguessable at every scale (flat);\nthe 'confident falsehood' rate is "
             "scoring-fragile — no reliable gradient", fontsize=11.5, pad=12)
ax.grid(axis="y", ls=":", alpha=0.5)
ax.legend(loc="center left", fontsize=8.5, framealpha=0.95)
ax.annotate("the hidden fact is\nnever recalled (flat)", xy=(1, 100), xytext=(0.5, 64),
            fontsize=8.5, color="#b02418",
            arrowprops=dict(arrowstyle="->", color="#b02418", alpha=0.7))
ax.annotate("two runs diverge at the top tier\n(12/15 → 0/15): no stable gradient",
            xy=(2, 6), xytext=(0.75, 30), fontsize=8.5, color="#444",
            arrowprops=dict(arrowstyle="->", color="#444", alpha=0.7))
fig.tight_layout()
fig.savefig("docs/study/figures/calibration-gradient.png", dpi=150)
print("wrote docs/study/figures/calibration-gradient.png")
