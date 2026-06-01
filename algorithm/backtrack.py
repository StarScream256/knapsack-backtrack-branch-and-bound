import time

from typing import Tuple
from model.models import Item

def standard_backtracking(items: list[Item], capacity: float) -> Tuple[float, int, float]:
    n: int = len(items)
    max_profit: float = 0
    nodes_visited: int = 0

    def dfs(level: int, current_weight: float, current_profit: float) -> None:
        nonlocal max_profit, nodes_visited
        nodes_visited += 1

        # stop exploring this branch if we exceed capacity
        if current_weight > capacity:
            return
        
        if current_profit > max_profit:
            max_profit = current_profit

        if level == n:
            return

        # branch 1: INCLUDE the current item
        dfs(level + 1, current_weight + items[level].price, current_profit + items[level].profit)
        
        # branch 2: EXCLUDE the current item
        dfs(level + 1, current_weight, current_profit)

    start_time: float = time.perf_counter()
    dfs(0, 0, 0)
    end_time: float = time.perf_counter()
    elapsed_time: float = end_time - start_time

    return max_profit, nodes_visited, elapsed_time