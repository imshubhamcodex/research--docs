import numpy as np
from config import *

def select_CHs(positions, energies, alive, E_total, round_num):
    """
    Selects Cluster Heads (CHs) based on energy level and distance-aware probability.

    Parameters:
    - positions: ndarray of shape (N, 2), node positions
    - energies: array of current energy levels of nodes
    - alive: boolean array of node liveliness
    - E_total: total initial energy of the network
    - round_num: current round number

    Returns:
    - is_CH: boolean array indicating selected CHs
    """
    E_avg = E_total * (1 - round_num / ROUNDS) / NUM_NODES
    is_CH = np.zeros(NUM_NODES, dtype=bool)

    for i in range(NUM_NODES):
        if not alive[i]:
            continue

        # Equation 11: CH selection probability Pi
        scaling = 1 + h * (alpha + S * beta) * E_avg
        Pi = p_opt * energies[i] / scaling

        # Equation 12: Threshold adjusted by distance to sink
        d_to_sink = np.linalg.norm(positions[i] - SINK_POS)
        try:
            denominator = 1 - Pi * (round_num % round(1 / Pi)) if Pi > 0 else 1
            threshold = Pi / denominator if denominator != 0 else 0
        except ZeroDivisionError:
            threshold = 0
        threshold /= d_to_sink  # Distance-aware adjustment

        if np.random.rand() < threshold:
            is_CH[i] = True

    return is_CH
