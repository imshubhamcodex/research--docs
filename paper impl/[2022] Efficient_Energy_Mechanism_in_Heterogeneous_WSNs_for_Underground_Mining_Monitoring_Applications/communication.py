import numpy as np
from config import *

def transmit(positions, energies, CH_indices, CM_indices, cluster_assignments):
    """
    Simulates the communication phase for one round.
    Cluster Members (CMs) send data to their Cluster Heads (CHs),
    and CHs forward aggregated data to the sink.
    """
    packets = 0
    do = np.sqrt(Efs / Emp)  # Crossover distance between free-space and multipath models

    # Communication: CM to CH (or directly to sink if unassigned)
    for cm in CM_indices:
        if cluster_assignments[cm] == -1:
            # No CH available, transmit directly to sink
            d = np.linalg.norm(positions[cm] - SINK_POS)
            ETx = packet_size * (Eelec + (Efs * d**2 if d < do else Emp * d**4))
            energies[cm] -= ETx
        else:
            ch = cluster_assignments[cm]
            # Transmit to assigned CH
            d = np.linalg.norm(positions[cm] - positions[ch])
            ETx = packet_size * (Eelec + (Efs * d**2 if d < do else Emp * d**4))
            energies[cm] -= ETx

            # CH receives and aggregates data
            ERx = packet_size * Eelec
            Eagg = packet_size * EDA
            energies[ch] -= (ERx + Eagg)
        
        packets += 1

    # Communication: CH to Sink
    for ch in CH_indices:
        d = np.linalg.norm(positions[ch] - SINK_POS)
        ETx = packet_size * (Eelec + (Efs * d**2 if d < do else Emp * d**4))
        energies[ch] -= ETx
        packets += 1

    return energies, packets
