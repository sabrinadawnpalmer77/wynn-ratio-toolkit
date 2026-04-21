# wynn_ratio/visualize.py
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict

def plot_phase_transition(results: Dict, figsize: tuple = (10, 6)):
    """
    Plots the WYNN Ratio phase transition (reproduces the key figure from the paper).
    Shows median Time to Equilibrium (TTE) and convergence rate vs S = C/V.
    """
    fig, ax1 = plt.subplots(figsize=figsize)
    
    S = np.array(results["S"])
    median_tte = np.array(results["median_TTE"])
    conv_rate = np.array(results["convergence_rate"])
    
    # Left axis: Median TTE
    ax1.plot(S, median_tte, 'b-o', linewidth=2, markersize=4, label='Median TTE')
    ax1.set_xscale('log')
    ax1.set_xlabel('S = C/V (log scale)')
    ax1.set_ylabel('Median Time to Equilibrium', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    
    # Right axis: Convergence Rate
    ax2 = ax1.twinx()
    ax2.plot(S, conv_rate, 'r--s', linewidth=2, markersize=4, label='Convergence Rate')
    ax2.set_ylabel('Convergence Probability', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    plt.title('WYNN Ratio Phase Transition\nTwo-Agent Coordination Game')
    plt.grid(True, which='both', ls='--', alpha=0.5)
    
    # Add vertical line at critical window
    plt.axvline(x=0.8, color='gray', linestyle=':', alpha=0.7)
    plt.axvline(x=1.1, color='gray', linestyle=':', alpha=0.7)
    plt.text(0.95, 0.05, 'Critical Window\n(≈ 0.8–1.1)', 
             transform=ax1.transAxes, ha='center', fontsize=10)
    
    plt.tight_layout()
    return fig


def plot_avalanche(sizes: np.ndarray, title: str = "Avalanche Size Distribution", figsize: tuple = (8, 5)):
    """
    Plots avalanche size distribution on log-log scale (for Figure 1 style).
    Used to visualize power-law behavior at criticality.
    """
    sizes = np.array(sizes)
    if len(sizes) == 0:
        raise ValueError("No avalanche sizes provided")
    
    # Histogram
    counts, bins = np.histogram(sizes[sizes > 0], bins=50)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    plt.figure(figsize=figsize)
    plt.loglog(bin_centers, counts, 'o', markersize=4, alpha=0.8)
    plt.xlabel('Avalanche Size')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.grid(True, which='both', ls='--', alpha=0.5)
    plt.tight_layout()
    return plt.gcf()
