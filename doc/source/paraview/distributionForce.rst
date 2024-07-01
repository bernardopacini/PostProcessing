Force Distribution
==================

Force distributions are useful for understanding loads on an aerodynamic body.
For example, understanding how distributions of lift and drag on a wing change throughout an optimization.
Computing these distributions is done through ParaView by importing the case, slicing it along a specific axis and plane, and computing sectional properties.

.. note::

   This utility expects a variable called ``force`` that is the force divided by area on each surface cell face.
   For the utility to work, this ``force`` variable must exist for the surfaces included in the force computation.

The force of a particular slice is computed by projecting the force on each cell face in the direction specified by the user.
The forces are then integrated over the slice to compute the total force.
This calculated force is a force per unit length, useful for understanding distributions.

The force distribution post-processing routine is available through both a command line executable and through the Python API.
Using either method, the utility will write one file per timestep including the geometric coordinate and force of each slice along the geometry.

Command Line
------------

To call the utility from the command line, simply call the utility using the following command with the desired options:

.. argparse::
   :filename: ../postprocessing/paraview/distributions.py
   :func: generate_force_distribution_parser
   :prog: generate_force_distribution

Python API
----------

To call the utility from Python, import the necessary modules and call the function with the necessary inputs:

.. autoapifunction:: postprocessing.paraview.distributions.generate_force_distribution
   :noindex:
