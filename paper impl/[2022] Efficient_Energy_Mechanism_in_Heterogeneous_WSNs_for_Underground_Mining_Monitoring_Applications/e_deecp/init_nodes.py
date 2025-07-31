import numpy as np
from config import *

def initialize_nodes():
    """
    Initializes sensor nodes with heterogeneous energy levels:
    - Normal nodes: energy = Eo
    - High-energy nodes: energy = Eo * (1 + alpha)
    - Super-energy nodes: energy = Eo * (1 + beta)

    Based on:
    - Eq. (3): total energy calculation with 3 node types
    - Eq. (4): simplified total energy expression

    Returns:
    - energies: array of initial energies
    - types: array of node types (0 = normal, 1 = high, 2 = super)
    """
    energies = np.zeros(NUM_NODES)
    types = np.zeros(NUM_NODES)  # 0 = normal, 1 = high, 2 = super

    Nh = int(h * NUM_NODES)        # High + super nodes (h fraction)
    Ns = int(S * Nh)               # Super nodes (S fraction of Nh)

    node_indices = np.random.permutation(NUM_NODES)  # Random assignment

    super_ids = node_indices[:Ns]              # First S*Nh nodes → super
    high_ids = node_indices[Ns:Nh]             # Next (h - S)*N nodes → high
    normal_ids = node_indices[Nh:]             # Remaining nodes → normal

    # Assign energy values and types
    energies[super_ids] = Eo * (1 + beta)
    types[super_ids] = 2

    energies[high_ids] = Eo * (1 + alpha)
    types[high_ids] = 1

    energies[normal_ids] = Eo
    types[normal_ids] = 0

    return energies, types
