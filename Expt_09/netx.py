import networkx as nx
import matplotlib.pyplot as plt


def build_graph_from_adjacency(matrix):
    """Build an undirected NetworkX graph from an adjacency matrix."""
    G = nx.Graph()
    n = len(matrix)
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                G.add_edge(i, j)
    return G


def has_euler_circuit(matrix):
    """Return True if the adjacency matrix defines an Eulerian graph."""
    G = build_graph_from_adjacency(matrix)
    return nx.is_eulerian(G)


def find_euler_circuit(matrix):
    """Return a node sequence for an Euler circuit or None if none exists."""
    G = build_graph_from_adjacency(matrix)
    if not nx.is_eulerian(G):
        return None

    edges = list(nx.eulerian_circuit(G))
    if not edges:
        return []

    path = [edges[0][0]]
    for u, v in edges:
        path.append(v)
    return path


def draw_euler_result(matrix, name, pos, axes):
    G = build_graph_from_adjacency(matrix)
    circuit = find_euler_circuit(matrix)

    nx.draw(G, pos, ax=axes[0], with_labels=True, node_color='lightgreen', node_size=500)
    axes[0].set_title(f"{name} - Original")

    nx.draw(G, pos, ax=axes[1], with_labels=True, node_color='lightgreen', node_size=500)
    if circuit and len(circuit) > 1:
        circuit_edges = [(circuit[i], circuit[i + 1]) for i in range(len(circuit) - 1)]
        circuit_edges.append((circuit[-1], circuit[0]))
        nx.draw_networkx_edges(G, pos, ax=axes[1], edgelist=circuit_edges, edge_color='red', width=3)
        axes[1].set_title(f"{name} - Euler Circuit")
    else:
        axes[1].set_title(f"{name} - No Euler Circuit")


def draw_two_graphs(graphs, names, poses):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Euler Circuit Check for Graph (a) and Graph (b)", fontsize=16)

    draw_euler_result(graphs[0], names[0], poses[0], axes[0])
    draw_euler_result(graphs[1], names[1], poses[1], axes[1])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("graph.png")
plt.close()


if __name__ == "__main__":
    graph_c = [
        [0, 1, 1, 1, 0],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]

    graph_d = [
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0],
    ]

    pos_c = {0: (0, 2), 4: (-1.5, 0.8), 1: (1.5, 0.8), 3: (-1, -1), 2: (1, -1)}
    pos_d = {0: (0.5, 2.5), 6: (-1, 1.8), 5: (-1.5, 0.5), 1: (2, 1.5), 2: (2.5, 0.2), 4: (0.2, -1), 3: (1.5, -1)}

    for name, graph in [("Graph (a)", graph_c), ("Graph (b)", graph_d)]:
        if has_euler_circuit(graph):
            circuit = find_euler_circuit(graph)
            print(f"{name}: Euler circuit exists.")
            print(f"{name} Circuit:", circuit)
        else:
            print(f"{name}: Euler circuit does not exist.")

    draw_two_graphs([graph_c, graph_d], ["Graph (a)", "Graph (b)"], [pos_c, pos_d])
