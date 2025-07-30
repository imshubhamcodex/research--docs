import matplotlib.pyplot as plt
import importlib
import sys
import numpy as np

# --- Dynamic config rewriter ---
def update_config_file(num_nodes, p_opt):
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

# --- Reload simulation environment ---
def reload_simulation_env():
    for mod in [
        "config",
        "index",
        "deecp.init_nodes",
        "e_deecp.init_nodes",
        "deecp.ch_selection",
        "e_deecp.ch_selection",
        "clustering",
        "communication",
    ]:
        if mod in sys.modules:
            importlib.reload(sys.modules[mod])
    from index import simulate
    return simulate

# --- Configs to test ---
configs = [
    (50, 0.21),
    (100, 0.05),
    (150, 0.02),
    (200, 0.01),
]

results = {}

print("\nSimulation Summary:\n")

for N, p in configs:
    update_config_file(N, p)
    simulate = reload_simulation_env()

    print(f"Running for NUM_NODES={N}")

    dead_b, alive_b, th_b = simulate(method="baseline")
    dead_p, alive_p, th_p = simulate(method="proposed")

    results[N] = {
        "baseline": {"dead": dead_b, "alive": alive_b, "throughput": th_b},
        "proposed": {"dead": dead_p, "alive": alive_p, "throughput": th_p},
    }

    last_b = next((i for i, x in enumerate(dead_b) if x == N), -1)
    last_p = next((i for i, x in enumerate(dead_p) if x == N), -1)

    print(f"  Baseline  DEECP - Last node died at round: {last_b}")
    print(f"  Proposed Method - Last node died at round: {last_p}\n")

# --- Plot Dead Nodes ---
plt.figure(figsize=(11, 5))
for N, _ in configs:
    plt.plot(results[N]["baseline"]["dead"], linestyle="--", label=f"Baseline N={N}")
    plt.plot(results[N]["proposed"]["dead"], label=f"Proposed N={N}")
plt.title("Dead Nodes During Network Operation")
plt.xlabel("Simulation Duration (sec)")
plt.ylabel("Dead Nodes")
plt.grid(True)
plt.legend()

# --- Plot Alive Nodes ---
plt.figure(figsize=(11, 5))
for N, _ in configs:
    plt.plot(results[N]["baseline"]["alive"], linestyle="--", label=f"Baseline N={N}")
    plt.plot(results[N]["proposed"]["alive"], label=f"Proposed N={N}")
plt.title("Alive Nodes During Network Operation")
plt.xlabel("Simulation Duration (sec)")
plt.ylabel("Alive Nodes")
plt.grid(True)
plt.legend()

# --- Bar Chart: Last node death round ---
labels = [str(N) for N, _ in configs]
baseline_lifetimes = []
proposed_lifetimes = []

for N, _ in configs:
    dead_b = results[N]["baseline"]["dead"]
    dead_p = results[N]["proposed"]["dead"]

    last_b = next((i for i, x in enumerate(dead_b) if x == N), -1)
    last_p = next((i for i, x in enumerate(dead_p) if x == N), -1)

    baseline_lifetimes.append(last_b)
    proposed_lifetimes.append(last_p)

x = np.arange(len(labels))
width = 0.2

plt.figure(figsize=(8, 5))
plt.bar(x - width / 2, baseline_lifetimes, width, label='DEECP (Baseline)', color='steelblue')
plt.bar(x + width / 2, proposed_lifetimes, width, label='Proposed Method', color='orange')
plt.xlabel('Number of Nodes')
plt.ylabel('Rounds until all nodes die')
plt.title('Network Lifetime Comparison')
plt.xticks(x, labels)
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
