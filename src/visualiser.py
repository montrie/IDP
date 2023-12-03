import osmnx as ox
import os
import pandas as pd
from config import ROOT_DIR
from geopandas import GeoDataFrame
from shapely.geometry import Point
import matplotlib.pyplot as plt


# Use this citation when referencing OSMnx in work
# Boeing, G. 2017. OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks.
# Computers, Environment and Urban Systems 65, 126-139.

path_map_munich = os.path.join(ROOT_DIR, "data", "map_munich.graphml")


def get_basemap(): # -> Union[MultiDiGraph, {edges}]:
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

    return graph

    #graph base map
    # _ = ox.plot_graph(graph,
    #                   node_size=0, node_color="black",
    #                   edge_linewidth=0.3, edge_color="white")


def get_detectors() -> GeoDataFrame:
    # load detector data
    detector_df = pd.read_csv(os.path.join(ROOT_DIR, "data", "default.csv"))

    # create GeoDataFrame
    geometry = [Point(lon, lat) for lon, lat in zip(detector_df['lon'], detector_df['lat'])]
    crs = {'init': 'epsg:4326'}
    detector_gdf = GeoDataFrame(detector_df, crs=crs, geometry=geometry)

    return detector_gdf


def plot():
    map = get_basemap()
    edges = ox.graph_to_gdfs(map, nodes=False)
    points = get_detectors()
    combined = edges

    fig, ax = ox.plot_graph(map,
                            node_size=0, node_color="black",
                            edge_linewidth=0.3, edge_color="white",
                            show=False, close=False)
    points.plot()
    plt.show()
