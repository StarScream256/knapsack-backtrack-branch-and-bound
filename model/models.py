class Item:
    price: float # weight in traditional knapsack
    processor: float
    memory: float
    storage: float
    profit: float # profit/value in traditinal knapsack
    ratio: float # ratio used for sorting in Branch and Bound (profit/weight)


    def __init__(self, price: float, processor: float, memory: float, storage: float, profit: float):
        self.price = price
        self.processor = processor
        self.memory = memory
        self.storage = storage
        self.profit = profit
        self.ratio = profit / price