import matplotlib.pyplot as plt
import networkx as nx

def visualize_kruskal_nx(n, edges):
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    
    pos = {1: (0, 1), 2: (1, 2), 3: (1, 0), 4: (2, 1), 
           5: (2, -1), 6: (3, 2), 7: (3, 0), 8: (4, 1)}

    edges.sort(key=lambda x: x[2])
    
    MST_G = nx.Graph()
    MST_G.add_nodes_from(range(1, n + 1))
    
    mst_edges = []
    rejected_edges = []
    total_cost = 0
    
    fig, axes = plt.subplots(4, 4, figsize=(18, 15), constrained_layout=True)
    axes = axes.flatten()

    for i, (u, v, weight) in enumerate(edges):
        ax = axes[i]
        is_added = False
        
        if not nx.has_path(MST_G, u, v):
            MST_G.add_edge(u, v, weight=weight)
            mst_edges.append((u, v))
            total_cost += weight
            is_added = True
        else:
            rejected_edges.append((u, v))

        components = list(nx.connected_components(MST_G))
        color_map = {}
        for idx, comp in enumerate(components):
            for node in comp:
                color_map[node] = idx
        
        node_colors = [color_map[node] for node in range(1, n + 1)]

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=plt.cm.Pastel1, 
                               edgecolors='black', node_size=300, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), edge_color='lightgray', 
                               width=0.5, style='dashed', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=rejected_edges, edge_color='red', width=1, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', width=4, ax=ax)

        status = "ADDED" if is_added else "REJECTED"
        ax.set_title(f"Step {i+1}: {u}-{v}(w:{weight})\n{status} | Total Cost: {total_cost}", fontsize=10)
        ax.axis('off')

    for j in range(len(edges), len(axes)):
        axes[j].axis('off')

    plt.suptitle("Kruskal's Algorithm (NetworkX Components & Cost)", fontsize=20)
    plt.savefig("graph.png")
plt.close()

graph_edges = [
    (1, 2, 6), (1, 3, 7), (2, 3, 8), (2, 4, 9), (2, 6, 14),
    (3, 4, 5), (3, 5, 4), (4, 5, 6), (4, 6, 10), (5, 7, 7),
    (6, 7, 11), (6, 8, 8), (7, 8, 6)
]

visualize_kruskal_nx(8, graph_edges)