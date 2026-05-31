import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import isomorphism

plt.figure(figsize=(12,12))

G1 = nx.Graph()
G2 = nx.Graph()

n1 = [1,2,3,4,5,6,7,8]
e1 = {(1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,8),(8,5),(1,5),(4,7)}

n2 = [1,2,3,4,5,6,7,8]
e2 = {(1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,8),(8,5),(1,5),(4,8)}

pos = {
1:(-2,2),2:(2,2),3:(2,-2),4:(-2,-2),
5:(-1,1),6:(1,1),7:(1,-1),8:(-1,-1)
}

G1.add_nodes_from(n1)
G1.add_edges_from(e1)

G2.add_nodes_from(n2)
G2.add_edges_from(e2)

plt.subplot(2,2,1)
nx.draw(G1,pos,with_labels=True,node_size=800)

plt.subplot(2,2,2)
nx.draw(G2,pos,with_labels=True,node_size=800)

GM = isomorphism.GraphMatcher(G1,G2)

if GM.is_isomorphic():
    print("Pair 1 -> ISOMORPHIC")
    print(GM.mapping)
else:
    print("Pair 1 -> NOT ISOMORPHIC")


G3 = nx.Graph()
G4 = nx.Graph()

G3.add_edges_from([(1,2),(2,3),(3,4),(4,5),(5,1)])
G4.add_edges_from([('a','c'),('a','d'),('b','d'),('b','e'),('c','e')])

plt.subplot(2,2,3)
nx.draw(G3,with_labels=True,node_size=800)

plt.subplot(2,2,4)
nx.draw(G4,with_labels=True,node_size=800)

GM2 = isomorphism.GraphMatcher(G3,G4)

if GM2.is_isomorphic():
    print("Pair 2 -> ISOMORPHIC")
    print(GM2.mapping)
else:
    print("Pair 2 -> NOT ISOMORPHIC")

plt.savefig("graph.png")
plt.close()