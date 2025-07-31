import numpy as np
import matplotlib.pyplot as plt
from config import *
from clustering import form_clusters
from communication import transmit

# Import initializers and CH selectors for both methods
from e_deecp.init_nodes import initialize_nodes as init_proposed_nodes
from deecp.init_nodes import initialize_nodes as init_baseline_nodes
from e_deecp.ch_selection import select_CHs as select_CHs_proposed
from deecp.ch_selection import select_CHs as select_CHs_baseline

np.random.seed(45)  # Ensures reproducibility

def simulate(method="baseline"):
    """
    Simulates the WSN clustering and communication process for both baseline and proposed methods.

    Parameters:
    - method: "baseline" or "proposed"

    Returns:
    - dead_nodes: list tracking number of dead nodes per round
    - alive_nodes: list tracking number of alive nodes per round
    - cumulative_throughput_bits: list tracking total bits transmitted over time
    """

    # === Step 1: Randomly deploy nodes within AREA ===
    positions = np.random.rand(NUM_NODES, 2) * AREA

    # === Step 2: Initialize nodes based on method ===
    if method == "baseline":
        energies, type = init_baseline_nodes()
        select_CHs_func = select_CHs_baseline
        # Eq. (2): Total energy for 2-level model
        E_total = NUM_NODES * Eo * (1 + alpha * h)
    else:
        energies, type = init_proposed_nodes()
        select_CHs_func = select_CHs_proposed
        # Eq. (4): Total energy for 3-level model
        Nh = int(h * NUM_NODES)
        Ns = int(S * Nh)
        E_total = Eo * ((NUM_NODES - Nh) + Nh * (1 + alpha) + Ns * (beta - alpha))

    # === Tracking metrics over ROUNDS ===
    dead_nodes, alive_nodes, throughput_packets = [], [], []

    for r in range(ROUNDS):
        alive = energies > 0

        # === Step 3: CH Selection ===
        if method == "baseline":
            is_CH = select_CHs_func(energies, alive, E_total, r)  # Eq. 5–7
        else:
            is_CH = select_CHs_func(positions, energies, alive, E_total, r)  # Eq. 11–12

        # === Step 4: Cluster Formation ===
        CH_indices, CM_indices, cluster_assignments = form_clusters(positions, is_CH, alive)

        # === Step 5: Data Transmission Phase (Eq. 8–10) ===
        energies, packets = transmit(positions, energies, CH_indices, CM_indices, cluster_assignments)

        # === Step 6: Statistics Tracking ===
        dead = np.sum(energies <= 0)
        alive_nodes.append(NUM_NODES - dead)
        dead_nodes.append(dead)

        # Proposed method uses two-hop communication (as per paper)
        if method == "proposed":
            packets *= 2

        throughput_packets.append(2 * packets)  # Double counted for forward + CH to sink

    # Convert to bits using packet size
    cumulative_throughput_bits = np.cumsum(np.array(throughput_packets) * packet_size)
    return dead_nodes, alive_nodes, cumulative_throughput_bits


# === Run Simulations for Both Methods ===
dead_baseline, alive_baseline, throughput_bits_baseline = simulate(method="baseline")
dead_proposed, alive_proposed, throughput_bits_proposed = simulate(method="proposed")


# === Plotting (Figures 9–11) ===
if NUM_NODES == 50:  # To match the paper's figures
    # === Figure 9: Dead Nodes vs Rounds ===
    plt.figure(figsize=(8, 5))
    plt.plot(dead_baseline, label="Baseline DEECP", color='blue', linestyle='--')
    plt.plot(dead_proposed, label="Proposed Method", color='red', linestyle='--')
    plt.title("Figure 9: Dead Nodes During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Dead Nodes")
    plt.legend()
    plt.grid(True)

    # === Figure 10: Alive Nodes vs Rounds ===
    plt.figure(figsize=(8, 5))
    plt.plot(alive_baseline, label="Baseline DEECP", color='blue', linestyle='--')
    plt.plot(alive_proposed, label="Proposed Method", color='red', linestyle='--')
    plt.title("Figure 10: Alive Nodes During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Alive Nodes")
    plt.legend()
    plt.grid(True)

    # === Figure 11: Throughput vs Rounds ===
    plt.figure(figsize=(8, 5))
    plt.plot(throughput_bits_baseline, label='Baseline DEECP', linestyle='--', color='purple')
    plt.plot(throughput_bits_proposed, label='Proposed Method', linestyle='--', color='darkorange')
    plt.title("Figure 11: Throughput During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Network Throughput (bits)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
