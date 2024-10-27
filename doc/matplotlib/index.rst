Overview
========

Matplotlib is a versitile library for generating figures in Python.
There are many standard examples for how to use Matplotlib available on the internet, but it is useful to template some specific plot types and define specific styles.
The code in this repository provides a few styles, helper functions, and templated examples that can be used to quickly generate plots and using the same themes.

Installation
------------

To install Matplotlib, simply install it in your Python environment:

.. prompt:: bash

    pip3 install matplotlib

The custom styles in this package use fonts that may not be installed on your system.
These fonts are optional; if a font is not found, Matplotlib will default to the default font (DejaVu Sans).
To install fonts, install the desired font on your system and delete Matplotlib's font cache(s) located in ``~/.cache/matplotlib``.
The custom fonts used in this package are:

.. generate_font_list::
    :path: /../postprocessing/matplotlib/styles
    :extension: .mplstyle

Utilities
---------

Matplotlib is a package specifically developed for data visualization.
In this package, I provide some styles, utilities, and examples that are listed below, and detailed in the following sections.

* :ref:`matplotlib_styles`
* :ref:`matplotlib_auto_examples`
