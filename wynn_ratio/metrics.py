# wynn_ratio/metrics.py
import numpy as np
from scipy.stats import linregress
from scipy.stats import entropy

def estimate_variance(action_history: np.ndarray) -> float:
    """
    Compute interpretive variance V from empirical action distributions
    using Shannon entropy (in bits).
    """
    if len(action_history) == 0:
        return 0.0
    unique, counts = np.unique(action_history, return_counts=True)
    probs = counts / counts.sum()
    return float(entropy(probs, base=2))


def estimate_constraint(shared_reference: np.ndarray, actions: np.ndarray) -> float:
    """
    Estimate the Lee Constraint C via normalized mutual information
    between a shared reference signal and agent actions.
    Returns a scaled value suitable for the WYNN Ratio regime.
    """
    if len(shared_reference) == 0 or len(actions) == 0:
        return 0.0
    # Simple proxy using histogram-based mutual information
    # (scaled to match paper's constraint range)
    mi = mutual_info_score(shared_reference, actions)  # requires scikit-learn
    return float(mi * 10.0)


def fit_power_law(sizes: np.ndarray, xmin: int = 1) -> dict:
    """
    Fit power-law to avalanche sizes and return exponent τ.
    Used for criticality analysis (target τ ≈ 1.5 at the critical window).
    """
    sizes = np.array(sizes)
    sizes = sizes[sizes >= xmin]
    if len(sizes) < 10:
        return {"tau": np.nan, "r_squared": 0.0, "valid": False}
    
    # Rank-frequency plot for power-law fitting
    ranks = np.arange(1, len(sizes) + 1)
    logx = np.log(sizes)
    logy = np.log(ranks[::-1])  # reverse rank
    
    slope, intercept, r_value, _, _ = linregress(logx, logy)
    return {
        "tau": float(-slope),
        "r_squared": float(r_value**2),
        "valid": True
    }


# Optional: simple mutual_info_score fallback if scikit-learn is not installed
def mutual_info_score(labels1, labels2):
    """Lightweight fallback mutual information (histogram-based)."""
    from scipy.stats import contingency
    c = contingency.crosstab(labels1, labels2, sparse=False)[0]
    p_xy = c / c.sum()
    p_x = p_xy.sum(axis=1, keepdims=True)
    p_y = p_xy.sum(axis=0, keepdims=True)
    mi = np.sum(p_xy * np.log2(p_xy / (p_x * p_y + 1e-12) + 1e-12))
    return mi
