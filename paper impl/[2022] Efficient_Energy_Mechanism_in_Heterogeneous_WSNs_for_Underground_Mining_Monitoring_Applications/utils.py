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

    print("────────────────────────────────────────────────────────────")
    print(f"{'Milestone':<20} {'Baseline':>10} {'Proposed':>10} {'Q-Learning':>12}")
    print("────────────────────────────────────────────────────────────")
    print(f"{'1st Node Death':<20} {b['1st']:>10} {p['1st']:>10} {q['1st']:>12}")
    print(f"{'50% Nodes Dead':<20} {b['50%']:>10} {p['50%']:>10} {q['50%']:>12}")
    print(f"{'90% Nodes Dead':<20} {b['90%']:>10} {p['90%']:>10} {q['90%']:>12}")
    print(f"{'Last Node Death':<20} {b['Last']:>10} {p['Last']:>10} {q['Last']:>12}")
    print("────────────────────────────────────────────────────────────")

