import numpy as np
from config import *

def initialize_nodes():
    """
    Initializes nodes with energy and type:
    - Normal nodes have energy = Eo
    - High-energy nodes have energy = Eo * (1 + alpha)
    
    Based on two-level heterogeneity model (Equation 1).
    
    Returns:
    - energies: array of node initial energies
    - types: 0 for normal, 1 for high-energy nodes
    """
    energies = np.zeros(NUM_NODES)
    types = np.zeros(NUM_NODES)  # 0 = normal, 1 = high-energy

    Nh = int(h * NUM_NODES)  # Number of high-energy nodes
    node_indices = np.random.permutation(NUM_NODES)

    high_energy_nodes = node_indices[:Nh]
    normal_energy_nodes = node_indices[Nh:]

    # Assign initial energies based on type
    energies[high_energy_nodes] = Eo * (1 + alpha)
    types[high_energy_nodes] = 1  # High-energy
    energies[normal_energy_nodes] = Eo
    types[normal_energy_nodes] = 0  # Normal-energy

    return energies, types
