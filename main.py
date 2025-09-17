import sys
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from matplotlib.animation import FuncAnimation

from network_model import NetworkModel
from data_acquisition import DataAcquisition
from metrics import Metrics
from visualization import Visualization

def calibration_mode(metrics, data_acq, duration=300):
    baseline_ci_t = 0
    baseline_sigma_h = 0
    baseline_lz_norm = 0
    start_time = time.time()
    samples = 0
    while time.time() - start_time < duration:
        eeg_gamma, light_intensity, _, _, fmri_fc, fnirs_hb, meg_coh = data_acq.acquire_data()
        sigma_h = np.mean(eeg_gamma)
        vitality = metrics.compute_vitality(0.1, np.ones(100) * 0.5)
        entropy = metrics.calculate_information(eeg_gamma)
        info_energy = metrics.calculate_info_energy(eeg_gamma)
        lz_norm = metrics.calculate_lz_norm(eeg_gamma)
        phi_norm = metrics.calculate_phi(np.ones((100, 100)) * 0.5)
        ci_t = metrics.compute_ci_t(sigma_h, vitality, light_intensity, entropy, info_energy, phi_norm, fmri_fc, fnirs_hb, meg_coh)
        baseline_ci_t += ci_t
        baseline_sigma_h += sigma_h
        baseline_lz_norm += lz_norm
        samples += 1
        time.sleep(0.033)
    return baseline_ci_t / samples, baseline_sigma_h / samples, baseline_lz_norm / samples

