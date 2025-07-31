import numpy as np
from q_learn_deecp.q_learning_agent import QLearningNodeAgent
from config import *

# Initialize one Q-agent per node
agents = []
last_actions = []
last_states = []

def init_agents(num_nodes):
    global agents, last_actions, last_states
    agents = [QLearningNodeAgent() for _ in range(num_nodes)]
    last_actions = [0 for _ in range(num_nodes)]
    last_states = [0 for _ in range(num_nodes)]

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val + 1e-9)

def select_CHs_q_learning(positions, energies, alive, E_total, round_num, agents, last_states, last_actions):
    num_nodes = len(energies)
    is_CH = np.zeros(num_nodes, dtype=bool)
    for i in range(num_nodes):
        if not alive[i]:
            continue

        energy_norm = normalize(energies[i], 0, Eo * (1 + beta))  # Normalize energy
        dist_to_sink = np.linalg.norm(positions[i] - np.array(SINK_POS))
        dist_norm = normalize(dist_to_sink, 0, np.sqrt(AREA**2 + AREA**2))  # Normalize

        state_idx = agents[i].get_state_index(energy_norm, dist_norm, round_num)
        action = agents[i].choose_action(state_idx)

        # Store for later reward update
        last_states[i] = state_idx
        last_actions[i] = action

        if action == 1:
            is_CH[i] = True

    return is_CH
