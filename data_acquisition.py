import numpy as np

def synthetic_eeg(n_channels=8, n_samples=256):
    """Generate fake EEG-like signals for coherence + entropy."""
    t = np.linspace(0, 1, n_samples)
    signals = []
    for _ in range(n_channels):
        freq = np.random.choice([10, 40])  # alpha or gamma
        signals.append(np.sin(2 * np.pi * freq * t) + 0.2 * np.random.randn(n_samples))
    return np.array(signals)


def entropy(signal: np.ndarray, bins=16) -> float:
    """Shannon entropy of normalized signal."""
    hist, _ = np.histogram(signal, bins=bins, density=True)
    hist = hist[hist > 0]
    p = hist / hist.sum()
    return float(-np.sum(p * np.log2(p)) / np.log2(bins))


def synthetic_resources(n=100):
    """Randomized resource stability profile."""
    return np.random.rand(n)

