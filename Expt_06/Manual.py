import matplotlib.pyplot as plt
import networkx as nx

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]: self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]: self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            return True
        return False

def visualize_mst_only(n, edges):
    G = nx.Graph()
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    
    pos = {1:(0,1), 2:(1,2), 3:(1,0), 4:(2,1), 5:(2,-1), 6:(3,2), 7:(3,0), 8:(4,1)}

    edges.sort(key=lambda x: x[2])
    dsu = DSU(n)
    mst_edges = []
    total_cost = 0
    
    steps_to_show = n - 1
    cols = 4
    rows = (steps_to_show + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(18, 4 * rows), constrained_layout=True)
    axes = axes.flatten()
    plot_idx = 0

    for u, v, weight in edges:
        if dsu.union(u, v):
            mst_edges.append((u, v))
            total_cost += weight
            ax = axes[plot_idx]
            
            nx.draw_networkx_nodes(G, pos, node_color='lightblue', edgecolors='black', node_size=250, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), edge_color='lightgray', width=0.5, style='dashed', ax=ax)
            
            # Draw current MST edges in green
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2, ax=ax)
            
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', width=3, ax=ax)

            ax.set_title(f"Step {plot_idx+1}: Added {u}-{v}({weight})\nTotal Cost: {total_cost}", fontsize=10)
            ax.axis('off')
            plot_idx += 1
            
        if plot_idx == steps_to_show:
            break

    for j in range(plot_idx, len(axes)):
        axes[j].axis('off')
        
    plt.savefig("graph.png")
plt.close()

graph_edges = [(1,2,6), (1,3,7), (2,3,8), (2,4,9), (2,6,14), (3,4,5), (3,5,4), (4,5,6), (4,6,10), (5,7,7), (6,7,11), (6,8,8), (7,8,6)]
visualize_mst_only(8, graph_edges)