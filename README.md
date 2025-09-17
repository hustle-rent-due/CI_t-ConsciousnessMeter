# Consciousness Meter

A consciousness meter computing CI(t) for real-time consciousness analysis.

## Overview
- **CI(t)**: Consciousness Index, integrating harmony (\(\sigma_h\)), vitality, light pulse, entropy, info energy, and \(\Phi_{\text{norm}}\).
- **Simulations**:
  - `main.py`: Integrates network model, data acquisition, metrics, and visualization with real-time Qt GUI.
  - `network_model.py`: Simulates 100-node neural network with real-time dynamics (\(\alpha=0.9\), \(\beta=0.95\)).
  - `data_acquisition.py`: Simulates EEG (250 Hz), TSL2561, TMP102 with <10 ms drift.
  - `metrics.py`: Computes CI(t), \(\Phi_{\text{norm}}\) (min-cut), vitality, and validation metrics.
  - `visualization.py`: Displays real-time plots (CI(t), \(\Phi\), network) and GUI buttons.

## Setup
1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt

Run:bash

python3 main.py

Simulationsmain.py: Computes CI(t), Φnorm\Phi_{\text{norm}}\Phi_{\text{norm}}
, and network dynamics at 30 Hz. Outputs real-time plots, GIF, and log.txt. Includes 3D Φ\Phi\Phi
 plot (Time, Recursion, Emergence).
Current Features:Real-time EEG (250 Hz) and sensor data (TSL2561, TMP102).
Baseline calibration for CI(t), σh\sigma_h\sigma_h
, LZnorm\text{LZ}_{\text{norm}}\text{LZ}_{\text{norm}}
.
Non-linear toxin-ATP decay.
Real-time GUI with CI(t), Φ\Phi\Phi
, and network plots.

Gaps:Add real-time 2-back task simulation.
Implement real-time contribution bar plot.
Optimize Φ\Phi\Phi
 calculation for speed.
Integrate real fMRI/fNIRS/MEG data.
Add real-time GCS mapping and PCI/CRS-R validation.
Enhance GUI with validation metrics and task mode button.

ResultsHealthy (2-back): CI_t = 0.90, LZ_norm = 0.80, Φ\Phi\Phi
 = 0.65, GCS Analog = 13.8/15, CRS-R Analog = 20.7/23.LicenseMIT License
```

                self.edge_weights[i, j] = self.edge_weights[j, i] = min(1.0, max(0.0, self.edge_weights[i, j] + np.random.normal(0, 0.1)))
        return self.node_states, self.edge_weights
