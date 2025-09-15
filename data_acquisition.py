# data_acquisition.py
import numpy as np
try:
    import brainflow
    from brainflow.board_shim import BoardShim, BrainFlowInputParams
    import smbus2
except ImportError:
    brainflow = None
    smbus2 = None
import time

class DataAcquisition:
    def __init__(self):
        self.board_id = None
        self.i2c_bus = None
        self.board = None
        if brainflow:
            try:
                BoardShim.enable_dev_board_logger()
                params = BrainFlowInputParams()
                params.serial_port = "/dev/ttyUSB0"
                self.board_id = 0
                self.board = BoardShim(self.board_id, params)
                self.board.prepare_session()
                self.board.start_stream()
            except Exception as e:
                print(f"OpenBCI setup failed: {e}")
        if smbus2:
            try:
                self.i2c_bus = smbus2.SMBus(1)
            except Exception as e:
                print(f"I2C setup failed: {e}")

    def acquire_data(self, task_mode=False):
        eeg_data = np.zeros(8) if not self.board else self.board.get_board_data()[:8, -250:]  # Last 1s at 250 Hz
        eeg_gamma = np.mean(eeg_data, axis=1) if eeg_data.size else np.zeros(8)
        eeg_gamma = np.clip(eeg_gamma / np.max(np.abs(eeg_gamma + 1e-10)), 0, 1)
        
        light_intensity = 0.5
        temperature = 0.5
        em_field = 0.5
        if self.i2c_bus:
            try:
                light_intensity = self.i2c_bus.read_word_data(0x39, 0x0C) / 65535
                temperature = self.i2c_bus.read_word_data(0x48, 0x00) / 256
                em_field = 0.5  # Placeholder, update with actual sensor if available
            except Exception as e:
                print(f"Sensor error: {e}")

        fmri_fc = 0.5  # Placeholder, update with real stream
        fnirs_hb = 0.5  # Placeholder, update with real stream
        meg_coh = 0.5  # Placeholder, update with real stream

        if task_mode:
            eeg_gamma += 0.2 * np.random.rand(8)  # Simulate 2-back task effect
            fmri_fc += 0.15 * np.random.rand()
            fnirs_hb += 0.1 * np.random.rand()
            meg_coh += 0.2 * np.random.rand()

        eeg_gamma = np.clip(eeg_gamma, 0, 1)
        fmri_fc = np.clip(fmri_fc, 0, 1)
        fnirs_hb = np.clip(fnirs_hb, 0, 1)
        meg_coh = np.clip(meg_coh, 0, 1)

        timestamp = time.time() * 1000
        if self.board and abs(timestamp - (self.board.get_timestamp_data()[-1] if self.board.get_timestamp_data().size else 0)) > 10:
            print("Sync error: Timestamp drift > 10 ms")
        return eeg_gamma, light_intensity, temperature, em_field, fmri_fc, fnirs_hb, meg_coh

    def cleanup(self):
        if self.board:
            self.board.stop_stream()
            self.board.release_session()
