import networkx as nx
import matplotlib.pyplot as plt

nodes = [0, 1, 2, 3, 4, 5, 6, 7]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),(1,7),
    (6, 7), (0, 6), (1, 6), (3, 7), (4, 7), (5, 6),(6,3),
    (0, 2), (2, 4), (3, 5), (4, 0), (5, 1),(7,2)
]

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

pos = {
    0: [-0.5, 0.8], 1: [0.5, 0.8], 2: [1, 0], 3: [0.5, -0.8],
    4: [-0.5, -0.8], 5: [-1, 0], 6: [0, 0.3], 7: [0, -0.3]
}

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

nx.draw(G, pos, ax=axes[0, 0], with_labels=True, node_color='red', edge_color='blue')
axes[0, 0].set_title("Original Graph")

induced_nodes = [0, 1, 5, 6]
g_induced = G.subgraph(induced_nodes)
nx.draw(g_induced, pos, ax=axes[0, 1], with_labels=True, node_color='cyan', edge_color="yellow")
axes[0, 1].set_title("Induced Subgraph")

spanning_edges = [(0, 1), (2, 3), (3, 4), (4, 5), (5, 0), (1, 6), (6, 7)]
g_spanning = nx.Graph()
g_spanning.add_nodes_from(G.nodes())
g_spanning.add_edges_from(spanning_edges)
nx.draw(g_spanning, pos, ax=axes[1, 0], with_labels=True, node_color='yellow', edge_color='blue')
axes[1, 0].set_title("Spanning Subgraph")

to_delete = [(6, 7), (0, 6), (1, 6), (2, 6)]
g_deleted = G.copy()
g_deleted.remove_edges_from(to_delete)
nx.draw(g_deleted, pos, ax=axes[1, 1], with_labels=True, node_color='green', edge_color='red')
axes[1, 1].set_title("Edge Deleted Subgraph")

plt.tight_layout()
plt.savefig("graph.png")
plt.close()