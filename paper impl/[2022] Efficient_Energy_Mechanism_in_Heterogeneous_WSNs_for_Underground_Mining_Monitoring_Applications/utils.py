import matplotlib.pyplot as plt
import numpy as np


def print_node_death_comparison(baseline_deaths, proposed_deaths, q_learning_deaths):
    def extract_milestones(death_rounds):
        total_nodes = len(death_rounds)
        death_rounds_sorted = sorted(death_rounds)
        def get_percentile(p):
            idx = int(p * total_nodes)
            return death_rounds_sorted[min(idx, total_nodes - 1)]
        return {
            "1st": get_percentile(0.0),
            "50%": get_percentile(0.5),
            "90%": get_percentile(0.9),
            "Last": get_percentile(1.0),
        }

    b = extract_milestones(baseline_deaths)
    p = extract_milestones(proposed_deaths)
    q = extract_milestones(q_learning_deaths)

    print("────────────────────────────────────────────────────────────────────────────────────────────────")
    print(f"{'Milestone':<30} {'Baseline DEECP':>20} {'Enhanced DEECP':>20} {'Q-Learning DEECP':>20}")
    print("────────────────────────────────────────────────────────────────────────────────────────────────")
    print(f"{'1st Node Death':<30} {b['1st']:>20} {p['1st']:>20} {q['1st']:>20}")
    print(f"{'50% Nodes Dead':<30} {b['50%']:>20} {p['50%']:>20} {q['50%']:>20}")
    print(f"{'90% Nodes Dead':<30} {b['90%']:>20} {p['90%']:>20} {q['90%']:>20}")
    print(f"{'Last Node Death':<30} {b['Last']:>20} {p['Last']:>20} {q['Last']:>20}")
    print("────────────────────────────────────────────────────────────────────────────────────────────────")

