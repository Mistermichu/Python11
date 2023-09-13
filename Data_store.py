import json


class FileHandler:
    def __init__(self, history_file, balance_file, inventory_file):
        self.history = self.load_history(history_file)
        self.account_balance = self.load_balance(balance_file)
        self.inventory = self.load_inventory(inventory_file)

    def load_history(self, history_file):
        with open(history_file, "r") as history_data:
            history = [line.strip()
                       for line in history_data.readlines() if line.strip()]
        return history

    def load_balance(self, balance_file):
        with open(balance_file, "r") as balance_data:
            account_balance = float(balance_data.readline())
        return account_balance

    def load_inventory(self, inventory_file):
        with open(inventory_file, "r") as inventory_data:
            inventory = json.load(inventory_data)
        return inventory


class FileWriter:
    def __init__(self, history_file, balance_file, inventory_file):
        self.history_file = history_file
        self.balance_file = balance_file
        self.inventory_file = inventory_file

    def save_history(self, history):
        with open(self.history_file, "w") as history_data:
            for new_history_position in history:
                history_data.write(new_history_position + "\n")

    def save_balance(self, balance):
        with open(self.balance_file, "w") as balance_data:
            balance_data.write(str(balance))

    def save_inventory(self, inventory):
        with open(self.inventory_file, "w") as inventory_data:
            json.dump(inventory, inventory_data)
