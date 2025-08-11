import matplotlib.pyplot as plt
import importlib
import sys
import numpy as np

from utils import print_node_death_comparison

# ------------------------------
# Step 1: Update Configuration
# ------------------------------
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


# ------------------------------
# Step 2: Reload Simulation Modules
# ------------------------------
def reload_simulation_env():
    """
    Reload all relevant modules to reflect configuration changes.
    """
    modules_to_reload = [
        "config",
        "index",
        "deecp.init_nodes",
        "e_deecp.init_nodes",
        "deecp.ch_selection",
        "e_deecp.ch_selection",
        "clustering",
        "communication",
        "q_learn_deecp.q_learning_ch_selection",
        "q_learn_deecp.q_learning_agent",
    ]

    for mod in modules_to_reload:
        if mod in sys.modules:
            importlib.reload(sys.modules[mod])

    from index import simulate
    return simulate


# ------------------------------
# Step 3: Simulation Configuration
# ------------------------------
configs = [
    (50, 0.21),
    (100, 0.05),
    (150, 0.02),
    # (200, 0.01),
]

results = {}

# ------------------------------
# Step 4: Run Simulations
# ------------------------------
print(f"\nSimulation Started")
for N, p in configs:
    update_config_file(N, p)
    simulate = reload_simulation_env()

    print(f"\nRunning for NUM_NODES={N}")

    dead_b, alive_b, th_b = simulate(method="baseline")
    dead_p, alive_p, th_p = simulate(method="proposed")
    dead_q, alive_q, th_q = simulate(method="q_learning")

    results[N] = {
        "baseline": {"dead": dead_b, "alive": alive_b, "throughput": th_b},
        "proposed": {"dead": dead_p, "alive": alive_p, "throughput": th_p},
        "q_learning": {"dead": dead_q, "alive": alive_q, "throughput": th_q},
    }

    baseline_death_rounds = [i for i, d in enumerate(dead_b) if d > 0 and (i == 0 or dead_b[i - 1] != d)]
    proposed_death_rounds = [i for i, d in enumerate(dead_p) if d > 0 and (i == 0 or dead_p[i - 1] != d)]
    q_learning_death_rounds = [i for i, d in enumerate(dead_q) if d > 0 and (i == 0 or dead_q[i - 1] != d)]

    print_node_death_comparison(baseline_death_rounds, proposed_death_rounds, q_learning_death_rounds)

print(f"\nSimulation Completed")
# ------------------------------
# Step 5: Plots for 50 Nodes
# ------------------------------
if 50 in results:
    res = results[50]

    # Dead Nodes
    plt.figure(figsize=(8, 5))
    plt.plot(res["baseline"]["dead"], label="Baseline DEECP", linestyle="--", color='blue')
    plt.plot(res["proposed"]["dead"], label="Enhanced DEECP", linestyle="--", color='red')
    plt.plot(res["q_learning"]["dead"], label="Q-Learning DEECP", linestyle="--", color='green')
    plt.title("Dead Nodes During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Dead Nodes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Alive Nodes
    plt.figure(figsize=(8, 5))
    plt.plot(res["baseline"]["alive"], label="Baseline DEECP", linestyle="--", color='blue')
    plt.plot(res["proposed"]["alive"], label="Enhanced DEECP", linestyle="--", color='red')
    plt.plot(res["q_learning"]["alive"], label="Q-Learning DEECP", linestyle="--", color='green')
    plt.title("Alive Nodes During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Number of Alive Nodes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Throughput
    plt.figure(figsize=(8, 5))
    plt.plot(res["baseline"]["throughput"], label='Baseline DEECP', linestyle='--', color='purple')
    plt.plot(res["proposed"]["throughput"], label='Enhanced DEECP', linestyle='--', color='orange')
    plt.plot(res["q_learning"]["throughput"], label='Q-Learning DEECP', linestyle='--', color='teal')
    plt.title("Throughput During Network Operation Time")
    plt.xlabel("Simulation Duration (sec)")
    plt.ylabel("Network Throughput (bits)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------
# Step 6: Comparison Across Configurations
# ------------------------------
plt.figure(figsize=(11, 5))
for N, _ in configs:
    plt.plot(results[N]["baseline"]["dead"], linestyle="--", label=f"Baseline DEECP N={N}")
    plt.plot(results[N]["proposed"]["dead"], label=f"Enhanced DEECP N={N}")
    plt.plot(results[N]["q_learning"]["dead"], linestyle="-.", label=f"Q-Learning DEECP N={N}")
plt.title("Dead Nodes During Network Operation")
plt.xlabel("Simulation Duration (sec)")
plt.ylabel("Number of Dead Nodes")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(11, 5))
for N, _ in configs:
    plt.plot(results[N]["baseline"]["alive"], linestyle="--", label=f"Baseline DEECP N={N}")
    plt.plot(results[N]["proposed"]["alive"], label=f"Enhanced DEECP N={N}")
    plt.plot(results[N]["q_learning"]["alive"], linestyle="-.", label=f"Q-Learning DEECP N={N}")
plt.title("Alive Nodes During Network Operation")
plt.xlabel("Simulation Duration (sec)")
plt.ylabel("Number of Alive Nodes")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------
# Step 7: Lifetime Comparison
# ------------------------------
labels = [str(N) for N, _ in configs]
x = np.arange(len(labels))
width = 0.25

baseline_lifetimes = [next((i for i, x in enumerate(results[N]["baseline"]["dead"]) if x == N), -1) for N, _ in configs]
proposed_lifetimes = [next((i for i, x in enumerate(results[N]["proposed"]["dead"]) if x == N), -1) for N, _ in configs]
q_learning_lifetimes = [next((i for i, x in enumerate(results[N]["q_learning"]["dead"]) if x == N), -1) for N, _ in configs]

plt.figure(figsize=(10, 6))
plt.bar(x - width, baseline_lifetimes, width, label='Baseline DEECP', color='steelblue')
plt.bar(x, proposed_lifetimes, width, label='Enhanced DEECP', color='orange')
plt.bar(x + width, q_learning_lifetimes, width, label='Q-Learning DEECP', color='green')

plt.xlabel("Number of Nodes")
plt.ylabel("Last Node Dead Round")
plt.title("Network Lifetime vs Number of Nodes")
plt.xticks(x, labels)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
