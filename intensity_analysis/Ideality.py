# -*- coding: utf-8 -*-
"""
Ideality Factor Plot
Compares pre- and post-irradiation ideality factors for five perovskite device configurations.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# INPUT YOUR IDEALITY FACTORS HERE
# ============================================================

configs = [
    "PFN-Br",
    r"Al$_2$O$_3$",
    r"Al$_2$O$_3$ + EDAI",
    r"Al$_2$O$_3$ + LiF",
    r"Al$_2$O$_3$ + LiF + EDAI"
]

pre_irradiation = [
    1.132,   # PFN-Br before irradiation
    1.321,   # Al2O3 before irradiation
    1.479,   # Al2O3 + EDAI before irradiation
    1.255,   # Al2O3 + LiF before irradiation
    1.224    # Al2O3 + LiF + EDAI before irradiation  <-- CHANGE THIS
]

post_irradiation = [
    2.561,   # PFN-Br after irradiation
    1.522,   # Al2O3 after irradiation
    1.491,   # Al2O3 + EDAI after irradiation
    1.498,   # Al2O3 + LiF after irradiation
    1.576    # Al2O3 + LiF + EDAI after irradiation   <-- CHANGE THIS
]

# ============================================================
# PLOT SETTINGS
# ============================================================

title = "Ideality Factor Before and After Irradiation"
y_label = "Ideality Factor"
output_filename = "ideality_factor_comparison.png"

# One colour per configuration
config_colours = [
    "tab:blue",    # PFN-Br
    "tab:orange",  # Al2O3
    "tab:green",   # Al2O3 + EDAI
    "tab:red",     # Al2O3 + LiF
    "tab:purple"   # Al2O3 + LiF + EDAI
]

# Faded transparency for post-irradiation
pre_alpha = 1.0
post_alpha = 0.45

# Marker styles
pre_marker = "D"   # diamond
post_marker = "^"  # triangle

# ============================================================
# CREATE PLOT
# ============================================================

x = np.arange(len(configs))
offset = 0.18

fig, ax = plt.subplots(figsize=(14, 6))

for i, config in enumerate(configs):
    colour = config_colours[i]

    # Before irradiation
    ax.scatter(
        x[i] - offset,
        pre_irradiation[i],
        marker=pre_marker,
        s=110,
        color=colour,
        alpha=pre_alpha,
        edgecolor="black",
        linewidth=0.5,
        zorder=3
    )

    # After irradiation
    ax.scatter(
        x[i] + offset,
        post_irradiation[i],
        marker=post_marker,
        s=130,
        color=colour,
        alpha=post_alpha,
        edgecolor="black",
        linewidth=0.5,
        zorder=3
    )

    # Line connecting before and after for each config
    ax.plot(
        [x[i] - offset, x[i] + offset],
        [pre_irradiation[i], post_irradiation[i]],
        linestyle="--",
        linewidth=1.5,
        alpha=0.45,
        color=colour,
        zorder=2
    )

    # Value labels
    ax.text(
        x[i] - offset,
        pre_irradiation[i] + 0.06,
        f"{pre_irradiation[i]:.2f}",
        ha="center",
        fontsize=10
    )

    ax.text(
        x[i] + offset,
        post_irradiation[i] + 0.06,
        f"{post_irradiation[i]:.2f}",
        ha="center",
        fontsize=10
    )

# X-axis labels
x_labels = []
x_positions = []

for i, config in enumerate(configs):
    x_positions.append(x[i] - offset)
    x_labels.append(f"{config}\nBefore\nIrradiation")

    x_positions.append(x[i] + offset)
    x_labels.append(f"{config}\nAfter\nIrradiation")

ax.set_xticks(x_positions)
ax.set_xticklabels(x_labels, fontsize=9)

# Axis labels and title
ax.set_ylabel(y_label, fontsize=13)
ax.set_title(title, fontsize=16)

# Y-axis range
max_value = max(max(pre_irradiation), max(post_irradiation))
ax.set_ylim(0, max_value + 0.6)

# Grid
ax.grid(axis="y", linestyle="--", alpha=0.35)

# ============================================================
# CUSTOM LEGEND / KEY
# ============================================================

legend_elements = [
    Line2D(
        [0], [0],
        marker=pre_marker,
        color="black",
        linestyle="None",
        markersize=9,
        label="Before Irradiation"
    ),
    Line2D(
        [0], [0],
        marker=post_marker,
        color="black",
        linestyle="None",
        markersize=10,
        label="After Irradiation"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="tab:blue",
        linestyle="None",
        markersize=9,
        label="PFN-Br"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="tab:orange",
        linestyle="None",
        markersize=9,
        label=r"Al$_2$O$_3$"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="tab:green",
        linestyle="None",
        markersize=9,
        label=r"Al$_2$O$_3$ + EDAI"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="tab:red",
        linestyle="None",
        markersize=9,
        label=r"Al$_2$O$_3$ + LiF"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="tab:purple",
        linestyle="None",
        markersize=9,
        label=r"Al$_2$O$_3$ + LiF + EDAI"
    )
]

ax.legend(
    handles=legend_elements,
    loc="upper right",
    fontsize=10,
    frameon=True
)

plt.tight_layout()
plt.savefig(output_filename, dpi=300)
plt.show()

print(f"Graph saved as: {output_filename}")
