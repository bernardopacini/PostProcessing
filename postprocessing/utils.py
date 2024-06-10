import numpy as np


def check_input_vector(var, name, check_norm=True):
    """
    Function to check an input vector to ensure it is valid, and return the corresponding vector in numpy format.

    Parameters
    ----------
    var : str or list
        Vector value either as a string (eg. X) or list [1 0 0].
    name : str
        Variable name.
    check_norm: bool
        Check the norm of the vector to ensure it is length one.

    Returns
    -------
    ndarray
        Vector of length three with the corresponding vector.
    """
    # Assign vector based on text
    if len(var) == 1:
        if var[0].upper() == "X+":
            return np.array([1.0, 0.0, 0.0])
        elif var[0].upper() == "X-":
            return np.array([-1.0, 0.0, 0.0])
        elif var[0].upper() == "Y+":
            return np.array([0.0, 1.0, 0.0])
        elif var[0].upper() == "Y-":
            return np.array([0.0, -1.0, 0.0])
        elif var[0].upper() == "Z+":
            return np.array([0.0, 0.0, 1.0])
        elif var[0].upper() == "Z-":
            return np.array([0.0, 0.0, -1.0])
        else:
            raise ValueError(
                "Provided {} value, {}, not recognized. When specified with a string, options are X+, X-, Y+, Y-, and Z+, Z-.".format(
                    name, var
                )
            )

    # Assign vector based on list
    else:
        if len(var) != 3:
            raise ValueError(
                "Provided {} value, {}, not recognized. When specified with a list, should be a list of length three specifying a vector.".format(
                    name, var
                )
            )
        else:
            x = float(var[0])
            y = float(var[1])
            z = float(var[2])

            mag = np.linalg.norm(np.array([x, y, z]))
            if check_norm and mag - 1 > 1e-5:
                print(
                    "Warning: Provided {} vector, {}, does not have a magnitude of 1. Normalizing the vector.".format(
                        name, var
                    )
                )
                return np.array([x / mag, y / mag, z / mag])
            else:
                return np.array([x, y, z])
