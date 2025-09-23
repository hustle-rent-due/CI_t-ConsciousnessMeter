"""
metrics.py

Implements Consciousness Index (CIₜ) metrics.
Includes both:
  - Linear weighted-sum version
  - Logistic activation version (refined)
"""

import numpy as np


class ConsciousnessMetrics:
    """
    Class to compute different versions of the Consciousness Index (CIₜ).
    """

    def __init__(self):
        pass

    @staticmethod
    def compute_ci_linear(components: dict, weights: dict) -> float:
        """
        Linear CIₜ (bounded weighted sum).

        Args:
            components (dict): {
                'sigma': σₕ,
                'vitality': V,
                'light': L,
                'entropy': Entropy_norm,
                'energy': E_norm,
                'phi': Φ_norm,
                'fmri': fMRI_fc,
                'fnirs': fNIRS_hb,
                'meg': MEG_coh
            }  # each ∈ [0,1]

            weights (dict): matching dict of weights (must sum ~1).

        Returns:
            float: CIₜ ∈ [0,1]
        """
        # normalize weights
        total = sum(weights.values())
        norm_weights = {k: v / total for k, v in weights.items()}

        # weighted sum
        CI_t = sum(norm_weights[k] * components.get(k, 0.0) for k in norm_weights)

        # cap to [0,1]
        return max(0.0, min(1.0, CI_t))

    @staticmethod
    def compute_ci_logistic(components: dict, weights: dict, theta: float = 0.5) -> float:
        """
        Logistic CIₜ (sigmoid threshold).

        Args:
            components (dict): {
                'sigma': σₕ,
                'vitality': V,
                'light': L,
                'entropy': Entropy_norm,
                'energy': E_norm,
                'phi': Φ_norm,
                'fmri': fMRI_fc,
                'fnirs': fNIRS_hb,
                'meg': MEG_coh
            }  # each ∈ [0,1]

            weights (dict): matching dict of weights (must sum ~1).
            theta (float): threshold parameter (default 0.5).

        Returns:
            float: CIₜ ∈ (0,1)
        """
        # normalize weights
        total = sum(weights.values())
        norm_weights = {k: v / total for k, v in weights.items()}

        # weighted sum (Z)
        Z = sum(norm_weights[k] * components.get(k, 0.0) for k in norm_weights)

        # logistic activation
        CI_t = 1.0 / (1.0 + np.exp(-(Z - theta)))
        return CI_t


# Example usage (can remove before production)
if __name__ == "__main__":
    components_example = {
        'sigma': 0.7,
        'vitality': 0.8,
        'light': 0.6,
        'entropy': 0.75,
        'energy': 0.65,
        'phi': 0.7,
        'fmri': 0.8,
        'fnirs': 0.7,
        'meg': 0.6
    }

    weights_example = {
        'sigma': 0.2,
        'vitality': 0.1,
        'light': 0.15,
        'entropy': 0.15,
        'energy': 0.1,
        'phi': 0.1,
        'fmri': 0.1,
        'fnirs': 0.05,
        'meg': 0.05
    }

    cm = ConsciousnessMetrics()
    linear = cm.compute_ci_linear(components_example, weights_example)
    logistic = cm.compute_ci_logistic(components_example, weights_example, theta=0.5)

    print(f"Linear CIₜ: {linear:.4f}")
    print(f"Logistic CIₜ: {logistic:.4f}")

