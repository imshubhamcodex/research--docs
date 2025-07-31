import numpy as np
from config import *

def transmit(positions, energies, CH_indices, CM_indices, cluster_assignments):
    """
    Simulates one communication round:
    - CMs send data to CHs
    - CHs aggregate and send data to sink

    Based on:
        Eq. (8) ETx = k * (Eelec + Efs*d^2) or k * (Eelec + Emp*d^4)
        Eq. (9) ECM = Einit + ETx
        Eq. (10) ECH = Einit + Estd (ERx + EDA + ETx to sink)

    Parameters:
    - positions: (N,2) node coordinates
    - energies: array of node energies
    - CH_indices: list of current cluster heads
    - CM_indices: list of cluster members
    - cluster_assignments: mapping from CM to CH index

    Returns:
    - Updated energies
    - Packet count for throughput tracking
    """
    packets = 0
    do = np.sqrt(Efs / Emp)  # Threshold distance (crossover for model selection)

    # CM to CH communication
    for cm in CM_indices:
        if cluster_assignments[cm] == -1:
            # No CH → direct to sink
            d = np.linalg.norm(positions[cm] - SINK_POS)
            ETx = packet_size * (Eelec + (Efs * d**2 if d < do else Emp * d**4))
            energies[cm] -= ETx
        else:
            # CM → CH
            ch = cluster_assignments[cm]
            d = np.linalg.norm(positions[cm] - positions[ch])
            ETx = packet_size * (Eelec + (Efs * d**2 if d < do else Emp * d**4))
            energies[cm] -= ETx

            # CH receives + aggregates data
            ERx = packet_size * Eelec
            Eagg = packet_size * EDA
            energies[ch] -= (ERx + Eagg)

        packets += 1

    # CH to sink transmission
    for ch in CH_indices:
        d = np.linalg.norm(positions[ch] - SINK_POS)
        ETx = packet_size * (Eelec + (Efs * d**2 if d < do else Emp * d**4))
        energies[ch] -= ETx
        packets += 1

    return energies, packets
