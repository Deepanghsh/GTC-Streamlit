import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

adj_matrix = np.array([
    [0, 1, 0, 0, 1, 1],
    [1, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0],
])

print("LINE GRAPH CONSTRUCTION")
print("\nA line graph L(G) of a graph G:")
print(" - Each edge in G becomes a vertex in L(G)")
print(" - Two vertices in L(G) are adjacent if their edges share a common endpoint")
print("\nAdjacency Matrix:")
print(adj_matrix)

G = nx.from_numpy_array(adj_matrix)
mapping = {i: i + 1 for i in range(len(adj_matrix))}
G = nx.relabel_nodes(G, mapping)

edge_list = list(G.edges())
edge_labels = {edge: f"e{i+1}" for i, edge in enumerate(edge_list)}

print("\nMETHOD 1: Using NetworkX built-in function")
L = nx.line_graph(G)
print(f"Edges in original graph: {edge_list}")
print(f"Vertices in L(G): {list(L.nodes())}")
print(f"Edges in L(G): {list(L.edges())}")
print(f"Number of vertices: {L.number_of_nodes()}")
print(f"Number of edges: {L.number_of_edges()}")

line_node_labels = {}
for node in L.nodes():
    sorted_node = tuple(sorted(node))
    e_name = edge_labels[sorted_node]
    line_node_labels[node] = f"{e_name}\n{sorted_node}"

pos1 = {
    1: (-3,  0),
    2: (-1,  2),
    3: ( 5,  2),
    4: ( 3,  2),
    5: ( 1,  1),
    6: ( 3,  0),
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.set_title("Original Graph", fontsize=14, fontweight='bold')
nx.draw(G, pos1, ax=ax1, with_labels=True, node_color="skyblue", node_size=800, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos1, edge_labels=edge_labels, ax=ax1, font_color='red', font_weight='bold')

pos2 = nx.spring_layout(L, seed=42)
ax2.set_title("Line Graph L(G)", fontsize=14, fontweight='bold')
nx.draw(L, pos2, ax=ax2, labels=line_node_labels, with_labels=True, node_color="salmon",
        node_size=1500, font_size=7, font_weight='bold')

plt.tight_layout()
plt.savefig("graph.png")
plt.close()