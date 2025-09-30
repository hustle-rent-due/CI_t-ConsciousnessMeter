import matplotlib.pyplot as plt

class LivePlot:
    def __init__(self, max_points=200):
        self.max_points = max_points
        self.values = []
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(8,4))

    def update(self, val):
        self.values.append(val)
        if len(self.values) > self.max_points:
            self.values.pop(0)
        self.ax.clear()
        self.ax.set_ylim(0, 1)
        self.ax.set_title("Universal Consciousness Index (UCIₜ)")
        self.ax.plot(self.values, color="#00c8ff", linewidth=2)
        plt.draw()
        plt.pause(0.01)






