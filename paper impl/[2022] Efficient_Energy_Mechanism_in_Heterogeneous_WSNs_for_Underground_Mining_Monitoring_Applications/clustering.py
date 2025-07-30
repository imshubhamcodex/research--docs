import numpy as np

def form_clusters(positions, is_CH, alive):
    """
    Forms clusters by assigning each alive cluster member (CM) to the nearest alive cluster head (CH).

    Parameters:
    - positions: ndarray of shape (N, 2), positions of the nodes
    - is_CH: boolean array indicating which nodes are cluster heads
    - alive: boolean array indicating which nodes are alive

    Returns:
    - CH_indices: indices of alive cluster heads
    - CM_indices: indices of alive cluster members
    - cluster_assignments: array of CH indices each CM is assigned to (-1 if no CH available)
    """
    CH_indices = np.where(is_CH & alive)[0]
    CM_indices = np.where(~is_CH & alive)[0]
    cluster_assignments = -np.ones(len(positions), dtype=int)  # Default: unassigned

    if CH_indices.size == 0:
        return CH_indices, CM_indices, cluster_assignments  # No CHs to assign to

    for cm in CM_indices:
        # Compute distances to all CHs
        distances = np.linalg.norm(positions[CH_indices] - positions[cm], axis=1)
        nearest_ch_index = np.argmin(distances)
        cluster_assignments[cm] = CH_indices[nearest_ch_index]

    return CH_indices, CM_indices, cluster_assignments
