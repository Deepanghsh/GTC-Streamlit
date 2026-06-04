import streamlit as st
import os
import subprocess
import sys
import glob
import shutil
import tempfile
import base64
import ast
import re

st.set_page_config(
    page_title="CMP-226 Graph Theory and Combinatorics Lab",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f0ede8;
    color: #1a1a1a;
}
[data-testid="stHeader"] {
    display: none;
}
.main .block-container {
    max-width: 1020px;
    padding-top: 5rem;
    padding-bottom: 3rem;
    background-color: #f0ede8;
}
.college-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 0.55rem 1.6rem;
    border: 1px solid #c8c2b8;
    border-top: 3px solid #1a1a1a;
    border-left: none;
    margin-bottom: 1.8rem;
    background: #faf8f5;
    border-radius: 0 2px 2px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    position: fixed;
    top: 0;
    left: 3.5rem;    /* ← leave room for the Streamlit >> sidebar toggle button */
    right: 0;
    z-index: 99999;
    pointer-events: none;
}
.college-header img,
.college-header .ch-divider,
.college-header .ch-text {
    pointer-events: auto;
}
/* Keep the >> sidebar expand button always visible & clickable above the fixed header.
   Only z-index is changed — position is left untouched so the sidebar isn't broken. */
[data-testid="collapsedControl"] {
    z-index: 999999 !important;
}
.college-header .ch-logo {
    flex-shrink: 0;
    width: 46px;
    height: 46px;
    object-fit: contain;
    border-radius: 2px;
}
.college-header .ch-divider {
    width: 1px;
    height: 36px;
    background: #d5cfc6;
    flex-shrink: 0;
}
.college-header .ch-text {
    text-align: left;
}
.college-header .ch-name {
    font-family: 'Source Serif 4', serif;
    font-size: 1.08rem; font-weight: 600; color: #1a1a1a;
    line-height: 1.2;
    margin-bottom: 0.1rem;
}
.college-header .ch-dept {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem; color: #666;
}
.exp-card {
    border: 1px solid #c8c2b8;
    border-radius: 3px;
    margin-bottom: 3.5rem;
    background: #faf8f5;
    overflow: visible;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}
.exp-titlebar {
    display: flex; align-items: center; gap: 1rem;
    background: #1a1a1a;
    padding: 1rem 1.6rem;
    border-radius: 3px 3px 0 0;
}
.exp-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 600;
    background: rgba(255,255,255,0.15); color: #e0dbd4;
    padding: 3px 10px; border-radius: 3px;
    white-space: nowrap; letter-spacing: 0.12em; text-transform: uppercase;
    border: 1px solid rgba(255,255,255,0.22);
}
.exp-title {
    font-family: 'Source Serif 4', serif;
    font-size: 1.08rem; font-weight: 600; color: #ffffff;
}
.exp-date {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 600;
    color: #e0dbd4; white-space: nowrap;
    letter-spacing: 0.1em; text-transform: uppercase;
}
.aim-section {
    padding: 1.1rem 1.6rem 1rem;
    border-bottom: 1px solid #e5e0d8;
}
.theory-section {
    padding: 1.1rem 1.6rem 1rem;
    border-bottom: 1px solid #e5e0d8;
    background: #f7f4ef;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; font-weight: 500; letter-spacing: 0.18em;
    text-transform: uppercase; color: #bbb; margin-bottom: 0.45rem;
}
.section-text { font-size: 0.93rem; color: #444; line-height: 1.75; margin: 0; }
.file-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; font-weight: 500; letter-spacing: 0.13em;
    text-transform: uppercase; color: #aaa;
    padding: 0.9rem 1.6rem 0.3rem;
    border-top: 1px solid #e5e0d8;
}
.output-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; font-weight: 500; letter-spacing: 0.15em;
    text-transform: uppercase; color: #bbb;
    padding: 0.5rem 1.6rem 0.2rem;
}
.conclusion-section {
    padding: 1.1rem 1.6rem 1.2rem;
    border-top: 1px solid #e5e0d8;
    background: #f4f0ea;
    border-radius: 0 0 3px 3px;
}
.conclusion-text {
    font-family: 'Source Serif 4', serif;
    font-size: 0.95rem; color: #555; line-height: 1.75;
    margin: 0; font-style: italic;
}
.gtc-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 999;
    text-align: center;
    padding: 0.55rem 1.5rem;
    background: #1a1a1a;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; color: #c8c2b8; letter-spacing: 0.08em;
    display: flex; align-items: center; justify-content: center; gap: 1.5rem;
}
.gtc-footer span { opacity: 0.45; }

/* ── Per-experiment tab navbar ───────────────────────── */
.exp-card .stTabs [data-baseweb="tab-list"] {
    background: #242424;
    border-radius: 0;
    gap: 0;
    padding: 0 1.2rem;
    border-bottom: 2px solid #3a3a3a;
}
.exp-card .stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #aaa;
    padding: 0.65rem 1.2rem;
    border-radius: 0;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: color 0.18s, border-color 0.18s;
}
.exp-card .stTabs [aria-selected="true"] {
    color: #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
    background: transparent !important;
}
.exp-card .stTabs [data-baseweb="tab"]:hover {
    color: #ddd;
    border-bottom-color: #666;
}
.exp-card .stTabs [data-baseweb="tab-panel"] {
    padding: 1.2rem 1.6rem 1.4rem;
    background: #faf8f5;
}
.exp-card .stTabs [data-baseweb="tab-highlight"] {
    display: none;
}
/* wrap the tab area inside the card dark header */
.exp-tab-wrapper {
    border: 1px solid #c8c2b8;
    border-radius: 3px;
    margin-bottom: 3.5rem;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}
