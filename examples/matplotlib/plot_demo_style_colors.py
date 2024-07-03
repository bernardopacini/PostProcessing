"""
==============================================================================
Matplotlib Style Colors Demo
==============================================================================
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
    fig, axs = plt.subplots(len(styles), 1, figsize=(8, 3 * len(styles)))
    axs = axs.flatten()

    # Iterate over styles
    for i, style in enumerate(styles):
        # Set current style
        with plt.style.context(pp_mpl.get_style(style)):
            # Select axis
            ax = axs[i]

            # Setup colors
            colors = pp_mpl.get_colors(rcParams=True)
            background = colors["Background"]
            for key in ["Axis", "Background", "Text", "Label"]:
                del colors[key]

            # Setup plot
            ax.set_title(style, pad=5.0)

            # Fill the background with the style's background color
            ax.fill_between([0, 1], [0, 0], [1, 1], color=background)

            # Swatch properties
            spacing = 0.025
            width = (1 - (len(colors) + 1) * spacing) / len(colors)

            # Plot the swatches
            for i_color, color in enumerate(colors.keys()):
                x_start = i_color * (spacing + width) + spacing
                x_end = width + x_start
                ax.fill_between([x_start, x_end], [0.05] * 2, [0.95] * 2, color=colors[color])
                ax.text((x_start + x_end) / 2, 0.5, color, va="center", ha="center", rotation=90)

            # Adjust axes
            ax.set_xlim([0, 1])
            ax.set_ylim([0, 1])
            ax.invert_yaxis()

            # Remote splines and ticks
            ax.spines[["top", "bottom", "left", "right"]].set_visible(False)
            ax.set_xticks(())
            ax.set_yticks(())

    pp_mpl.save_figs(fig, "demo_style_colors", ["png", "svg"], bbox_inches="tight")


if __name__ == "__main__":
    main()
