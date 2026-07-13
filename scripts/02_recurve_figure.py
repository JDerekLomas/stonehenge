"""Figure: recurve rate in carvings vs axes with Wilson CIs."""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).parent.parent
with open(ROOT / "data" / "processed" / "recurve_results.json") as f:
    results = json.load(f)

fig, ax = plt.subplots(figsize=(7, 4.5))

labels, ps, err_lo, err_hi, ns = [], [], [], [], []
for r in results:
    c = r["carvings"]
    a = r["axes"]
    tag = r["comparison"].split(" vs ")[0]
    labels.append(f"{tag}\n(n={c['n']})")
    ps.append(c["p"] * 100)
    err_lo.append((c["p"] - c["ci95"][0]) * 100)
    err_hi.append((c["ci95"][1] - c["p"]) * 100)
    ns.append(c["n"])

axe_p = results[0]["axes"]["p"] * 100
axe_ci = results[0]["axes"]["ci95"]
labels.append(f"British EBA axes\n(n={results[0]['axes']['n']})")
ps.append(axe_p)
err_lo.append((results[0]["axes"]["p"] - axe_ci[0]) * 100)
err_hi.append((axe_ci[1] - results[0]["axes"]["p"]) * 100)

colors = ["#c14545", "#c14545", "#c14545", "#4a6fa5"]
x = np.arange(len(labels))
ax.bar(x, ps, yerr=[err_lo, err_hi], capsize=6, color=colors,
       edgecolor="black", linewidth=0.8)
for i, p in enumerate(ps):
    ax.text(i, p + err_hi[i] + 1.5, f"{p:.1f}%", ha="center", fontsize=10)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel("Percentage with recurve feature", fontsize=11)
ax.set_ylim(0, 60)
ax.set_title("Recurve is 5–6× more common on Stonehenge carvings than on real EBA axes",
             fontsize=11.5, pad=12)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Annotation
ax.annotate("Fisher exact p = 1.3×10⁻⁷\nOdds ratio = 8.1",
            xy=(2, 40), xytext=(1.2, 52),
            fontsize=9, ha="left",
            arrowprops=dict(arrowstyle="->", color="black", lw=0.7))

plt.tight_layout()
plt.savefig(ROOT / "figures" / "recurve_comparison.png", dpi=200,
            bbox_inches="tight")
plt.savefig(ROOT / "figures" / "recurve_comparison.pdf",
            bbox_inches="tight")
print("Saved figures/recurve_comparison.{png,pdf}")
