import numpy as np
from config import *

def select_CHs(energies, alive, E_total, round_num):
    """
    Selects Cluster Heads (CHs) based on energy-aware probabilistic thresholding.

    Parameters:
    - energies: array of node energies
    - alive: boolean array indicating which nodes are alive
    - E_total: initial total network energy
    - round_num: current round

    Returns:
    - is_CH: boolean array indicating CHs
    """
    E_avg = E_total * (1 - round_num / ROUNDS) / NUM_NODES  # Estimate average energy
    is_CH = np.zeros(NUM_NODES, dtype=bool)

    for i in range(NUM_NODES):
        if not alive[i]:
            continue
     
        Pi = p_opt * (energies[i] / E_avg) if E_avg > 0 else 0  # Prevent divide-by-zero

        try:
            denominator = 1 - Pi * ((round_num % round(1 / Pi)) if Pi > 0 else 1)
            threshold = Pi / denominator if denominator != 0 else 0
        except ZeroDivisionError:
            threshold = 0

        if np.random.rand() < threshold:
            is_CH[i] = True

    return is_CH
