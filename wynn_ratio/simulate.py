# wynn_ratio/simulate.py
import numpy as np
from typing import Dict, Tuple

def coordination_game(C: float, V: float, n_actions: int = 8, max_rounds: int = 1000, seed: int = 42) -> Dict:
    """Two memoryless agents. Payoff = 1 only if actions match."""
    np.random.seed(seed)
    constraint_strength = C / (C + V)
    actions = np.random.randint(0, n_actions, size=(2, max_rounds))
    matches = np.zeros(max_rounds, dtype=bool)
    last_match = -1

    for t in range(max_rounds):
        if t > 0 and np.random.rand() < constraint_strength:
            # Bias toward repeating last successful action (simulates constraint)
            actions[0, t] = actions[0, last_match] if last_match >= 0 else actions[0, t]
            actions[1, t] = actions[1, last_match] if last_match >= 0 else actions[1, t]
        matches[t] = actions[0, t] == actions[1, t]
        if matches[t]:
            last_match = t

    # Time to equilibrium = first time we get 5 consecutive matches
    streak = np.convolve(matches.astype(int), np.ones(5, dtype=int), mode='valid')
    tte_idx = np.where(streak == 5)[0]
    tte = int(tte_idx[0] +
