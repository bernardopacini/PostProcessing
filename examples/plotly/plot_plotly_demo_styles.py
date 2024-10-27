"""
Plotly Style Demo
=================

This script demonstrates some available styles.
"""

# External imports
import io
import numpy as np
from PIL import Image
import plotly
import plotly.graph_objects as go
import plotly.io as pio

# Internal imports
import postprocessing.plotly as pp_plty


def gaussian(x, mu, sig):
    return 1.0 / (np.sqrt(2.0 * np.pi) * sig) * np.exp(-np.power((x - mu) / sig, 2.0) / 2)


def main():
    # Get styles
    styles = pp_plty.utils.get_available_styles()

    # Generate analytic gaussian distribution
    x_min = -3
    x_max = 3
    x_line = np.linspace(x_min, x_max, 1000)
    y_line = gaussian(x_line, 0, 1)
    mask = (x_line >= -1) & (x_line <= 1)
    x_fill = np.concatenate(([x_line[mask][0]], x_line[mask], [x_line[mask][-1]]))
    y_fill = np.concatenate(([0], y_line[mask], [0]))

    # Generate some fake "measured" data points with some noise
    np.random.seed(0)
    x_rand = np.random.uniform(x_min, x_max, 45)
    y_rand = gaussian(x_rand, 0, 1) + np.random.normal(0, 0.02, len(x_rand))
    y_rand[y_rand < 0] += 0.05

    # Create a version of the plot with each niceplots style and the default plotly style
    figure_bytes = []
    for formatting in ["default"] + styles:
        # Use the style to determine plot properties
        pio.templates[formatting] = pp_plty.get_style(formatting)
        pio.templates.default = formatting
        if formatting != "default":
            colors = pp_plty.get_colors(rcParams=True)
            bg_color = colors["Background"]
            label_color = colors["Label"]
            colors = list(colors.values())
        else:
            # colors = plotly.colors.DEFAULT_PLOTLY_COLORS
            colors = plotly.colors.qualitative.Plotly
            bg_color = "white"
            label_color = "gray"

        # Initialize figure
        fig = go.Figure()

        # Create scatter traces for the line and markers
        fig.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines", name="Calculated", line=dict(color=colors[0])))
        fig.add_trace(go.Scatter(x=x_rand, y=y_rand, mode="markers", name="Measured", marker=dict(color=colors[1])))

        # Add a shaded +/- 1 std dev region
        fig.add_trace(
            go.Scatter(
                x=x_fill,
                y=y_fill,
                fill="toself",
                fillcolor=label_color,
                opacity=0.2,
                line=dict(color="rgba(0,0,0,0)"),  # Hide the line
                name="68.27%",
                showlegend=False,
            ),
        )

        # Add annotations
        fig.add_annotation(text="Calculated", x=-1.5, y=0.2, showarrow=False, font=dict(color=fig.data[0].line.color))
        fig.add_annotation(text="Measured", x=0.7, y=0.395, showarrow=False, font=dict(color=fig.data[1].marker.color))
        fig.add_annotation(text="68.27%", x=0, y=0.085, showarrow=False, font=dict(color=label_color))
        fig.add_annotation(
            x=-1,
            y=0.07,
            ax=0.0,
            ay=0.07,
            standoff=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=label_color,
            xanchor="left",
        )
        fig.add_annotation(
            x=1,
            y=0.07,
            ax=0.0,
            ay=0.07,
            standoff=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=label_color,
            xanchor="right",
        )

        # Customize each subplot's appearance
        fig.update_xaxes(
            title_text="$\\text{Some variable, }x$",
            tickvals=[x_min, -1, 0, 1, x_max],
            range=[x_min - 0.025, x_max + 0.025],
        )
        fig.update_yaxes(
            title_text="$\\mathbb{E}(x, \\mu=0, \\sigma=1)$", tickvals=[0, 0.4], range=[0 - 0.01, 0.4 + 0.01]
        )

        if formatting != "default":
            fig.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color)

        # Adjust layout settings for better spacing
        # fig.update_traces(cliponaxis=False)
        fig.update_layout(
            width=1000,
            height=400,
            title=formatting,
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=75),
        )

        # Store figure
        img_bytes = io.BytesIO()
        pio.write_image(fig, img_bytes, format="png")
        img_bytes.seek(0)
        figure_bytes.append(img_bytes.getvalue())

    # Convert byte data to PIL images
    images = [Image.open(io.BytesIO(b)) for b in figure_bytes]

    # Combine images vertically
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    combined_image = Image.new("RGBA", (max_width, total_height))

    # Paste each image into the combined image
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    # Save the combined image
    combined_image.save("plotly_demo_styles.png")


if __name__ == "__main__":
    main()
