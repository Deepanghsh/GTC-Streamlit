import networkx as nx
import matplotlib.pyplot as plt

def havel_hakimi_builtin(degree_sequence):
    if not nx.is_graphical(degree_sequence):
        print("Not Graphical Sequence")
        return

    G = nx.havel_hakimi_graph(degree_sequence)

    plt.figure(figsize=(6, 6))
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightgreen',
            node_size=800, edge_color='blue', width=2)
    plt.title(f"Graph using Built-in Havel-Hakimi\nSequence: {degree_sequence}")
    plt.savefig("graph.png")
plt.close()


seq = [2, 2, 2, 2, 2, 2, 2, 2]
havel_hakimi_builtin(seq)