Post-Processing
===============

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/postprocessing/badge/?version=latest)](https://postprocessing.readthedocs.io/en/latest/?badge=latest)
[![Style Checks](https://github.com/bernardopacini/PostProcessing/actions/workflows/formatting.yaml/badge.svg?branch=main)](https://github.com/bernardopacini/PostProcessing/actions/workflows/formatting.yaml)
[![Install and Test](https://github.com/bernardopacini/PostProcessing/actions/workflows/install_test.yaml/badge.svg?branch=main)](https://github.com/bernardopacini/PostProcessing/actions/workflows/install_test.yaml)

This package is a collection of utilities and techinques for post-processing aerospace related analyses and optimizations.
The tools in this package are developed to automate workflows that can be scripted to avoid repeated operations when post-processing cases.
The functionality is also meant to facilitiate post-processing when generating plots in specific formats.

Installation
------------

This repository is a pure-Python package that can be installed using PIP.
To install the package, the package and all dependencies, just the documentation dependencies, or just the style check dependencies, run one of the following commands:

```
pip3 install .        # The package, with only required dependencies
pip3 install .[all]   # The package and all dependencies
pip3 install .[doc]   # The package and the optional documentation dependencies
pip3 install .[test]  # The package and the optional testing dependencies
pip3 install .[style] # The package and the optional style check dependencies
```

The package can also be installed in development mode using the `-e` flag.

Documentation
-------------

This repository and the utilities in it are accompanied by documentation.
To build and open this documentation, install the documentation dependencies and navigate to the documentation directory, `/doc`.
To build the documentation and open the files, use the following commands:

```
make html
open _build/html/index.html
```

The documentation will open in a web browser.
If it does not, direct your web browser to the `index.html` file.


Operating System Compatibility
------------------------------

The code in this repository consists of several components that may or may not be compatible with individual systems.
Ths code is developed and tested on Linux (using Ubuntu), but is also used regularly on MacOS.
The Matplotlib components of this package should be generally compatibile with many systems, but compatibility with tools like ParaView and TecPlot can be more challenging to configure.
