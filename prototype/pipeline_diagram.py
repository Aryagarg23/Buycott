"""
Explanatory diagram only: what Buycott's pipeline looked like as built, not a
result. No accuracies, no counts, no distributions — the real RoBERTa model
and tagged corpus aren't in this repo and no evaluation data survived the
hackathon weekend, so there is nothing measured left to plot.
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK = "#282215"
HAIRLINE = "#c6b99f"
TECHNICAL = "#3b42db"
PERSONAL = "#e85b30"

# (label, x, y, width, height, edge color, edge width)
BOXES = [
    ("barcode\nscan", 1.0, 4.6, 1.8, 1.3, INK, 1.0),
    ("Google Vision API\n(image → text)", 3.6, 4.6, 2.2, 1.3, INK, 1.0),
    ("product → parent\ncompany resolution", 6.4, 4.6, 2.2, 1.3, INK, 1.0),
    ("GDELT news pull\n(per company)", 9.2, 4.6, 2.2, 1.3, INK, 1.0),
    ("fine-tuned RoBERTa\nstance classifier\n(pro-A / neutral / pro-B)", 9.2, 1.6, 2.4, 1.5, TECHNICAL, 1.8),
    ("card: stance +\nsource articles", 6.4, 1.6, 2.2, 1.3, INK, 1.0),
    ("human\ndecides", 3.6, 1.6, 1.8, 1.3, PERSONAL, 1.8),
]

ARROWS = [
    (1.9, 4.6, 2.5, 4.6),   # barcode -> vision
    (4.7, 4.6, 5.3, 4.6),   # vision -> resolution
    (7.5, 4.6, 8.1, 4.6),   # resolution -> gdelt
    (10.3, 3.95, 10.3, 2.35),  # gdelt -> classifier (down)
    (8.0, 1.6, 7.5, 1.6),   # classifier -> card
    (5.3, 1.6, 4.5, 1.6),   # card -> human decides
]


def box(ax, label, x, y, w, h, edge, lw):
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="square,pad=0.12",
        linewidth=lw,
        edgecolor=edge,
        facecolor="#f2ece0",
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(x, y, label, ha="center", va="center", fontsize=9.5, color=INK, zorder=3)


def arrow(ax, x0, y0, x1, y1):
    a = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.2,
        color=INK,
        zorder=1,
    )
    ax.add_patch(a)


def plot_pipeline(out_path):
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title(
        "How Buycott turns a scanned barcode into a sourced stance — architecture as built",
        fontsize=12,
    )

    for label, x, y, w, h, edge, lw in BOXES:
        box(ax, label, x, y, w, h, edge, lw)
    for x0, y0, x1, y1 in ARROWS:
        arrow(ax, x0, y0, x1, y1)

    ax.text(
        0.0, 0.15,
        "architecture as built — no scores shown, no evaluation data survived the weekend",
        transform=ax.transData, ha="left", va="bottom",
        fontsize=9, style="italic", color="#c2491d",
    )

    fig.savefig(out_path, dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    figures_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(figures_dir, exist_ok=True)

    out_path = os.path.join(figures_dir, "pipeline.png")
    plot_pipeline(out_path)
    print(f"saved {out_path}")
