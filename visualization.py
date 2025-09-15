# visualization.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import datetime

class Visualization(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consciousness Meter")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Figure and subplots for real-time data
        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6, self.ax7) = plt.subplots(
            7, 1, gridspec_kw={'height_ratios': [2, 2, 2, 2, 2, 1, 1]}, figsize=(10, 12)
        )
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Initialize data buffers
        self.atp_level = np.zeros(250)  # 1s buffer at 250 Hz
        self.contrast_level = np.zeros(250)
        self.ci_level = np.zeros(250)
        self.phi_level = np.zeros(250)
        self.info_energy_level = np.zeros(250)
        self.decay_level = np.zeros(250)

        # Plot lines
        self.line, = self.ax1.plot(self.atp_level)
        self.contrast_line, = self.ax2.plot(self.contrast_level)
        self.ci_line, = self.ax3.plot(self.ci_level)
        self.phi_line, = self.ax4.plot(self.phi_level)
        self.info_energy_line, = self.ax5.plot(self.info_energy_level)
        self.decay_line, = self.ax6.plot(self.decay_level)

        # Contribution bars (ax7)
        self.contrib_bars = self.ax7.bar(range(9), np.zeros(9))  # Placeholder for 9 contribution factors
        self.ax7.set_ylim(0, 1)

        # Labels and buttons
        self.status_label = QLabel("Status: Initializing...")
        self.layout.addWidget(self.status_label)

        self.thz_button = QPushButton("Toggle THz")
        self.mag_button = QPushButton("Toggle Mag")
        self.task_button = QPushButton("Toggle Task")
        self.save_button = QPushButton("Save Outputs")
        self.calibrate_button = QPushButton("Calibrate")

        self.layout.addWidget(self.thz_button)
        self.layout.addWidget(self.mag_button)
        self.layout.addWidget(self.task_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.calibrate_button)

        # Set up axes
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6]:
            ax.set_xlim(0, 250)
            ax.set_ylim(0, 1)
        self.ax1.set_title("ATP Level")
        self.ax2.set_title("Light Intensity")
        self.ax3.set_title("CI(t)")
        self.ax4.set_title("Phi")
        self.ax5.set_title("Info Energy")
        self.ax6.set_title("Decay Rate")
        self.ax7.set_title("Contributions")

        # Ensure QApplication is used (handled by main.py, but we can check version)
        print(f"Running with Python {sys.version}")

    def update_status(self, text):
        self.status_label.setText(f"Status: {text}")

    def update_contributions(self, contributions):
        if len(contributions) == 9:  # Assuming 9 factors as per metrics.explain_ci_t
            for bar, val in zip(self.contrib_bars, contributions):
                bar.set_height(val)
            self.ax7.relim()
            self.ax7.autoscale_view()
            self.canvas.draw()

    def save_outputs(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.fig.savefig(f"output_{timestamp}.png")
        print(f"Saved output to output_{timestamp}.png")

    def show(self):
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Visualization()
    window.show()
    sys.exit(app.exec_())
