Geometry Distribution
=====================

Geometric distributions are useful for understanding a geometry when it has been updated through any analysis or optimization.
For example, extracting the twist, chord, and thickness distributions along a wing can show how an optimization updated a geometry.
Computing these distributions is done through ParaView by importing the geometry, slicing it along a specific axis and plane, and computing sectional properties.

This utility is geared specifically towards wing geometries.
The twist is computed by identifying the trailing edge of an airfoil section and computing the point on the leading edge furthest from the trailing edge point.
Because the computational grid is discrete, this point does not necessarily represent the exact leading edge.
Instead, a circle is inscribed through the identified leading edge point as well as its two neighbors.
The point on this circle furthest from the trailing edge is then used as the true leading edge coordinate, as suggested by :cite:t:`Vassberg2016`.
In addition to using the leading edge point for the twist distribution, it is then to compute the chord and thickness distributions, too.
The chord distribution is computed by simply taking the distance between the leading edge point and trailing edge point, for each section along the span.
The thickness is instead computed as the distance between the upper and lower surface, perpendicular to the chord line (this approach sometimes refered to as the "British convention").

The geometry distribution post-processing routine is available through both a command line executable and through the Python API.
Using either method, the utility will write one file per timestep including the geometric coordinate, twist, chord, and thickness of each slice along the geometry.

Command Line
------------

To call the utility from the command line, simply call the utility using the following command with the desired options:

.. argparse::
   :filename: ../postprocessing/paraview/distributions.py
   :func: generate_geometry_distribution_parser
   :prog: generate_geometry_distribution

Python API
----------

To call the utility from Python, import the necessary modules and call the function with necessary imputs:

.. autoapifunction:: postprocessing.paraview.distributions.generate_geometry_distribution
   :noindex:

.. bibliography::
