# Energy-Efficient Routing in Wireless Sensor Networks using DEECP and Proposed Method

This project simulates and compares two energy-efficient clustering protocols for Wireless Sensor Networks (WSNs):

- **Baseline DEECP** (Distributed Energy Efficient Clustering Protocol)
- **Proposed Method** (Enhanced DEECP)

Simulations are implemented in Python and visualize:
- Dead Nodes vs Rounds
- Alive Nodes vs Rounds
- Network Throughput
- Lifetime Comparison (Bar chart)

---

## ⚙️ Parameters in `config.py`

```python
AREA = 200              # Field dimensions (200x200 meters)
NUM_NODES = 50          # Number of nodes (modifiable)
ROUNDS = 12000          # Total simulation rounds
SINK_POS = (100, 100)   # Central sink location

Eo = 0.5                # Initial energy of normal nodes
alpha = 1.5             # Energy factor for high-energy nodes
h = 0.5                 # Fraction of high-energy nodes
beta = 3.0              # Super-energy node factor
S = 0.4                 # Fraction of super-energy nodes

packet_size = 3000      # Size in bits
p_opt = 0.21            # CH selection probability (auto-updated)
```
project/
├── config.py                  # Global parameters (e.g. NUM_NODES, p_opt)
├── index.py                  # Main simulation script
├── simulate_all_configs.py   # Auto-simulates all node configs
├── deecp/
│   ├
│   ├── init_nodes.py         # Node initialization for DEECP
│   └── ch_selection.py       # CH selection logic for DEECP
├── e_deecp/
│   ├
│   ├── init_nodes.py         # Node init for Proposed Method
│   └── ch_selection.py       # CH selection for Proposed Method
├── clustering.py             # Cluster formation logic
├── communication.py          # Data transmission & energy update logic
└── README.md                 # This file
