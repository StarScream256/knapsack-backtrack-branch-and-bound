from __future__ import annotations

import streamlit as st

from benchmark.multiple_run import render_multiple_run_page
from benchmark.single_run import render_single_run_page


PROJECT_TITLE = "0/1 Knapsack Problem: Backtracking vs Branch and Bound"


st.set_page_config(page_title=PROJECT_TITLE, layout="wide")

mode = st.sidebar.radio(
    "Mode",
    ["Single Run", "Multiple Run"],
)

if mode == "Single Run":
    render_single_run_page(configured=True)
else:
    render_multiple_run_page(configured=True)