/* Run panel */
.run-panel {
    background: #f0ede8;
    border: 1px solid #d5cfc6;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.2rem;
}
.run-panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; font-weight: 500; letter-spacing: 0.18em;
    text-transform: uppercase; color: #999;
    margin-bottom: 0.5rem;
}
/* Style the run button */
div[data-testid="stButton"] > button[kind="primary"] {
    background: #1a1a1a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.4rem !important;
    transition: background 0.18s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #333 !important;
}
</style>
""", unsafe_allow_html=True)

EXPERIMENTS = [
    {
        "key": "Expt_01", "num": 1, "date": "28/01/2026",
        "name": "Basic Graphs",
        "aim": "To implement basic graphs such as Complete Graph (Kₙ), Cycle Graph (Cₙ), Path Graph (Pₙ) and Complete Bipartite Graph (Kₘ,ₙ).",
        "theory": (
            "A Graph G is formally defined as an ordered pair G = (V, E), consisting of a set V of vertices (or nodes) and a set E of edges, which represent the connections between pairs of vertices.\n\n"
            "The Complete Graph (Kₙ) is a simple undirected structure where every possible pair of distinct vertices is connected by a unique edge. "
            "The K₅ graph is initialized with nodes {1, 2, 3, 4, 5}. Its structural density is maximized, resulting in a total of n(n-1)/2 edges. For 5 nodes, this equals 10 connections.\n\n"
            "The Cycle Graph (Cₙ) represents a sparse and symmetric topology where vertices are linked in a closed chain. "
            "The C₅ graph connects nodes in a continuous loop: (1→2→3→4→5→1). Every single vertex maintains a degree of exactly two.\n\n"
            "Path Graph (Pₙ) is similar to the cycle but lacking the closing connection. "
            "The P₅ structure follows a linear sequence (1→2→3→4→5). Internal nodes (2, 3, 4) have a degree of two, while the two end nodes (1 and 5) have a degree of only one because they do not loop back to complete a circuit.\n\n"
            "Complete Bipartite Graph (Kₘ,ₙ): The Bipartite Graph is characterized by the division of vertices into two disjoint and independent sets, U and V. "
            "The defining property is that every edge connects a vertex from U to one in V. No edges exist between vertices within the same set.\n\n"
            "NetworkX Functions — nx.Graph(): Initializes a new, empty undirected graph object. add_nodes_from(): Adds a list of nodes to the graph. "
            "add_edges_from(): Defines relationships between nodes using a list of tuples, automatically creating connections. "
            "nx.draw(): Acts as a wrapper for Matplotlib mapping nodes and edges onto axes. Uses parameters like with_labels=True, node_size=800, node_color='red'.\n\n"
            "Matplotlib Functions — plt.figure(figsize=(...)): Initializes the main window, setting dimensions (10x10 inches) so four subplots are legible. "
            "plt.subplot(rows, cols, index): Activates a specific grid position before plotting. plt.title(): Assigns a label to the active subplot. plt.show(): Renders the final figure window."
        ),
        "conclusion": "Basic graphs — Complete (K₅), Cycle (C₅), Path (P₅), and Complete Bipartite (K₃,₃) — were successfully implemented using NetworkX and visualised with Matplotlib. The structural properties such as degree, edge count and adjacency were verified to match their respective theoretical definitions.",
    },
    {
        "key": "Expt_02", "num": 2, "date": "05/02/2026",
        "name": "Graph Isomorphism Verification",
        "aim": "To implement graph isomorphism verification in order to compare structural equivalence of two graphs.",
        "theory": (
            "Two graphs G and H are identical (G = H) if V(G) = V(H), E(G) = E(H). If two graphs are identical they can be represented by identical diagrams. "
            "However, it is also possible for graphs that are not identical to have essentially the same diagram — such graphs are isomorphic.\n\n"
            "Two graphs G and H are isomorphic (G ≅ H) if there exist bijections θ : V(G)→V(H) and φ : E(G)→E(H) such that an edge e connects u and v in G if and only if φ(e) connects θ(u) and θ(v) in H. "
            "Such a pair (θ, φ) is called an isomorphism between G and H. Since we are primarily interested in structural properties, we often omit labels when drawing graphs.\n\n"
            "NetworkX Functions — nx.Graph(): Initializes a new undirected graph. add_nodes_from(): Adds multiple nodes (1 through 16). add_edges_from(): Adds edges from a list of tuples. "
            "G.nodes(): Returns all nodes. G.degree(): Returns the degree for each node. G.neighbors(u): Returns all nodes connected to u. G.has_edge(u, v): Returns True if an edge exists.\n\n"
            "Adjacency: nx.to_numpy_array(): Converts the graph adjacency structure into a 2D NumPy array.\n\n"
            "Isomorphism Testing — nx.is_isomorphic(G1, G2): Returns True if two graphs are structurally identical. "
            "nx.isomorphism.vf2pp_isomorphism(G1, G2): Implements the VF2++ algorithm to find the specific node-to-node mapping that proves isomorphism.\n\n"
            "Matplotlib Functions — plt.figure(figsize=(18, 6)): Creates the main window. plt.subplot(1, 3, n): Selects the nth slot in a 1×3 grid. "
            "plt.title(): Adds a text label to each plot. plt.tight_layout(): Adjusts spacing between subplots. plt.show(): Displays the final visualizations. "
            "nx.draw(G, pos, ...): Primary drawing command. pos: Dictionary of node coordinates. with_labels=True: Prints node numbers. node_color: Sets fill color. font_weight='bold': Makes labels easier to read."
        ),
        "conclusion": "Verification of graph isomorphism was successfully implemented using the VF2++ algorithm. The program correctly determines whether two graphs are structurally equivalent and outputs the bijective vertex mapping when they are isomorphic.",
    },
    {
        "key": "Expt_03", "num": 3, "date": "12/02/2026",
        "name": "Generation of Various Subgraphs",
        "aim": "To implement generation of various subgraphs such as induced subgraphs, spanning subgraphs and edge-deleted subgraphs.",
        "theory": (
            "A graph H is a subgraph of G if the vertex set of H is a subset of the vertex set of G, the edge set of H is a subset of the edge set of G, and the endpoints of edges in H are the same as in G. "
            "If H is a subgraph of G but is not equal to G, it is called a proper subgraph.\n\n"
            "Spanning Subgraph: A spanning subgraph includes every vertex of the original graph. Even if edges are removed, the total number of vertices remains identical to the original graph.\n\n"
            "Induced Subgraph: An induced subgraph is formed by taking a subset of vertices from the original graph and including every edge that connects those specific vertices in the original graph. This is often referred to as a vertex-induced subgraph.\n\n"
            "Edge-Induced Subgraph: An edge-induced subgraph is formed by taking a subset of edges from the original graph. The vertex set of this subgraph consists of only the vertices that are endpoints of the chosen edges.\n\n"
            "Graph Operations — Vertex deletion: Removes a vertex and all edges connected to it. Edge deletion: Removes a specific edge while keeping all original vertices, creating a spanning subgraph.\n\n"
            "NetworkX Functions — nx.Graph(): Initializes a new undirected graph. add_edges_from(edges): Adds multiple edges at once. add_nodes_from(nodes): Adds nodes ensuring all original vertices are present. "
            "G.copy(): Creates a complete copy allowing modifications without affecting the base graph. remove_edges_from(edges): Removes specific edges. remove_nodes_from(nodes): Removes nodes and all their incident edges. "
            "has_edge(u, v): Checks if a connection exists between two nodes.\n\n"
            "Matplotlib Functions — plt.figure(figsize=(w, h)): Sets up the drawing area. plt.subplot(rows, cols, index): Creates a grid of plots for side-by-side comparison. "
            "nx.draw(): Renders the graph. pos: Predefined coordinates to keep nodes in the same position across subgraphs. with_labels=True: Displays node numbers. node_color: Assigns colors to differentiate subgraph types. "
            "plt.tight_layout(): Adjusts spacing so titles and labels do not overlap. plt.show(): Renders and displays the final window."
        ),
        "conclusion": "Subgraphs — spanning subgraph, induced subgraph, and edge-deleted subgraph — were successfully generated from the original graph using NetworkX operations. The structural differences and preservation of vertex/edge sets were clearly demonstrated through side-by-side visualisations.",
    },
    {
        "key": "Expt_04", "num": 4, "date": "19/02/2026",
        "name": "Degree Sequence & Havel-Hakimi Algorithm",
        "aim": "To check if the given degree sequence is graphical or not graphical using Handshaking Lemma and Havel-Hakimi Theorem.",
        "theory": (
            "The Degree of a Vertex: The degree of a vertex is the number of edges connected to it. According to the Handshaking Lemma, the sum of all vertex degrees in a graph is equal to twice the number of edges: Σ deg(v) = 2|E|. "
            "This implies that the sum of degrees must always be an even number, and the number of vertices with an odd degree must also be even.\n\n"
            "Degree Sequences: A degree sequence is a list of the degrees of all vertices in a graph, typically written in non-increasing order. "
            "While any graph has a degree sequence, not every sequence of integers can form a simple graph (a graph without loops or multiple edges).\n\n"
            "Graphical Sequences: A sequence is called graphical if there exists a simple graph that corresponds to that specific degree sequence. "
            "To determine if a sequence is graphical, it must satisfy parity requirements and specific structural constraints.\n\n"
            "The Havel-Hakimi Algorithm is a recursive method used to determine if a degree sequence is graphical:\n"
            "(1) Remove the largest degree from the sequence. (2) Subtract 1 from the next largest degrees in the remaining sequence. "
            "(3) Sort the new sequence and repeat. If the process results in all zeros, the sequence is graphical. If negative numbers appear, it is not graphical.\n\n"
            "NetworkX Functions — nx.Graph(): Initializes a new undirected graph. G.add_nodes_from(range(len(degree_sequence))): Adds nodes based on the input sequence length. "
            "G.add_edge(u, v): Creates a connection between two nodes. nx.spring_layout(G, seed=42): Computes a visually balanced position using a force-directed algorithm.\n\n"
            "Standard Python Logic — sum(sequence) % 2 != 0: Checks the Handshaking Lemma (parity check). sorted(sequence, reverse=True): Keeps the sequence in non-increasing order. nodes.pop(0): Removes the node with the highest degree."
        ),
        "conclusion": "The Handshaking Lemma (parity check) and the Havel-Hakimi algorithm were successfully implemented to determine whether a given degree sequence is graphical. The program correctly classifies the sequence and, when graphical, constructs and visualises a realising graph.",
    },
    {
        "key": "Expt_05", "num": 5, "date": "12/03/2026",
        "name": "Line Graph Conversion",
        "aim": "To implement conversion of a given graph into a line graph L(G) where each vertex represents an edge of the original graph, and adjacency reflects shared endpoints.",
        "theory": (
            "Definition of a Line Graph: The Line Graph L(G) (also known as the adjoint, conjugate, or derivative graph) follows two fundamental rules:\n"
            "Vertex Correspondence: Each edge in the original graph G represents exactly one vertex in the line graph L(G).\n"
            "Adjacency Rule: Two vertices in L(G) are connected by an edge if and only if their corresponding edges in G share a common endpoint (i.e., they are incident to the same vertex).\n\n"
            "Objective: To understand the properties of a Line Graph L(G) and implement its construction from an original graph G using both manual algorithmic steps and built-in library functions.\n\n"
            "Mathematical Observations: |V(L(G))| = |E(G)|. Using a spring layout, the line graph typically appears more dense than the original graph because high-degree nodes in G create cliques (complete subgraphs) in L(G).\n\n"
            "Method A — Manual Construction: (1) Edge Extraction: Iterate through the adjacency matrix to identify all existing edges. "
            "(2) Node Mapping: Create a new graph where each identified edge is added as a node. "
            "(3) Connectivity Check: Compare every pair of edges. If they share a common vertex index, an edge is added between them in the new graph.\n\n"
            "Method B — Library-Based Construction: Using nx.line_graph(G), the software internally maps the edge-to-vertex transitions, providing a benchmark for the manual method.\n\n"
            "Code Structure — get_adjacency_matrix(): Handles user input for the graph structure. construct_line_graph_manual(): Implements the step-by-step logic. visualize_graphs(): Uses matplotlib to display the side-by-side comparison of G and L(G)."
        ),
        "conclusion": "Construction of the line graph L(G) using both manual algorithmic steps and the built-in NetworkX nx.line_graph() function was successfully implemented. Both methods produced identical results, confirming the correctness of the manual construction based on the shared-endpoint adjacency rule.",
    },
    {
        "key": "Expt_06", "num": 6, "date": "02/04/2026",
        "name": "Minimum Spanning Tree — Kruskal's Algorithm",
        "aim": "To implement finding the minimum spanning tree for a given graph using Kruskal's algorithm, ensuring all vertices are connected with the minimum possible total edge weight and without forming cycles.",
        "theory": (
            "Definition of a Tree: A tree is a connected graph that contains no cycles (it is acyclic). A key property of any tree is that the number of edges is always exactly one less than the number of vertices. "
            "If a graph is acyclic but not necessarily connected, it is called a forest.\n\n"
            "Spanning Trees: A spanning tree is a subgraph that includes all the vertices of the original graph and is also a tree. Every connected graph contains at least one spanning tree. "
            "If you add any edge to a spanning tree, you will create exactly one cycle.\n\n"
            "Kruskal's Algorithm (Greedy MST):\n"
            "(1) List all edges in increasing order of their weights. (2) Select the edge with the smallest weight. "
            "(3) Continue selecting the next smallest edge only if it does not form a cycle with the edges already picked. (4) Stop when (number of vertices - 1) edges have been selected.\n\n"
            "NetworkX Functions — nx.Graph(): Creates a new undirected graph. add_weighted_edges_from(edges_data): Adds edges while assigning a 'weight' attribute to each. "
            "nx.minimum_spanning_tree(G, weight='weight'): Implements an MST algorithm and returns the optimal tree. mst.size(weight='weight'): Calculates the total sum of weights of all MST edges.\n\n"
            "nx.draw_networkx_nodes(): Draws only the vertices. nx.draw_networkx_labels(): Adds text labels to nodes. nx.draw_networkx_edges(): Draws connections — used twice: once with dashed lines for original edges and once with solid lines for MST edges.\n\n"
            "Matplotlib Functions — plt.subplots(rows, cols, figsize=...): Creates the layout for visualization. ax.set_title(): Sets a title for each subplot. ax.axis('off'): Removes X and Y axes to focus purely on the graph. plt.show(): Opens the window to display results."
        ),
        "conclusion": "The Minimum Spanning Tree was successfully found using Kruskal's algorithm via both the NetworkX built-in nx.minimum_spanning_tree() and a manual step-by-step implementation. Each step of the greedy selection was visualised, confirming that the algorithm correctly avoids cycles and minimises total weight.",
    },
    {
        "key": "Expt_07", "num": 7, "date": "09/04/2026",
        "name": "Shortest Path — Dijkstra's Algorithm",
        "aim": "To implement the shortest path algorithm in order to compute the shortest path from the source vertex to all the other vertices in a weighted graph.",
        "theory": (
            "The Shortest Path Problem: In a weighted graph, every edge is assigned a numerical weight representing length, cost, or time. "
            "The shortest path problem aims to find a route between two vertices such that the sum of the weights of the edges on that path is minimized. This is a fundamental problem in network optimization.\n\n"
            "Dijkstra's Algorithm is a greedy algorithm used to find the shortest path from a single source node to all other nodes in a graph with non-negative edge weights. "
            "It works by maintaining a set of vertices whose shortest distance from the source is already known.\n\n"
            "Steps of the Algorithm:\n"
            "(1) Initialize: Set the distance to the source node to 0 and all other nodes to infinity. "
            "(2) Visit: Pick the unvisited node with the smallest current distance. "
            "(3) Update: For the current node, check all its neighbors. If the path through the current node is shorter than the previously recorded distance, update the neighbor's distance. "
            "(4) Repeat: Mark the current node as visited and repeat until all nodes are processed.\n\n"
            "For Dijkstra's algorithm to work correctly, all edge weights must be non-negative. If negative weights are present, the algorithm may fail to find the true shortest path.\n\n"
            "NetworkX Functions — nx.Graph(): Initializes a new undirected graph. add_nodes_from(): Adds nodes (A through G). add_weighted_edges_from(): Adds edges with numerical weights. "
            "nx.shortest_path(G, source, target, weight='weight'): Implements Dijkstra's algorithm to find the minimum-weight path. nx.shortest_path_length(): Calculates the numerical sum of weights along the shortest path.\n\n"
            "Matplotlib Functions — plt.figure(figsize=(w, h)): Sets the output window dimensions. nx.draw(): Renders the graph using pos for node coordinates, with_labels=True for node names, "
            "node_color to differentiate path nodes, edge_color to highlight shortest path edges in red. plt.title(): Adds a label such as 'Dijkstra\'s Shortest Path from A to G'. plt.show(): Displays the final graph."
        ),
        "conclusion": "The shortest path from source vertex A to all other vertices was successfully computed using Dijkstra's algorithm, implemented both with NetworkX's nx.shortest_path() and a manual priority-queue approach. The resulting path and its total weight were highlighted on the graph visualisation.",
    },
    {
        "key": "Expt_08", "num": 8, "date": "30/04/2026",
        "name": "Closed Walks, Trails and Paths",
        "aim": "To implement the generation of closed walks, trails and paths in a connected graph.",
        "theory": (
            "A walk in G is defined as a finite alternating sequence of vertices and edges of the form W = v₀, e₁, v₁, e₂, v₂, …, eₖ, vₖ, "
            "where each edge eᵢ = (vᵢ₋₁, vᵢ) ∈ E for i = 1, 2, …, k. The integer k is called the length of the walk, representing the number of edges. "
            "In a walk, both vertices and edges may be repeated any number of times. Walks are the most general type of traversal in a graph.\n\n"
            "A walk is said to be closed if the initial vertex and the final vertex are the same, that is, v₀ = vₖ. If v₀ ≠ vₖ, the walk is called an open walk.\n\n"
            "A trail is a walk in which all edges are distinct, that is, eᵢ ≠ eⱼ for all i ≠ j. However, vertices may still repeat in a trail. "
            "A trail is said to be closed if v₀ = vₖ; such a closed trail is sometimes referred to as a circuit. If v₀ ≠ vₖ, the trail is called an open trail.\n\n"
            "A path is a walk in which all vertices are distinct, that is, vᵢ ≠ vⱼ for all i ≠ j. As a result, no edge can be repeated in a path. "
            "A path is said to be open if v₀ ≠ vₖ. A closed path is one in which v₀ = vₖ and no other vertices are repeated — such a closed path is called a cycle.\n\n"
            "Every path is a trail and every trail is a walk, but the converse is not necessarily true."
        ),
        "conclusion": "Generation of closed walks, trails and paths in a connected graph was successfully implemented. The program correctly identifies and visualises each type of traversal, demonstrating the distinctions in vertex/edge repetition allowed under each definition.",
    },
    {
        "key": "Expt_09", "num": 9, "date": "30/04/2026",
        "name": "Eulerian Circuit Detection — Fleury's Algorithm",
        "aim": "To implement an algorithm that checks existence of an Eulerian circuit and constructs a circuit that traverses every edge of the graph exactly once.",
        "theory": (
            "Let G = (V, E) be a finite, connected, undirected graph. An Eulerian circuit in G is defined as a closed trail represented by the sequence v₀, e₁, v₁, e₂, …, eₘ, vₘ such that:\n"
            "(1) v₀ = vₘ, which means the circuit starts and ends at the same vertex, forming a closed loop.\n"
            "(2) For each i = 1, 2, …, m, the edge eᵢ connects the vertices vᵢ₋₁ and vᵢ, ensuring consecutive vertices are adjacent.\n"
            "(3) eᵢ ≠ eⱼ for all i ≠ j, which ensures no edge is repeated in the traversal.\n"
            "(4) {e₁, e₂, …, eₘ} = E, which means every edge of the graph is included exactly once in the circuit.\n\n"
            "A connected graph G has an Eulerian circuit if and only if deg(v) ≡ 0 (mod 2) for all v ∈ V — that is, every vertex of the graph has even degree. This is known as Euler's Theorem. "
            "If exactly two vertices have odd degree, then the graph contains an Eulerian path but not an Eulerian circuit.\n\n"
            "Fleury's Algorithm:\n"
            "Step 1: Choose an arbitrary vertex v₀ ∈ V and set w₀ = v₀.\n"
            "Step 2: Suppose that a trail w₀, e₁, w₁, …, eₖ, wₖ has been constructed.\n"
            "Step 3: From the set of edges incident on wₖ, select an edge eₖ₊₁ such that it is not a bridge in the remaining graph, or eₖ₊₁ is the only edge incident on wₖ.\n"
            "Step 4: Let wₖ₊₁ be the vertex adjacent to wₖ via edge eₖ₊₁. Extend the trail by adding eₖ₊₁ and wₖ₊₁, and remove edge eₖ₊₁ from the graph.\n"
            "Step 5: Repeat Steps 2 to 5 until all edges of the graph are removed.\n"
            "Step 6: The resulting sequence w₀, e₁, w₁, …, eₘ, wₘ forms an Eulerian circuit, where w₀ = wₘ and every edge is traversed exactly once."
        ),
        "conclusion": "An algorithm that checks the existence of an Eulerian circuit using Euler's Theorem (all vertices must have even degree) and constructs the circuit using Fleury's Algorithm was successfully implemented. The constructed circuit traverses every edge of the graph exactly once, returning to the starting vertex.",
    },
    {
        "key": "Expt_10", "num": 10, "date": "07/05/2026",
        "name": "Hamiltonian Circuit Detection",
        "aim": "To implement a method that determines whether a graph contains a Hamiltonian Circuit that is a cycle that visits every vertex exactly once except the starting vertex.",
        "theory": (
            "Let G = (V, E) be a finite, connected, undirected graph. A Hamiltonian circuit in G is defined as a closed cycle represented by the sequence v₀, v₁, v₂, …, vₙ₋₁, vₙ such that:\n"
            "(1) v₀ = vₙ — the circuit starts and ends at the same vertex, forming a closed loop.\n"
            "(2) For each i = 1, 2, …, n, the vertices vᵢ₋₁ and vᵢ are adjacent, meaning there exists an edge joining consecutive vertices.\n"
            "(3) vᵢ ≠ vⱼ for all 0 ≤ i < j < n, which ensures no vertex is repeated except the starting and ending vertex.\n"
            "(4) {v₀, v₁, v₂, …, vₙ₋₁} = V, which means every vertex of the graph is included exactly once.\n\n"
            "A graph G is said to be Hamiltonian if it contains a Hamiltonian circuit. "
            "The main objective of a Hamiltonian circuit is to traverse every vertex of the graph exactly once and return to the starting vertex. "
            "Unlike Eulerian circuits which focus on visiting every edge exactly once, Hamiltonian circuits are concerned with visiting every vertex exactly once.\n\n"
            "Finding a Hamiltonian circuit is an NP-complete problem; no known polynomial-time algorithm exists for the general case. "
            "The backtracking approach explores all possible vertex orderings, pruning branches that violate the adjacency or non-repetition constraints.\n\n"
            "A Hamiltonian path is a path that visits every vertex exactly once but does not return to the starting vertex. "
            "If such a path forms a closed loop by connecting the last vertex back to the first, it becomes a Hamiltonian circuit.\n\n"
            "Applications: Travelling Salesman Problem (TSP), circuit board drilling, DNA sequencing, computer networks, scheduling, and routing optimization problems."
        ),
        "conclusion": "A backtracking algorithm that determines whether a graph contains a Hamiltonian circuit was successfully implemented. The program correctly identifies the circuit when one exists and reports its absence otherwise. The found circuit was visualised on the graph, with highlighted edges forming the Hamiltonian path.",
    },
    {
        "key": "Expt_11", "num": 11, "date": "14/05/2026",
        "name": "Graph Coloring — Greedy Algorithm",
        "aim": "To implement graph coloring algorithm that assigns colour to the vertices such that no two adjacent vertices share the same color with minimum chromatic number.",
        "theory": (
            "Graph coloring is a method of assigning colors to the vertices of a graph such that no two adjacent vertices have the same color. Let a graph be represented as G = (V, E) where V = set of vertices and E = set of edges.\n\n"
            "A vertex coloring of a graph is a function C : V → {1, 2, 3, …, k} such that C(u) ≠ C(v) for all (u, v) ∈ E. "
            "This means that if two vertices are connected by an edge, they must be assigned different colors. "
            "The minimum number of colors required to color a graph is called the Chromatic Number, denoted by χ(G):\n"
            "χ(G) = min { k : G can be colored using k colors }\n\n"
            "Greedy Graph Coloring Algorithm (DSatur): The Greedy Coloring Algorithm assigns colors to vertices one by one following a specific order. "
            "For each vertex, the algorithm assigns the smallest available color that has not been used by its adjacent vertices.\n\n"
            "In this method:\n"
            "(1) The vertex having the highest saturation degree is selected first. "
            "(2) Saturation degree is the number of different colors used by adjacent vertices. "
            "(3) If saturation degrees are equal, the vertex with the highest ordinary degree is selected.\n\n"
            "Algorithm Steps:\n"
            "Step 1: Start with all vertices uncolored.\n"
            "Step 2: Select a vertex with highest saturation degree.\n"
            "Step 3: Assign the smallest possible color not used by any adjacent vertex.\n"
            "Step 4: Update the saturation degree of neighboring vertices.\n"
            "Step 5: Repeat Steps 2 to 4 until all vertices are colored.\n"
            "Step 6: Count the total number of colors used. For every edge (u, v) ∈ E, the coloring condition C(u) ≠ C(v) must be satisfied."
        ),
        "conclusion": "The greedy graph coloring algorithm (DSatur) was successfully implemented. Colors were assigned to all vertices such that no two adjacent vertices share the same color. The chromatic number χ(G) was computed and verified, and the coloring was displayed visually with each color represented by a distinct node color.",
    },
]


PATCH_HEADER = """\
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as _plt_module
import os as _os_p

