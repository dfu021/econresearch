
import os 
import geopandas as gp
import numpy as np
import networkx as nx
import osmnx as ox 
import shapely
import json
# import rasterio as rio
import fiona
import pickle
import matplotlib.pyplot as plt
# import momepy
from networkx.algorithms import approximation as approx


# class Node(object):
#     def __init__ (self, x, y):
#         self.idx = idx 
#         self.x = x
#         self.y = y
    
# class Edge(object):
#     def __init__ (self,nodes,speeds = None):
#         self.nodes = nodes
#         self.speeds = speed
#     def get_nodes (self):
#         return(self.nodes[0].idx, self.nodes[1].idx)

# class Path(object):
#     #hold relevant metadata (street type, etc)
#     def __init__ (self, edges = None, properties = None):
#         self.edges = edges
#         if properties = None: 
#             properties = {}
#         self.properties = properties
#     def add_edge(self,edge):
#         self.edges.append(edge)
#     def add_data(self,property,value):
#         self.properties[property] = value

def geojson_to_nx (geojson, graph_name = None):
    f = open('SF2.geojson')
    data = json.load(f)
    G = nx.MultiDiGraph()
    for i in data["features"]: 
        startnodeid = i['properties']['osmstartnodeid']
        startnodecoord = i['geometry']['coordinates'][0]
        endnodeid = i['properties']['osmendnodeid']
        endnodecoord = i['geometry']['coordinates'][-1]
        edgeid = i['properties']['osmwayid']
        edgetype = i['properties']['osmhighway']
        if 'speed_mean_mph' in i['properties']:
            meanspeed = i['properties']['speed_mean_mph']
        else:
            meanspeed = None
        if 'pct_from_freeflow' in i['properties']:
            freeflowpct = i['properties']['pct_from_freeflow']
        else: 
            freeflowpct = None
        if 'speed_freeflow_mph' in i['properties']:
            freeflowspd = i['properties']['speed_freeflow_mph']
        else:
            freeflowspd = None
        G.add_node(startnodeid, coord = "startnodecoord")
        G.add_node(endnodeid, coord = "endnodecoord")
        G.add_edge(startnodeid, endnodeid, wayid = edgeid, type = edgetype, meansp = meanspeed, freeflowp = freeflowpct, freeflowspd = freeflowspd)
    # Get Edge attributes. printing G.edgesonly returns start end?
    # for edge in G.edges: 
    #     print(G.get_edge_data(*edge))
    return G

def graphinfo(G):
    nodenum = G.number_of_nodes()
    edgenum = G.size()
    connectivity = approx.node_connectivity(G)
    avgdegree = nx.k_nearest_neighbors(G)
def nxanalysis (G):
    #all shortest simple path between two nodes
    # paths = {00 : []}
    # for node in G.nodes:
    #     for node2 in G.nodes:
    #         key1 = int(str(node) + str(node2))
    #         #make key that is just two nodeids concatenated together
    #         while True:
    #             try:
    #                 res = nx.all_shortest_paths(G,source = node, target = node2)
    #                 pathlist = [p for p in res]
    #                 break
    #             except nx.exception.NetworkXNoPath:
    #                 pathlist = []
    #         paths[key1] = pathlist 
    #all shortest paths between pairs but not all shortest paths??
    path = dict(nx.all_pairs_shortest_path(G))


SFgraph = geojson_to_nx('SF2.geojson')
graphinfo(SFgraph)
nxanalysis(SFgraph)

