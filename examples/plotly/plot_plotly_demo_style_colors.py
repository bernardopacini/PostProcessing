"""
Plotly Style Colors Demo
========================

This script demonstrates colors available in each style.
"""

# External imports
import plotly.graph_objects as go

# Internal Imports
import postprocessing.plotly as pp_plty


def main():
    # Get styles
    styles = pp_plty.utils.get_available_styles()

    # Initialize figure
    fig = go.Figure()

    # Cover the background in white
    fig.add_shape(type="rect", x0=0, y0=-len(styles), x1=1, y1=0, fillcolor="white", line=dict(width=0))

    # Iterate over each style
    for i, style in enumerate(styles):
        # Get the colors for the current style
        colors = pp_plty.get_colors(style, rcParams=True)
        background = colors["Background"]
        text = colors["Text"]
        for key in ["Axis", "Background", "Text", "Label"]:
            del colors[key]

        # Create a colored background using a rectangle shape
        fig.add_shape(type="rect", x0=0, y0=-i - 1, x1=1, y1=-i - 0.2, fillcolor=background, line=dict(width=0))

        # Swatch properties
        spacing = 0.025  # Space between swatches
        width = (1 - (len(colors) + 1) * spacing) / len(colors)

        # Create color swatches for each color
        for j, (color_name, color_value) in enumerate(colors.items()):
            x_start = j * (spacing + width) + spacing
            x_end = x_start + width

            # Add swatch rectangles
            fig.add_shape(
                type="rect", x0=x_start, y0=-i - 0.95, x1=x_end, y1=-i - 0.25, fillcolor=color_value, line=dict(width=0)
            )

            # Add text annotation for the color name
            fig.add_annotation(
                text=color_name,
                x=(x_start + x_end) / 2,
                y=-i - 0.6,
                showarrow=False,
                font=dict(size=18, color=text),
                xanchor="center",
                yanchor="middle",
                textangle=-90,
            )

        # Add title for each style
        fig.add_annotation(
            text=style,
            x=0.5,
            y=-i - 0.15,
            showarrow=False,
            xanchor="center",
            yanchor="middle",
            font=dict(size=20, color="black"),
        )

    # Adjust layout
    fig.update_layout(
        height=300 * len(styles),
        width=800,
        yaxis=dict(
            tickvals=[], showgrid=False, zeroline=False, showline=False, showticklabels=False, range=[-len(styles), 0]
        ),
        xaxis=dict(tickvals=[], showgrid=False, zeroline=False, showline=False, showticklabels=False, range=[0, 1]),
        margin=dict(t=30, b=30, l=30, r=30),
    )

    pp_plty.save_figs(fig, "plotly_demo_style_colors", ["png"])


if __name__ == "__main__":
    main()
