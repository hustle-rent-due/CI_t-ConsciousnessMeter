import numpy as np
from data_acquisition import synthetic_eeg, entropy, synthetic_resources
from network_model import SimpleNetwork
from metrics import coherence_sigma, sustainability_mu, quantum_q, omega_order, psi_integration
from visualization import LivePlot

# Weights (must sum to 1)
alpha, beta, gamma, delta, epsilon = 0.2, 0.2, 0.2, 0.2, 0.2
lambda_ = 0.3

# Init
UCI_prev = 0.5
net = SimpleNetwork()
plotter = LivePlot()

for step in range(500):
    # Signals
    eeg = synthetic_eeg()
    resources = synthetic_resources()
    net_state = net.step()

    # Metrics
    sigma = coherence_sigma(eeg)
    mu = sustainability_mu(resources)
    q = quantum_q(net_state)
    H = entropy(eeg.flatten())
    omega = omega_order(H)
    psi = psi_integration(net_state)

    # UCI calculation
    instantaneous = alpha * sigma + beta * mu + gamma * q + delta * omega + epsilon * psi
    UCI_t = (1 - lambda_) * UCI_prev + lambda_ * instantaneous
    UCI_prev = UCI_t

    # Log + plot
    print(f"Step {step}: UCIₜ={UCI_t:.3f}")
    plotter.update(UCI_t)

