import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import isomorphism

def check_isomorphism(G, H, pair_name):
    print(f"Analysis for {pair_name}")
    
    n1, n2 = G.number_of_nodes(), H.number_of_nodes()
    e1, e2 = G.number_of_edges(), H.number_of_edges()
    deg1 = sorted([d for n, d in G.degree()])
    deg2 = sorted([d for n, d in H.degree()])

    print(f"Nodes: {n1} vs {n2} | Edges: {e1} vs {e2}")
    print(f"Degree Sequences match: {deg1 == deg2}")

    GM = isomorphism.GraphMatcher(G, H)
    is_iso = GM.is_isomorphic()
    
    if is_iso:
        print(f"RESULT: {pair_name} is ISOMORPHIC")
        print("Mapping (G -> H):")
        for g_node, h_node in GM.mapping.items():
            print(f"  Node {g_node} maps to {h_node}")
    else:
        print(f"RESULT: {pair_name} is NOT ISOMORPHIC")
    print("\n")
    return is_iso

plt.figure(figsize=(12, 10))

G1 = nx.Graph()
G1.add_edges_from([(1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,8),(8,5),(1,5),(4,7)])
G2 = nx.Graph()
G2.add_edges_from([(1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,8),(8,5),(1,5),(4,8)])

pos_cube = {1:(-2,2), 2:(2,2), 3:(2,-2), 4:(-2,-2), 5:(-1,1), 6:(1,1), 7:(1,-1), 8:(-1,-1)}

G3 = nx.Graph()
G3.add_edges_from([(1,2),(2,3),(3,4),(4,5),(5,1)])
G4 = nx.Graph()
G4.add_edges_from([('a','c'),('a','d'),('b','d'),('b','e'),('c','e')])

plt.subplot(2,2,1); nx.draw(G1, pos_cube, with_labels=True, node_color='lightgreen', node_size=700); plt.title("G1")
plt.subplot(2,2,2); nx.draw(G2, pos_cube, with_labels=True, node_color='lightblue', node_size=700); plt.title("G2")
plt.subplot(2,2,3); nx.draw(G3, with_labels=True, node_color='lightpink', node_size=700); plt.title("G3 (Pentagon)")
plt.subplot(2,2,4); nx.draw(G4, with_labels=True, node_color='lavender', node_size=700); plt.title("G4 (Star Pentagon)")

check_isomorphism(G1, G2, "Pair 1")
check_isomorphism(G3, G4, "Pair 2")

plt.tight_layout()
plt.savefig("graph.png")
plt.close()