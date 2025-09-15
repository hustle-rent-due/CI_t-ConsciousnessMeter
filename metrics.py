# metrics.py
import numpy as np
from scipy.stats import spearmanr
from scipy.fft import fft

class Metrics:
    def __init__(self, num_nodes=100):
        self.num_nodes = num_nodes
        self.k_B = 1.38e-23
        self.T = 300
        self.ln2 = np.log(2)
        self.w_H, self.w_V, self.w_L, self.w_S, self.w_E, self.w_Phi = 1.0, 1.0, 0.8, 0.8, 0.5, 0.3
        self.w_fMRI, self.w_fNIRS, self.w_MEG = 0.2, 0.15, 0.25
        self.theta = 1.2

    def calculate_information(self, signal_stream):
        hist, _ = np.histogram(signal_stream, bins=16, density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        return entropy / 4

    def calculate_fft_peak(self, signal):
        if len(signal) > 1:
            fft_vals = np.abs(fft(signal))[:len(signal)//2]
            freqs = np.fft.fftfreq(len(signal), d=1/250)[:len(signal)//2]
            gamma_range = (freqs >= 30) & (freqs <= 100)
            if np.any(gamma_range):
                return np.max(fft_vals[gamma_range]) / np.max(fft_vals + 1e-10)
        return 0.5

    def calculate_lz_norm(self, signal):
        def lzw_compress(signal):
            binary = (signal > np.mean(signal)).astype(int).tobytes()
            dictionary = {bytes([i]): i for i in range(256)}
            result = []
            w = b""
            dict_size = 256
            for c in binary:
                wc = w + bytes([c])
                if wc in dictionary:
                    w = wc
                else:
                    result.append(dictionary[w])
                    dictionary[wc] = dict_size
                    dict_size += 1
                    w = bytes([c])
            if w:
                result.append(dictionary[w])
            return len(result)
        lz = lzw_compress(signal)
        surrogate = lzw_compress(np.random.randint(0, 2, len(signal)))
        return lz / surrogate if surrogate > 0 else 0.5

    def calculate_info_energy(self, signal_stream):
        entropy = self.calculate_information(signal_stream) * 4
        bits_per_node = min(8, 8 * entropy)
        return self.num_nodes * bits_per_node * self.k_B * self.T * self.ln2

    def calculate_phi(self, edge_weights):
        min_mi = float('inf')
        nodes = list(range(self.num_nodes))
        for _ in range(5):  # Reduced to 5 for real-time
            s1 = np.random.choice(nodes, self.num_nodes // 2, replace=False)
            s2 = list(set(nodes) - set(s1))
            mi = sum(edge_weights[i, j] for i in s1 for j in s2 if i < j and edge_weights[i, j] > 0)
            min_mi = min(min_mi, mi)
        phi_norm = min_mi / np.log2(2 ** self.num_nodes) if self.num_nodes > 0 else 0.5
        return phi_norm

    def compute_vitality(self, toxins, atp_level):
        return np.exp(-0.5 * toxins * np.std(atp_level))

    def compute_ci_t(self, sigma_h, vitality, light_pulse, entropy, info_energy, phi_norm, fmri_fc, fnirs_hb, meg_coh):
        weighted_sum = (self.w_H * sigma_h + self.w_V * vitality + self.w_L * light_pulse +
                        self.w_S * (1 - entropy) + self.w_E * info_energy + self.w_Phi * phi_norm +
                        self.w_fMRI * fmri_fc + self.w_fNIRS * fnirs_hb + self.w_MEG * meg_coh - self.theta)
        return 1 / (1 + np.exp(-weighted_sum))

    def validate_ci_t(self, ci_t, ground_truth_pci, ground_truth_crs_r, ground_truth_gcs):
        rho_pci = spearmanr([ci_t], [ground_truth_pci])[0] if len([ci_t]) > 1 and len([ground_truth_pci]) > 1 else 0
        rho_crs_r = spearmanr([ci_t], [ground_truth_crs_r])[0] if len([ci_t]) > 1 and len([ground_truth_crs_r]) > 1 else 0
        rho_gcs = spearmanr([ci_t], [ground_truth_gcs])[0] if len([ci_t]) > 1 and len([ground_truth_gcs]) > 1 else 0
        return rho_pci, rho_crs_r, rho_gcs

    def explain_ci_t(self, ci_t, sigma_h, vitality, light_pulse, entropy, info_energy, phi_norm, fmri_fc, fnirs_hb, meg_coh):
        contributions = {
            "Harmony": ci_t * (1 - ci_t) * self.w_H * sigma_h,
            "Vitality": ci_t * (1 - ci_t) * self.w_V * vitality,
            "Light Pulse": ci_t * (1 - ci_t) * self.w_L * light_pulse,
            "Entropy": ci_t * (1 - ci_t) * self.w_S * (1 - entropy),
            "Info Energy": ci_t * (1 - ci_t) * self.w_E * info_energy,
            "Phi": ci_t * (1 - ci_t) * self.w_Phi * phi_norm,
            "fMRI FC": ci_t * (1 - ci_t) * self.w_fMRI * fmri_fc,
            "fNIRS Hb": ci_t * (1 - ci_t) * self.w_fNIRS * fnirs_hb,
            "MEG Coherence": ci_t * (1 - ci_t) * self.w_MEG * meg_coh
        }
        return contributions

    def map_to_gcs(self, ci_t):
        return min(15, max(3, 3 + 12 * ci_t))
