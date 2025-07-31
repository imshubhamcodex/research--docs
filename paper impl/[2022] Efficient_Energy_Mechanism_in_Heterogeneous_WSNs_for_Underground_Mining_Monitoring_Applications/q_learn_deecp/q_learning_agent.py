import numpy as np

class QLearningNodeAgent:
    def __init__(self, num_states=27, num_actions=2, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate

        self.q_table = np.zeros((num_states, num_actions))

    def get_state_index(self, energy_level, dist_to_sink, round_phase):
        """
        Converts discretized features into a unique state index [0–26]
        """
        energy_idx = min(int(energy_level * 3), 2)  # 0=low, 1=med, 2=high
        dist_idx = min(int(dist_to_sink * 3), 2)     # 0=near, 1=med, 2=far
        round_idx = round_phase % 3                  # 0=early, 1=mid, 2=late

        return energy_idx * 9 + dist_idx * 3 + round_idx

    def choose_action(self, state_idx):
        """
        ε-greedy policy to choose an action (0: not CH, 1: become CH)
        """
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[state_idx])

    def update_q(self, state_idx, action, reward, next_state_idx):
        """
        Q-learning update rule
        """
        best_next = np.max(self.q_table[next_state_idx])
        td_target = reward + self.gamma * best_next
        td_error = td_target - self.q_table[state_idx][action]

        self.q_table[state_idx][action] += self.alpha * td_error
