import numpy as np


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
    n_points = np.size(coords, 0)

    # Find segments
    segments = []
    i_start = 0
    for i in range(1, n_points):
        if arclen[i] < arclen[i - 1]:
            segments.append((i_start, i - 1))
            i_start = i

    segments.append((i_start, n_points - 1))

    # Sort segments
    if len(segments) > 1:
        segment_order = [0]
        segment_flip = [False]

        # Find segment end points
        segment_ends = np.zeros((len(segments), 2, 2))
        for i in range(len(segments)):
            segment_ends[i, 0, :] = coords[segments[i][0], :]
            segment_ends[i, 1, :] = coords[segments[i][1], :]

        # Form change of segments, connecting matching endpoints
        current_end = segment_ends[0, 1, :]
        segment_list = list(range(1, len(segments)))
        for i in range(1, len(segments)):
            segment_found = False

            for j in range(len(segment_list)):
                # Try starting point
                if np.linalg.norm(segment_ends[segment_list[j], 0, :] - current_end) < 1e-8:
                    current_end = segment_ends[segment_list[j], 1, :]
                    segment_flip.append(False)
                    segment_found = True

                # Try end point
                elif np.linalg.norm(segment_ends[segment_list[j], 1, :] - current_end) < 1e-8:
                    current_end = segment_ends[segment_list[j], 0, :]
                    segment_flip.append(True)
                    segment_found = True

                if segment_found:
                    segment_order.append(segment_list[j])
                    segment_list.pop(j)
                    break

            if not segment_found:
                raise RuntimeError("Connected segment not found. Ensure the airfoil slice is closed.")

        # Sort coordinates
        coords_sort = np.zeros((n_points, 2))
        arclen_sort = np.zeros(n_points)
        indice_sort = np.zeros(n_points, dtype=int)
        i_segment_start = 0
        for i_segment, flip in zip(segment_order, segment_flip):
            i_segment_end = i_segment_start + segments[i_segment][1] - segments[i_segment][0] + 1
            if flip:
                coords_sort[i_segment_start:i_segment_end] = np.flip(
                    coords[segments[i_segment][0] : segments[i_segment][1] + 1, :], axis=0
                )
                arclen_sort[i_segment_start:i_segment_end] = np.flip(
                    arclen[segments[i_segment][0] : segments[i_segment][1] + 1]
                )
                indice_sort[i_segment_start:i_segment_end] = np.flip(
                    np.arange(segments[i_segment][0], segments[i_segment][1] + 1, dtype=int)
                )
            else:
                coords_sort[i_segment_start:i_segment_end] = coords[
                    segments[i_segment][0] : segments[i_segment][1] + 1, :
                ]
                arclen_sort[i_segment_start:i_segment_end] = arclen[segments[i_segment][0] : segments[i_segment][1] + 1]
                indice_sort[i_segment_start:i_segment_end] = np.arange(
                    segments[i_segment][0], segments[i_segment][1] + 1, dtype=int
                )
            i_segment_start = i_segment_end

        coords = coords_sort
        arclen = arclen_sort
        indice = indice_sort
    else:
        indice = np.arange(0, np.size(arc_length), dtype=int)

    # Remove duplicate nodes
    coords_x_unique = sorted(np.unique(coords[:, 0], return_index=True)[1])
    coords_y_unique = sorted(np.unique(coords[:, 1], return_index=True)[1])

    mask = np.ones(n_points, dtype=bool)
    for i in range(n_points):
        if i not in coords_x_unique and i not in coords_y_unique:
            mask[i] = False

    coords = np.array([coords[:, 0][mask], coords[:, 1][mask]]).T
    arclen = arclen[mask]
    indice = indice[mask]
    n_points = np.size(arclen)

    # Compute area to ensure counter-clockwise orientation
    area = 0.0
    for i in range(n_points - 1):
        area += coords[i, 0] * coords[i + 1, 1] - coords[i, 1] * coords[i + 1, 0]
    area *= 0.5

    if area < 0:
        coords = np.flip(coords, axis=0)
        arclen = np.flip(arclen)
        indice = np.flip(indice)

    # Shift coordinates to start at upper trailing edge point
    _, te_idx = find_te(coords)

    coords = np.roll(coords, -te_idx[0], axis=0)
    arclen = np.roll(arclen, -te_idx[0])
    indice = np.roll(indice, -te_idx[0])

    return coords, arclen, indice


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

        if np.abs(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))) < 1.0:
            theta[i] = np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        else:
            theta[i] = np.pi

    # Find TE candidates
    te_candidates = np.argwhere(theta < np.deg2rad(145.0))[:, 0]

    if np.size(te_candidates) < 2:
        raise RuntimeError("Unable to find blunt trailing edge.")
    elif np.size(te_candidates) > 2:
        print(
            "Warning: found more than 2 trailing edge point candidates. Selecting the points with the largest X values."
        )
        te_candidates = np.argsort(coords[te_candidates, 0])[-2:]

    if coords[te_candidates[0], 1] < coords[te_candidates[1], 1]:
        te_candidates = np.flip(te_candidates)
    te_pts = np.array([coords[te_candidates[0], :], coords[te_candidates[1], :]])
    te_idx = np.array([te_candidates[0], te_candidates[1]])

    return te_pts, te_idx
