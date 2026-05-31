import networkx as nx
import matplotlib.pyplot as plt

def solve_greedy_with_nx(matrix, labels, pos):
    G = nx.Graph()
    n = len(matrix)
    
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                G.add_edge(labels[i], labels[j])

    coloring = nx.greedy_color(G, strategy='DSATUR')

    unique_colors = sorted(set(coloring.values()))
    num_colors = len(unique_colors)
    print(f"\nColors used: {num_colors}")

    color_palette = ['red', 'blue', 'green', 'orange', 'yellow', 'purple']
    color_map = {val: color_palette[i % len(color_palette)] for i, val in enumerate(unique_colors)}

    print("Node coloring assignment (NetworkX DSATUR):")
    for node, color_id in sorted(coloring.items()):
        print(f"  {node}: color {color_map[color_id]}")

    violations = []
    for u, v in G.edges():
        if coloring[u] == coloring[v]:
            violations.append((u, v))
    if violations:
        print(f"\n  Coloring violations found: {violations}")
    else:
        print("\n Valid coloring — no adjacent nodes share a color!")

    node_colors = [color_map[coloring[node]] for node in G.nodes()]

    plt.figure(figsize=(10, 7))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=1000,
        font_weight='bold',
        font_size=11,
        font_color='white',  
        edge_color='black',
        width=1.5
    )
    plt.title(f"DSATUR Graph Coloring — {num_colors} colors used", fontsize=14)
    plt.tight_layout()
    plt.savefig("graph.png")
plt.close()


if __name__ == "__main__":
    graph_g4 = [
        [0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 0],
    ]

    node_labels = {0: 'Vc', 1: 'V1', 2: 'V2', 3: 'V3', 4: 'V4', 5: 'V5', 6: 'V6'}

    pos_g4 = {
        'Vc': (0, 0),
        'V1': (-0.5, 0.86),
        'V2': (0.5, 0.86),
        'V3': (1, 0),
        'V4': (0.5, -0.86),
        'V5': (-0.5, -0.86),
        'V6': (-1, 0)
    }

    solve_greedy_with_nx(graph_g4, node_labels, pos_g4)