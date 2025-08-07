import numpy as np
import matplotlib.pyplot as plt
from config import *
from clustering import form_clusters
from communication import transmit

from e_deecp.init_nodes import initialize_nodes as init_proposed_nodes
from deecp.init_nodes import initialize_nodes as init_baseline_nodes
from e_deecp.ch_selection import select_CHs as select_CHs_proposed
from deecp.ch_selection import select_CHs as select_CHs_baseline

from q_learn_deecp.q_learning_agent import QLearningNodeAgent
from q_learn_deecp.q_learning_ch_selection import normalize, select_CHs_q_learning

np.random.seed(48)  # Ensures reproducibility

def simulate(method="baseline"):
    np.random.seed(48)
    """
    Simulates the WSN clustering and communication process for baseline, proposed, or Q-learning methods.
    """
    positions = np.random.rand(NUM_NODES, 2) * AREA

    # Initialize based on method
    if method == "q_learning":
        agents = [QLearningNodeAgent() for _ in range(NUM_NODES)]
        last_actions = [0 for _ in range(NUM_NODES)]
        last_states = [0 for _ in range(NUM_NODES)]
        
        energies, types = init_proposed_nodes()
        Nh = int(h * NUM_NODES)
        Ns = int(S * Nh)
        E_total = Eo * ((NUM_NODES - Nh) + Nh * (1 + alpha) + Ns * (beta - alpha))

        def select_CHs_func(positions, energies, alive, E_total, round_num):
            return select_CHs_q_learning(
                positions, energies, alive, E_total, round_num,
                agents, last_states, last_actions
            )

    elif method == "baseline":
        energies, types = init_baseline_nodes()
        E_total = NUM_NODES * Eo * (1 + alpha * h)
        select_CHs_func = select_CHs_baseline

    else:  # proposed
        energies, types = init_proposed_nodes()
        Nh = int(h * NUM_NODES)
        Ns = int(S * Nh)
        E_total = Eo * ((NUM_NODES - Nh) + Nh * (1 + alpha) + Ns * (beta - alpha))
        select_CHs_func = select_CHs_proposed

    # Tracking
    dead_nodes, alive_nodes, throughput_packets = [], [], []

    for r in range(ROUNDS):
        alive = energies > 0

        # CH Selection
        is_CH = select_CHs_func(positions, energies, alive, E_total, r)

        # Clustering
        CH_indices, CM_indices, cluster_assignments = form_clusters(positions, is_CH, alive)

        # Communication
        energies, packets = transmit(positions, energies, CH_indices, CM_indices, cluster_assignments)

        # Q-Learning reward and update
        if method == "q_learning":
            for i in range(NUM_NODES):
                if not alive[i]:
                    continue

                is_ch = last_actions[i] == 1
                survived = energies[i] > 0
                
                energy_norm = normalize(energies[i], 0, Eo * (1 + beta))
                alive_ratio = np.sum(energies > 0) / NUM_NODES
                dist_to_sink = np.linalg.norm(positions[i] - np.array(SINK_POS))
                dist_norm = normalize(dist_to_sink, 0, np.sqrt(AREA**2 + AREA**2))

                if is_ch and survived:
                    reward = (
                        0.8 + 0.2 * energy_norm +     # High energy CH gets more reward
                        0.1 * (1 - dist_norm) +       # Prefer CHs close to sink
                        0.2 * alive_ratio             # Favor when more nodes are alive
                    )
                elif is_ch and not survived:
                    reward = -1.0                    # Strong penalty for dying CH
                elif not is_ch and survived:
                    reward = 0.1 * energy_norm + 0.1 * alive_ratio
                else:
                    reward = 0.0

                # Q-learning update
                next_state = agents[i].get_state_index(energy_norm, dist_norm, r + 1)
                agents[i].update_q(last_states[i], last_actions[i], reward, next_state)

        # Tracking stats
        dead = np.sum(energies <= 0)
        alive_nodes.append(NUM_NODES - dead)
        dead_nodes.append(dead)

        if method in ["proposed", "q_learning"]:
            packets *= 2
        throughput_packets.append(2 * packets)

    cumulative_throughput_bits = np.cumsum(np.array(throughput_packets) * packet_size)
    return dead_nodes, alive_nodes, cumulative_throughput_bits


# # === Run Simulations for All Methods ===
# dead_baseline, alive_baseline, throughput_bits_baseline = simulate(method="baseline")
# dead_proposed, alive_proposed, throughput_bits_proposed = simulate(method="proposed")
# dead_q_learning, alive_q_learning, throughput_bits_q_learning = simulate(method="q_learning")
