import networkx as nx
# weighted MultiGraph
M = nx.MultiGraph()
M.add_edge(1,2,weight=7)
M.add_edge(1,2,weight=19)
M.add_edge(2,3,weight=42)

# create weighted graph from M
G = nx.Graph()
for u,v,data in M.edges_iter(data=True):
    w = data['weight'] if 'weight' in data else 1.0
    if G.has_edge(u,v):
        G[u][v]['weight'] += w
    else:
        G.add_edge(u, v, weight=w)

print G.edges(data=True)
# [(1, 2, {'weight': 26}), (2, 3, {'weight': 42})]


def convert_multigraph(mg):



