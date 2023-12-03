import osmnx as ox
import os
from config import ROOT_DIR

# Use this citation when referencing OSMnx in work
# Boeing, G. 2017. OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks.
# Computers, Environment and Urban Systems 65, 126-139.

path_map_munich = os.path.join(ROOT_DIR, "data", "map_munich.graphml")

def plot_basemap():
    """
    Create a base map of munich, add detector data pulled with pull_static_mobilithek.py
    and plot the resulting graph
    """
    # Create/load base map
    if not os.path.exists(path_map_munich):
        graph = ox.graph_from_place("Munich, Bavaria, Germany", network_type="drive", simplify=True)
        ox.save_graphml(graph, path_map_munich)
    else:
        graph = ox.load_graphml(path_map_munich)

    #graph base map
    _ = ox.plot_graph(graph,
                      node_size=0, node_color="black",
                      edge_linewidth=0.3, edge_color="white")
