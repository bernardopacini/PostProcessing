# External imports
import os
import csv
import argparse
import numpy as np

# Paraview imports
import paraview.simple as paraview
from vtk.util import numpy_support as vtk_np

# Internal Imports
import postprocessing.utils as utils
import postprocessing.paraview.utils as pv_utils


def slices_cp_cmd():
    """
    Wrapper around the slices_cp() function to call it from the
    command line with arguments.
    """
    # Parse arguments
    parser = slices_cp_parser()

    # Call function
    slices_cp(**vars(parser.parse_args()))


def slices_cp_parser():
    """
    Parser for options for the slices_cp() function to call it from
    the command line with arguments.

    Returns
    -------
    parser
        Parser with specified arguments.
    """
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "-i",
        "--input_file",
        help="Relative path to input file.",
        type=str,
        default="",
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        help="Relative path to output directory. Default is ./",
        type=str,
        default="./",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name pattern to write out files in the output directory. Default is slice.",
        type=str,
        default="slice",
    )
    parser.add_argument(
        "-p",
        "--patches",
        help="Patches to include in the calculation. Default is group/wall.",
        type=str,
        nargs="+",
        default="group/wall",
    )
    parser.add_argument(
        "-s",
        "--span_direction",
        help="Span direction. String in (X+, X-, Y+, Y-, Z+, Z-) or list of floats specifying vector. Default is Z+.",
        type=str,
        nargs="+",
        default=["Z+"],
    )
    parser.add_argument(
        "-l",
        "--lift_direction",
        help="Lift direction. String in (X+, X-, Y+, Y-, Z+, Z-) or list of floats specifying vector. Default is Y+.",
        type=str,
        nargs="+",
        default=["Y+"],
    )
    parser.add_argument(
        "-d",
        "--drag_direction",
        help="Drag direction. String in (X+, X-, Y+, Y-, Z+, Z-) or list of floats specifying vector. Default is X+.",
        type=str,
        nargs="+",
        default=["X+"],
    )
    parser.add_argument(
        "-x",
        "--x",
        help="Coordinates to sample. Default is [[0, 0, 0]].",
        type=str,
        nargs="+",
        action="append",
    )
    parser.add_argument(
        "-r0",
        "--rho0",
        help="Freestream density.",
        type=float,
    )
    parser.add_argument(
        "-u0",
        "--u0",
        help="Freestream velocity magnitude.",
        type=float,
    )
    parser.add_argument(
        "-p0",
        "--p0",
        help="Freestream pressure.",
        type=float,
    )
    return parser


