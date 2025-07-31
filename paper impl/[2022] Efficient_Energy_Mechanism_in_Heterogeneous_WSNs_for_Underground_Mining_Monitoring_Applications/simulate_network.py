import matplotlib.pyplot as plt
import importlib
import sys
import numpy as np

# --- Step 1: Dynamically update configuration file (config.py) with node count and optimal p ---
def update_config_file(num_nodes, p_opt):
    """
    Update NUM_NODES and p_opt values in the config.py file.
    """
    with open("config.py", "r") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if line.strip().startswith("NUM_NODES"):
            updated_lines.append(f"NUM_NODES = {num_nodes}\n")
        elif line.strip().startswith("p_opt"):
            updated_lines.append(f"p_opt = {p_opt}\n")
        else:
            updated_lines.append(line)

    with open("config.py", "w") as f:
        f.writelines(updated_lines)

# --- Step 2: Reload simulation environment after configuration changes ---
def reload_simulation_env():
    """
    Reload all simulation-related modules to reflect updated configuration.
    """
    for mod in [
        "config",
        "index",
        "deecp.init_nodes",
        "e_deecp.init_nodes",
        "deecp.ch_selection",
        "e_deecp.ch_selection",
        "clustering",
        "communication",
        "q_learn_deecp.q_learning_ch_selection",
        "q_learn_deecp.q_learning_agent"
    ]:
        if mod in sys.modules:
            importlib.reload(sys.modules[mod])
    from index import simulate
    return simulate

# --- Step 3: Define test configurations (num_nodes, p_opt) ---
configs = [
    (50, 0.21),
    (100, 0.05),
    (150, 0.02),
    (200, 0.01),
]

results = {}  # Store results for all configurations

print("\nSimulation Summary:\n")

# --- Step 4: Run simulations for all configurations and store results ---
for N, p in configs:
    update_config_file(N, p)
    simulate = reload_simulation_env()

    print(f"Running for NUM_NODES={N}")

    dead_b, alive_b, th_b = simulate(method="baseline")
    dead_p, alive_p, th_p = simulate(method="proposed")
    dead_q, alive_q, th_q = simulate(method="q_learning")

    results[N] = {
        "baseline": {"dead": dead_b, "alive": alive_b, "throughput": th_b},
        "proposed": {"dead": dead_p, "alive": alive_p, "throughput": th_p},
        "q_learning": {"dead": dead_q, "alive": alive_q, "throughput": th_q}
    }

    # --- Compute lifetime metrics ---
    last_b = next((i for i, x in enumerate(dead_b) if x == N), -1)
    last_p = next((i for i, x in enumerate(dead_p) if x == N), -1)
    last_q = next((i for i, x in enumerate(dead_q) if x == N), -1)

    first_b = next((i for i, x in enumerate(dead_b) if x >= 1), -1)
    first_p = next((i for i, x in enumerate(dead_p) if x >= 1), -1)
    first_q = next((i for i, x in enumerate(dead_q) if x >= 1), -1)

    print(f"  Baseline       - First node died at round: {first_b}, Last node died at round: {last_b}")
    print(f"  Proposed       - First node died at round: {first_p}, Last node died at round: {last_p}")
    print(f"  Q_learning     - First node died at round: {first_q}, Last node died at round: {last_q}\n")

# --- Step 5: Plot for NUM_NODES = 50 (matching Figures 9–11) ---
if 50 in results:
    res = results[50]

    # --- Figure 9: Dead Nodes ---
    plt.figure(figsize=(8, 5))
    plt.plot(res["baseline"]["dead"], label="Baseline DEECP", linestyle="--", color='blue')
    plt.plot(res["proposed"]["dead"], label="Proposed Method", linestyle="--", color='red')
    plt.plot(res["q_learning"]["dead"], label="Q-Learning Method", linestyle="--", color='green')
    plt.title("Figure 9: Dead Nodes During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Dead Nodes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Figure 10: Alive Nodes ---
    plt.figure(figsize=(8, 5))
    plt.plot(res["baseline"]["alive"], label="Baseline DEECP", linestyle="--", color='blue')
    plt.plot(res["proposed"]["alive"], label="Proposed Method", linestyle="--", color='red')
    plt.plot(res["q_learning"]["alive"], label="Q-Learning Method", linestyle="--", color='green')
    plt.title("Figure 10: Alive Nodes During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Alive Nodes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Figure 11: Throughput ---
    plt.figure(figsize=(8, 5))
    plt.plot(res["baseline"]["throughput"], label='Baseline DEECP', linestyle='--', color='purple')
    plt.plot(res["proposed"]["throughput"], label='Proposed Method', linestyle='--', color='orange')
    plt.plot(res["q_learning"]["throughput"], label='Q-Learning Method', linestyle='--', color='teal')
    plt.title("Figure 11: Throughput During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Network Throughput (bits)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- Step 6: Comparison Plots Across All Configs ---
# Dead Nodes vs Rounds
plt.figure(figsize=(11, 5))
for N, _ in configs:
    plt.plot(results[N]["baseline"]["dead"], linestyle="--", label=f"Baseline N={N}")
    plt.plot(results[N]["proposed"]["dead"], label=f"Proposed N={N}")
    plt.plot(results[N]["q_learning"]["dead"], linestyle="-.", label=f"Q-Learning N={N}")
plt.title("Dead Nodes During Network Operation")
plt.xlabel("Simulation Duration (sec)")
plt.ylabel("Number of Dead Nodes")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Alive Nodes vs Rounds
plt.figure(figsize=(11, 5))
for N, _ in configs:
    plt.plot(results[N]["baseline"]["alive"], linestyle="--", label=f"Baseline N={N}")
    plt.plot(results[N]["proposed"]["alive"], label=f"Proposed N={N}")
    plt.plot(results[N]["q_learning"]["alive"], linestyle="-.", label=f"Q-Learning N={N}")
plt.title("Alive Nodes During Network Operation")
plt.xlabel("Simulation Duration (sec)")
plt.ylabel("Number of Alive Nodes")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Step 7: Bar Chart - Last Node Dead Round (Lifetime) ---
labels = [str(N) for N, _ in configs]
x = np.arange(len(labels))
width = 0.25

baseline_lifetimes = [next((i for i, x in enumerate(results[N]["baseline"]["dead"]) if x == N), -1) for N, _ in configs]
proposed_lifetimes = [next((i for i, x in enumerate(results[N]["proposed"]["dead"]) if x == N), -1) for N, _ in configs]
q_learning_lifetimes = [next((i for i, x in enumerate(results[N]["q_learning"]["dead"]) if x == N), -1) for N, _ in configs]

plt.figure(figsize=(10, 6))
plt.bar(x - width, baseline_lifetimes, width, label='DEECP Baseline', color='steelblue')
plt.bar(x, proposed_lifetimes, width, label='Proposed Method', color='orange')
plt.bar(x + width, q_learning_lifetimes, width, label='Q-Learning Method', color='green')

plt.xlabel("Number of Nodes")
plt.ylabel("Last Node Dead Round")
plt.title("Network Lifetime vs Number of Nodes")
plt.xticks(x, labels)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
