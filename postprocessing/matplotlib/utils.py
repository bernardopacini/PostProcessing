# External imports
import os
import copy
from collections import OrderedDict
import matplotlib.pyplot as plt


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
        if ext == ".mplstyle":
            styles.append(name)

    # Sort styles alphabetically
    styles.sort()

    return styles


def get_style(style_name="doumont-light"):
    """
    Function to get the stylesheet that can be passed to matplotlib's style
    setting functions.

    Parameters
    ----------
    style_name : str
        Name of desired style. Default is "doumont-light".

    Returns
    -------
    str
        The style string that can be passed to the matplotlib style setting
        function.
    """
    # Check if the style exists locally and if so, return path
    if style_name in get_available_styles():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", style_name + ".mplstyle")
    # If the style does not exist, assume it is a default matplotlib style
    else:
        return style_name


def get_colors(style_name=None, rcParams=False):
    """
    Function to get colors associated with a matplotlib style, using either the
    current style or a specified style.

    This function does not work for built-in matplotlib styles.

    Parameters
    ----------
    style_name : str
        Name of the desired style. Default is None, which returns the colors
        from the current style.
    rcParams : bool
        Flag to return the colors associated with rcParams. Default is False.

    Returns
    -------
    dict
        Dictionary of colors used in the style.
    """

    def get_colors_from_current_style(rcParams=False):
        # Get color codes and names
        color_codes = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        color_names = plt.rcParams["keymap.help"]

        # Check the number of color codes match the number of color names
        if len(color_codes) != len(color_names):
            raise ValueError(
                "The colors are not properly named in the stylesheet, the number of color codes should match the number of color names."
            )

        # Write colors to dictionary
        colors = OrderedDict(zip(color_names, color_codes))
        if rcParams:
            colors["Axis"] = plt.rcParams["axes.edgecolor"]
            colors["Background"] = plt.rcParams["axes.facecolor"]
            colors["Text"] = plt.rcParams["text.color"]
            colors["Label"] = plt.rcParams["axes.labelcolor"]

        return colors

    if style_name:
        with plt.style.context(get_style(style_name)):
            return get_colors_from_current_style(rcParams)
    else:
        return get_colors_from_current_style(rcParams)


def adjust_spines(ax=None, spines=["left", "bottom"], outward=True):
    """
    Function to shift the axes/spines.

    Parameters
    ----------
    ax : Matplotlib axes
        Figure axes to adjust. Default is None, which will pickup the current
        axes.
    spines : list
        List of strings defining which spines to adjust. Default is left and
        bottom.
    outward : bool
        Flag to shift spines outward. Default is False.
    """
    if ax is None:
        ax = plt.gca()

    # Loop over spines
    for loc, spine in ax.spines.items():
        if loc in spines:
            ax.spines[loc].set_visible(True)
            if outward:
                spine.set_position(("outward", 12))
        else:
            ax.spines[loc].set_visible(False)

    # Adjust Y-axis ticks
    if "left" in spines:
        ax.yaxis.set_ticks_position("left")
    elif "right" in spines:
        ax.yaxis.set_ticks_position("right")
    else:
        ax.yaxis.set_visible(False)

    # Adjust X-axis ticks
    if "bottom" in spines:
        ax.xaxis.set_ticks_position("bottom")
    elif "top" in spines:
        ax.xaxis.set_ticks_position("top")
    else:
        # ax.xaxis.set_ticks([])
        ax.xaxis.set_visible(False)


def save_figs(fig, name, formats, format_kwargs=None, **kwargs):
    """
    Function to save figures in multiple file formats with user specied
    options.

    Parameters
    ----------
    fig : Matplotlib figure
        The figure to save.
    name : str
        Output path for the figure files, e.g "path/to/file/file_name". No file
        extension required.
    formats : str or list
        File formats to save the figure in, e.g. "png", "pdf", "svg".
    format_kwargs : dict
        A dictionary of dictionaries, where the keys are the file formats and
        the values are any keyword arguments that should only be applied to
        that format. These kwargs will be added to ones passed to all formats,
        by default None
    kwargs :
        Any keyword arguments to pass to `plt.savefig()` for all formats.
    """
    # Remove extensions from the filename
    file_name = os.path.splitext(name)[0]

    # Convert the format to list if given as a string
    if isinstance(formats, str):
        formats = [formats]

    # Save the figure
    for ext in formats:
        if ext[0] == ".":
            ext = ext[1:]
        # Add format-specific kwargs
        ext_kwargs = copy.deepcopy(kwargs)
        if format_kwargs is not None and ext in format_kwargs:
            ext_kwargs.update(format_kwargs[ext])
        fig.savefig(file_name + "." + ext, **ext_kwargs)
