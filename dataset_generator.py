import random
from models import Item

def generate_knapsack(num_items):
    items = []
    
    # generate random weights (1 to 20 kg) and profits ($10 to $100)
    for _ in range(num_items):
        weight = random.randint(1, 20)
        profit = random.randint(10, 100)
        items.append(Item(weight, profit))
        
    # capacity is 40% of total weight to ensure it's a challenging problem
    # total_weight = sum(item.weight for item in items)
    # capacity = int(total_weight * 0.4)
    
    return items