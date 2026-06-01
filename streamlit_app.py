import streamlit as st
import os
import subprocess
import sys

st.set_page_config(
    page_title="Graph Theory and Combinatorics",
    layout="wide"
)

st.markdown("""
<style>
.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Graph Theory and Combinatorics")
st.caption("Practical Lab Experiments")

st.divider()

for exp in sorted(os.listdir(".")):

    if (
        os.path.isdir(exp)
        and exp.startswith("Expt_")
        and exp != ".venv"
    ):

        exp_no = exp.split("_")[1]

        st.subheader(f"Experiment {exp_no}")

        for file in sorted(os.listdir(exp)):

            if file.endswith(".py"):

                path = os.path.join(exp, file)

                col1, col2 = st.columns([12, 1])

                with col1:
                    with st.expander(f"📄 {file}"):

                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                code = f.read()

                            st.code(code, language="python")

                        except Exception as e:
                            st.error(f"Error reading file: {e}")

                with col2:

                    if st.button(
                        "▶",
                        key=f"{exp}_{file}"
                    ):

                        try:

                            result = subprocess.run(
                                [sys.executable, path],
                                capture_output=True,
                                text=True,
                                encoding="utf-8"
                            )

                            st.session_state[f"stdout_{path}"] = result.stdout
                            st.session_state[f"stderr_{path}"] = result.stderr

                        except Exception as e:

                            st.session_state[f"stderr_{path}"] = str(e)

                if (
                    f"stdout_{path}" in st.session_state
                    or f"stderr_{path}" in st.session_state
                ):

                    with st.container():

                        st.markdown("#### Output")

                        if st.session_state.get(f"stdout_{path}"):
                            st.code(st.session_state[f"stdout_{path}"])

                        if st.session_state.get(f"stderr_{path}"):
                            st.error(st.session_state[f"stderr_{path}"])

                        if os.path.exists("graph.png"):
                            st.image(
                                "graph.png",
                                caption="Generated Graph",
                                use_container_width=True
                            )

        st.divider()