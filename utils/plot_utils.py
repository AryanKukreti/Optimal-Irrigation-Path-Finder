import numpy as np
import networkx as nx
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from utils.graph_utils import ensure_connected  # Corrected import
from .irrigation_utils import is_edge_valid

def plot_results(tri, G, image_array, starting_point, points):
    """Plot the results and compute the Minimum Spanning Tree."""
    G = ensure_connected(G)
    mst = nx.minimum_spanning_tree(G)
    mst_edges = list(mst.edges)

    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    ax.imshow(image_array, cmap="gray", alpha=0.6)

    # Plot shaded triangles
    for simplex in tri.simplices:
        if all(is_edge_valid(points[simplex[i]], points[simplex[(i + 1) % 3]], image_array, 60) for i in range(3)):
            triangle = Polygon(points[simplex], closed=True, color='yellow', alpha=0.3)
            ax.add_patch(triangle)

    # Plot MST edges
    for edge in mst_edges:
        p1, p2 = edge
        p1 = np.array(p1)
        p2 = np.array(p2)
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='blue', lw=0.5)

    # Plot points
    plt.scatter(points[:, 0], points[:, 1], color='red', s=10, zorder=5)
    plt.scatter([starting_point[0]], [starting_point[1]], color='yellow', s=50, zorder=6, label="Starting Point")
    plt.title("Irrigation Graph with Minimum Spanning Tree")
    plt.legend()
