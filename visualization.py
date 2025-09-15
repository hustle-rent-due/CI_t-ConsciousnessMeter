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

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6, self.ax7) = plt.subplots(7, 1, gridspec_kw={'height_ratios': [2, 2, 2, 2, 2, 1, 1]}, figsize=(10, 12))
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.atp_level = np.zeros(250)  # 1s buffer at 250 Hz
        self.contrast_level = np.zeros(250)
        self.ci_level = np.zeros(250)
        self.phi_level = np.zeros(250)
        self.info_energy_level = np.zeros(250)
        self.decay_level = np.zeros(250)

        self.line, = self.ax1.plot(self.atp_level)
        self.contrast_line, = self.ax2.plot(self.contrast_level)
        self.ci_line, = self.ax3.plot(self.ci_level)
        self.phi_line, = self.ax4.plot(self.phi_level)
        self.info_energy_line, = self.ax5.plot(self.info_energy_level)
        self.decay_line, = self.ax6.plot(self.decay_level)
        self.contrib_bars = self.ax7.bar([], [])

        self.ax1.set_title("ATP Level")
        self.ax2.set_title("Light Intensity")
        self.ax3.set_title("CI(t)")
        self.ax4.set_title("Phi Norm")
        self.ax5.set_title("Info Energy (J)")
        self.ax6.set_title("Decay Rate")
        self.ax7.set_title("Feature Contributions")

        self.ax1.set_ylim(0, 1.5)
        self.ax2.set_ylim(0, 1.5)
        self.ax3.set_ylim(0, 1.5)
        self.ax4.set_ylim(0, 1.5)
        self.ax5.set_ylim(0, 2e-17)
        self.ax6.set_ylim(0, 1.5)
        self.ax7.set_ylim(0, 1.0)

        self.thz_button = QPushButton("Toggle Light Pulse")
        self.mag_button = QPushButton("Toggle Magnetic Field")
        self.task_button = QPushButton("Toggle 2-back Task")
        self.save_button = QPushButton("Save Outputs")
        self.calibrate_button = QPushButton("Start Calibration")
        self.status_label = QLabel("Status: Initializing...")

        self.layout.addWidget(self.thz_button)
        self.layout.addWidget(self.mag_button)
        self.layout.addWidget(self.task_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.calibrate_button)
        self.layout.addWidget(self.status_label)

        self.contrib_bars_data = {}

    def update_contributions(self, contributions):
        self.contrib_bars_data = contributions
        labels = list(contributions.keys())
        values = list(contributions.values())
        self.ax7.clear()
        self.contrib_bars = self.ax7.bar(labels, values)
        self.ax7.set_ylim(0, max(values) * 1.2 if values else 1.0)
        self.canvas.draw()

    def update_status(self, text):
        self.status_label.setText(text)

    def save_outputs(self):
        self.fig.savefig(f"output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    def save_frame(self):
        self.canvas.draw()
