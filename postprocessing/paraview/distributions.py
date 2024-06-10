# External imports
import os
import csv
import argparse
import numpy as np
import scipy
from scipy.interpolate import Akima1DInterpolator

# Paraview imports
import paraview.simple as paraview
from vtk.util import numpy_support as vtk_np

# Internal Imports
import postprocessing.utils as utils
import postprocessing.paraview.utils as pv_utils


def generate_force_distribution_cmd():
    """
    Wrapper around the generate_force_distribution() function to call it from the
    command line with arguments.
    """
    # Parse arguments
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
        help="Relative path to output directory.",
        type=str,
        default="",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name pattern to write out files in the output directory. Default is force_distribution.",
        type=str,
        default="force_distribution",
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
        default="Z+",
    )
    parser.add_argument(
        "-f",
        "--force_direction",
        help="Force direction. String in (X+, X-, Y+, Y-, Z+, Z-) or list of floats specifying vector. Default is Y+.",
        type=str,
        nargs="+",
        default="Y+",
    )
    parser.add_argument(
        "-xs",
        "--x_start",
        help="Coordinate to start slices from. Default is [0, 0, 0].",
        type=str,
        nargs="+",
        default=[0, 0, 0],
    )
    parser.add_argument(
        "-xe",
        "--x_end",
        help="Coordinate to end slices a. Default is [0, 0, 1].",
        type=str,
        nargs="+",
        default=[0, 0, 1],
    )
    parser.add_argument(
        "-ns",
        "--n_span",
        help="Number of spanwise samples. Default is 100.",
        type=int,
        default=100,
    )

    # Call function
    generate_force_distribution(**vars(parser.parse_args()))


def generate_force_distribution(
    input_file=None,
    output_directory="./",
    name="force_distribution",
    patches="group/wall",
    span_direction="Z+",
    force_direction="Y+",
    x_start=[0, 0, 0],
    x_end=[0, 0, 1],
    n_span=100,
):
    """
    Function to compute a force distribution using Paraview.


    Parameters
    ----------
    input_file : str
        Path to file to load with Paraview.
    output_directory : str
        Path to directory where the distribution files will be written. Default
        is "./".
    name : str
        Name pattern to write out files in the output directory. Default is
        "force_distribution".
    patches : str or list
        Patch name(s) over which to compute the force distribution. Default
        is "group/wall".
    span_direction : str or list
        Vector direction for span direction either as a string (eg. X) or list
        (eg. [0 0 1]). Should be of magnitude 1. Default is "Z+".
    force_direction : str or list
        Vector direction for force direction either as a string (eg. X) or list
        (eg. [0 1 0]). Should be of magnitude 1. Default is "Y+".
    x_start : list
        Coordinates to start slices from. Default is [0, 0, 0].
    x_end : list
        Coordinates to end slices at. Default is [0, 0, 1].
    n_span : int
        Number of spanwise samples. Default is 100.
    """
    # Check if output directory exists
    if not os.path.isdir(output_directory):
        raise RuntimeError("Output directory {} does not exist.".format(output_directory))

    # Generate direction vectors
    span_direction = utils.check_input_vector(span_direction, "span direction", check_norm=True)
    force_direction = utils.check_input_vector(force_direction, "force direction", check_norm=True)

    # Generate sample points
    if len(x_start) != 3:
        raise ValueError("x_start should be list of length 3, not {} with length {}.".format(x_start, len(x_start)))
    if len(x_end) != 3:
        raise ValueError("x_end should be list of length 3, not {} with length {}.".format(x_end, len(x_end)))
    x = np.array(
        [
            np.linspace(float(x_start[0]), float(x_end[0]), n_span),
            np.linspace(float(x_start[1]), float(x_end[1]), n_span),
            np.linspace(float(x_start[2]), float(x_end[2]), n_span),
        ]
    )

    # Import case
    if input_file == None:
        raise ValueError("Input file not set.")
    paraviewfoam = paraview.OpenFOAMReader(
        registrationName="paraview.foam", FileName=str(os.getcwd()) + "/{}".format(input_file)
    )
    paraviewfoam.MeshRegions = patches
    paraviewfoam.CellArrays = ["force"]

    # Read time data
    animationScene1 = paraview.GetAnimationScene()
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    reader = paraview.GetActiveSource()
    times = reader.TimestepValues

    force = np.zeros(n_span)
    for i in range(len(times)):
        paraview.UpdatePipeline(time=times[i], proxy=paraviewfoam)

        # Zero Force Array
        force[:] = 0.0

        # Iterate over span
        for j in range(n_span):
            # Create a slice
            slice1 = paraview.Slice(registrationName="Slice1", Input=paraviewfoam)

            # Set slice location and normal
            slice1.SliceType.Origin = [x[0, j], x[1, j], x[2, j]]
            slice1.SliceType.Normal = [span_direction[0], span_direction[1], span_direction[2]]

            # Set calculator
            calculator1 = paraview.Calculator(registrationName="Calculator", Input=slice1)
            calculator1.ResultArrayName = "force_dot_dir"
            calculator1.Function = "dot(force,{}*iHat + {}*jHat + {}*kHat)".format(
                force_direction[0], force_direction[1], force_direction[2]
            )

            # Integrate variables
            integrateVariables1 = paraview.IntegrateVariables(registrationName="IntegrateVariables", Input=calculator1)

            # Get arrays
            passArrays1 = paraview.PassArrays(Input=integrateVariables1)
            passArrays1.CellDataArrays = ["force_dot_dir"]
            passArrays1.PointDataArrays = ["force_dot_dir"]

            # Store data
            data = paraview.servermanager.Fetch(passArrays1)
            force[j] = data.GetPointData().GetArray("force_dot_dir").GetValue(0)

            # Cleanup
            paraview.Delete(passArrays1)
            paraview.Delete(integrateVariables1)
            paraview.Delete(calculator1)
            paraview.Delete(slice1)

        # Write CSV file
        fields = ["X", "Y", "Z", "Force"]
        results = np.stack((x[0, :], x[1, :], x[2, :], force), axis=1)
        with open(output_directory + name + "_" + str(i) + ".csv", "w") as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(fields)
            # writing the data rows
            csvwriter.writerows(results)


