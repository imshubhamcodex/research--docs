import numpy as np
from config import *

def select_CHs(energies, alive, E_total, round_num):
    """
    Selects Cluster Heads based on DEECP logic.
    
    References:
    - Eq. (5): CH selection probability based on energy ratio
    - Eq. (6): Threshold using modulo-based round fairness
    - Eq. (7): Average energy estimate for current round

    Parameters:
    - energies: array of node energies
    - alive: boolean array for alive status
    - E_total: initial total energy of network
    - round_num: current round number

    Returns:
    - is_CH: boolean array (True if selected as CH)
    """
    E_avg = E_total * (1 - round_num / ROUNDS) / NUM_NODES  # Eq. (7)
    is_CH = np.zeros(NUM_NODES, dtype=bool)

    for i in range(NUM_NODES):
        if not alive[i]:
            continue

        # Eq. (5): Pi depends on energy ratio
        Pi = p_opt * (energies[i] / E_avg) if E_avg > 0 else 0

        try:
            # Eq. (6): Threshold for CH candidacy
            denominator = 1 - Pi * ((round_num % round(1 / Pi)) if Pi > 0 else 1)
            threshold = Pi / denominator if denominator != 0 else 0
        except ZeroDivisionError:
            threshold = 0

        # Node becomes CH if random number < threshold
        if np.random.rand() < threshold:
            is_CH[i] = True

    return is_CH
