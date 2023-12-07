import osmnx as ox
import os
import pandas as pd
import numpy as np
from config import ROOT_DIR
from geopandas import GeoDataFrame
from shapely.geometry import Point, Polygon
from osmnx import settings, utils_graph, io


# Use this citation when referencing OSMnx in work
# Boeing, G. 2017. OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks.
# Computers, Environment and Urban Systems 65, 126-139.

path_map_munich = os.path.join(ROOT_DIR, "static_data", "map_munich.graphml")


def save_graph_shapefile_directional(graph, filepath=None, encoding="utf-8"):
    # default filepath if none was provided
    if filepath is None:
        filepath = os.path.join(ox.settings.data_folder, "graph_shapefile")

    # if save folder does not already exist, create it (shapefiles
    # get saved as set of files)
    if not filepath == "" and not os.path.exists(filepath):
        os.makedirs(filepath)
    filepath_nodes = os.path.join(filepath, "nodes.shp")
    filepath_edges = os.path.join(filepath, "edges.shp")

    # convert undirected graph to gdfs and stringify non-numeric columns
    gdf_nodes, gdf_edges = ox.utils_graph.graph_to_gdfs(graph)
    gdf_nodes = ox.io._stringify_nonnumeric_cols(gdf_nodes)
    gdf_edges = ox.io._stringify_nonnumeric_cols(gdf_edges)
    # We need a unique ID for each edge
    gdf_edges["fid"] = np.arange(0, gdf_edges.shape[0], dtype='int')
    # save the nodes and edges as separate ESRI shapefiles
    gdf_nodes.to_file(filepath_nodes, encoding=encoding)
    gdf_edges.to_file(filepath_edges, encoding=encoding)


def get_base_graphml(): # -> Union[MultiDiGraph, {edges}]:
    """
    Create a base map of munich, add detector static_data pulled with pull_static_mobilithek.py
    and plot the resulting graph
    https://github.com/cyang-kth/osm_mapmatching
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
    # load detector static_data
    detector_df = pd.read_csv(os.path.join(ROOT_DIR, "static_data", "default.csv"))

    # create GeoDataFrame
    geometry = [Point(lon, lat) for lon, lat in zip(detector_df['lon'], detector_df['lat'])]
    crs = {'init': 'epsg:4326'}
    detector_gdf = GeoDataFrame(detector_df, crs=crs, geometry=geometry)

    return detector_gdf


def plot():
    map = get_base_graphml()
    edges = ox.graph_to_gdfs(map, nodes=False)
    points = get_detectors()
    # Add detector static_data to map
    # https://stackoverflow.com/questions/64104884/osmnx-project-point-to-street-segments
    combined = edges.join(points)

    fig, ax = ox.plot_graph(combined,
                            node_size=0, node_color="black",
                            edge_linewidth=0.3, edge_color="white",
                            show=False)
    # points.plot()
    # plt.show()
