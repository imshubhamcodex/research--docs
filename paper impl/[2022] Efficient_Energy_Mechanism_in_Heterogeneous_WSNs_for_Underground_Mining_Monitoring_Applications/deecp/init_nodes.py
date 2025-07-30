import numpy as np
from config import *

def initialize_nodes():
    # Initialize energy and type arrays
    energies = np.zeros(NUM_NODES)
    types = np.zeros(NUM_NODES)  # 0 = normal, 1 = high-energy

    # Calculate number of high-energy nodes
    Nh = int(h * NUM_NODES)

    # Randomly shuffle node indices
    node_indices = np.random.permutation(NUM_NODES)

    # Assign high-energy and normal-energy nodes
    high_energy_nodes = node_indices[:Nh]
    normal_energy_nodes = node_indices[Nh:]

    # Set energy levels and types
    energies[high_energy_nodes] = Eo * (1 + alpha)
    types[high_energy_nodes] = 1  # High-energy nodes

    energies[normal_energy_nodes] = Eo
    types[normal_energy_nodes] = 0  # Normal nodes

    return energies, types
