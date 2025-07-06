# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from unittest.mock import MagicMock

# List the modules you want to mock
MOCK_MODULES = ["paraview.simple", "vtk.util"]
sys.modules.update((mod_name, MagicMock()) for mod_name in MOCK_MODULES)

this_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath("."))

# -- Project information -----------------------------------------------------

project = "Post-Processing"
copyright = "2024, Bernardo Pacini"
author = "Bernardo Pacini"

# The full version, including alpha/beta/rc tags
# release = "1.0.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_prompt",
    "sphinxcontrib.bibtex",
    "sphinxarg.ext",
    "autoapi.extension",
    "numpydoc",
    "sphinx_gallery.gen_gallery",
    "parse_fonts",
]
bibtex_bibfiles = ["refs.bib"]

autoapi_dirs = ["../postprocessing/"]
autoapi_root = "developer_docs/autodoc/"
autoapi_add_toctree_entry = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

sphinx_gallery_conf = {
    "examples_dirs": ["../examples/matplotlib", "../examples/plotly"],
    "gallery_dirs": ["matplotlib/auto_examples", "plotly/auto_examples"],
    "image_scrapers": ("imag_scraper.png_scraper"),
}
