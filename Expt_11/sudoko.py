import networkx as nx
import matplotlib.pyplot as plt

sudoku = [[0,0,1,0],[2,0,0,0],[0,0,0,0],[0,0,0,3]]
SIZE, SUBGRID = 4, 2
G = nx.sudoku_graph(2)
steps = []

def is_safe(board, row, col, num):
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    sr, sc = (row//SUBGRID)*SUBGRID, (col//SUBGRID)*SUBGRID
    return all(board[r][c] != num for r in range(sr, sr+SUBGRID) for c in range(sc, sc+SUBGRID))

def solve(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                for num in range(1, SIZE+1):
                    if is_safe(board, row, col, num):
                        steps.append(f"Pick cell ({row+1},{col+1}) -> Assign {num}")
                        board[row][col] = num
                        if solve(board): return True
                        board[row][col] = 0
                        steps.append(f"Backtrack cell ({row+1},{col+1})")
                return False
    return True

print("\nInitial Sudoku:\n"); [print(r) for r in sudoku]
solve(sudoku)
print("\nSteps:\n"); [print(s) for s in steps]
print("\nSolved Sudoku:\n"); [print(r) for r in sudoku]

# Layout: perspective cube — outer ring + inner ring
INNER, OUTER, SQ = 0.30, 0.78, 0.80
ip = [(-INNER,-INNER*SQ),(INNER,-INNER*SQ),(-INNER,INNER*SQ),(INNER,INNER*SQ)]
op = [(-OUTER,-OUTER*SQ),(OUTER,-OUTER*SQ),(-OUTER,OUTER*SQ),(OUTER,OUTER*SQ)]

corner_map = {(0,0):op[0],(0,3):op[1],(3,0):op[2],(3,3):op[3],
              (1,1):ip[0],(1,2):ip[1],(2,1):ip[2],(2,2):ip[3]}

def lerp(a, b, t): return (a[0]*(1-t)+b[0]*t, a[1]*(1-t)+b[1]*t)

def get_pos(r, c):
    if (r,c) in corner_map: return corner_map[(r,c)]
    if r == 0: return lerp(op[0], op[1], c/3)
    if r == 3: return lerp(op[2], op[3], c/3)
    if c == 0: return lerp(op[0], op[2], r/3)
    if c == 3: return lerp(op[1], op[3], r/3)
    tr, tc = (r-1)/2, (c-1)/2
    return lerp(lerp(ip[0],ip[1],tc), lerp(ip[2],ip[3],tc), tr)

pos = {i*SIZE+j: get_pos(i,j) for i in range(SIZE) for j in range(SIZE)}

value_colors = {1:"#e05252", 2:"#4caf76", 3:"#4f9fd4", 4:"#f0c040"}
node_colors = [value_colors[sudoku[i][j]] for i in range(SIZE) for j in range(SIZE)]
labels = {i*SIZE+j: str(sudoku[i][j]) for i in range(SIZE) for j in range(SIZE)}

def classify(u, v):
    if u//SIZE == v//SIZE: return "row"
    if u%SIZE == v%SIZE: return "col"
    return "box"

edge_groups = {"row":[], "col":[], "box":[]}
for u, v in G.edges(): edge_groups[classify(u,v)].append((u,v))

def draw_curved_edges(ax, edges, color, alpha, lw, rad):
    for u, v in edges:
        ax.annotate("", xy=pos[v], xytext=pos[u],
            arrowprops=dict(arrowstyle="-", color=color, lw=lw, alpha=alpha,
                            connectionstyle=f"arc3,rad={rad}"))

fig, ax = plt.subplots(figsize=(8,8))

draw_curved_edges(ax, edge_groups["row"], "#cc2222", alpha=0.85, lw=2.2, rad=0.40)
draw_curved_edges(ax, edge_groups["col"], "#228833", alpha=0.85, lw=2.2, rad=0.40)
draw_curved_edges(ax, edge_groups["box"], "#3355cc", alpha=0.90, lw=1.6, rad=0.25)

nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=900,
                       edgecolors='black', linewidths=2.0)
nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=13,
                        font_weight='bold', font_color='black')

ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_title("Sudoku — Graph Coloring (Cube Layout)", fontsize=15, pad=16, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.savefig("graph.png")
plt.close()