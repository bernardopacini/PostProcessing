# External imports
from collections import OrderedDict
import copy
import json
import os
import plotly.io as pio


def get_available_styles():
    """
    Function to get a list of the names of the available styles.

    Returns
    -------
    list
        List of names of available styles.
    """
    # Read the style filenames
    style_filenames = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles"))

    # Iteratively add styles from style files
    styles = []
    for style_filename in style_filenames:
        name, ext = os.path.splitext(style_filename)
        if ext == ".json":
            styles.append(name)

    # Sort styles alphabetically
    styles.sort()

    return styles


def get_style(style_name="doumont-light"):
    """
    Function to get the stylesheet that can be passed to plotly's style
    setting functions.

    Parameters
    ----------
    style_name : str
        Name of desired style. Default is "doumont-light".

    Returns
    -------
    tuple of string and dict
        The style string and dictionary (as a tuple) that can be passed to the
        plotly template setting function.
    """
    # Check if the style exists locally and if so, return the style
    if style_name in get_available_styles():
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", style_name + ".json")) as f:
            return json.load(f)
    # If the style does not exist, assume it is a default plotly style
    else:
        return pio.templates.default


def get_colors(style_name=None, rcParams=False):
    """
    Function to get colors associated with a Plotly template.

    Parameters
    ----------
    style_name : str
        Name of the desired Plotly template. Default is None, which returns the colors
        from the current template.
    rcParams : bool
        Flag to return additional color settings (axis, background, text). Default is False.

    Returns
    -------
    dict
        Dictionary of colors used in the template.
    """

    def get_colors_from_current_template(template, rcParams=False):
        colorway = template.layout.colorway
        color_names = template.layout.meta.get("color_names", {})

        if len(colorway) != len(color_names):
            raise ValueError(
                "The colors are not properly named in the template. The number of color codes should match the number of color names."
            )

        # Create a dictionary for the colors
        colors = OrderedDict(zip(color_names, colorway))

        if rcParams:
            # Extract other colors related to axis, background, and text
            colors["Axis"] = template.layout.xaxis.linecolor
            colors["Background"] = template.layout.plot_bgcolor
            colors["Text"] = template.layout.font.color
            colors["Label"] = template.layout.xaxis.tickcolor

        return colors

    if style_name:
        current_template = pio.templates.default
        current_layout = pio.templates[current_template]

        pio.templates[style_name] = get_style(style_name)
        pio.templates.default = style_name
        colors = get_colors_from_current_template(pio.templates[style_name], rcParams)

        pio.templates[current_template] = current_layout
        pio.templates.default = current_template
        return colors
    else:
        return get_colors_from_current_template(pio.templates[pio.templates.default], rcParams)


def save_figs(fig, name, formats, format_kwargs=None, **kwargs):
    """
    Function to save Plotly figures in multiple file formats with user-specified
    options.

    Parameters
    ----------
    fig : Plotly figure
        The figure to save.
    name : str
        Output path for the figure files, e.g "path/to/file/file_name". No file
        extension required.
    formats : str or list
        File formats to save the figure in, e.g. "png", "pdf", "svg", "html".
    format_kwargs : dict
        A dictionary of dictionaries, where the keys are the file formats and
        the values are any keyword arguments that should only be applied to
        that format. These kwargs will be added to ones passed to all formats,
        by default None.
    kwargs :
        Any keyword arguments to pass to the saving function for all formats.
    """
    # Remove extensions from the filename
    file_name = os.path.splitext(name)[0]

    # Convert the format to list if given as a string
    if isinstance(formats, str):
        formats = [formats]

    # Save the figure in each format
    for ext in formats:
        if ext[0] == ".":
            ext = ext[1:]

        # Create a copy of the common kwargs to allow per-format customization
        ext_kwargs = copy.deepcopy(kwargs)

        # Add format-specific kwargs
        if format_kwargs is not None and ext in format_kwargs:
            ext_kwargs.update(format_kwargs[ext])

        # Determine the correct Plotly saving function
        if ext in ["png", "pdf", "svg"]:
            pio.write_image(fig, file_name + "." + ext, **ext_kwargs)
        elif ext == "html":
            pio.write_html(fig, file_name + "." + ext, **ext_kwargs)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
