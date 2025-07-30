
AREA = 200
NUM_NODES = 200
ROUNDS = 12000
SINK_POS = (AREA / 2, AREA / 2)

# Energy Model (from paper Table 3)
Eo = 0.5           # Initial energy for normal-energy nodes
alpha = 1.5        # Additional energy factor for high-energy nodes
h = 0.5            # Fraction of high-energy nodes (Nh/N)
Eelec = 50e-9      # TX/RX energy
EDA = 5e-9         # Data aggregation or compression energy
Efs = 10e-12       # Free-space model
Emp = 0.0013e-12   # Multipath model
packet_size = 3000 # Bits
p_opt = 0.01
beta = 3.0         # Additional energy factor for super-energy nodes
S = 0.4            # Fraction of super-energy nodes (NS/N)

# NUM_NODES, p_opt  50 , 100, 150, 200 :: 0.21,  0.05, 0.02, 0.01 :)
