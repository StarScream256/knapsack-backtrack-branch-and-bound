import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backtrack import standard_backtracking
from backtrack_bb import branch_and_bound
from dataset_generator import generate_knapsack

project_title = "0/1 Knapsack Problem: Backtracking vs Branch and Bound"
st.set_page_config(page_title=project_title, layout="wide")
st.title(project_title)

st.subheader("Generate Knapsack Dataset")
st.write("Jumlah dataset yang dibuat akan menghasilkan kemungkinan 2^n kompleksitas waktu untuk kasus terburuk backtracking")

def delete_results():
    if "bt_results" in st.session_state:
        del st.session_state["bt_results"]
    if "bb_results" in st.session_state:
        del st.session_state["bb_results"]

def reset_dataset():
    if "dataset" in st.session_state:
        new_count = st.session_state["dataset_count_input"]
        if new_count != len(st.session_state["dataset"]["items"]):
            del st.session_state["dataset"]
        delete_results()

def update_capacity():
    if "dataset" in st.session_state:
        new_cap = st.session_state["cap_input"]
        st.session_state["dataset"]["capacity"] = new_cap
        delete_results()

cols = st.columns(2)
with cols[0]:
    dataset_count = st.number_input(
        "Jumlah Item (n)",
        min_value=1,
        value=10,
        step=1,
        key="dataset_count_input",
        on_change=reset_dataset
    )
    possible_combinations = 2 ** dataset_count

with cols[1]:
    capacity = st.number_input(
        "Kapasitas Knapsack",
        min_value=1,
        value=1,
        step=1,
        key="cap_input",
        on_change=update_capacity
    )


if st.button("Generate Dataset"):
    items = generate_knapsack(dataset_count)
    current_capacity = st.session_state.get("cap_input", 1)
    st.session_state["dataset"] = {"items": items, "capacity": current_capacity}
    delete_results()

if "dataset" in st.session_state:
    items = st.session_state["dataset"]["items"]
    capacity = st.session_state["dataset"]["capacity"]
    
    items_df = pd.DataFrame([{"Weight": item.weight, "Profit": item.profit} for item in items])
    st.dataframe(items_df)
    st.info(f"Total kombinasi yang mungkin 2^{dataset_count} = {possible_combinations:,}")

    cols = st.columns(2)
    
    with cols[0]:
        st.subheader("Backtracking")
        st.write("Backtracking adalah metode brute-force yang mengeksplorasi semua kemungkinan kombinasi item. Kompleksitas waktu bisa mencapai O(2^n) dalam kasus terburuk, terutama ketika banyak item dan kapasitas besar.")
        
        if st.button("Run Backtracking"):
            bt_profit, bt_nodes, bt_time = standard_backtracking(items, capacity)
            st.session_state["bt_results"] = {
                "profit": bt_profit, "nodes": bt_nodes, "time": bt_time
            }
            
        if "bt_results" in st.session_state:
            res = st.session_state["bt_results"]
            st.success(f"**Profit**: {res['profit']}")
            st.write(f"**Node dikunjungi**: {res['nodes']:,} dari {possible_combinations:,} kemungkinan kombinasi")
            st.write(f"**Waktu**: {res['time']:.8f} seconds")


    with cols[1]:
        st.subheader("Branch and Bound")
        st.write("Branch and Bound adalah metode yang lebih cerdas yang menggunakan teknik pemangkasan untuk menghindari eksplorasi cabang yang tidak menjanjikan. Dengan bounding yang baik, kompleksitas waktu bisa jauh lebih rendah daripada backtracking, terutama pada dataset yang lebih besar.")
        
        if st.button("Run Branch and Bound"):
            bb_profit, bb_nodes, bb_time = branch_and_bound(items, capacity)
            st.session_state["bb_results"] = {
                "profit": bb_profit, "nodes": bb_nodes, "time": bb_time
            }
            
        if "bb_results" in st.session_state:
            res = st.session_state["bb_results"]
            st.success(f"**Profit**: {res['profit']}")
            st.write(f"**Node dikunjungi**: {res['nodes']:,} dari {possible_combinations:,} kemungkinan kombinasi")
            st.write(f"**Waktu**: {res['time']:.8f} seconds")
    
    if "bt_results" in st.session_state and "bb_results" in st.session_state:
        st.divider()
        st.subheader("Komparasi Hasil")
        # TODO: Add a bar chart comparing profit, nodes visited, and time for both algorithms
