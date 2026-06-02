import streamlit as st
import os
import subprocess
import sys
import glob
import shutil
import tempfile

st.set_page_config(
    page_title="CMP-226 Graph Theory and Combinatorics Lab",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f0ede8;
    color: #1a1a1a;
}
.main .block-container {
    max-width: 1020px;
    padding-top: 2rem;
    background-color: #f0ede8;
}
.college-header {
    text-align: center;
    padding: 2.2rem 1.5rem 1.8rem;
    border: 1px solid #c8c2b8;
    border-top: 4px solid #1a1a1a;
    margin-bottom: 3rem;
    background: #faf8f5;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.college-header h1 {
    font-family: 'Source Serif 4', serif;
    font-size: 1.55rem; font-weight: 600; color: #1a1a1a;
    margin: 0; letter-spacing: 0.01em;
}
.college-header h2 {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem; font-weight: 400; color: #888;
    margin: 0.35rem 0 0; font-style: italic;
}
.course-info {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.98rem; color: #333; margin-top: 1rem;
    font-weight: 600; letter-spacing: 0.02em;
    border-top: 1px solid #ddd; padding-top: 0.9rem;
}
.student-info { font-size: 0.82rem; color: #999; margin-top: 0.3rem; }

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
    font-size: 0.65rem; font-weight: 500;
    background: rgba(255,255,255,0.1); color: #888;
    padding: 3px 10px; border-radius: 3px;
    white-space: nowrap; letter-spacing: 0.12em; text-transform: uppercase;
    border: 1px solid rgba(255,255,255,0.08);
}
.exp-title {
    font-family: 'Source Serif 4', serif;
    font-size: 1.08rem; font-weight: 600; color: #f5f2ee;
}
.exp-date {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; color: #666; white-space: nowrap;
}
.aim-section {
    padding: 1.1rem 1.6rem 1rem;
    border-bottom: 1px solid #e5e0d8;
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="college-header">
    <h1>Goa College of Engineering</h1>
    <h2>"Bhausaheb Bandodkar Technical Education Complex" &nbsp;&middot;&nbsp; Farmagudi – 403 401, Goa</h2>
    <div class="course-info">CMP-226 &nbsp;:&nbsp; Graph Theory and Combinatorics Lab</div>
    <div class="student-info">
        Deepanghsh Dilkush Naik &nbsp;|&nbsp; Roll No: 24B-CO-017 &nbsp;|&nbsp;
        Fourth Semester &nbsp;&middot;&nbsp; Computer Engineering &nbsp;|&nbsp; 2025–2026
    </div>
</div>
""", unsafe_allow_html=True)

EXPERIMENTS = [
    {
        "key": "Expt_01", "num": 1, "date": "28/01/2026",
        "name": "Basic Graphs",
        "aim": "To implement basic graphs such as complete graph, cycle graph, path graph and complete bipartite graph.",
        "conclusion": "Basic graphs were successfully implemented using NetworkX and Matplotlib.",
    },
    {
        "key": "Expt_02", "num": 2, "date": "05/02/2026",
        "name": "Graph Isomorphism Verification",
        "aim": "To implement graph isomorphism verification in order to compare structural equivalence between two graphs.",
        "conclusion": "Verification of graph isomorphism was successfully implemented.",
    },
    {
        "key": "Expt_03", "num": 3, "date": "12/02/2026",
        "name": "Generation of Various Subgraphs",
        "aim": "To implement generation of various subgraphs such as induced subgraphs, spanning subgraphs and edge-deleted subgraphs.",
        "conclusion": "Subgraphs such as induced subgraphs, spanning subgraphs and edge-deleted subgraphs were successfully plotted using the original graph.",
    },
    {
        "key": "Expt_04", "num": 4, "date": "19/02/2026",
        "name": "Degree Sequence & Havel-Hakimi Algorithm",
        "aim": "To implement construction of a graph for a given degree sequence in order to realize there is a graphical sequence using Havel-Hakimi algorithm.",
        "conclusion": "The given sequence is verified as graphical or not using the Handshaking Lemma and Havel-Hakimi Theorem.",
    },
    {
        "key": "Expt_05", "num": 5, "date": "12/03/2026",
        "name": "Line Graph Conversion",
        "aim": "To implement conversion of a given graph into a line graph where each vertex represents an edge of the original graph, and adjacency reflects shared endpoints.",
        "conclusion": "Construction of line graph using NetworkX function and manually were both successfully implemented.",
    },
    {
        "key": "Expt_06", "num": 6, "date": "02/04/2026",
        "name": "Minimum Spanning Tree — Kruskal's Algorithm",
        "aim": "To implement finding the minimum spanning tree for a given graph using Kruskal's algorithm, ensuring all vertices are connected with the minimum possible total edge weight and without forming cycles.",
        "conclusion": "Construction of minimum spanning tree using Kruskal's algorithm via both NetworkX function and manual implementation were successfully demonstrated.",
    },
    {
        "key": "Expt_07", "num": 7, "date": "09/04/2026",
        "name": "Shortest Path — Dijkstra's Algorithm",
        "aim": "To implement the shortest path algorithm in order to compute the shortest path from the source vertex to all other vertices in a weighted graph.",
        "conclusion": "Shortest path was successfully found using Dijkstra's algorithm with both NetworkX function and manual implementation.",
    },
    {
        "key": "Expt_08", "num": 8, "date": "30/04/2026",
        "name": "Generation of Closed Walks, Trails and Paths",
        "aim": "To implement generation of closed walks, trails and paths in a connected graph.",
        "conclusion": "Generation of closed walks, trails and paths in a connected graph was successfully implemented.",
    },
    {
        "key": "Expt_09", "num": 9, "date": "30/04/2026",
        "name": "Eulerian Circuit Detection",
        "aim": "To implement an algorithm that checks for the existence of an Eulerian circuit and constructs a circuit that traverses every edge of the graph exactly once.",
        "conclusion": "An algorithm that checks existence of an Eulerian circuit and constructs a circuit traversing every edge exactly once was successfully implemented.",
    },
    {
        "key": "Expt_10", "num": 10, "date": "07/05/2026",
        "name": "Hamiltonian Circuit Detection",
        "aim": "To implement a method that determines whether a graph contains a Hamiltonian circuit, i.e. a cycle that visits every vertex exactly once.",
        "conclusion": "A method that determines whether a graph contains a Hamiltonian circuit — a cycle visiting every vertex exactly once except the starting vertex — was successfully implemented.",
    },
    {
        "key": "Expt_11", "num": 11, "date": "14/05/2026",
        "name": "Greedy Graph Coloring",
        "aim": "To implement the greedy graph coloring algorithm that assigns colors to vertices such that no two adjacent vertices share the same color, with minimal chromatic number.",
        "conclusion": "A graph coloring algorithm assigning colors to vertices such that no two adjacent vertices share the same color with minimum chromatic number was successfully implemented.",
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


def run_script(path):
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
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=script_dir,
            env=env,
            timeout=60,
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

for meta in EXPERIMENTS:
    exp_dir = os.path.join(BASE_DIR, meta["key"])
    num = meta["num"]
    cache_key = f"ran_{meta['key']}"

    if cache_key not in st.session_state:
        py_files = sorted(glob.glob(os.path.join(exp_dir, "*.py"))) if os.path.isdir(exp_dir) else []
        results = []
        for path in py_files:
            try:
                stdout, stderr, imgs = run_script(path)
            except Exception as e:
                stdout, stderr, imgs = "", str(e), []
            results.append({
                "file": os.path.basename(path),
                "stdout": stdout,
                "stderr": stderr,
                "imgs": imgs,
            })
        st.session_state[cache_key] = results

    results = st.session_state[cache_key]

    st.markdown(f"""
<div class="exp-card">
    <div class="exp-titlebar">
        <span class="exp-badge">Experiment {num:02d}</span>
        <span class="exp-title">{meta['name']}</span>
        <span class="exp-date">&#128197; {meta['date']}</span>
    </div>
    <div class="aim-section">
        <div class="section-label">Aim</div>
        <p class="section-text">{meta['aim']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

    if os.path.isdir(exp_dir):
        py_files = sorted(glob.glob(os.path.join(exp_dir, "*.py")))
        for i, path in enumerate(py_files):
            fname = os.path.basename(path)

            st.markdown(f"<div class='file-label'>&#128196; Code — {fname}</div>", unsafe_allow_html=True)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    st.code(f.read(), language="python")
            except Exception as e:
                st.error(str(e))

            if i < len(results):
                r = results[i]
                st.markdown(f"<div class='output-label'>&#9654; Output — {fname}</div>", unsafe_allow_html=True)
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
        st.warning(f"Folder `{meta['key']}` not found in {BASE_DIR}")

    st.markdown(f"""
<div style="border:1px solid #c8c2b8; border-top:none; border-radius:0 0 3px 3px;
            background:#f4f0ea; padding:1.1rem 1.6rem 1.2rem; margin-top:0; margin-bottom:3.5rem;">
    <div class="section-label">Conclusion</div>
    <p class="conclusion-text">{meta['conclusion']}</p>
</div>
""", unsafe_allow_html=True)