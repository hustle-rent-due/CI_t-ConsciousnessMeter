# visualization.py
"""
Visualization module for Consciousness Meter, displaying CI(t), ATP, and network dynamics.
"""
import matplotlib
matplotlib.use("Qt5Agg")  # Force Qt backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
import numpy as np
import datetime
import imageio

class Visualization:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 12))
        self.canvas = FigureCanvas(self.fig)
        gs = self.fig.add_gridspec(8, 1, height_ratios=[2, 2, 2, 2, 2, 2, 1, 1])
        self.ax1 = self.fig.add_subplot(gs[0])
        self.ax2 = self.fig.add_subplot(gs[1])
        self.ax3 = self.fig.add_subplot(gs[2])
        self.ax4 = self.fig.add_subplot(gs[3], projection='3d')
        self.ax5 = self.fig.add_subplot(gs[4])
        self.ax6 = self.fig.add_subplot(gs[5])
        self.ax7 = self.fig.add_subplot(gs[6])
        self.ax8 = self.fig.add_subplot(gs[7], projection='3d')
        self.atp_level = np.ones(100) * 0.5
        self.contrast_level = np.ones(100) * 0.5
        self.ci_level = np.ones(100) * 0.5
        self.phi_level = np.ones(100) * 0.5
        self.info_energy_level = np.ones(100) * 0.5
        self.decay_level = np.ones(100) * 0.5
        self.line, = self.ax1.plot(self.atp_level, label='ATP')
        self.contrast_line, = self.ax2.plot(self.contrast_level, label='Light')
        self.ci_line, = self.ax3.plot(self.ci_level, label='CI(t)')
        self.phi_line, = self.ax5.plot(self.phi_level, label='Phi')
        self.info_energy_line, = self.ax6.plot(self.info_energy_level, label='Info Energy')
        self.decay_line, = self.ax6.plot(self.decay_level, label='Decay')
        self.ax1.legend()
        self.ax2.legend()
        self.ax3.legend()
        self.ax5.legend()
        self.ax6.legend()
        self.ax7.set_title('Status')
        self.ax8.set_title('Phi Evolution')
        self.contrib_bars = []
        self.thz_button = QPushButton('Toggle THz')
        self.mag_button = QPushButton('Toggle Magnetic')
        self.task_button = QPushButton('Toggle 2-back')
        self.save_button = QPushButton('Save Outputs')
        self.calibrate_button = QPushButton('Calibrate')
        self.frames = []
        self.widget = None

    def build_gui(self):
        self.widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.thz_button)
        layout.addWidget(self.mag_button)
        layout.addWidget(self.task_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.calibrate_button)
        self.widget.setLayout(layout)

    def update_contributions(self, contributions):
        self.ax5.clear()
        self.contrib_bars = self.ax5.bar(contributions.keys(), contributions.values())
        self.ax5.set_title('CI(t) Contributions')
        self.ax5.legend(['Contributions'])

    def update_status(self, text):
        self.ax7.clear()
        self.ax7.text(0.5, 0.5, text, ha='center', va='center', fontsize=10, wrap=True)
        self.ax7.axis('off')

    def save_frame(self):
        self.frames.append(np.array(self.fig.canvas.buffer_rgba())[:, :, :3])

    def save_outputs(self):
        if self.frames:
            imageio.mimsave(f"consciousness_meter_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.gif", self.frames, fps=30)
            self.frames = []

    def show(self):
        if self.widget:
            self.widget.showMaximized()





