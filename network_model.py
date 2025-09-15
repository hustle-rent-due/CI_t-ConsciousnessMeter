# network_model.py
import numpy as np
import networkx as nx

class NetworkModel:
    def __init__(self, num_nodes=100):
        self.G = nx.erdos_renyi_graph(num_nodes, 0.1)
        self.pos = nx.spring_layout(self.G, dim=3)
        self.node_states = np.zeros(num_nodes)
        self.edge_weights = np.zeros((num_nodes, num_nodes))
        self.alpha = 0.9
        self.beta = 0.95

    def update_dynamics(self, vitality, toxins):
        self.node_states = self.alpha * self.node_states + (1 - self.alpha) * vitality * np.random.rand(len(self.node_states))
        self.edge_weights = self.beta * self.edge_weights * np.exp(-0.01 * toxins)
        for i, j in self.G.edges():
            if np.random.rand() < 0.1:  # Sparse updates for real-time
                self.edge_weights[i, j] = self.edge_weights[j, i] = min(1.0, max(0.0, self.edge_weights[i, j] + np.random.normal(0, 0.1)))
        return self.node_states, self.edge_weights
