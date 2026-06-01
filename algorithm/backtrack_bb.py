import time
from typing import Tuple
from model.models import Item


def branch_and_bound(items: list[Item], capacity: float) -> Tuple[float, int, float]:
    # create items and sort by profit/weight ratio (Greedy approach)
    items = sorted(items, key=lambda x: x.ratio, reverse=True)
    
    n: int = len(items)
    max_profit: float = 0
    nodes_visited: int = 0

    # the "Bounding" math
    def get_bound(level: int, current_weight: float, current_profit: float) -> float:
        if current_weight >= capacity:
            return 0
        
        profit_bound: float = current_profit
        total_weight: float = current_weight
        j: int = level
        
        # greedily add remaining items until we hit capacity
        while j < n and total_weight + items[j].price <= capacity:
            total_weight += items[j].price
            profit_bound += items[j].profit
            j += 1
            
        # add a fraction of the next item to get the absolute theoretical max
        if j < n:
            profit_bound += (capacity - total_weight) * items[j].ratio
            
        return profit_bound

    def dfs_bb(level: int, current_weight: float, current_profit: float):
        nonlocal max_profit, nodes_visited
        nodes_visited += 1

        if current_weight <= capacity and current_profit > max_profit:
            max_profit = current_profit

        if level == n:
            return

        # calculate the theoretical maximum profit of this branch
        bound: float = get_bound(level, current_weight, current_profit)

        # pruning rule
        # only explore further if the theoretical max is BETTER than current best
        if bound > max_profit:
            # branch 1: include
            if current_weight + items[level].price <= capacity:
                dfs_bb(level + 1, current_weight + items[level].price, current_profit + items[level].profit)
            
            # branch 2: exclude
            dfs_bb(level + 1, current_weight, current_profit)

    start_time: float = time.perf_counter()
    dfs_bb(0, 0, 0)
    end_time: float = time.perf_counter()
    elapsed_time: float = end_time - start_time

    return max_profit, nodes_visited, elapsed_time