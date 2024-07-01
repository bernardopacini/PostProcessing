ParaView
========

`ParaView <https://www.paraview.org>`_ is an opensource visualization tool that is useful for post-processing data.
The tool can be used as a GUI, to visualize 2D and 3D results, or it can be used as a scripting package through Python.
In this package, ParaView is used through its Python API to generate data that is useful for post-processing cases.
The first step for using ParaView is to install it.

Installation
------------

To install ParaView, navigate to the `download section <https://www.paraview.org/download/>`_ of the ParaView website and download the version that is compatible with your system.

.. warning::

   For ParaView Python to work directly with your local Python version, be sure to select the ParaView download with the correct Python version.

Once you have ParaView downloaded, place the files somewhere accessible.
On Mac, ParaView will install and provide an application icon that you can launch and use as a regular tool.
On Linux, it is easiest to launch ParaView from the terminal.
To do this, add the following command to your ``~/.bashrc`` (or equivalent environment configuration script).

.. code-block:: bash

   export PATH=$PATH:/<path>/<to>/ParaView/bin

You can then load ParaView using:

.. prompt:: bash

   paraview

The GUI has its own Python version that you can copy-paste scripts into.
However, this post-processing repository is designed to call ParaView's Python core directly, not through the GUI.
Connecting to ParaView Python is more challenging.
It can be done by simply using the provided version of Python from ParaView.
This is done by calling the ``pvpython`` object provided in the ParaView bin directory.
This has the unfortunate drawback of restricting you to specific Python packages, making it impractical.
Instead, you can add ParaView Python to your existing Python environment.
To do this, add the following commands to your ``~/.bashrc`` (or equivalent configuration script).

.. code-block:: bash

   export PYTHONPATH=$PYTHONPATH:/<path>/<to>/ParaView/lib/python<paraview version>/site-packages
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/<path>/<to>/ParaView/lib

This connection means ParaView can be directly loaded into Python scripts.

.. warning::

   Adding ParaView to your existing Python will overwrite any existing packages that conflict with the ones provided with ParaView Python.
   To avoid this, I recommend adding a flag to your configuration script to selectively enable / disable the link to ParaView Python.

The ParaView utilities included in this package are available as command line executables.
The naming convention for these utilities is ``pv_<function name>``.

Utilities
---------

ParaView is particularly useful for manipulating data that must be post-processed.
In this package, I provide a few routines that automate specific workflows into command line calls or function calls through Python.
They are listed below and detailed in the following sections.

.. toctree::
   :maxdepth: 1

   distributionGeometry
   distributionForce
   slicesCP
