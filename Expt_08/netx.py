import networkx as nx
import matplotlib.pyplot as plt


def build_graph_from_adjacency(matrix):
    """Build an undirected NetworkX graph from an adjacency matrix."""
    G = nx.Graph()
    for i in range(len(matrix)):
        G.add_node(i + 1)
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] > 0:
                G.add_edge(i + 1, j + 1)
    return G


def draw_sub_graph(G, pos, path, ax, title, color):
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightgrey',
            edge_color='lightgrey', node_size=500, font_size=10)
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=path, node_color=color, node_size=500)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, edge_color=color, width=3)
    ax.set_title(f"{title}: {path}")


def process_graph(name, matrix, pos, axes):
    """Build the graph and display the same 2x2 plot layout inside provided axes."""
    G = build_graph_from_adjacency(matrix)

    # Compute cycle (closed walk/path)
    cycles = get_cycle_basis(G)
    if cycles:
        cycle = cycles[0] + [cycles[0][0]]
    else:
        cycle = [1, 2, 1]  # dummy cycle if none found

    c_walk = cycle  # closed walk is the cycle

    # Compute closed trail
    trail_edges = list(nx.edge_dfs(G, source=1))
    if trail_edges:
        trail_nodes = [trail_edges[0][0]]
        for u, v in trail_edges:
            if trail_nodes[-1] == u:
                trail_nodes.append(v)
            else:
                trail_nodes.append(u)
        if trail_nodes[0] != trail_nodes[-1]:
            trail_nodes.append(trail_nodes[0])
    else:
        trail_nodes = [1, 2, 1]  # dummy trail

    c_trail = trail_nodes

    draw_sub_graph(G, pos, c_walk, axes[0], "Closed Walk", "orange")
    draw_sub_graph(G, pos, c_trail, axes[1], "Closed Trail", "cyan")
    draw_sub_graph(G, pos, cycle, axes[2], "Cycle (Closed Path)", "green")

    axes[3].axis('off')


def get_cycle_basis(G):
    """Return a list of simple cycles (cycle basis) in the graph."""
    return nx.cycle_basis(G)


def analyze_graph(matrix):
    """Analyze the graph and return built-in NetworkX structural results."""
    G = build_graph_from_adjacency(matrix)
    return {
        "nodes": list(G.nodes()),
        "edges": list(G.edges()),
        "cycle_basis": get_cycle_basis(G),
        "is_connected": nx.is_connected(G),
    }


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

    pos_c = {1: (0, 2), 5: (-1.5, 0.8), 2: (1.5, 0.8), 4: (-1, -1), 3: (1, -1)}
    pos_d = {1: (0.5, 2.5), 7: (-1, 1.8), 6: (-1.5, 0.5), 2: (2, 1.5), 3: (2.5, 0.2), 5: (0.2, -1), 4: (1.5, -1)}

    fig, axes = plt.subplots(2, 4, figsize=(18, 10))
    fig.suptitle("Closed Sequence Analysis: Graph (c) and Graph (d)", fontsize=16)

    process_graph("Graph (c)", graph_c, pos_c, axes=axes[0])

    process_graph("Graph (d)", graph_d, pos_d, axes=axes[1])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("graph.png")
plt.close()
