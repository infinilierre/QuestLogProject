import json
import os
from .models import Quest, Inventory

class QuestLogManager:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.load_data()

    def load_data(self):
        # Load Inventory
        with open(self.config['inventory_file'], 'r') as f:
            self.inventory = Inventory(json.load(f))
        
       
        with open(self.config['quest_file'], 'r') as f:
            data = json.load(f)
            self.quests = [Quest(q['name'], q['items']) for q in data]

    def save_inventory(self):
        with open(self.config['inventory_file'], 'w') as f:
            json.dump(self.inventory.data, f, indent=4)

    def find_quest(self, name):
        for q in self.quests:
            if q.name.lower() == name.lower():
                return q
        return None

    def get_gap(self, quest_name):
        quest = self.find_quest(quest_name)
        if not quest:
            raise ValueError(f"Quest '{quest_name}' not found.")
        
        gaps = {}
        for item, req in quest.items.items():
            stock = self.inventory.get_stock(item)
            if stock < req:
                gaps[item] = req - stock
        return gaps

    def can_complete(self, quest):
        return all(self.inventory.get_stock(it) >= qty for it, qty in quest.items.items())

    def complete_quest(self, quest_name):
        quest = self.find_quest(quest_name)
        if not quest:
            raise ValueError("Quest not found.")
        
        if not self.can_complete(quest):
            raise ValueError(f"Quest '{quest_name}' cannot be completed yet.")

        for it, qty in quest.items.items():
            self.inventory.use_item(it, qty)
        
        self.save_inventory()

    def process_batch_file(self, file_path):
        results = []
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")

        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = line.split()
                try:
                    cmd, item, qty = parts[0].upper(), parts[1], int(parts[2])
                    if cmd == "ADD":
                        self.inventory.add_item(item, qty)
                        results.append(f"SUCCESS: {line}")
                    elif cmd == "USE":
                        self.inventory.use_item(item, qty)
                        results.append(f"SUCCESS: {line}")
                    else:
                        results.append(f"ERROR: Unknown command '{cmd}'")
                except Exception as e:
                    results.append(f"ERROR: {str(e)}")

        self.save_inventory()
        
        os.makedirs(os.path.dirname(self.config['report_file']), exist_ok=True)
        with open(self.config['report_file'], 'w') as f:
            f.write("\n".join(results))

            