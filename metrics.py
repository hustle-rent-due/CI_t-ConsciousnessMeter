import numpy as np

def coherence_sigma(signals: np.ndarray) -> float:
    """Σ (Sigma): Coherence — synchronized information flow."""
    if signals.shape[0] < 2:
        return 0.0
    corr = np.corrcoef(signals)
    upper = corr[np.triu_indices_from(corr, k=1)]
    return float(np.clip(np.mean(np.abs(upper)), 0, 1))


def sustainability_mu(resources: np.ndarray, toxins: float = 0.1) -> float:
    """M (Mu): Sustainability — stability of resources (ATP, power, memory)."""
    stability = np.std(resources)
    score = np.mean(resources) * np.exp(-toxins * stability)
    return float(np.clip(score, 0, 1))


def quantum_q(signal: np.ndarray) -> float:
    """Q (Quantum): Fine dynamics — high-frequency processing."""
    fft_vals = np.fft.rfft(signal)
    peak = np.max(np.abs(fft_vals))
    norm = peak / (len(signal) * 10)
    return float(np.clip(norm, 0, 1))


def omega_order(entropy_val: float) -> float:
    """Ω (Omega): Order — inverse entropy (1−H)."""
    return float(np.clip(1 - entropy_val, 0, 1))


def psi_integration(connectivity: np.ndarray) -> float:
    """Ψ (Psi): Integration — irreducible information flow."""
    if connectivity.size == 0:
        return 0.0
    norm_eff = np.mean(connectivity)
    return float(np.clip(norm_eff, 0, 1))