def slices_cp(
    input_file=None,
    output_directory="./",
    name="slice",
    patches="group/wall",
    span_direction="Z+",
    lift_direction="Y+",
    drag_direction="X+",
    x=None,
    rho0=None,
    u0=None,
    p0=None,
):
    """
    Function to compute slices using Paraview.


    Parameters
    ----------
    input_file : str
        Path to file to load with Paraview.
    output_directory : str
        Path to directory where the slice files will be written. Default is
        "./".
    name : str
        Name pattern to write out files in the output directory. Default is
        "slice".
    patches : str or list
        Patch name(s) over which to compute the force distribution. Default
        is "group/wall".
    span_direction : str or list
        Vector direction for span direction either as a string (eg. X) or list
        (eg. [0 0 1]). Should be of magnitude 1. Default is "Z+".
    lift_direction : str or list
        Vector direction for lift direction either as a string (eg. X+) or list
        (eg. [0 1 0]). Should be of magnitude 1. Default is "Y+".
    drag_direction : str or list
        Vector direction for drag direction either as a string (eg. X+) or list
        (eg. [1 0 0]). Should be of magnitude 1. Default is "X+".
    x : list
        Coordinates to sample.
    rho0 : float
        Freestream density.
    u0 : float
        Freestream velocity magnitude.
    p0 : float
        Freestream pressure.
    """
    # Check if output directory exists
    if not os.path.isdir(output_directory):
        raise RuntimeError("Output directory {} does not exist.".format(output_directory))

    # Check that slice locations were provided
    if x is None:
        raise ValueError("No slice locations (x) provided.")

    # Check that freestream values were provided
    if rho0 is None:
        raise ValueError("No freestream density (rho0) provided.")
    if u0 is None:
        raise ValueError("No freestream velocity (u0) provided.")
    if p0 is None:
        raise ValueError("No freestream pressure (p0) provided.")

    # Generate direction vectors
    span_direction = utils.check_input_vector(span_direction, "span direction", check_norm=True)
    lift_direction = utils.check_input_vector(lift_direction, "lift direction", check_norm=True)
    drag_direction = utils.check_input_vector(drag_direction, "drag direction", check_norm=True)

    # Generate sample points
    x_slice = np.zeros((len(x), 3))
    for i in range(len(x)):
        if len(x[i]) != 3:
            raise ValueError(
                "All entries in x should be list of length 3, not {} with length {}.".format(x[i, :], len(x[i, :]))
            )

        x_slice[i, :] = [x[i][0], x[i][1], x[i][2]]
    x = x_slice

    # Import case
    if input_file is None:
        raise ValueError("Input file not set.")
    paraviewfoam = paraview.OpenFOAMReader(
        registrationName="paraview.foam", FileName=str(os.getcwd()) + "/{}".format(input_file)
    )
    paraviewfoam.MeshRegions = patches
    paraviewfoam.CellArrays = ["p"]

    # Read time data
    animationScene1 = paraview.GetAnimationScene()
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    reader = paraview.GetActiveSource()
    times = reader.TimestepValues

    for i in range(len(times)):
        paraview.UpdatePipeline(time=times[i], proxy=paraviewfoam)

        # Iterate over span
        for j in range(np.size(x_slice, 0)):
            # Create a slice
            slice1 = paraview.Slice(registrationName="Slice1", Input=paraviewfoam)

            # Set slice location and normal
            slice1.SliceType.Origin = [x[j, 0], x[j, 1], x[j, 2]]
            slice1.SliceType.Normal = [span_direction[0], span_direction[1], span_direction[2]]

            # Plot on Sorted Line
            plotOnSortedLines1 = paraview.PlotOnSortedLines(registrationName="PlotOnSortedLines1", Input=slice1)

            # Extract Data
            data = paraview.servermanager.Fetch(plotOnSortedLines1).GetBlock(0)
            coords = np.zeros((0, 3))
            arclen = np.zeros(0)
            pressure = np.zeros(0)
            for k in range(data.GetNumberOfBlocks()):
                if data.GetBlock(k).GetNumberOfBlocks() > 0:
                    seg_coords = vtk_np.vtk_to_numpy(data.GetBlock(k).GetBlock(0).GetPoints().GetData())
                    seg_arclen = vtk_np.vtk_to_numpy(data.GetBlock(k).GetBlock(0).GetPointData().GetArray("arc_length"))
                    seg_pressure = vtk_np.vtk_to_numpy(data.GetBlock(k).GetBlock(0).GetPointData().GetArray("p"))
                    coords = np.concatenate((coords, seg_coords), axis=0)
                    arclen = np.concatenate((arclen, seg_arclen), axis=0)
                    pressure = np.concatenate((pressure, seg_pressure), axis=0)

            # Cleanup Paraview Objects
            paraview.Delete(plotOnSortedLines1)
            paraview.Delete(slice1)

            # Rotate points to X-Y plane
            R = np.array([drag_direction, lift_direction, np.cross(drag_direction, lift_direction)])
            coords2D = (R @ coords.T).T[:, :2]

            # Sort
            coords2D, arclen, indices = pv_utils.sort_airfoil(coords2D, arclen)
            pressure = pressure[indices]

            # Compute pressure coefficient
            cp = (pressure - p0) / (0.5 * rho0 * u0 * u0)

            # Write CSV file
            fields = ["X", "Y", "CP"]
            results = np.stack((coords2D[:, 0], coords2D[:, 1], cp), axis=1)
            with open(output_directory + name + "_" + str(i) + "_" + str(j) + ".csv", "w") as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the fields
                csvwriter.writerow(fields)
                # writing the data rows
                csvwriter.writerows(results)
