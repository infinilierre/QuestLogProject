class Quest:
    """Represents a quest with a name and required items."""
    def __init__(self, name, items):
        self.name = name
        self.items = items  

class Inventory:
    """Handles adding, using, and checking item quantities."""
    def __init__(self, data):
        self.data = data

    def add_item(self, item_name, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.data[item_name] = self.data.get(item_name, 0) + quantity

    def use_item(self, item_name, quantity):
        current = self.data.get(item_name, 0)
        if current < quantity:
            raise ValueError(f"Not enough {item_name}. Have: {current}, Need: {quantity}")
        self.data[item_name] -= quantity

    def get_stock(self, item_name):
        return self.data.get(item_name, 0)
    
    