"""
Matplotlib Style Colors Demo
============================

This script demonstrates colors available in each style.
"""

# External imports
import matplotlib.pyplot as plt

# Internal Imports
import postprocessing.matplotlib as pp_mpl


def main():
    # Get styles
    styles = pp_mpl.utils.get_available_styles()

    # Initialize figure
    fig = plt.figure(figsize=(8, 3 * len(styles)))
    ax = plt.gca()

    # Iterate over each style
    for i, style in enumerate(styles):
        # Get the colors for the current style
        with plt.style.context(pp_mpl.get_style(style)):
            # Setup colors
            colors = pp_mpl.get_colors(rcParams=True)
            background = colors["Background"]
            for key in ["Axis", "Background", "Text", "Label"]:
                del colors[key]

            # Create a colored background using a rectangle shape
            ax.fill_between([0, 1], [-i - 1] * 2, [-i - 0.2] * 2, color=background)

            # Swatch properties
            spacing = 0.025
            width = (1 - (len(colors) + 1) * spacing) / len(colors)

            # Create color swatches for each color
            for i_color, color in enumerate(colors.keys()):
                x_start = i_color * (spacing + width) + spacing
                x_end = width + x_start

                # Add swatch rectangles
                ax.fill_between([x_start, x_end], [-i - 0.95] * 2, [-i - 0.25] * 2, color=colors[color])

                # Add text annotation for the color name
                ax.text((x_start + x_end) / 2, -i - 0.6, color, va="center", ha="center", rotation=90)

            # Add title for each style
            ax.text(0.5, -i - 0.15, style, va="center", ha="center", rotation=0, size=12, color="black")

    # Adjust layout
    ax.set_xlim([0, 1])
    ax.set_ylim([-len(styles), 0])
    ax.spines[["top", "bottom", "left", "right"]].set_visible(False)
    ax.set_xticks(())
    ax.set_yticks(())

    pp_mpl.save_figs(fig, "matplotlib_demo_style_colors", ["png"], bbox_inches="tight")


if __name__ == "__main__":
    main()
