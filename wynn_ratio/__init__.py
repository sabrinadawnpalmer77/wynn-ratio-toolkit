# wynn_ratio/__init__.py

__version__ = "0.1.0"

# Core simulation and game functions
from .simulate import (
    phase_transition_sweep,
    coordination_game,
    ckcs_game
)

# Visualization utilities
from .visualize import (
    plot_phase_transition,
    plot_avalanche
)

# Metrics and analysis tools
from .metrics import (
    estimate_variance,
    estimate_constraint,
    fit_power_law
)

# Make the main functions easily importable
__all__ = [
    "phase_transition_sweep",
    "coordination_game",
    "ckcs_game",
    "plot_phase_transition",
    "plot_avalanche",
    "estimate_variance",
    "estimate_constraint",
    "fit_power_law"
]
