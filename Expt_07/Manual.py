import networkx as nx
import matplotlib.pyplot as plt
import sys

def dijkstra_with_visualization(edges, start_node):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    nodes = sorted(list(G.nodes()))
    n = len(nodes)
    
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    visited = set()
    predecessors = {node: None for node in nodes}

    print(f"{'Step':<5} | {'Pick':<5} | {'Distances (Node 0 to 6)':<35}")
    print("-" * 55)

    step = 1
    while len(visited) < n:
        u = min((node for node in nodes if node not in visited), key=lambda x: distances[x])
        
        if distances[u] == float('inf'):
            break
            
        visited.add(u)

        for v in G.neighbors(u):
            if v not in visited:
                weight = G[u][v]['weight']
                new_dist = distances[u] + weight
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
        
        dist_list = [str(distances[node]) if distances[node] != float('inf') else "∞" for node in nodes]
        print(f"{step:<5} | {u:<5} | {str(dist_list):<35}")
        step += 1

    pos = {
        0: (0, 2), 1: (2, 1.5), 2: (4, 2),
        3: (0.5, 0.5), 4: (3, 0.5),
        5: (1.5, -0.5), 6: (4.5, -0.5)
    }

    plt.figure(figsize=(10, 6))
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=1000, font_size=12, font_weight='bold')
    
    # Draw weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    path_edges = []
    for node, pred in predecessors.items():
        if pred is not None:
            path_edges.append((pred, node))
    
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title(f"Dijkstra Result from Node {start_node} (Shortest Paths in Red)")
    plt.axis('off')
    plt.savefig("graph.png")
plt.close()
graph_edges = [
    (0, 1, 7), (0, 3, 5), (1, 2, 8), (1, 3, 9), (1, 4, 7),
    (2, 4, 5), (3, 4, 15), (3, 5, 6), (4, 5, 8), (4, 6, 9), (5, 6, 11)
]

if __name__ == "__main__":
    dijkstra_with_visualization(graph_edges, start_node=0)