# visualization.py
"""
Visualization module for Consciousness Meter, displaying CI(t), ATP, and network dynamics.
"""

import matplotlib
matplotlib.use("Qt5Agg")  # ✅ Force Qt backend

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import numpy as np
import datetime

class Visualization(QWidget):  # ✅ Subclass QWidget
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consciousness Meter")
        self.setGeometry(100, 100, 1200, 800)

        # Layout
        self.layout = QVBoxLayout(self)

        # Status label
        self.status_label = QLabel("Status: Initializing...")
        self.layout.addWidget(self.status_label)

        # Buttons
        self.thz_button = QPushButton("Toggle THz")
        self.mag_button = QPushButton("Toggle Magnetic")
        self.task_button = QPushButton("Toggle 2-back")
        self.save_button = QPushButton("Save Outputs")
        self.calibrate_button = QPushButton("Calibrate")
        for btn in [self.thz_button, self.mag_button, self.task_button, self.save_button, self.calibrate_button]:
            self.layout.addWidget(btn)

        # Figure and canvas
        self.fig = plt.figure(figsize=(10, 12))
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Subplots
        gs = self.fig.add_gridspec(7, 1, height_ratios=[2, 2, 2, 2, 2, 1, 1])
        self.ax1 = self.fig.add_subplot(gs[0])
        self.ax2 = self.fig.add_subplot(gs[1])
        self.ax3 = self.fig.add_subplot(gs[2])
        self.ax4 = self.fig.add_subplot(gs[3], projection='3d')
        self.ax5 = self.fig.add_subplot(gs[4])
        self.ax6 = self.fig.add_subplot(gs[5])
        self.ax7 = self.fig.add_subplot(gs[6])

        # Data buffers
        self.atp_level = np.zeros(250)
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

        # Contribution bars
        self.contrib_bars = self.ax7.bar(range(9), np.zeros(9))
        self.ax7.set_ylim(0, 1)

        # Axis titles
        self.ax1.set_title("ATP Level")
        self.ax2.set_title("Light Intensity")
        self.ax3.set_title("CI(t)")
        self.ax4.set_title("Phi")
        self.ax5.set_title("Info Energy")
        self.ax6.set_title("Decay Rate")
        self.ax7.set_title("Contributions")

        # Set axis limits
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6]:
            ax.set_xlim(0, 250)
            ax.set_ylim(0, 1)

        self.frames = []

    def update_status(self, text):
        self.status_label.setText(f"Status: {text}")

    def update_contributions(self, contributions):
        if len(contributions) == 9:
            for bar, val in zip(self.contrib_bars, contributions):
                bar.set_height(val)
            self.ax7.relim()
            self.ax7.autoscale_view()
            self.canvas.draw()

    def save_frame(self):
        self.frames.append(self.fig.canvas.copy_from_bbox(self.fig.bbox))

    def save_outputs(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.fig.savefig(f"output_{timestamp}.png")
        print(f"Saved output to output_{timestamp}.png")

    def show(self):
        self.showMaximized()


