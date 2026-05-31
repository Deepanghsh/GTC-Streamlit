import networkx as nx
import matplotlib.pyplot as plt
from typing import Any, Dict, List, Optional


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


def find_hamiltonian_cycle(matrix):
    """Return a Hamiltonian cycle as a node list ending at the start node."""
    n = len(matrix)
    if n == 0:
        return None

    visited = [False] * n
    path = [0]
    visited[0] = True

    def backtrack(current):
        if len(path) == n:
            if matrix[current][path[0]] > 0:
                return path + [path[0]]
            return None

        for nxt in range(n):
            if matrix[current][nxt] > 0 and not visited[nxt]:
                visited[nxt] = True
                path.append(nxt)
                result = backtrack(nxt)
                if result is not None:
                    return result
                path.pop()
                visited[nxt] = False

        return None

    return backtrack(0)


def graph_summary(matrix, name) -> Dict[str, Any]:
    G = build_graph_from_adjacency(matrix)
    n = G.number_of_nodes()
    m = G.number_of_edges()
    degrees = sorted((deg for _, deg in G.degree()), reverse=True)
    components = nx.number_connected_components(G) if n > 0 else 0
    connected = nx.is_connected(G) if n > 0 else True
    min_degree = min(degrees) if degrees else 0

    print(f"{name}: vertices = {n}")
    print(f"{name}: edges = {m}")
    print(f"{name}: connected components = {components}")
    print(f"{name}: connected = {connected}")
    print(f"{name}: degree sequence = {degrees}")
    if n > 2:
        print(f"{name}: minimum vertex degree = {min_degree}")
        print(f"{name}: deg(v) >= 2 for all vertices -> {min_degree >= 2}")

    return {
        "vertices": n,
        "edges": m,
        "components": components,
        "connected": connected,
        "degree_sequence": degrees,
        "min_degree": min_degree,
        "min_degree_condition": min_degree >= 2,
    }


def explain_hamiltonian_reasoning(matrix, name):
    print(f"\n{name}")
    graph_summary(matrix, name)
    n = len(matrix)
    if n == 0:
        print(f"{name}: empty graph, no Hamiltonian circuit exists.")
        return None

    G = build_graph_from_adjacency(matrix)
    if not nx.is_connected(G):
        print(f"{name}: disconnected graph, no Hamiltonian circuit is possible.")
        return None

    print(f"{name}: searching for Hamiltonian circuit...")
    cycle = find_hamiltonian_cycle(matrix)
    if cycle:
        print(f"{name}: Hamiltonian circuit exists.")
        print(f"{name} Cycle: {cycle}")
    else:
        print(f"{name}: no Hamiltonian circuit exists.")
    return cycle


def has_hamiltonian_cycle(matrix):
    return find_hamiltonian_cycle(matrix) is not None


def draw_hamiltonian_steps(matrix, name, pos):
    G = build_graph_from_adjacency(matrix)
    cycle = find_hamiltonian_cycle(matrix)
    if not cycle:
        fig, ax = plt.subplots(figsize=(6, 5))
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=500,
                edge_color='lightgray', width=1)
        ax.set_title(f"{name} - No Hamiltonian Circuit")
        ax.axis('off')
        plt.savefig("graph.png")
        plt.close()
        return

    cycle_edges = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]
    total_steps = len(cycle_edges)
    cols = 3
    rows = (total_steps + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    axes = axes.flatten()

    for step_idx in range(total_steps):
        ax = axes[step_idx]
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=500,
                edge_color='lightgray', width=1)

        accepted_edges = cycle_edges[:step_idx]
        current_edge = [cycle_edges[step_idx]]
        if accepted_edges:
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=accepted_edges,
                                   edge_color='green', width=3)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=current_edge,
                               edge_color='blue', width=4)

        u, v = cycle_edges[step_idx]
        ax.set_title(f"Step {step_idx + 1}: {u}-{v}")
        ax.axis('off')

    for extra_ax in axes[total_steps:]:
        extra_ax.axis('off')

    fig.suptitle(f"{name} Hamiltonian Traversal Steps", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("graph.png")
plt.close()


def draw_hamiltonian_steps_two_graphs(graphs, names, poses):
    data = []
    max_steps = 0
    for matrix in graphs:
        cycle = find_hamiltonian_cycle(matrix)
        if cycle:
            steps = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]
        else:
            steps = []
        data.append(steps)
        max_steps = max(max_steps, len(steps))

    rows = len(graphs)
    cols = max_steps if max_steps > 0 else 1
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    if rows == 1:
        axes = [axes]
    for r in range(rows):
        if cols == 1:
            axes[r] = [axes[r]]
        elif rows == 1:
            axes[r] = [axes[r]]

    for r, (matrix, name, pos, steps) in enumerate(zip(graphs, names, poses, data)):
        G = build_graph_from_adjacency(matrix)
        if not steps:
            ax = axes[r][0]
            nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=500,
                    edge_color='lightgray', width=1)
            ax.set_title(f"{name} - No Hamiltonian Circuit")
            ax.axis('off')
            for extra_ax in axes[r][1:]:
                extra_ax.axis('off')
            continue

        for step_idx in range(cols):
            ax = axes[r][step_idx]
            if step_idx >= len(steps):
                ax.axis('off')
                continue
            nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=500,
                    edge_color='lightgray', width=1)
            accepted_edges = steps[:step_idx]
            current_edge = [steps[step_idx]]
            if accepted_edges:
                nx.draw_networkx_edges(G, pos, ax=ax, edgelist=accepted_edges,
                                       edge_color='green', width=3)
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=current_edge,
                                   edge_color='blue', width=4)
            u, v = steps[step_idx]
            ax.set_title(f"{name} Step {step_idx + 1}: {u}-{v}")
            ax.axis('off')

    fig.suptitle("Hamiltonian Traversal Steps for Both Graphs", fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("graph.png")
plt.close()


def draw_hamiltonian_result(matrix, name, pos, axes):
    G = build_graph_from_adjacency(matrix)
    cycle = find_hamiltonian_cycle(matrix)

    nx.draw(G, pos, ax=axes[0], with_labels=True, node_color='lightblue', node_size=500)
    axes[0].set_title(f"{name} - Original Graph")

    if cycle:
        nx.draw(G, pos, ax=axes[1], with_labels=True, node_color='lightblue', node_size=500,
                edge_color='lightgray', width=1)
        accepted_edges = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]
        nx.draw_networkx_edges(G, pos, ax=axes[1], edgelist=accepted_edges,
                               edge_color='green', width=3)
        axes[1].set_title(f"{name} - Hamiltonian Circuit")
    else:
        nx.draw(G, pos, ax=axes[1], with_labels=True, node_color='lightblue', node_size=500,
                edge_color='lightgray', width=1)
        axes[1].set_title(f"{name} - No Hamiltonian Circuit")


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
        explain_hamiltonian_reasoning(graph, name)

    draw_hamiltonian_steps_two_graphs([graph_c, graph_d], ["Graph (a)", "Graph (b)"], [pos_c, pos_d])
