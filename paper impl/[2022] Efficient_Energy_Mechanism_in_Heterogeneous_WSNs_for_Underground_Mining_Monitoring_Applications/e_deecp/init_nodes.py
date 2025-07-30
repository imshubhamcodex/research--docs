import numpy as np
from config import *

def initialize_nodes():
    # Initialize energy and type arrays
    energies = np.zeros(NUM_NODES)
    types = np.zeros(NUM_NODES)  # 0 = normal, 1 = high, 2 = super

    # Calculate number of high and super energy nodes
    Nh = int(h * NUM_NODES)       # High-energy nodes (including super)
    Ns = int(S * Nh)              # Super-energy nodes (subset of high-energy)

    # Shuffle node indices randomly
    node_indices = np.random.permutation(NUM_NODES)

    # Assign super, high, and normal energy node indices
    super_ids = node_indices[:Ns]
    high_ids = node_indices[Ns:Nh]
    normal_ids = node_indices[Nh:]

    # Set energy levels and types
    energies[super_ids] = Eo * (1 + beta)
    types[super_ids] = 2  # Super nodes

    energies[high_ids] = Eo * (1 + alpha)
    types[high_ids] = 1   # High-energy nodes

    energies[normal_ids] = Eo
    types[normal_ids] = 0  # Normal nodes

    return energies, types
