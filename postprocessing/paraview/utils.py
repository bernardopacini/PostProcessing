import numpy as np


# TODO: Update this function to sort segments, ensure clockwise orientation, then shift so top TE point is first.
def sort_airfoil(coords, arclen):
    """
    Airfoil slices from Paraview are typically well sorted because they follow
    the curvature of the section. But, segments can be out of order. This
    function sorts these segments into counter-clockwise ordering starting
    at the top of the trailing edge.

    Parameters
    ----------
    coords : ndarray
        Unsorted 2D airfoil coordinates in an X-Y plane with the flow
        direction as +X and lift direction as +Y.
    arclen : ndarray
        Arclengh along the segments corresponding to the input coordinates.

    Returns
    -------
    ndarray
        Sorted airfoil coordinates.
    ndarray
        Sorted arclength array matching the sorted airfoil coordinates.
    ndarray
        Indice mapping from unsorted to sorted coordinate array.
    """
    x = np.array(coords[:, 0])
    y = np.array(coords[:, 1])
    nPoints = len(x)

    # Find Segments
    segments = []
    iStart = 0
    for i in range(1, nPoints):
        if arclen[i] < arclen[i - 1]:
            segments.append((iStart, i))
            iStart = i

    segments.append((iStart, nPoints))
    if len(segments) == 1:
        # Assumes one continuous segment. Checks the direction to be
        # counter-clockwise and checks starting point to be the top of the TE.
        pass

    elif len(segments) == 2:
        raise RuntimeWarning("Sorting two-segment airfoils is not yet supported!")

    elif len(segments) == 3:
        # Assumes the segments are Top, Bottom, and TE. Sorts by averaging
        # values to determine where segments are in relation to each other.

        # Find TE Segment
        meanX = -np.inf
        segTE = -1
        for i in range(len(segments)):
            mean = np.mean(x[segments[i][0] : segments[i][1]])
            if mean > meanX:
                segTE = i
                meanX = mean

        if segTE == -1:
            raise RuntimeError("Trailing edge segment not found!")

        # Find Top Segment
        meanY = -np.inf
        segTop = -1
        for i in range(len(segments)):
            if i == segTE:
                continue

            mean = np.mean(y[segments[i][0] : segments[i][1]])
            if mean > meanY:
                segTop = i
                meanY = mean

        if segTop == -1:
            raise RuntimeError("Top surface segment not found!")

        for i in range(len(segments)):
            if i != segTE and i != segTop:
                segBot = i

        # Sort and Combine Segments
        xSort = np.zeros(nPoints)
        ySort = np.zeros(nPoints)
        arclenSort = np.zeros(nPoints)

        # Top Surface
        iStart = segments[segTop][0]
        iEnd = segments[segTop][1]
        nPointsTop = iEnd - iStart

        if x[iStart] > x[iEnd - 1]:
            xSort[0:nPointsTop] = x[iStart:iEnd]
            ySort[0:nPointsTop] = y[iStart:iEnd]
            arclenSort[0:nPointsTop] = arclen[iStart:iEnd]
        else:
            xSort[0:nPointsTop] = np.flip(x[iStart:iEnd])
            ySort[0:nPointsTop] = np.flip(y[iStart:iEnd])
            arclenSort[0:nPointsTop] = np.flip(arclen[iStart:iEnd])

        # Bottom Surface
        iStart = segments[segBot][0]
        iEnd = segments[segBot][1]
        nPointsBot = iEnd - iStart

        if x[iStart] < x[iEnd - 1]:
            xSort[nPointsTop : nPointsTop + nPointsBot] = x[iStart:iEnd]
            ySort[nPointsTop : nPointsTop + nPointsBot] = y[iStart:iEnd]
            arclenSort[nPointsTop : nPointsTop + nPointsBot] = arclen[iStart:iEnd]
        else:
            xSort[nPointsTop : nPointsTop + nPointsBot] = np.flip(x[iStart:iEnd])
            ySort[nPointsTop : nPointsTop + nPointsBot] = np.flip(y[iStart:iEnd])
            arclenSort[nPointsTop : nPointsTop + nPointsBot] = np.flip(arclen[iStart:iEnd])

        # TE
        iStart = segments[segTE][0]
        iEnd = segments[segTE][1]
        nPointsTE = iEnd - iStart

        if y[iStart] < y[iEnd - 1]:
            xSort[nPointsTop + nPointsBot : nPointsTop + nPointsBot + nPointsTE] = x[iStart:iEnd]
            ySort[nPointsTop + nPointsBot : nPointsTop + nPointsBot + nPointsTE] = y[iStart:iEnd]
            arclenSort[nPointsTop + nPointsBot : nPointsTop + nPointsBot + nPointsTE] = arclen[iStart:iEnd]
        else:
            xSort[nPointsTop + nPointsBot : nPointsTop + nPointsBot + nPointsTE] = np.flip(x[iStart:iEnd])
            ySort[nPointsTop + nPointsBot : nPointsTop + nPointsBot + nPointsTE] = np.flip(y[iStart:iEnd])
            arclenSort[nPointsTop + nPointsBot : nPointsTop + nPointsBot + nPointsTE] = np.flip(arclen[iStart:iEnd])
    else:
        raise RuntimeError("Unable to sort airfoil, {} segments found".format(len(segments)))

    # Remove Duplicates
    xiSortUni = sorted(np.unique(xSort, return_index=True)[1])
    yiSortUni = sorted(np.unique(ySort, return_index=True)[1])

    mask = np.ones(nPoints, dtype=bool)
    for i in range(nPoints):
        if i not in xiSortUni and i not in yiSortUni:
            mask[i] = False

    xSort = xSort[mask]
    ySort = ySort[mask]
    arclenSort = arclenSort[mask]

    return np.array([xSort, ySort]).T, arclenSort, None


def find_te(coords):
    """
    Identify trailing edge coordinates and their corresponding indices from 2D
    airfoil data in an X-Y plane.

    Parameters
    ----------
    coords : ndarray
        Sorted 2D airfoil coordinates in an X-Y plane with the flow
        direction as +X and lift direction as +Y. The coordinate ordering
        should be counter-clockwise.

    Returns
    -------
    ndarray
        Coordinates of the upper and lower surface TE points
    ndarray
        Indices of the upper and lower surface TE points
    """
    theta = np.zeros(np.size(coords, 0))
    for i in range(np.size(coords, 0)):
        # Compute interior angle
        if i == 0:
            a = coords[-1, :] - coords[i, :]
            b = coords[i + 1, :] - coords[i, :]
        elif i == np.size(coords, 0) - 1:
            a = coords[i - 1, :] - coords[i, :]
            b = coords[0, :] - coords[i, :]
        else:
            a = coords[i - 1, :] - coords[i, :]
            b = coords[i + 1, :] - coords[i, :]

        theta[i] = np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    # Find TE candidates
    te_candidates = np.argwhere(theta < np.deg2rad(145.0))[:, 0]

    if np.size(te_candidates) < 2:
        raise RuntimeError("Unable to find blunt trailing edge.")
    elif np.size(te_candidates) > 2:
        print(
            "Warning: found more than 2 trailing edge point candidates. Selecting the points with the largest X values."
        )
        idxs = np.argsort(coords[te_candidates, 0])[-2:]

    te_pts = np.array([coords[te_candidates[0], :], coords[te_candidates[1], :]])
    te_idx = np.array([te_candidates[0], te_candidates[1]])

    return te_pts, te_idx
