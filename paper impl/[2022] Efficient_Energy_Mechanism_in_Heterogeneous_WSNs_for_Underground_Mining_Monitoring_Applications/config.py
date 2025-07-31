# Network Area and Setup
AREA = 200
NUM_NODES = 200
ROUNDS = 12000
SINK_POS = (AREA / 2, AREA / 2)  # Sink at center

# === Energy Model Parameters (from Table 3) ===
Eo = 0.5           # Initial energy for normal nodes
alpha = 1.5        # High-energy node boost factor → Eq. (1), (3)
h = 0.5            # Fraction of high-energy nodes → Eq. (1), (3)
beta = 3.0         # Super-energy node boost → Eq. (3)
S = 0.4            # Fraction of super-energy nodes → Eq. (3)

Eelec = 50e-9      # Electronics energy (per bit)
EDA = 5e-9         # Aggregation energy (per bit)
Efs = 10e-12       # Free space model energy (d^2) for short range
Emp = 0.0013e-12   # Multipath model energy (d^4) for long range

packet_size = 3000  # bits per message

# Optimal probability of CH election (used in DEECP + Proposed) → Eq. (5), (11)
p_opt = 0.01

# Notes:
# - Total energy (Eq. 2 / Eq. 4) calculated in main simulation.
# - Energy models switch at distance threshold: do = sqrt(Efs / Emp)

# NUM_NODES, p_opt  50 , 100, 150, 200 :: 0.21,  0.05, 0.02, 0.01 :)
