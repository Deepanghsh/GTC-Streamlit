import networkx as nx
import networkx.algorithms.approximation as approx
import matplotlib.pyplot as plt


def build_graph_from_adjacency(matrix):
    G = nx.Graph()
    n = len(matrix)
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                G.add_edge(i, j)
    return G


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
pos_d = {0: (0.5, 2.5), 6: (-1, 1.8), 5: (-1.5, 0.5),
         1: (2, 1.5), 2: (2.5, 0.2), 4: (0.2, -1), 3: (1.5, -1)}


def find_hamiltonian_nx(G):
    nodes = list(G.nodes())
    n = len(nodes)

    complete_G = nx.complete_graph(nodes)
    for u, v in complete_G.edges():
        complete_G[u][v]['weight'] = 1 if G.has_edge(u, v) else 1000

    try:
        cycle = approx.traveling_salesman_problem(complete_G, weight='weight')
        total_weight = sum(
            complete_G[cycle[i]][cycle[i + 1]]['weight']
            for i in range(len(cycle) - 1)
        )
        if total_weight == n:
            return cycle
    except Exception:
        pass
    return None


def draw_hamiltonian_steps_two_graphs(graphs, names, poses):
    data = []
    max_steps = 0
    for matrix in graphs:
        G = build_graph_from_adjacency(matrix)
        cycle = find_hamiltonian_nx(G)
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

    for r, (matrix, name, pos, steps) in enumerate(zip(graphs, names, poses, data)):
        G = build_graph_from_adjacency(matrix)
        if not steps:
            ax = axes[r][0]
            nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue',
                    node_size=500, edge_color='lightgray', width=1)
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
            nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue',
                    node_size=500, edge_color='lightgray', width=1)
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


if __name__ == "__main__":
    for name, matrix in [("Graph (a)", graph_c), ("Graph (b)", graph_d)]:
        G = build_graph_from_adjacency(matrix)
        cycle = find_hamiltonian_nx(G)
        if cycle:
            print(f"{name}: Hamiltonian circuit exists.")
            print(f"{name} Cycle: {cycle}")
        else:
            print(f"{name}: No Hamiltonian circuit found.")

    draw_hamiltonian_steps_two_graphs(
        [graph_c, graph_d],
        ["Graph (a)", "Graph (b)"],
        [pos_c, pos_d]
    )