_SAVE_DIR = {save_dir!r}
_fig_counter = [0]

def _patched_show(*a, **kw):
    figs = list(_plt_module.get_fignums())
    if not figs:
        return
    for fnum in figs:
        fig = _plt_module.figure(fnum)
        out = _os_p.path.join(_SAVE_DIR, f'fig_{{_fig_counter[0]}}.png')
        fig.savefig(out, bbox_inches='tight', dpi=130)
        _fig_counter[0] += 1
    _plt_module.close('all')

def _patched_savefig(fname, *a, **kw):
    out = _os_p.path.join(_SAVE_DIR, f'fig_{{_fig_counter[0]}}.png')
    kw.setdefault('bbox_inches', 'tight')
    kw.setdefault('dpi', 130)
    _plt_module.gcf().savefig(out, *a, **kw)
    _fig_counter[0] += 1
    _plt_module.close('all')

import matplotlib.pyplot as plt
plt.show = _patched_show
plt.savefig = _patched_savefig

"""


def run_script(path, stdin_input=""):
    script_dir = os.path.dirname(os.path.abspath(path))
    script_name = os.path.splitext(os.path.basename(path))[0]
    tmp_dir = tempfile.mkdtemp()
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            original = f.read()
        patched_source = PATCH_HEADER.format(save_dir=tmp_dir) + original
        patched_path = os.path.join(tmp_dir, "_patched.py")
        with open(patched_path, "w", encoding="utf-8") as f:
            f.write(patched_source)
        env = os.environ.copy()
        env["MPLBACKEND"] = "Agg"
        result = subprocess.run(
            [sys.executable, patched_path],
            input=stdin_input if stdin_input else None,
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            cwd=script_dir, env=env, timeout=60,
        )
        images = sorted(glob.glob(os.path.join(tmp_dir, "fig_*.png")))
        img_data = []
        for img_path in images:
            dest = os.path.join(script_dir, f"_cached_{script_name}_{os.path.basename(img_path)}")
            shutil.copy2(img_path, dest)
            img_data.append(dest)
        return result.stdout.strip(), result.stderr.strip(), img_data
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with st.sidebar:
    if "selected_exp" not in st.session_state:
        st.session_state.selected_exp = "all"
    if st.button("📋 All Experiments", use_container_width=True):
        st.session_state.selected_exp = "all"
    st.markdown("**Jump to**")
    for meta in EXPERIMENTS:
        if st.button(f"{meta['num']:02d} · {meta['name']}", use_container_width=True, key=f"nav_{meta['key']}"):
            st.session_state.selected_exp = meta["key"]

_logo_path = os.path.join(BASE_DIR, "WhatsApp Image 2026-06-04 at 12.22.52 PM.jpeg")
_logo_b64 = ""
if os.path.exists(_logo_path):
    with open(_logo_path, "rb") as _f:
        _logo_b64 = base64.b64encode(_f.read()).decode()

st.markdown(f"""
<div class="college-header">
    {f'<img class="ch-logo" src="data:image/jpeg;base64,{_logo_b64}" alt="GEC Logo">' if _logo_b64 else ''}
    {'<div class="ch-divider"></div>' if _logo_b64 else ''}
    <div class="ch-text">
        <div class="ch-name">Graph Theory and Combinatorics Lab</div>
        <div class="ch-dept">Department of Computer Engineering &nbsp;·&nbsp; Goa College of Engineering</div>
    </div>