def generate_geometry_distribution_cmd():
    """
    Wrapper around the generate_geometry_distribution() function to call it from the
    command line with arguments.
    """
    # Parse arguments
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
        help="Relative path to output directory.",
        type=str,
        default="",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name pattern to write out files in the output directory. Default is geometry_distribution.",
        type=str,
        default="geometry_distribution",
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
        default="Z+",
    )
    parser.add_argument(
        "-l",
        "--lift_direction",
        help="Lift direction. String in (X+, X-, Y+, Y-, Z+, Z-) or list of floats specifying vector. Default is Y+.",
        type=str,
        nargs="+",
        default="Y+",
    )
    parser.add_argument(
        "-d",
        "--drag_direction",
        help="Drag direction. String in (X+, X-, Y+, Y-, Z+, Z-) or list of floats specifying vector. Default is X+.",
        type=str,
        nargs="+",
        default="Y+",
    )
    parser.add_argument(
        "-xs",
        "--x_start",
        help="Coordinate to start slices from. Default is [0, 0, 0].",
        type=str,
        nargs="+",
        default=[0, 0, 0],
    )
    parser.add_argument(
        "-xe",
        "--x_end",
        help="Coordinate to end slices a. Default is [0, 0, 1].",
        type=str,
        nargs="+",
        default=[0, 0, 1],
    )
    parser.add_argument(
        "-ns",
        "--n_span",
        help="Number of spanwise samples. Default is 100.",
        type=int,
        default=100,
    )

    # Call function
    generate_geometry_distribution(**vars(parser.parse_args()))


