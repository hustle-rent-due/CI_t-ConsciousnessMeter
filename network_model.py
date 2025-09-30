import numpy as np

class SimpleNetwork:
    def __init__(self, n_nodes=20):
        self.n_nodes = n_nodes
        self.state = np.random.rand(n_nodes)

    def step(self):
        """Random recurrent update with noise."""
        W = np.random.rand(self.n_nodes, self.n_nodes) < 0.1
        influence = W.dot(self.state) / max(1, W.sum())
        self.state = 0.9 * self.state + 0.1 * influence + 0.05 * np.random.randn(self.n_nodes)
        self.state = np.clip(self.state, 0, 1)
        return self.state
