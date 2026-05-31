import networkx as nx
import matplotlib.pyplot as plt

K5 = nx.Graph()
K5.add_nodes_from([1, 2, 3, 4, 5])
K5.add_edges_from([
    (1,2),(1,3),(1,4),(1,5),
    (2,3),(2,4),(2,5),
    (3,4),(3,5),
    (4,5)
])

C5 = nx.Graph()
C5.add_nodes_from([1, 2, 3, 4, 5])
C5.add_edges_from([
    (1,2),(2,3),(3,4),(4,5),(5,1)
])

P5 = nx.Graph()
P5.add_nodes_from([1, 2, 3, 4, 5])
P5.add_edges_from([
    (1,2),(2,3),(3,4),(4,5)
])

K23 = nx.Graph()
K23.add_nodes_from([1,2,3,4,5])
K23.add_edges_from([
    (1,3),(1,4),(1,5),
    (2,3),(2,4),(2,5)
])

plt.figure(figsize=(10,10))

plt.subplot(2,2,1)
nx.draw(K5, with_labels=True, node_size=800, edge_color='red')
plt.title("K5 (Complete Graph)")

plt.subplot(2,2,2)
nx.draw(C5, with_labels=True, node_size=800)
plt.title("C5 (Cycle Graph)")

plt.subplot(2,2,3)
nx.draw(P5, with_labels=True, node_color="green", node_size=800, edge_color='yellow')
plt.title("P5 (Path Graph)")

plt.subplot(2,2,4)
pos = {}
pos[1] = (0,1)
pos[2] = (1,1)
pos[3] = (0,0)
pos[4] = (1,0)
pos[5] = (2,0)

nx.draw(K23,pos, with_labels=True, node_color="green", node_size=800, edge_color='red')
plt.title("K2,3 (Complete Bipartite Graph)")

plt.savefig("graph.png")
plt.close()