def generate_geometry_distribution(
    input_file=None,
    output_directory="./",
    name="geometry_distribution",
    patches="group/wall",
    span_direction="Z+",
    lift_direction="Y+",
    drag_direction="X+",
    x_start=[0, 0, 0],
    x_end=[0, 0, 1],
    n_span=100,
):
    """
    Function to compute a force distribution using Paraview.


    Parameters
    ----------
    input_file : str
        Path to file to load with Paraview.
    output_directory : str
        Path to directory where the distribution files will be written. Default
        is "./".
    name : str
        Name pattern to write out files in the output directory. Default is
        "geometry_distribution".
    patches : str or list
        Patch name(s) over which to compute the force distribution. Default
        is "group/wall".
    span_direction : str or list
        Vector direction for span direction either as a string (eg. X+) or list
        (eg. [0 0 1]). Should be of magnitude 1. Default is "Z+".
    lift_direction : str or list
        Vector direction for lift direction either as a string (eg. X+) or list
        (eg. [0 1 0]). Should be of magnitude 1. Default is "Y+".
    drag_direction : str or list
        Vector direction for drag direction either as a string (eg. X+) or list
        (eg. [1 0 0]). Should be of magnitude 1. Default is "X+".
    x_start : list
        Coordinates to start slices from. Default is [0, 0, 0].
    x_end : list
        Coordinates to end slices at. Default is [0, 0, 1].
    n_span : int
        Number of spanwise samples. Default is 100.
    """
    # Check if output directory exists
    if not os.path.isdir(output_directory):
        raise RuntimeError("Output directory {} does not exist.".format(output_directory))

    # Generate direction vectors
    span_direction = utils.check_input_vector(span_direction, "span direction", check_norm=True)
    lift_direction = utils.check_input_vector(lift_direction, "lift direction", check_norm=True)
    drag_direction = utils.check_input_vector(drag_direction, "drag direction", check_norm=True)

    # Generate sample points
    if len(x_start) != 3:
        raise ValueError("x_start should be list of length 3, not {} with length {}.".format(x_start, len(x_start)))
    if len(x_end) != 3:
        raise ValueError("x_end should be list of length 3, not {} with length {}.".format(x_end, len(x_end)))
    x = np.array(
        [
            np.linspace(float(x_start[0]), float(x_end[0]), n_span),
            np.linspace(float(x_start[1]), float(x_end[1]), n_span),
            np.linspace(float(x_start[2]), float(x_end[2]), n_span),
        ]
    )

    # Import case
    if input_file == None:
        raise ValueError("Input file not set.")
    paraviewfoam = paraview.OpenFOAMReader(
        registrationName="paraview.foam", FileName=str(os.getcwd()) + "/{}".format(input_file)
    )
    paraviewfoam.MeshRegions = patches

    # Read time data
    animationScene1 = paraview.GetAnimationScene()
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    reader = paraview.GetActiveSource()
    times = reader.TimestepValues

    chord = np.zeros(n_span)
    twist = np.zeros(n_span)
    thickness = np.zeros(n_span)
    for i in range(len(times)):
        paraview.UpdatePipeline(time=times[i], proxy=paraviewfoam)

        # Zero Arrays
        chord[:] = 0.0
        twist[:] = 0.0
        thickness[:] = 0.0

        # Iterate over span
        for j in range(n_span):
            # Create a slice
            slice1 = paraview.Slice(registrationName="Slice1", Input=paraviewfoam)

            # Set slice location and normal
            slice1.SliceType.Origin = [x[0, j], x[1, j], x[2, j]]
            slice1.SliceType.Normal = [span_direction[0], span_direction[1], span_direction[2]]

            # Compute Sorted Line
            plotOnSortedLines1 = paraview.PlotOnSortedLines(registrationName="PlotOnSortedLines1", Input=slice1)

            # Extract Data
            data = paraview.servermanager.Fetch(plotOnSortedLines1).GetBlock(0)
            coords = np.zeros((0, 3))
            arclen = np.zeros(0)
            for k in range(data.GetNumberOfBlocks()):
                if data.GetBlock(k).GetNumberOfBlocks() > 0:
                    seg_coords = vtk_np.vtk_to_numpy(data.GetBlock(k).GetBlock(0).GetPoints().GetData())
                    seg_arclen = vtk_np.vtk_to_numpy(data.GetBlock(k).GetBlock(0).GetPointData().GetArray("arc_length"))
                    coords = np.concatenate((coords, seg_coords), axis=0)
                    arclen = np.concatenate((arclen, seg_arclen), axis=0)

            # Cleanup Paraview Objects
            paraview.Delete(plotOnSortedLines1)
            paraview.Delete(slice1)

            # Rotate points to X-Y plane
            coords2D = coords[:, :2]

            # Sort
            coords2D, arclen, _ = pv_utils.sort_airfoil(coords2D, arclen)

            # Compute sectional properties
            chord[j], twist[j], thickness[j] = compute_section_properties(coords2D)

        # Write CSV File
        fields = ["X", "Y", "Z", "Twist", "Chord", "Thick"]
        results = np.stack((x[0, :], x[1, :], x[2, :], twist, chord, thickness), axis=1)
        with open(output_directory + name + "_" + str(i) + ".csv", "w") as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(fields)
            # writing the data rows
            csvwriter.writerows(results)


