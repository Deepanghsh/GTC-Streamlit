# To implement an algorithm that checks the existence of an Euler circuit and constructs the circuit that traverses every edge of the graph exactly once

import networkx as nx
import matplotlib.pyplot as plt


def is_connected(graph):
    n = len(graph)
    visited = [False] * n

    start = None
    for i in range(n):
        if sum(graph[i]) > 0:
            start = i
            break
    if start is None:
        return True

    stack = [start]
    visited[start] = True
    while stack:
        u = stack.pop()
        for v, edge_count in enumerate(graph[u]):
            if edge_count > 0 and not visited[v]:
                visited[v] = True
                stack.append(v)

    for i in range(n):
        if sum(graph[i]) > 0 and not visited[i]:
            return False
    return True


def has_euler_circuit(graph):
    if not is_connected(graph):
        return False
    for row in graph:
        if sum(row) % 2 != 0:
            return False
    return True


def find_euler_circuit(graph):
    if not has_euler_circuit(graph):
        return None

    g = [row[:] for row in graph]
    n = len(g)
    start = next((i for i, row in enumerate(g) if sum(row) > 0), 0)

    path = [start]
    circuit = []

    while path:
        current = path[-1]
        found = False
        for v in range(n):
            if g[current][v] > 0:
                g[current][v] -= 1
                g[v][current] -= 1
                path.append(v)
                found = True
                break
        if not found:
            circuit.append(path.pop())
    
    return circuit[::-1]


def build_graph_from_adjacency(graph):
    G = nx.Graph()
    n = len(graph)
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] > 0:
                G.add_edge(i, j)
    return G


def draw_euler_result(graph, name, pos, axes):
    G = build_graph_from_adjacency(graph)
    circuit = find_euler_circuit(graph)

    nx.draw(G, pos, ax=axes[0], with_labels=True, node_color='lightgreen', node_size=500)
    axes[0].set_title(f"{name} - Original")

    nx.draw(G, pos, ax=axes[1], with_labels=True, node_color='lightgreen', node_size=500)
    if circuit and len(circuit) > 1:
        circuit_edges = [(circuit[k], circuit[k+1]) for k in range(len(circuit)-1)]
        circuit_edges.append((circuit[-1], circuit[0]))
        nx.draw_networkx_edges(G, pos, ax=axes[1], edgelist=circuit_edges, edge_color='red', width=3)
        axes[1].set_title(f"{name} - Euler Circuit")
    else:
        axes[1].set_title(f"{name} - No Euler Circuit")


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

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Euler Circuit Check for Graph (a) and Graph (b)", fontsize=16)

    draw_euler_result(graph_c, "Graph (a)", pos_c, axes[0])
    draw_euler_result(graph_d, "Graph (b)", pos_d, axes[1])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("graph.png")
plt.close()
