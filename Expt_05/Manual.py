import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

adj_matrix = np.array([
    [0, 1, 0, 0, 1, 1],
    [1, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0],
])

pos1 = {
    0: (-3,  0),
    1: (-1,  2),
    2: ( 5,  2),
    3: ( 3,  2),
    4: ( 1,  1),
    5: ( 3,  0),
}

def construct_line_graph_manual(adj_matrix):
    print("LINE GRAPH CONSTRUCTION")
    print("\nA line graph L(G) of a graph G:")
    print(" - Each edge in G becomes a vertex in L(G)")
    print(" - Two vertices in L(G) are adjacent if their edges share a common endpoint")

    print("\nAdjacency Matrix:")
    print(adj_matrix)

    n = len(adj_matrix)
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] != 0:
                edges.append((i, j))

    print("\nMETHOD 2: Manual construction without NetworkX function")

    print("\nStep 1: List all edges from original graph")
    print(f"Edges: {edges}")
    print(f"Total edges: {len(edges)}")

    print("\nStep 2: Each edge becomes a vertex in line graph L(G)")
    print(f"Vertices in L(G): {edges}")

    print("\nStep 3: Create empty line graph L(G)")

    print("\nStep 4: Add vertices to L(G)")
    L_G_manual = nx.Graph()
    for edge in edges:
        L_G_manual.add_node(edge)
    print(f"Added {L_G_manual.number_of_nodes()} vertices")

    print("\nStep 5 & 6: Check adjacency (shared vertex condition)")
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            edge1 = edges[i]
            edge2 = edges[j]
            if edge1[0] in edge2 or edge1[1] in edge2:
                L_G_manual.add_edge(edge1, edge2)
                print(f"{edge1} and {edge2} share a vertex -> Add edge")

    print("\nStep 7: Resulting Line Graph L(G)")
    print(f"Vertices: {list(L_G_manual.nodes())}")
    print(f"Edges: {list(L_G_manual.edges())}")
    print(f"Number of vertices: {L_G_manual.number_of_nodes()}")
    print(f"Number of edges: {L_G_manual.number_of_edges()}")

    G_manual = nx.Graph()
    G_manual.add_nodes_from(range(n))
    for edge in edges:
        G_manual.add_edge(edge[0], edge[1])

    return G_manual, L_G_manual


def visualize_graphs(G, L_G):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.set_title('Original Graph G', fontsize=14, fontweight='bold')
    nx.draw(G, pos1, ax=ax1, with_labels=True, node_color='lightblue',
            node_size=800, font_size=12, font_weight='bold', edge_color='gray', width=2)

    pos_lg = nx.spring_layout(L_G, seed=42)
    ax2.set_title('Line Graph L(G)', fontsize=14, fontweight='bold')
    nx.draw(L_G, pos_lg, ax=ax2, with_labels=True, node_color='lightcoral',
            node_size=1200, font_size=9, font_weight='bold', edge_color='gray', width=2)

    plt.tight_layout()


G, L_G = construct_line_graph_manual(adj_matrix)
visualize_graphs(G, L_G)
plt.savefig("graph.png")
plt.close()