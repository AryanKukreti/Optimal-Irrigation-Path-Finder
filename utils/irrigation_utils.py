import numpy as np
import networkx as nx

def is_edge_valid(p1, p2, image_array, threshold, num_samples=10):
    """ Check if the edge between p1 and p2 passes through a dark region. """
    for i in range(num_samples):
        x = int(p1[0] + (p2[0] - p1[0]) * i / num_samples)
        y = int(p1[1] + (p2[1] - p1[1]) * i / num_samples)
        if image_array[y, x] < threshold:
            return False  # Edge is invalid if it crosses a dark region
    return True  # Edge is valid if all sampled points are in bright regions

def ensure_connected(G):
    """ Ensure that the graph is connected by adding edges if necessary. """
    G_copy = G.copy()
    
    components = list(nx.connected_components(G_copy))
    
    if len(components) == 1:
        return G_copy
    
    for i in range(len(components) - 1):
        node1 = list(components[i])[0]
        node2 = list(components[i + 1])[0]
        G_copy.add_edge(node1, node2, weight=1e10)
    
    return G_copy
