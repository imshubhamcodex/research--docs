import numpy as np
from config import *

def select_CHs(positions, energies, alive, E_total, round_num):
    """
    Selects Cluster Heads (CHs) using energy and distance-aware probabilistic thresholds.

    Based on:
    - Eq. (11): Energy-level aware CH probability
    - Eq. (12): Distance-aware threshold to penalize far nodes
    - Eq. (7): E_avg = average energy for round

    Parameters:
    - positions: ndarray (N, 2) → (x, y) positions of nodes
    - energies: array of node energy levels
    - alive: boolean array indicating alive status
    - E_total: total initial energy of network
    - round_num: current round number

    Returns:
    - is_CH: boolean array indicating CH selection
    """
    E_avg = E_total * (1 - round_num / ROUNDS) / NUM_NODES  # Eq. (7)
    is_CH = np.zeros(NUM_NODES, dtype=bool)

    for i in range(NUM_NODES):
        if not alive[i]:
            continue

        # Eq. (11): Energy-based CH selection probability
        scaling = (1 + h * (alpha + S * beta)) * E_avg
        Pi = p_opt * energies[i] / scaling if scaling > 0 else 0

        # Distance to sink (used in Eq. 12)
        d_to_sink = np.linalg.norm(positions[i] - SINK_POS)

        # Eq. (12): Threshold includes distance penalty
        try:
            denominator = 1 - Pi * (round_num % round(1 / Pi)) if Pi > 0 else 1
            threshold = Pi / denominator if denominator != 0 else 0
        except ZeroDivisionError:
            threshold = 0

        # Distance-aware adjustment (inverse proportional)
        threshold /= d_to_sink if d_to_sink > 0 else 1  # Avoid div by 0

        # Node becomes CH if random number falls below threshold
        if np.random.rand() < threshold:
            is_CH[i] = True

    return is_CH
