# 💡 Energy-Efficient Routing in Wireless Sensor Networks (WSNs)

## Protocols Compared

- 🟦 **Baseline DEECP** — *Distributed Energy-Efficient Clustering Protocol*
- 🟥 **Proposed Method** — *Enhanced DEECP with Three-Level Node Heterogeneity and Distance-Aware CH Selection*

This Python-based simulation compares two clustering protocols for WSNs used in underground mining or similar harsh environments. It evaluates their energy efficiency and network lifetime across multiple node configurations.

---

## 📊 Simulated Performance Metrics

Each protocol is evaluated based on:

- 📉 **Dead Nodes vs Rounds**
- 📈 **Alive Nodes vs Rounds**
- 📡 **Network Throughput (bits over time)**
- 🧱 **Network Lifetime (Bar chart of last node death)**

---

## ⚙️ Parameters — `config.py`

```python
AREA = 200              # Area dimensions (200x200 meters)
NUM_NODES = 50          # Number of sensor nodes (auto-updated)
ROUNDS = 12000          # Total simulation rounds
SINK_POS = (100, 100)   # Central base station position

Eo = 0.5                # Initial energy of normal nodes
alpha = 1.5             # Extra energy factor for high-energy nodes
h = 0.5                 # Fraction of high-energy nodes
beta = 3.0              # Super node energy factor
S = 0.4                 # Fraction of super nodes among high-energy nodes

packet_size = 3000      # Data packet size in bits
p_opt = 0.21            # CH selection probability (auto-updated during multi-config runs)
```

---

## 📁 Project Structure

```
project/
├── config.py                  # Global simulation parameters
├── index.py                   # Entry point for a single simulation run
├── simulate_all_configs.py    # Runs multiple simulations for various node counts
├── deecp/                     # Baseline DEECP components
│   ├── init_nodes.py          # Two-level node energy initialization
│   └── ch_selection.py        # CH selection logic (energy-based)
├── e_deecp/                   # Proposed method components
│   ├── init_nodes.py          # Three-level node initialization (normal, high, super)
│   └── ch_selection.py        # CH selection (energy + distance aware)
├── clustering.py              # Forms clusters from CHs and CMs
├── communication.py           # Simulates energy consumption during data transmission
└── README.md                  # Project documentation (this file)
```

---

## 🧪 Experimental Setup

- The `simulate_all_configs.py` script runs simulations for:

  | Nodes | `p_opt` |
  |-------|---------|
  | 50    | 0.21    |
  | 100   | 0.05    |
  | 150   | 0.02    |
  | 200   | 0.01    |

- These values replicate the experimental setup from the reference paper to ensure a fair comparison of DEECP and the Proposed Method.

---
---

## 📌 Citation

If this simulation helps your research or work, consider citing the original paper:

> *"Efficient Energy Mechanism in Heterogeneous WSNs for Underground Mining Monitoring Applications" (2022)*

---
