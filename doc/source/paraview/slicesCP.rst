.. _paraview_slicesCP:

Slices CP
=========

Coefficient of pressure slices along an aerodynamic body are useful for understanding how pressure changes over a surface.
For example, seeing how the coefficient of pressure on a wing section behaves is useful for understanding wing efficiency.
Computing these slices is done through ParaView by importing the case, slicing at user-defined points, and computing sectional properties.

.. note::

   This utility expects a variable called ``p`` that is the pressure on each surface cell face.
   For the utility to work, this ``p`` variable must exist for the surfaces included in the coefficient of pressure computation.

The pressure on a particular slice is computed and converted to a distribution on a section.

The coefficient of pressure post-processing routine is available through both a command line executable and through the Python API.
Using either method, the utility will write one file per timestep per slice, including the airfoil coordinates and pressure at each point.

Command Line
------------

To call the utility from the command line, simply call the utility using the following command with the desired options:

.. argparse::
   :filename: postprocessing/paraview/slices.py
   :func: slices_cp_parser
   :prog: slices_cp

Python API
----------

To call the utility from Python, import the necessary modules and call the function with the necessary inputs:

.. autoapifunction:: postprocessing.paraview.slices.slices_cp
   :noindex:
