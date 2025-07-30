import numpy as np
import matplotlib.pyplot as plt
from config import *
from clustering import form_clusters
from communication import transmit

from e_deecp.init_nodes import initialize_nodes as init_proposed_nodes
from deecp.init_nodes import initialize_nodes as init_baseline_nodes
from e_deecp.ch_selection import select_CHs as select_CHs_proposed
from deecp.ch_selection import select_CHs as select_CHs_baseline

np.random.seed(45) # 45, 48


def simulate(method="baseline"):
    # Generate random node positions within the AREA
    positions = np.random.rand(NUM_NODES, 2) * AREA

    # Initialize energy and CH selection logic
    if method == "baseline":
        energies, type = init_baseline_nodes()
        select_CHs_func = select_CHs_baseline
        E_total = NUM_NODES * Eo * (1 + alpha * h)
    else:
        energies, type = init_proposed_nodes()
        select_CHs_func = select_CHs_proposed
        Nh = int(h * NUM_NODES)
        Ns = int(S * Nh)
        E_total = Eo * ((NUM_NODES - Nh) + Nh * (1 + alpha) + Ns * (beta - alpha))

    dead_nodes, alive_nodes, throughput_packets = [], [], []

    for r in range(ROUNDS):
        alive = energies > 0

        if method == "baseline":
            is_CH = select_CHs_func(energies, alive, E_total, r)
        else:
            is_CH = select_CHs_func(positions, energies, alive, E_total, r)

        CH_indices, CM_indices, cluster_assignments = form_clusters(positions, is_CH, alive)
        energies, packets = transmit(positions, energies, CH_indices, CM_indices, cluster_assignments)

        dead = np.sum(energies <= 0)
        alive_nodes.append(NUM_NODES - dead)
        dead_nodes.append(dead)

        if method == "proposed":
            packets *= 2 # Two hopping in proposed method

        throughput_packets.append(2*packets)

    cumulative_throughput_bits = np.cumsum(np.array(throughput_packets) * packet_size)
    return dead_nodes, alive_nodes, cumulative_throughput_bits


# Run both simulations
dead_baseline, alive_baseline, throughput_bits_baseline = simulate(method="baseline")
dead_proposed, alive_proposed, throughput_bits_proposed = simulate(method="proposed")


# Plotting
if NUM_NODES == 50:
    plt.figure(figsize=(8, 5))
    plt.plot(dead_baseline, label="Baseline DEECP", color='blue', linestyle='--')
    plt.plot(dead_proposed, label="Proposed Method", color='red', linestyle='--')
    plt.title("Figure 9: Dead Nodes vs Rounds")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Dead Nodes")
    plt.legend()
    plt.grid(True)

    plt.figure(figsize=(8, 5))
    plt.plot(alive_baseline, label="Baseline DEECP", color='blue', linestyle='--')
    plt.plot(alive_proposed, label="Proposed Method", color='red', linestyle='--')
    plt.title("Figure 10: Alive Nodes vs Rounds")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Alive Nodes")
    plt.legend()
    plt.grid(True)

    plt.figure(figsize=(8, 5))
    plt.plot(throughput_bits_baseline, label='Baseline DEECP', linestyle='--', color='purple')
    plt.plot(throughput_bits_proposed, label='Proposed Method', linestyle='--', color='darkorange')
    plt.title("Figure 11: Network Throughput vs Round")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Network Throughput (bits)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
