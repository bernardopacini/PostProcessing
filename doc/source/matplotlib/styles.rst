.. _matplotlib_styles:

Styles
======

Defining specific styles in Matplotlib is useful for standardizing plots throughout reports or projects.
These styles are defined as ``.mplstyle`` files in the ``/postprocessing/matplotlib/styles/`` directory.
In addition to all of the existing Matplotlib styles, the defined style files can be set as the styles used when generating plots with this repository.

Custom Styles
-------------

The existing styles define colors, fonts, and other parameters that are necessary to customize figure styles.
The colors in the custom styles are show below and are accessible when using the style:

.. image:: auto_examples/images/sphx_glr_plot_demo_style_colors_001.png
  :alt: Custom matplotlib color styles.

In addition to defining specific colormaps, the styles adjust aspects of the plots.
The default Matplotlib and custom styles defined in this package are shown below, for an example line and scatter plot.

.. image:: auto_examples/images/sphx_glr_plot_demo_styles_001.png
  :alt: Some of the available matplotlib styles, including the custom styles.

Adding Styles
-------------

To add a custom style, add a ``.mplstyle`` in ``/postprocessing/matplotlib/styles/`` directory.
Modify the Matplotlib parameters as desired and add a descriptive name.
If possible, add both a light and dark mode version of the style, named with the following convention: ``<style_name>-light.mplstyle`` and ``<style_name>-dark.mplstyle``.

.. note::

    To visualize the new style and compare it to existing styles, run the ``/examples/matplotlib/plot_demo_style_colors.py`` and ``/examples/matplotlib/plot_demo_styles.py`` scripts.
    These scripts will automatically generate plots comparing all of the custom colormaps and styles.
