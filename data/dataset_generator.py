import random
from typing import Tuple
from model.models import Item

def generate_knapsack(num_items: int) -> Tuple[list[Item], int]:
    items: list[Item] = []
    
    # generate random prices (Rp 5 to 50 (juta)) and random specs (1 to 10) for processor, memory, storage
    for _ in range(num_items):
        price = random.randint(5, 50)
        processor = random.randint(1, 10)
        memory = random.randint(1, 10)
        storage = random.randint(1, 10)
        profit = (processor + memory + storage) / 3
        items.append(Item(price, processor, memory, storage, profit))
        
    # capacity is 40% of total profit to ensure it's a challenging problem
    suggested_capacity: int = int(sum(item.price for item in items) * 0.4)
    
    return items, suggested_capacity