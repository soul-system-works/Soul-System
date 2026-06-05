#!/usr/bin/env python3
"""Calibration gradient (SOUL-137): across a capability ladder, the recall of an unguessable
fact stays flat at ~floor (the fact is never re-derived), while the rate of CONFIDENTLY
asserting the false mechanism RISES with capability. Deterministic; regenerates the PNG.
Data: recall/F038 no-fact arms, n=15/tier (3 arms x 5). Grade A = fails to recall (endorses
@-import under -p). Grade B = explicitly + confidently asserts the false '-p == interactive'
mechanism (counts approximate -> shown as a range)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

tiers = ["Haiku 4.5\n(weak)", "Sonnet 4.6\n(mid)", "Opus 4.8\n(frontier)"]
x = [0, 1, 2]

# Grade A: fail-to-recall, /15  -> 14, 15, 15
gradeA = [14/15*100, 15/15*100, 15/15*100]
# Grade B: confident false assertion, approximate ranges /15
gradeB_lo = [2/15*100, 5/15*100, 11/15*100]
gradeB_hi = [4/15*100, 7/15*100, 13/15*100]
gradeB_mid = [(lo+hi)/2 for lo, hi in zip(gradeB_lo, gradeB_hi)]
gradeB_err = [[m-lo for m, lo in zip(gradeB_mid, gradeB_lo)],
              [hi-m for m, hi in zip(gradeB_mid, gradeB_hi)]]

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(x, gradeA, "o-", color="#b02418", lw=2.4, ms=9,
        label="Fails to recall the fact (Grade A) — endorses the trap")
ax.errorbar(x, gradeB_mid, yerr=gradeB_err, fmt="s--", color="#1f5fb0", lw=2.4, ms=9,
            capsize=5, label="Confidently asserts the falsehood (Grade B, approx.)")

ax.set_xticks(x); ax.set_xticklabels(tiers)
ax.set_ylim(0, 105); ax.set_ylabel("% of no-fact cells  (n = 15 / tier)")
ax.set_title("Capability does not resolve confident fabrication —\nit makes it more articulate",
             fontsize=12, pad=12)
ax.grid(axis="y", ls=":", alpha=0.5)
ax.legend(loc="center left", fontsize=9, framealpha=0.95)
ax.annotate("the unguessable fact is\nnever re-derived (flat)", xy=(1, 100), xytext=(0.55, 70),
            fontsize=8.5, color="#b02418",
            arrowprops=dict(arrowstyle="->", color="#b02418", alpha=0.7))
ax.annotate("the strongest model states\nthe falsehood most cleanly", xy=(2, 80), xytext=(0.9, 86),
            fontsize=8.5, color="#1f5fb0",
            arrowprops=dict(arrowstyle="->", color="#1f5fb0", alpha=0.7))
fig.tight_layout()
fig.savefig("docs/study/figures/calibration-gradient.png", dpi=150)
print("wrote docs/study/figures/calibration-gradient.png")
