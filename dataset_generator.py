import random

def generate_knapsack(num_items):
    weights = []
    profits = []
    
    # generate random weights (1 to 20 kg) and profits ($10 to $100)
    for _ in range(num_items):
        weights.append(random.randint(1, 20))
        profits.append(random.randint(10, 100))
        
    # capacity is 40% of total weight to ensure it's a challenging problem
    total_weight = sum(weights)
    capacity = int(total_weight * 0.4)
    
    return weights, profits, capacity