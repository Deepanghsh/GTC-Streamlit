import networkx as nx
import matplotlib.pyplot as plt

def havel_hakimi_final(degree_sequence):
    if sum(degree_sequence) % 2 != 0:
        print("Not Graphical: Odd sum of degrees.")
        return

    nodes = [[deg, i] for i, deg in enumerate(degree_sequence)]
    G = nx.Graph()
    G.add_nodes_from(range(len(degree_sequence)))

    while True:
        nodes.sort(key=lambda x: x[0], reverse=True)
        
        if nodes[0][0] == 0:
            break

        d, u = nodes.pop(0)

        if d > len(nodes):
            print("Not Graphical: Degree too high.")
            return

        for i in range(d):
            nodes[i][0] -= 1
            v = nodes[i][1]
            G.add_edge(u, v)

            if nodes[i][0] < 0:
                print("Not Graphical: Negative degree encountered.")
                return

    # Final Visualization
    plt.figure(figsize=(6, 6))
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=800, edge_color='red', width=2)
    plt.title(f"Final Realized Graph\nSequence: {degree_sequence}")
    plt.savefig("graph.png")
plt.close()

raw = input("Enter degree sequence (space-separated integers): ")
seq = list(map(int, raw.split()))
print(f"Input sequence: {seq}")
havel_hakimi_final(seq)