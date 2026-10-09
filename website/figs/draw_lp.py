"""Draw 7 copy-ready graph-paper answer figures for Q1(b) LP0-LP6."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

OUT = "figs"

STYLE = {
    "paper": "#f4faf4",
    "major": "#7fbf7f",
    "minor": "#c4e6c4",
    "cons": "#1a3a5f",
    "branch": "#b91c1c",
    "shade": "#bfe3f5",
    "opt": "#f59e0b",
}

# feasible polygons (ordered vertices) per node; None = infeasible
POLY = {
    "LP0": [(1, 0), (2.5, 0), (1.5, 2), (0, 3.5), (0, 1)],
    "LP1": [(1, 0), (1, 2.5), (0, 3.5), (0, 1)],
    "LP2": [(2, 0), (2.5, 0), (2, 1)],
    "LP3": [(1, 0), (1, 2), (0, 2), (0, 1)],
    "LP4": [(0, 3), (0.5, 3), (0, 3.5)],
    "LP5": [(0, 3), (0, 3.5)],
    "LP6": None,
}
OPT = {
    "LP0": ((1.5, 2), 19.75, "Branch x1"),
    "LP1": ((1, 2.5), 19.0, "Branch x2"),
    "LP2": ((2, 1), 18.0, "Integer: fathomed (test 3), z* = 18"),
    "LP3": ((1, 2), 16.5, "Integer, 16.5 <= 18: fathomed (test 1)"),
    "LP4": ((0.5, 3), 18.25, "Branch x1"),
    "LP5": ((0, 3.5), 17.5, "17.5 <= 18: fathomed (test 1)"),
    "LP6": (None, None, "Infeasible: fathomed (test 2)"),
}
ADDED = {
    "LP0": "added: none",
    "LP1": "added: x1 <= 1",
    "LP2": "added: x1 >= 2",
    "LP3": "added: x1 <= 1, x2 <= 2",
    "LP4": "added: x1 <= 1, x2 >= 3",
    "LP5": "added: x1 <= 1, x2 >= 3, x1 <= 0",
    "LP6": "added: x1 <= 1, x2 >= 3, x1 >= 1",
}
BRANCH_LINES = {
    "LP1": [("v", 1, "x1=1"),
             ],
    "LP2": [("v", 2, "x1=2")],
    "LP3": [("v", 1, "x1=1"), ("h", 2, "x2=2")],
    "LP4": [("v", 1, "x1=1"), ("h", 3, "x2=3")],
    "LP5": [("h", 3, "x2=3")],
    "LP6": [("v", 1, "x1=1"), ("h", 3, "x2=3")],
}


def base_ax(title):
    fig, ax = plt.subplots(figsize=(7, 6.2))
    fig.patch.set_facecolor("white")
    ax.set_facecolor(STYLE["paper"])
    ax.set_xlim(-0.4, 4.2)
    ax.set_ylim(-0.5, 4.6)
    ax.set_xlabel("x1", fontsize=13)
    ax.set_ylabel("x2", fontsize=13)
    ax.set_xticks(range(0, 5))
    ax.set_yticks(range(0, 5))
    for spine in ax.spines.values():
        spine.set_color("black")
        spine.set_linewidth(1.2)
    ax.grid(which="major", color=STYLE["major"], linewidth=0.7)
    ax.grid(which="minor", color=STYLE["minor"], linewidth=0.4)
    ax.set_axisbelow(True)
    # minor ticks every 0.5 like graph paper squares (2 per unit)
    ax.set_xticks(np.arange(0, 4.5, 0.5), minor=True)
    ax.set_yticks(np.arange(0, 5.0, 0.5), minor=True)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    return fig, ax


def draw_constraints(ax):
    x = np.linspace(-0.4, 4.2, 200)
    # (1) 2x1+2x2=7 -> x2 = 3.5-x1
    ax.plot(x, 3.5 - x, color=STYLE["cons"], lw=2)
    # (2) 2x1+x2=5 -> x2 = 5-2x1
    ax.plot(x, 5 - 2 * x, color=STYLE["cons"], lw=2)
    # (3) x1+x2=1 -> x2 = 1-x1
    ax.plot(x, 1 - x, color=STYLE["cons"], lw=2)
    ax.text(3.35, 0.35, "(1) 2x1+2x2=7", fontsize=10)
    ax.text(2.55, 0.6, "(2) 2x1+x2=5", fontsize=10)
    ax.text(1.15, 0.15, "(3) x1+x2=1", fontsize=10)
    # intercept labels
    for px, py, s in [(3.5, 0, "3.5"), (0, 3.5, "3.5"),
                      (2.5, 0, "2.5"), (0, 5, ""), (1, 0, "1"), (0, 1, "1")]:
        if s and -0.4 <= px <= 4.2 and -0.5 <= py <= 4.6:
            ax.plot(px, py, "o", color=STYLE["cons"], ms=5)
    # feasible-side arrows (origin side for (1)(2), far side for (3))
    ax.annotate("", xy=(0.5, 0.5), xytext=(0.9, 0.9),
                arrowprops=dict(arrowstyle="->", color=STYLE["cons"], lw=1.5))
    ax.text(0.15, 0.62, "(1)(2)", fontsize=9)
    ax.annotate("", xy=(2.2, 2.2), xytext=(1.8, 1.8),
                arrowprops=dict(arrowstyle="->", color=STYLE["cons"], lw=1.5))
    ax.text(2.3, 2.25, "(3)", fontsize=9)


def draw_branch(ax, node):
    for kind, val, label in BRANCH_LINES.get(node, []):
        if kind == "v":
            ax.plot([val, val], [-0.5, 4.6], color=STYLE["branch"], lw=2.2)
            ax.text(val + 0.05, 4.25, label + " (branch)",
                    fontsize=10, color=STYLE["branch"], fontweight="bold")
        else:
            ax.plot([-0.4, 4.2], [val, val], color=STYLE["branch"], lw=2.2)
            ax.text(3.35, val + 0.08, label + " (branch)",
                    fontsize=10, color=STYLE["branch"], fontweight="bold")


def draw(node):
    (oxoy, z, verdict) = OPT[node]
    title = f"{node} ({ADDED[node]})"
    fig, ax = base_ax(title)
    draw_constraints(ax)
    draw_branch(ax, node)
    poly = POLY[node]
    if poly is not None:
        if len(poly) > 2:
            ax.add_patch(Polygon(poly, closed=True, facecolor=STYLE["shade"],
                                 edgecolor="#0e7490", alpha=0.55, lw=1.5))
        else:  # LP5 vertical segment x1=0, x2 in [3,3.5]
            (ax0, ay0), (ax1, ay1) = poly
            ax.plot([ax0, ax1], [ay0, ay1], color="#0e7490", lw=8,
                    solid_capstyle="round", alpha=0.55)
        ox, oy = oxoy
        ax.plot(ox, oy, "o", ms=16, mfc="none", mec=STYLE["opt"], mew=3)
        ax.text(ox + 0.12, oy + 0.12, f"({ox:g}, {oy:g})\nz = {z:g}",
                fontsize=11, fontweight="bold",
                bbox=dict(facecolor="white", edgecolor=STYLE["opt"], boxstyle="round,pad=0.3"))
    else:  # LP6 infeasible annotation
        ax.text(1.9, 3.6, "x1=1 needs x2<=2.5\nbut x2>=3: contradiction",
                fontsize=11, color=STYLE["branch"], fontweight="bold",
                bbox=dict(facecolor="white", edgecolor=STYLE["branch"], boxstyle="round,pad=0.4"))
        ax.text(1.0, 0.4, "INFEASIBLE", fontsize=22, fontweight="bold",
                color=STYLE["branch"], alpha=0.85)
    ax.text(0.5, -0.32, verdict, fontsize=11, fontweight="bold",
            transform=ax.transData, ha="left", va="top",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))
    fig.tight_layout()
    fig.savefig(f"{OUT}/{node.lower()}.png", dpi=150)
    plt.close(fig)
    print("wrote", node)


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for n in ["LP0", "LP1", "LP2", "LP3", "LP4", "LP5", "LP6"]:
        draw(n)
