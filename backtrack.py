import time
from models import Item

def standard_backtracking(items: list[Item], capacity: float):
    n = len(items)
    max_profit = 0
    nodes_visited = 0

    def dfs(level, current_weight, current_profit):
        nonlocal max_profit, nodes_visited
        # track node visits
        nodes_visited += 1

        # stop exploring this branch if we exceed capacity
        if current_weight > capacity:
            return
        
        if current_profit > max_profit:
            max_profit = current_profit

        if level == n:
            return

        # branch 1: INCLUDE the current item
        dfs(level + 1, current_weight + items[level].weight, current_profit + items[level].profit)
        
        # branch 2: EXCLUDE the current item
        dfs(level + 1, current_weight, current_profit)

    start_time = time.perf_counter()
    dfs(0, 0, 0)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    return max_profit, nodes_visited, elapsed_time