def compute_section_properties(coords2D):
    """
    Compute the chord and twist of an airfoil section given a set of ordered
    points.

    Parameters
    ----------
    coords2D : ndarray
        Sorted 2D airfoil coordinates rotated to an X-Y plane, with the flow
        direction as +X and lift direction as +Y.

    Returns
    -------
    float
        Section chord length, in current working units.
    float
        Section twist, in degrees.
    float
        Section maximum thickness, in current working units.
    """
    # Find the trailing edge
    te_pts, te_idx = pv_utils.find_te(coords2D)
    x_te = np.mean(te_pts, axis=0)

    # Find coordinate furthest from LE and two neighbors
    max_dist = 0.0
    i_max_dist = -1
    for k in range(1, np.size(coords2D, 0)):
        dist = np.linalg.norm(coords2D[k, :] - x_te)
        if dist > max_dist:
            max_dist = dist
            i_max_dist = k

    x_le_pt_down = coords2D[i_max_dist - 1, :]
    x_le_pt = coords2D[i_max_dist, :]
    x_le_pt_up = coords2D[i_max_dist + 1, :]

    # Compute center and radius of LE circle
    def circle_from_3_points(x1, x2, x3):
        z1 = complex(x1[0], x1[1])
        z2 = complex(x2[0], x2[1])
        z3 = complex(x3[0], x3[1])

        if (z1 == z2) or (z2 == z3) or (z3 == z1):
            raise ValueError(f"Duplicate points: {z1}, {z2}, {z3}")

        w = (z3 - z1) / (z2 - z1)

        # Check for colinear points
        if abs(w.imag) <= 1e-5:
            raise ValueError(f"Points are collinear: {z1}, {z2}, {z3}")

        c = (z2 - z1) * (w - abs(w) ** 2) / (2j * w.imag) + z1
        r = abs(z1 - c).real

        c = np.array([c.real, c.imag])
        return c, r

    c, r = circle_from_3_points(x_le_pt_down, x_le_pt, x_le_pt_up)

    # Find true LE
    def minFunc(theta, c, r, xTE):
        x = np.array([r * np.cos(theta[0]) + c[0], r * np.sin(theta[0]) + c[1]])
        return -np.linalg.norm(x - x_te)

    res = scipy.optimize.minimize(minFunc, x0=[np.pi / 2], args=(c, r, x_te), bounds=[(0, 2 * np.pi)], tol=1e-12)
    x_le = np.array([r * np.cos(res.x[0]) + c[0], r * np.sin(res.x[0]) + c[1]])

    # Compute chord
    chord = np.linalg.norm(x_te - x_le)

    # Compute twist
    twist = np.rad2deg(np.arctan2((x_le[1] - x_te[1]), -(x_le[0] - x_te[0])))

    # Rotate airfoil
    R = np.array(
        [
            [np.cos(np.deg2rad(twist)), -np.sin(np.deg2rad(twist))],
            [np.sin(np.deg2rad(twist)), np.cos(np.deg2rad(twist))],
        ]
    )
    coords_disp = (R @ (coords2D[:, :] - x_le).T).T

    # Isolate coordinates
    coords_top = np.flip(coords_disp[0:i_max_dist, :], axis=0)
    coords_bot = coords_disp[i_max_dist + 1 :, :][0 : te_idx[1] - i_max_dist]

    # Parameterize spline through upper surface
    spline_top = Akima1DInterpolator(coords_top[:, 0], coords_top[:, 1])
    spline_bot = Akima1DInterpolator(coords_bot[:, 0], coords_bot[:, 1])

    # Iterate along chord and compute thickness
    x_sample = np.linspace(chord * 0.01, chord * 0.99, 100)
    thickness = 0.0
    for x_loc in x_sample:
        y_top = spline_top(x_loc)
        y_bot = spline_bot(x_loc)

        thick_loc = y_top - y_bot
        if thick_loc > thickness:
            thickness = thick_loc

    return chord, twist, thickness
