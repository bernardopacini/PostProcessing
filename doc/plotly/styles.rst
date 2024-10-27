.. _plotly_styles:

Styles
======

Defining specific styles in Plotly is useful for standardizing plots throughout reports or projects.
These styles are defined as ``.json`` files in the ``/postprocessing/plotly/styles/`` directory.
In addition to all of the existing Plotly styles, the defined style files can be set as the styles used when generating plots with this repository.

Custom Styles
-------------

The existing styles define colors, fonts, and other parameters that are necessary to customize figure styles.
The colors in the custom styles are show below and are accessible when using the style:

.. image:: auto_examples/images/sphx_glr_plot_plotly_demo_style_colors_001.png
  :alt: Custom Plotly color styles.

In addition to defining specific colormaps, the styles adjust aspects of the plots.
The default Plotly and custom styles defined in this package are shown below, for an example line and scatter plot.

.. image:: auto_examples/images/sphx_glr_plot_plotly_demo_styles_001.png
  :alt: Some of the available Plotly styles, including the custom styles.

Adding Styles
-------------

To add a custom style, add a ``.json`` in ``/postprocessing/plotly/styles/`` directory.
Modify the Plotly parameters as desired and add a descriptive name.
If possible, add both a light and dark mode version of the style, named with the following convention: ``<style_name>-light.json`` and ``<style_name>-dark.json``.

.. note::

    To visualize the new style and compare it to existing styles, run the ``/examples/plotly/plot_demo_style_colors.py`` and ``/examples/plotly/plot_demo_styles.py`` scripts.
    These scripts will automatically generate plots comparing all of the custom colormaps and styles.
