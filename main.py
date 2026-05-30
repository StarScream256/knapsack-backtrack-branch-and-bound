from backtrack import standard_backtracking
from backtrack_bb import branch_and_bound
from dataset_generator import generate_knapsack

class Item:
    def __init__(self, weight, profit):
        self.weight = weight
        self.profit = profit
        self.ratio = profit / weight

if __name__ == "__main__":
    weights, profits, capacity = generate_knapsack(10)

    print("--- STANDARD BACKTRACKING ---")
    bt_profit, bt_nodes, bt_time = standard_backtracking(weights, profits, capacity)
    print(f"Max Profit Found: {bt_profit}")
    print(f"Nodes Visited:    {bt_nodes}")
    print(f"Execution Time:   {bt_time:.8f} seconds\n")

    print("--- BRANCH AND BOUND ---")
    bb_profit, bb_nodes, bb_time = branch_and_bound(weights, profits, capacity)
    print(f"Max Profit Found: {bb_profit}")
    print(f"Nodes Visited:    {bb_nodes}")
    print(f"Execution Time:   {bb_time:.8f} seconds\n")