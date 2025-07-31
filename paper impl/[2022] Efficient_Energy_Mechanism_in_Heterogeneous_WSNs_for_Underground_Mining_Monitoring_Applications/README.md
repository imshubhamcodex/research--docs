# 💡 Energy-Efficient Routing in Wireless Sensor Networks (WSNs)

## 🔄 Protocols Compared

- 🟦 **Baseline DEECP** — *Distributed Energy-Efficient Clustering Protocol*
- 🟥 **Proposed Method** — *Enhanced DEECP with Three-Level Node Heterogeneity and Distance-Aware CH Selection*
- 🟩 **Q-Learning Enhanced DEECP (Future Scope)** — *Reinforcement Learning-based Cluster Head Selection with Energy and Distance Awareness*

This Python-based simulation compares three clustering protocols for WSNs used in underground mining or other energy-constrained environments. It evaluates their energy efficiency and network longevity across varying node deployments.

---

## 📊 Simulated Performance Metrics

Each protocol is evaluated based on:

- 📉 **Dead Nodes vs Rounds**
- 📈 **Alive Nodes vs Rounds**
- 📡 **Network Throughput (bits transmitted over time)**
- 🧱 **Network Lifetime (Bar chart of last node death across configurations)**

---

## ⚙️ Parameters — `config.py`

```python
AREA = 200              # Area dimensions (200x200 meters)
NUM_NODES = 50          # Number of sensor nodes (auto-updated per run)
ROUNDS = 12000          # Total simulation rounds
SINK_POS = (100, 100)   # Base station at center of field

Eo = 0.5                # Initial energy of normal nodes
alpha = 1.5             # Extra energy for high-energy nodes
h = 0.5                 # Fraction of high-energy nodes
beta = 3.0              # Super node energy multiplier
S = 0.4                 # Fraction of super nodes among high-energy nodes

packet_size = 3000      # Data packet size in bits
p_opt = 0.21            # Optimal CH probability (adjusted dynamically)
```

---

## 🧠 Q-Learning Highlights (New)

- ✨ Each node is equipped with an independent **QLearningNodeAgent**
- 🔄 Learns from experience using rewards based on:
  - Remaining energy
  - Role survival (CH survival or failure)
  - Distance to sink
- 📉 **Epsilon decay** added for improved exploration early and exploitation later
- 📈 Reward function tuned to encourage:
  - High-energy nodes to become CH
  - Penalize early node death
  - Balance throughput and energy saving

---

## 📁 Project Structure

```
project/
├── config.py                  # Global simulation parameters
├── index.py                   # Main simulator (runs one round of each method)
├── simulate_network.py    # Multi-config batch simulation and plotting
├── deecp/                     # Baseline DEECP components
│   ├── init_nodes.py          # Two-level node initialization
│   └── ch_selection.py        # Energy-based CH selection
├── e_deecp/                   # Proposed method components
│   ├── init_nodes.py          # Three-level node initialization
│   └── ch_selection.py        # Energy + distance-based CH selection
├── q_learn_deecp/                   # Q-learning components
│   ├── q_learning_agent.py    # Q-learning agent class with epsilon decay
│   └── q_learning_ch_selection.py  # CH selection using learned Q-values
├── clustering.py              # Cluster formation from CHs and members
├── communication.py           # Energy-aware communication phase
└── README.md                  # This documentation file
```

---

## 🧪 Experimental Setup

- The `simulate_all_configs.py` script evaluates performance across:

  | Nodes | `p_opt` |
  |-------|---------|
  | 50    | 0.21    |
  | 100   | 0.05    |
  | 150   | 0.02    |
  | 200   | 0.01    |

- These settings replicate the experimental setup from the original DEECP paper.
- Random seed is reset before each simulation for **result reproducibility**.

---

## 📉 Sample Output (Summary)

```text
Simulation Summary:

Running for NUM_NODES=50
  Baseline       - First node died at round: 1203, Last node died at round: 3842
  Proposed       - First node died at round: 315, Last node died at round: 9705
  Q_learning     - First node died at round: 496, Last node died at round: 10587

Running for NUM_NODES=100
  Baseline       - First node died at round: 1151, Last node died at round: 3123
  Proposed       - First node died at round: 331, Last node died at round: 10156
  Q_learning     - First node died at round: 487, Last node died at round: 11186

Running for NUM_NODES=150
  Baseline       - First node died at round: 1011, Last node died at round: 3407
  Proposed       - First node died at round: 340, Last node died at round: 10452
  Q_learning     - First node died at round: 464, Last node died at round: 11417

Running for NUM_NODES=200
  Baseline       - First node died at round: 836, Last node died at round: 3713
  Proposed       - First node died at round: 347, Last node died at round: 11021
  Q_learning     - First node died at round: 455, Last node died at round: 11127
```

---

## 📌 Citation

If this simulation or methodology helps your research or publication, please consider citing the original work:

> *"Efficient Energy Mechanism in Heterogeneous WSNs for Underground Mining Monitoring Applications" (2022)*

---

## 🙋 Contribution

Feel free to fork, modify, or extend this project for:

- Fuzzy logic CH selection
- Deep Q-Learning (DQN)
- Mobile sink optimization
- Multi-hop routing enhancements

---