</div>
""", unsafe_allow_html=True)

sel = st.session_state.selected_exp
show_experiments = EXPERIMENTS if sel == "all" else [m for m in EXPERIMENTS if m["key"] == sel]

for meta in show_experiments:
    exp_dir = os.path.join(BASE_DIR, meta["key"])
    results = st.session_state.get(f"ran_{meta['key']}", [])

    st.markdown(f"""
<div class="exp-tab-wrapper">
    <div class="exp-titlebar">
        <span class="exp-badge">Experiment {meta['num']:02d}</span>
        <span class="exp-title">{meta['name']}</span>
        <span class="exp-date">DATE &nbsp;: &nbsp;{meta['date']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

    py_files = sorted(glob.glob(os.path.join(exp_dir, "*.py"))) if os.path.isdir(exp_dir) else []
    has_code = bool(py_files)

    tab_labels = ["📌 Aim", "📖 Theory", "💻 Code", "📊 Output", "✅ Conclusion"]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        st.markdown(f"""
        <div class="section-label" style="margin-top:0.3rem;">Aim</div>
        <p class="section-text">{meta['aim']}</p>
        """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown(f"""
        <div class="section-label" style="margin-top:0.3rem;">Theory</div>
        <p class="section-text">{meta['theory'].replace(chr(10), '<br>')}</p>
        """, unsafe_allow_html=True)

    with tabs[2]:
        if has_code:
            for path in py_files:
                fname = os.path.basename(path)
                st.markdown(f"<div class='file-label' style='padding-left:0;border-top:none;'>&#128196; {fname}</div>", unsafe_allow_html=True)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        st.code(f.read(), language="python")
                except Exception as e:
                    st.error(str(e))
        else:
            st.warning(f"No Python files found in `{meta['key']}/`.")

    with tabs[3]:
        ck = f"ran_{meta['key']}"
        results = st.session_state.get(ck, [])

        if has_code:
            # ── Collect all input() prompts across every file in this experiment
            all_prompts = []   # list of (file_index, prompt_index, prompt_str, widget_key)
            for fi, path in enumerate(py_files):
                try:
                    src = open(path, "r", encoding="utf-8", errors="replace").read()
                    tree = ast.parse(src)
                    pi = 0
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            fn = node.func
                            is_input = (
                                (isinstance(fn, ast.Name) and fn.id == "input") or
                                (isinstance(fn, ast.Attribute) and fn.attr == "input")
                            )
                            if is_input:
                                if node.args and isinstance(node.args[0], ast.Constant):
                                    prompt_txt = str(node.args[0].value)
                                else:
                                    prompt_txt = f"Value {pi + 1}"
                                wk = f"inp_{meta['key']}_f{fi}_p{pi}"
                                all_prompts.append((fi, pi, prompt_txt, wk))
                                pi += 1
                except Exception:
                    pass

            # ── Input fields — one per input() call ─────────────────
            if all_prompts:
                st.markdown(
                    "<div class='run-panel-label' style='margin-bottom:0.6rem;'>"
                    "Program Inputs"
                    "</div>",
                    unsafe_allow_html=True
                )
                for fi, pi, prompt_txt, wk in all_prompts:
                    # Strip trailing colon/space for the label
                    label = prompt_txt.rstrip(": ").strip() or f"Value {pi+1}"
                    # Show filename prefix if there are multiple files
                    full_label = (
                        f"{os.path.basename(py_files[fi])} › {label}"
                        if len(py_files) > 1 else label
                    )
                    if wk not in st.session_state:
                        st.session_state[wk] = ""
                    st.text_input(
                        full_label,
                        key=wk,
                        placeholder="Enter value…",
                    )

            # ── Run button ───────────────────────────────────────────
            run_col, _ = st.columns([1, 5])
            with run_col:
                run_clicked = st.button(
                    "▶  Run",
                    key=f"run_{meta['key']}",
                    type="primary",
                    use_container_width=True,
                )

            if run_clicked:
                # Build per-file stdin strings from the individual widgets
                file_stdins = [""] * len(py_files)
                for fi, pi, prompt_txt, wk in all_prompts:
                    val = st.session_state.get(wk, "")
                    file_stdins[fi] += val + "\n"

                with st.spinner(f"Running {meta['name']}…"):
                    run_results = []
                    for fi, path in enumerate(py_files):
                        try:
                            stdout, stderr, imgs = run_script(
                                path,
                                stdin_input=file_stdins[fi] if all_prompts else ""
                            )
                        except Exception as e:
                            stdout, stderr, imgs = "", str(e), []
                        run_results.append({
                            "file": os.path.basename(path),
                            "stdout": stdout,
                            "stderr": stderr,
                            "imgs": imgs,
                        })
                    st.session_state[ck] = run_results
                    results = run_results
                st.success("Done!")

            # ── Display results ──────────────────────────────────────
            if results:
                for i, path in enumerate(py_files):
                    fname = os.path.basename(path)
                    if i < len(results):
                        r = results[i]
                        st.markdown(
                            f"<div class='file-label' style='padding-left:0;border-top:none;'>&#9654; {fname}</div>",
                            unsafe_allow_html=True
                        )
                        if r["stdout"]:
                            st.code(r["stdout"], language="")
                        for img_path in r["imgs"]:
                            if os.path.exists(img_path):
                                col1, col2, col3 = st.columns([1, 5, 1])
                                with col2:
                                    st.image(img_path, use_container_width=True)
                        if r["stderr"] and not r["stdout"] and not r["imgs"]:
                            st.error(r["stderr"])
            else:
                st.info("Click **▶ Run** above to execute the experiment.")
        else:
            st.warning(f"No Python files found in `{meta['key']}/`.")

    with tabs[4]:
        st.markdown(f"""
        <div class="section-label" style="margin-top:0.3rem;">Conclusion</div>
        <p class="conclusion-text">{meta['conclusion']}</p>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:2.5rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="gtc-footer">
    <span>CMP-226</span>
    &nbsp;·&nbsp;
    <span>Graph Theory and Combinatorics Lab</span>
    &nbsp;·&nbsp;
    <span>Goa College of Engineering</span>
</div>
""", unsafe_allow_html=True)