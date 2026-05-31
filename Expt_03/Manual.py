import networkx as nx
import matplotlib.pyplot as plt

nodes = [0, 1, 2, 3, 4, 5, 6, 7]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),(1,7),
    (6, 7), (0, 6), (1, 6), (3, 7), (4, 7), (5, 6),(6,3),
    (0, 2), (2, 4), (3, 5), (4, 0), (5, 1),(7,2)
]

G = nx.Graph()
for n in nodes:
    G.add_node(n)
for u, v in edges:
    G.add_edge(u, v)

pos = {
    0: [-0.5, 0.8], 1: [0.5, 0.8], 2: [1, 0], 3: [0.5, -0.8],
    4: [-0.5, -0.8], 5: [-1, 0], 6: [0, 0.3], 7: [0, -0.3]
}

def create_induced_subgraph(source_graph, node_list):
    sub = nx.Graph()
    for n in node_list:
        sub.add_node(n)
    for u, v in source_graph.edges():
        if u in node_list and v in node_list:
            sub.add_edge(u, v)
    return sub

def create_spanning_subgraph(source_graph, edge_list):
    sub = nx.Graph()
    for n in source_graph.nodes():
        sub.add_node(n)
    for u, v in edge_list:
        if source_graph.has_edge(u, v):
            sub.add_edge(u, v)
    return sub

def create_edge_deleted_subgraph(source_graph, deleted_edges):
    sub = nx.Graph()
    for n in source_graph.nodes():
        sub.add_node(n)
    for u, v in source_graph.edges():
        is_deleted = False
        for du, dv in deleted_edges:
            if (u == du and v == dv) or (u == dv and v == du):
                is_deleted = True
                break
        if not is_deleted:
            sub.add_edge(u, v)
    return sub

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

nx.draw(G, pos, ax=axes[0, 0], with_labels=True, node_color='red', edge_color='blue')
axes[0, 0].set_title("Original Graph")

induced_nodes = [0, 1, 5, 6]
g_induced = create_induced_subgraph(G, induced_nodes)
nx.draw(g_induced, pos, ax=axes[0, 1], with_labels=True, node_color='cyan', edge_color="yellow")
axes[0, 1].set_title("Induced Subgraph")

spanning_edges = [(0, 1), (2, 3), (3, 4), (4, 5), (5, 0), (1, 6), (6, 7)]
g_spanning = create_spanning_subgraph(G, spanning_edges)
nx.draw(g_spanning, pos, ax=axes[1, 0], with_labels=True, node_color='yellow', edge_color='blue')
axes[1, 0].set_title("Spanning Subgraph")

to_delete = [(6, 7), (0, 6), (1, 6), (2, 6)]
g_deleted = create_edge_deleted_subgraph(G, to_delete)
nx.draw(g_deleted, pos, ax=axes[1, 1], with_labels=True, node_color='green', edge_color='red')
axes[1, 1].set_title("Edge Deleted Subgraph")

plt.tight_layout()
plt.savefig("graph.png")
plt.close()