def main():
    app = QApplication(sys.argv)

    model = NetworkModel()
    data_acq = DataAcquisition()
    metrics = Metrics()

    vis = Visualization()
    vis.build_gui()

    THz_resonance = False
    magnetic_field = False
    task_mode = False
    log_file = "log.txt"

    baseline_ci_t, baseline_sigma_h, baseline_lz_norm = calibration_mode(metrics, data_acq)

    def update(frame):
        eeg_gamma, light_intensity, _, _, fmri_fc, fnirs_hb, meg_coh = data_acq.acquire_data(task_mode)
        toxins = 0.1
        atp_level = np.ones(100) * 0.5
        node_states, edge_weights = model.update_dynamics(metrics.compute_vitality(toxins, atp_level), toxins)
        sigma_h = np.mean(eeg_gamma)
        vitality = metrics.compute_vitality(toxins, atp_level)
        entropy = metrics.calculate_information(eeg_gamma)
        info_energy = metrics.calculate_info_energy(eeg_gamma)
        lz_norm = metrics.calculate_lz_norm(eeg_gamma)
        phi_norm = metrics.calculate_phi(edge_weights)
        ci_t = metrics.compute_ci_t(sigma_h, vitality, light_intensity, entropy, info_energy, phi_norm, fmri_fc, fnirs_hb, meg_coh)
        contributions = metrics.explain_ci_t(ci_t, sigma_h, vitality, light_intensity, entropy, info_energy, phi_norm, fmri_fc, fnirs_hb, meg_coh)
        gcs_score = metrics.map_to_gcs(ci_t)
        rho_pci, rho_crs_r, rho_gcs = metrics.validate_ci_t(ci_t, 0.7, 18, gcs_score)

        vis.atp_level = np.roll(vis.atp_level, -1)
        vis.atp_level[-1] = atp_level.mean()
        vis.line.set_ydata(vis.atp_level)

        vis.contrast_level = np.roll(vis.contrast_level, -1)
        vis.contrast_level[-1] = light_intensity
        vis.contrast_line.set_ydata(vis.contrast_level)

        vis.ci_level = np.roll(vis.ci_level, -1)
        vis.ci_level[-1] = ci_t
        vis.ci_line.set_ydata(vis.ci_level)

        vis.phi_level = np.roll(vis.phi_level, -1)
        vis.phi_level[-1] = phi_norm

        # ✅ Refresh 3D phi plot
        x = np.arange(len(vis.phi_level))
        y = np.zeros(len(vis.phi_level))
        z = vis.phi_level
        vis.ax4.clear()
        vis.phi_line, = vis.ax4.plot(x, y, z, color='purple')
        vis.ax4.set_xlabel("Δx = Time")
        vis.ax4.set_ylabel("Δt = Recursion")
        vis.ax4.set_zlabel("Φ = Emergence")
        vis.ax4.set_xlim(0, len(vis.phi_level))
        vis.ax4.set_ylim(-1, 1)
        vis.ax4.set_zlim(0, 1)

        vis.info_energy_level = np.roll(vis.info_energy_level, -1)
        vis.info_energy_level[-1] = info_energy
        vis.info_energy_line.set_ydata(vis.info_energy_level)

        vis.decay_level = np.roll(vis.decay_level, -1)
        vis.decay_level[-1] = np.mean(edge_weights)
        vis.decay_line.set_ydata(vis.decay_level)

        vis.ax4.scatter([p[0] for p in model.pos.values()],
                        [p[1] for p in model.pos.values()],
                        [p[2] for p in model.pos.values()],
                        c=node_states, cmap=plt.cm.viridis, s=200)

        for i, j in model.G.edges():
            x_line = [model.pos[i][0], model.pos[j][0]]
            y_line = [model.pos[i][1], model.pos[j][1]]
            z_line = [model.pos[i][2], model.pos[j][2]]
            vis.ax4.plot(x_line, y_line, z_line, 'k-', alpha=edge_weights[i, j], linewidth=edge_weights[i, j] * 3)

        vis.update_contributions(contributions)

        status_text = f"Light Pulse: {'ON' if THz_resonance else 'OFF'} | Magnetic Field: {'ON' if magnetic_field else 'OFF'} | Task: {'ON' if task_mode else 'OFF'}\nHarmony: {sigma_h:.2f} | CI(t): {ci_t:.2f} | Phi: {phi_norm:.2f}\nInfo Energy: {info_energy:.2e} J | Decay Rate: {np.mean(edge_weights):.2f}\nGCS: {gcs_score:.2f} | ρ_PCI: {rho_pci:.2f} | ρ_CRS-R: {rho_crs_r:.2f} | ρ_GCS: {rho_gcs:.2f}"
        clean_status = status_text.replace('\n', ' | ')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"{timestamp} | {clean_status} | Contributions: {contributions}\n")

        vis.update_status(status_text)
        vis.save_frame()

        return [vis.line, vis.contrast_line, vis.ci_line, vis.info_energy_line, vis.decay_line] + list(vis.contrib_bars)

    def toggle_thz():
        nonlocal THz_resonance
        THz_resonance = not THz_resonance
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Light Pulse toggled to {'ON' if THz_resonance else 'OFF'}\n")

    def toggle_mag():
        nonlocal magnetic_field
        magnetic_field = not magnetic_field
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Magnetic Field toggled to {'ON' if magnetic_field else 'OFF'}\n")

    def toggle_task():
        nonlocal task_mode
        task_mode = not task_mode
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 2-back Task toggled to {'ON' if task_mode else 'OFF'}\n")

    def calibrate():
        nonlocal baseline_ci_t, baseline_sigma_h, baseline_lz_norm
        baseline_ci_t, baseline_sigma_h, baseline_lz_norm = calibration_mode(metrics, data_acq)

    vis.thz_button.clicked.connect(toggle_thz)
    vis.mag_button.clicked.connect(toggle_mag)
    vis.task_button.clicked.connect(toggle_task)
    vis.save_button.clicked.connect(vis.save_outputs)
    vis.calibrate_button.clicked.connect(calibrate)

    ani = FuncAnimation(vis.fig, update, interval=33, cache_frame_data=False)
    vis.widget.showMaximized()
    sys.exit(app.exec_())
    data_acq.cleanup()

if __name__ == "__main__":
    main()


