import numpy as np

def form_clusters(positions, is_CH, alive):
    """
    Assigns each alive Cluster Member (CM) to the nearest alive Cluster Head (CH).

    Parameters:
    - positions: ndarray of shape (N, 2), node coordinates
    - is_CH: Boolean array, True if node is a Cluster Head
    - alive: Boolean array, True if node is alive

    Returns:
    - CH_indices: indices of alive CHs
    - CM_indices: indices of alive CMs
    - cluster_assignments: array mapping each CM to a CH index (or -1 if no CH found)
    """
    CH_indices = np.where(is_CH & alive)[0]
    CM_indices = np.where(~is_CH & alive)[0]
    cluster_assignments = -np.ones(len(positions), dtype=int)  # Default unassigned

    if CH_indices.size == 0:
        return CH_indices, CM_indices, cluster_assignments  # No CHs to assign

    # Assign each CM to the nearest CH
    for cm in CM_indices:
        distances = np.linalg.norm(positions[CH_indices] - positions[cm], axis=1)
        nearest_ch_index = np.argmin(distances)
        cluster_assignments[cm] = CH_indices[nearest_ch_index]

    return CH_indices, CM_indices, cluster_assignments
