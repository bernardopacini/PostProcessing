# External imports
import os
import argparse
import glob

# Paraview imports
import paraview.simple as paraview

# Internal Imports


def extract_geometry_cmd():
    """
    Wrapper around the extract_geometry() function to call it from
    the command line with arguments.
    """
    # Parse arguments
    parser = extract_geometry_parser()

    # Call function
    extract_geometry(**vars(parser.parse_args()))


def extract_geometry_parser():
    """
    Parser for options for the extract_geometry() function to call it from the
    command line with arguments.

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
        "-ow",
        "--overwrite",
        help="Flag to overwrite existing temporary geometry and geometry files. Default is False.",
        type=str,
        default="False",
    )
    return parser


def extract_geometry(input_file=None, output_directory="./", overwrite="False"):
    """
    Function to extract a geometry from an OpenFOAM mesh and write it as an
    STL.

    Parameters
    ----------
    input_file : str
        Path to file to load with Paraview.
    output_directory : str
        Path to directory where the geometry files will be written. Default is
        "./".
    overwrite : str
        Flag to overwrite existing temporary geometry and geometry files.
        Default is False.
    """
    # Check if exist exist
    if glob.glob(output_directory + "/Temp*.stl") and overwrite != "True":
        raise RuntimeError(
            "Temporary geometry files exist, remove all Temp<#>.stl files or run with overwrite set to True."
        )
    elif glob.glob(output_directory + "/Temp*.stl"):
        print("Warning: Overwriting existing temporary geometry files.")

    if glob.glob(output_directory + "/Geometry.stl") and overwrite != "True":
        raise RuntimeError("Geometry file exists, remove the Geometry.stl file or run with overwrite=True.")
    elif glob.glob(output_directory + "/Geometry.stl"):
        print("Warning: Overwriting existing geometry file.")

    # Import case
    if input_file is None:
        raise ValueError("Input file not set.")
    paraviewfoam = paraview.OpenFOAMReader(
        registrationName="paraview.foam", FileName=str(os.getcwd()) + "/{}".format(input_file)
    )
    paraviewfoam.MeshRegions = ["group/wall"]

    # Save walls to STLs

    paraview.SaveData(output_directory + "/Temp.stl", proxy=paraviewfoam, FieldDataArrays=["CasePath"])

    # Close OpenFOAM case
    paraview.Delete(paraviewfoam)
    del paraviewfoam

    # Import STL files
    temp_files = glob.glob(output_directory + "/Temp*.stl")
    temp_STL = []
    for temp_file in temp_files:
        temp_STL.append(paraview.STLReader(registrationName=temp_file, FileNames=[output_directory + "/" + temp_file]))

    # Append geometry
    appendGeometry1 = paraview.AppendGeometry(registrationName="AppendGeometry1", Input=temp_STL)

    # Save STL
    paraview.SaveData(output_directory + "/Geometry.stl", proxy=appendGeometry1)

    # Destroy geometry
    paraview.Delete(appendGeometry1)
    del appendGeometry1

    # Destroy STLs
    for i in range(len(temp_STL)):
        paraview.Delete(temp_STL[0])
        del temp_STL[0]

    # Delete temporary files
    for temp_file in temp_files:
        os.remove(temp_file)
