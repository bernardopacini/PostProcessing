.. _paraview_extract_geometry:

Extract Geometry
================

Having a geometry file of an object is useful for testing geometry parameterizations or visualizing specific aspects of the geometry.
For example, it can be helpful to prototype design variables on a simplified geometry before applying it to a complete mesh and case.
Extracting a geometry is done through ParaView by importing the mesh, isolating the desired patches, and exporting the surfaces.

The extract geometry post-processing routine is available through both a command line executable and through the Python API.
Using either method, the utility will read the mesh and write out the wall surfaces into a STL file.

Command Line
------------

To call the utility from the command line, simply call the utility using the following command with the desired options:

.. argparse::
   :filename: postprocessing/paraview/geometry.py
   :func: extract_geometry_parser
   :prog: extract_geometry

Python API
----------

To call the utility from Python, import the necessary modules and call the function with the necessary inputs:

.. autoapifunction:: postprocessing.paraview.geometry.extract_geometry
   :noindex:
