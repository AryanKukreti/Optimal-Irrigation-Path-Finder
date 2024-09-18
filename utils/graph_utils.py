import numpy as np
import networkx as nx
from scipy.spatial import Delaunay
from .irrigation_utils import is_edge_valid

def generate_graph(points, image_array, ditch_threshold):
    """Perform Delaunay triangulation and generate the graph."""
    tri = Delaunay(points)
    G = nx.Graph()

    for simplex in tri.simplices:
        for i in range(3):
            p1 = tuple(points[simplex[i]])
            p2 = tuple(points[simplex[(i + 1) % 3]])
            if is_edge_valid(p1, p2, image_array, ditch_threshold):
                G.add_edge(p1, p2, weight=np.linalg.norm(np.array(p1) - np.array(p2)))

    return tri, G  # Ensure both values are returned

def astar_pathfinding(graph, start, goal):
    from queue import PriorityQueue

    def heuristic(a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic(start, goal)

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor]['weight']

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set.queue]:
                    open_set.put((f_score[neighbor], neighbor))

    return []  # No path found

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]  # Reverse the path

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
