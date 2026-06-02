from __future__ import annotations

from typing import Any, cast

import streamlit as st

from algorithm.backtrack import standard_backtracking
from algorithm.backtrack_bb import branch_and_bound
from app_ui import bar_chart, clear_session_keys, items_to_dataframe, render_metric_summary
from data.dataset_generator import generate_knapsack
from model.models import Item


PROJECT_TITLE = "0/1 Knapsack Problem: Backtracking vs Branch and Bound"


def _reset_single_dataset() -> None:
    if "single_dataset" not in st.session_state:
        return

    new_count = int(cast(int, st.session_state["single_dataset_count_input"]))
    dataset = cast(dict[str, Any], st.session_state["single_dataset"])
    if new_count != len(cast(list[Item], dataset["items"])):
        st.session_state.pop("single_dataset", None)
    clear_session_keys(["single_bt_results", "single_bb_results"])


def _update_single_capacity() -> None:
    if "single_dataset" not in st.session_state:
        return

    # User will input capacity manually; just clear previous results when capacity changes
    clear_session_keys(["single_bt_results", "single_bb_results"])


def render_single_run_page(configured: bool = False) -> None:
    if not configured:
        st.set_page_config(page_title=PROJECT_TITLE, layout="wide")

    st.title(PROJECT_TITLE)
    st.subheader("Studi kasus pembelian komputer dengan budget terbatas")
    st.divider()

    st.subheader("Generate Knapsack Dataset")
    st.write("Jumlah dataset yang dibuat akan menghasilkan kemungkinan 2^n kompleksitas waktu untuk kasus terburuk backtracking")

    dataset_count = st.number_input(
        "Jumlah Item (n)",
        min_value=1,
        value=10,
        step=1,
        key="single_dataset_count_input",
        on_change=_reset_single_dataset,
    )
    possible_combinations = 2 ** int(dataset_count)

    if st.button("Generate Dataset"):
        items, _ = generate_knapsack(int(dataset_count))
        # Do not auto-fill the budget (capacity); user must input it manually
        st.session_state["single_dataset"] = {"items": items}
        clear_session_keys(["single_bt_results", "single_bb_results"])

    st.number_input(
        "Budget (Juta Rupiah)",
        min_value=1,
        step=1,
        key="single_cap_input",
        on_change=_update_single_capacity,
    )

    if "single_dataset" not in st.session_state:
        st.info("Generate dataset terlebih dahulu untuk menjalankan perbandingan single run.")
        return

    items = cast(list[Item], st.session_state["single_dataset"]["items"])
    # Read capacity from the user's manual input widget
    capacity = float(st.session_state["single_cap_input"])

    st.dataframe(items_to_dataframe(items), use_container_width=True)  # type: ignore
    st.info(f"Total kombinasi yang mungkin 2^{int(dataset_count)} = {possible_combinations:,}")

    columns = st.columns(2)

    with columns[0]:
        st.subheader("Backtracking")
        st.write("Backtracking adalah metode brute-force yang mengeksplorasi semua kemungkinan kombinasi item. Kompleksitas waktu bisa mencapai O(2^n) dalam kasus terburuk, terutama ketika banyak item dan kapasitas besar.")

        if st.button("Run Backtracking"):
            bt_profit, bt_nodes, bt_time = standard_backtracking(items.copy(), capacity)
            st.session_state["single_bt_results"] = {"profit": bt_profit, "nodes": bt_nodes, "time": bt_time}

        if "single_bt_results" in st.session_state:
            result = st.session_state["single_bt_results"]
            render_metric_summary(float(result["profit"]), int(result["nodes"]), float(result["time"]), possible_combinations)

    with columns[1]:
        st.subheader("Branch and Bound")
        st.write("Branch and Bound adalah metode yang lebih cerdas yang menggunakan teknik pemangkasan untuk menghindari eksplorasi cabang yang tidak menjanjikan. Dengan bounding yang baik, kompleksitas waktu bisa jauh lebih rendah daripada backtracking, terutama pada dataset yang lebih besar.")

        if st.button("Run Branch and Bound"):
            bb_profit, bb_nodes, bb_time = branch_and_bound(items.copy(), capacity)
            st.session_state["single_bb_results"] = {"profit": bb_profit, "nodes": bb_nodes, "time": bb_time}

        if "single_bb_results" in st.session_state:
            result = st.session_state["single_bb_results"]
            render_metric_summary(float(result["profit"]), int(result["nodes"]), float(result["time"]), possible_combinations)

    if "single_bt_results" in st.session_state and "single_bb_results" in st.session_state:
        st.divider()
        st.subheader("Komparasi Hasil")
        compare_columns = st.columns(2)

        with compare_columns[0]:
            nodes_chart = bar_chart(
                ["Backtracking", "Branch and Bound"],
                [
                    float(st.session_state["single_bt_results"]["nodes"]),
                    float(st.session_state["single_bb_results"]["nodes"]),
                ],
                "Node dikunjungi",
                "{0:,.0f}",
                ["#FF6B35", "#3A86FF"],
            )
            st.plotly_chart(nodes_chart, use_container_width=True)

        with compare_columns[1]:
            time_chart = bar_chart(
                ["Backtracking", "Branch and Bound"],
                [
                    float(st.session_state["single_bt_results"]["time"]),
                    float(st.session_state["single_bb_results"]["time"]),
                ],
                "Waktu Eksekusi (detik)",
                "{0:.8f}",
                ["#FF6B35", "#3A86FF"],
            )
            st.plotly_chart(time_chart, use_container_width=True)


if __name__ == "__main__":
    render_single_run_page()