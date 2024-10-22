Overview
========

Plotly is a versitile library for generating figures in Python.
There are many standard examples for how to use Plotly available on the internet, but it is useful to template some specific plot types and define specific styles.
The code in this repository provides a few styles, helper functions, and templated examples that can be used to quickly generate plots and using the same themes.

Installation
------------

To install Plotly, simply install it in your Python environment:

.. prompt:: bash

    pip3 install plotly

The custom styles in this package use fonts that may not be installed on your system.
These fonts are optional; if a font is not found, Plotly will default to the default font (Open Sans).
The custom fonts used in this package are:

.. generate_font_list::
    :path: /../postprocessing/plotly/styles
    :extension: .json

Utilities
---------

Plotly is a package specifically developed for data visualization.
In this package, I provide some styles, utilities, and examples that are listed below, and detailed in the following sections.

* :ref:`plotly_styles`
* :ref:`plotly_auto_examples`
