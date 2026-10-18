"""Streamlit front end for the schedule risk tool."""
import pathlib
import sys
import tempfile

import matplotlib.pyplot as plt
import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.network import load_activities  # noqa: E402
from engine.simulate import percentiles, project_duration  # noqa: E402

st.set_page_config(page_title="Schedule Risk Tool", layout="wide")
st.title("Schedule risk simulator")
st.caption("Monte Carlo schedule risk for Indian building projects")

with st.sidebar:
    st.header("Inputs")
    uploaded = st.file_uploader("Activity CSV", type="csv")
    n_iter = st.select_slider("Iterations", [1000, 5000, 10000, 50000], value=10000)
    seed = st.number_input("Random seed", value=42, step=1)

default_path = ROOT / "data" / "benchmark_6_activity.csv"

try:
    if uploaded is not None:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp.write(uploaded.getvalue())
            path = tmp.name
    else:
        path = default_path
    acts = load_activities(path)
except ValueError as err:
    st.error(f"Input problem: {err}")
    st.stop()

with st.spinner("Running simulation..."):
    durations = project_duration(acts, n_iter=n_iter, seed=int(seed))
    results = percentiles(durations)

col1, col2, col3 = st.columns(3)
col1.metric("P50 duration (days)", f"{results['P50']:.1f}")
col2.metric("P80 duration (days)", f"{results['P80']:.1f}")
col3.metric("P90 duration (days)", f"{results['P90']:.1f}")

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.hist(durations, bins=60, color="#2E6F9E", alpha=0.85)
for key in ["P50", "P80", "P90"]:
    ax.axvline(results[key], linestyle="--", label=key)
ax.set_xlabel("Project duration (days)")
ax.set_ylabel("Iterations")
ax.legend()
st.pyplot(fig)

with st.expander("Activities loaded"):
    st.dataframe(
        [{"id": a["id"], "name": a["name"], "O": a["o"], "M": a["m"],
          "P": a["p"], "predecessors": ", ".join(a["preds"])} for a in acts.values()]
    )
