from __future__ import annotations

import pandas as pd
import streamlit as st

from algorithm.backtrack import standard_backtracking
from algorithm.backtrack_bb import branch_and_bound
from app_ui import clear_session_keys, line_chart
from data.dataset_generator import generate_knapsack


PROJECT_TITLE = "0/1 Knapsack Problem: Backtracking vs Branch and Bound"


def _reset_benchmark_results() -> None:
    clear_session_keys(["multi_results"])


def render_multiple_run_page(configured: bool = False) -> None:
    if not configured:
        st.set_page_config(page_title=PROJECT_TITLE, layout="wide")

    st.title(PROJECT_TITLE)
    st.subheader("Benchmark beberapa ukuran dataset untuk membandingkan tren waktu dan operasi")
    st.divider()

    st.subheader("Multiple Run Benchmark")
    st.write("Halaman ini menjalankan beberapa nilai n sehingga kamu bisa melihat bagaimana jumlah node dan waktu berubah ketika ukuran item bertambah.")

    columns = st.columns(3)
    with columns[0]:
        min_items = st.number_input(
            "n minimum",
            min_value=1,
            value=5,
            step=1,
            key="multi_min_items",
            on_change=_reset_benchmark_results,
        )
    with columns[1]:
        max_items = st.number_input(
            "n maksimum",
            min_value=1,
            value=20,
            step=1,
            key="multi_max_items",
            on_change=_reset_benchmark_results,
        )
    with columns[2]:
        step_items = st.number_input(
            "Langkah n",
            min_value=1,
            value=5,
            step=1,
            key="multi_step_items",
            on_change=_reset_benchmark_results,
        )

    if min_items > max_items:
        st.error("n minimum harus lebih kecil atau sama dengan n maksimum.")
        return

    n_values = list(range(int(min_items), int(max_items) + 1, int(step_items)))
    if not n_values:
        st.error("Rentang n tidak valid.")
        return

    if st.button("Run Multiple Benchmark"):
        results: list[dict[str, float | int]] = []

        for n in n_values:
            items, capacity = generate_knapsack(n)
            bt_profit, bt_nodes, bt_time = standard_backtracking(items.copy(), capacity)
            bb_profit, bb_nodes, bb_time = branch_and_bound(items.copy(), capacity)

            results.append({
                "n": n,
                "capacity": capacity,
                "bt_profit": bt_profit,
                "bt_nodes": bt_nodes,
                "bt_time": bt_time,
                "bb_profit": bb_profit,
                "bb_nodes": bb_nodes,
                "bb_time": bb_time,
            })

        st.session_state["multi_results"] = results

    if "multi_results" not in st.session_state:
        st.info("Jalankan benchmark untuk melihat chart perbandingan antar n.")
        return

    results = st.session_state["multi_results"]
    summary_rows = pd.DataFrame([
        {
            "n": int(row["n"]),
            "capacity": int(row["capacity"]),
            "Backtracking Nodes": int(row["bt_nodes"]),
            "Branch and Bound Nodes": int(row["bb_nodes"]),
            "Backtracking Time (s)": float(row["bt_time"]),
            "Branch and Bound Time (s)": float(row["bb_time"]),
        }
        for row in results
    ])

    st.dataframe(summary_rows, use_container_width=True)

    st.divider()
    st.subheader("Komparasi Tren")
    compare_columns = st.columns(2)
    n_axis = [int(row["n"]) for row in results]

    with compare_columns[0]:
        nodes_chart = line_chart(
            n_axis,
            {
                "Backtracking": [float(row["bt_nodes"]) for row in results],
                "Branch and Bound": [float(row["bb_nodes"]) for row in results],
            },
            "Jumlah Node terhadap n",
            "Node dikunjungi",
        )
        st.plotly_chart(nodes_chart, use_container_width=True)

    with compare_columns[1]:
        time_chart = line_chart(
            n_axis,
            {
                "Backtracking": [float(row["bt_time"]) for row in results],
                "Branch and Bound": [float(row["bb_time"]) for row in results],
            },
            "Waktu Eksekusi terhadap n",
            "Waktu (detik)",
        )
        st.plotly_chart(time_chart, use_container_width=True)


if __name__ == "__main__":
    render_multiple_run_page()