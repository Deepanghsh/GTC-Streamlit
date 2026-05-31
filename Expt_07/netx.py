import networkx as nx
import matplotlib.pyplot as plt

def dijkstra_builtin(edges, start_node):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    distances, paths = nx.single_source_dijkstra(G, start_node)

    print("Shortest Distances:")
    for node in sorted(distances):
        print(f"{start_node} -> {node} = {distances[node]}")

    pos = {
        0: (0, 2), 1: (2, 1.5), 2: (4, 2),
        3: (0.5, 0.5), 4: (3, 0.5),
        5: (1.5, -0.5), 6: (4.5, -0.5)
    }

    plt.figure(figsize=(10, 6))
    
    nx.draw(G, pos, with_labels=True, node_color='lightgreen',
            node_size=1000, font_size=12, font_weight='bold')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    path_edges = []
    for target in paths:
        path = paths[target]
        for i in range(len(path) - 1):
            path_edges.append((path[i], path[i+1]))

    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title(f"Built-in Dijkstra from Node {start_node}")
    plt.axis('off')
    plt.savefig("graph.png")
plt.close()


graph_edges = [
    (0, 1, 7), (0, 3, 5), (1, 2, 8), (1, 3, 9), (1, 4, 7),
    (2, 4, 5), (3, 4, 15), (3, 5, 6), (4, 5, 8), (4, 6, 9), (5, 6, 11)
]

dijkstra_builtin(graph_edges, 0)