import networkx as nx
import matplotlib.pyplot as plt

def has_coloring_conflict(graph, colors, node, color):
    for neighbor, is_connected in enumerate(graph[node]):
        if is_connected and colors[neighbor] == color:
            return True
    return False

def find_greedy_coloring(graph):
    n = len(graph)
    colors = [-1] * n
    colors[0] = 1 
    for u in range(1, n):
        color = 1
        while has_coloring_conflict(graph, colors, u, color):
            color += 1
        colors[u] = color
    return colors

def draw_coloring_result(graph, node_labels, pos, title):
    G = nx.Graph()
    n = len(graph)
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                G.add_edge(node_labels[i], node_labels[j])

    color_map_indices = find_greedy_coloring(graph)
    
    color_palette = ['red', 'blue', 'green', 'orange', 'yellow', 'purple']
    
    print("\nNode coloring assignment (Manual Greedy):")
    for i in range(n):
        assigned_num = color_map_indices[i]
        color_name = color_palette[(assigned_num - 1) % len(color_palette)]
        print(f"  {node_labels[i]}: color {color_name}")

    node_colors = [color_palette[(color_map_indices[i] - 1) % len(color_palette)] for i in range(n)]

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, font_weight='bold', font_color='white')
    plt.title(title)
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

    labels = {0: 'Vc', 1: 'V1', 2: 'V2', 3: 'V3', 4: 'V4', 5: 'V5', 6: 'V6'}
    pos_g4 = {
        'Vc': (0, 0),
        'V1': (-0.5, 0.86), 'V2': (0.5, 0.86), 'V3': (1, 0),
        'V4': (0.5, -0.86), 'V5': (-0.5, -0.86), 'V6': (-1, 0)
    }

    draw_coloring_result(graph_g4, labels, pos_g4, "Manual Greedy Coloring (Rich Palette)")