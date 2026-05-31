import time
from models import Item


def branch_and_bound(items: list[Item], capacity: float):
    # create items and sort by profit/weight ratio (Greedy approach)
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    n = len(items)
    max_profit = 0
    nodes_visited = 0

    # the "Bounding" math
    def get_bound(level, current_weight, current_profit):
        if current_weight >= capacity:
            return 0
        
        profit_bound = current_profit
        total_weight = current_weight
        j = level
        
        # greedily add whole items
        while j < n and total_weight + items[j].weight <= capacity:
            total_weight += items[j].weight
            profit_bound += items[j].profit
            j += 1
            
        # add a fraction of the next item to get the absolute theoretical max
        if j < n:
            profit_bound += (capacity - total_weight) * items[j].ratio
            
        return profit_bound

    def dfs_bb(level, current_weight, current_profit):
        nonlocal max_profit, nodes_visited
        nodes_visited += 1 # Track every node we touch!

        if current_weight <= capacity and current_profit > max_profit:
            max_profit = current_profit

        if level == n:
            return

        # calculate the theoretical maximum profit of this branch
        bound = get_bound(level, current_weight, current_profit)

        # pruning rule
        # only explore further if the theoretical max is BETTER than current best
        if bound > max_profit:
            # branch 1: include
            if current_weight + items[level].weight <= capacity:
                dfs_bb(level + 1, current_weight + items[level].weight, current_profit + items[level].profit)
            
            # branch 2: exclude
            dfs_bb(level + 1, current_weight, current_profit)

    start_time = time.perf_counter()
    dfs_bb(0, 0, 0)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    return max_profit, nodes_visited, elapsed_time