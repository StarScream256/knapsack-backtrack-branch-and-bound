class Item:
    def __init__(self, weight: float, profit: float):
        self.weight = weight
        self.profit = profit
        self.ratio = profit / weight