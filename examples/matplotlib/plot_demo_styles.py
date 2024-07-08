"""
Matplotlib Style Demo
=====================

This script demonstrates some available styles.
"""

# External imports
import matplotlib.pyplot as plt
import numpy as np

# Internal imports
import postprocessing.matplotlib as pp_mpl


def gaussian(x, mu, sig):
    return 1.0 / (np.sqrt(2.0 * np.pi) * sig) * np.exp(-np.power((x - mu) / sig, 2.0) / 2)


def main():
    # Get styles
    styles = pp_mpl.utils.get_available_styles()

    # Generate analytic gaussian distribution
    x_min = -3
    x_max = 3
    x_line = np.linspace(x_min, x_max, 1000)
    y_line = gaussian(x_line, 0, 1)

    # Generate some fake "measured" data points with some noise
    np.random.seed(0)
    x_rand = np.random.uniform(x_min, x_max, 45)
    y_rand = gaussian(x_rand, 0, 1) + np.random.normal(0, 0.02, len(x_rand))
    y_rand[y_rand < 0] += 0.05

    # Initialize figure
    fig = plt.figure(figsize=(10, 5 * len(styles) + 1))
    subfigs = fig.subfigures(ncols=1, nrows=len(styles) + 1)

    # Create a version of the plot with each niceplots style and the default matplotlib style
    for i, formatting in enumerate(["default"] + styles):
        with plt.style.context(pp_mpl.get_style(formatting)):
            # Select axis
            ax = subfigs[i].subplots(1, 1)
            font = {"fontname": plt.rcParams["font.sans-serif"][0]}

            # Get colors if using custom style
            if formatting != "default":
                colors = pp_mpl.get_colors(rcParams=True)
                ax.label_outer()
                subfigs[i].set_facecolor(colors["Background"])

            # Setup axes
            ax.set_yticks([0, 0.4])
            ax.set_ylim(bottom=0.0, top=0.4)
            ax.set_xticks([x_min, -1, 0, 1, x_max])

            # Write LaTeX in axis labels
            ax.set_xlabel("Some variable, $x$", **font)
            ax.set_ylabel("$\\mathbb{E}(x,\\mu=0, \\sigma=1)$", rotation="horizontal", ha="right", **font)

            # Plot data
            (line,) = ax.plot(x_line, y_line, clip_on=False)
            (markers,) = ax.plot(x_rand, y_rand, "o", clip_on=False)

            # Insert text
            ax.annotate("Calculated", xy=(-1.2, 0.2), ha="right", va="bottom", color=line.get_color(), **font)
            ax.annotate("Measured", xy=(0.7, 0.395), ha="left", va="top", color=markers.get_color(), **font)

            # Plot the shaded area indicating the +/- 1 std dev region.
            if formatting == "default":
                fill_color = "gray"
            else:
                fill_color = colors["Label"]

            # Add annotations
            ax.fill_between(x_line, y_line, 0, where=np.abs(x_line) <= 1, facecolor=fill_color, alpha=0.2, zorder=0)
            ax.annotate("68.27%", xy=(0, 0.075), ha="center", va="bottom", color=fill_color, font="CMU Bright", **font)
            ax.annotate(
                "", xy=(-1, 0.07), xytext=(1.0, 0.07), arrowprops=dict(arrowstyle="<|-|>", color=fill_color), **font
            )

            # Add title
            ax.set_title("{}".format(formatting), fontsize=20, pad=15, **font)

            # Adjust spines when possible
            if formatting != "default":
                pp_mpl.adjust_spines(ax)
            else:
                plt.tight_layout()
            plt.subplots_adjust(left=0.2, right=0.95, bottom=0.2, top=0.85)

    pp_mpl.save_figs(fig, "demo_styles", ["png", "svg"])


if __name__ == "__main__":
    main()
