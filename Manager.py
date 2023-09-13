class Manager:
    def __init__(self, history, account_balance, inventory):
        self.history = history
        self.account_balance = account_balance
        self.inventory = inventory
        self.actions = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate

    def execute(self, name):
        if name not in self.actions:
            print("Akcja niezdefiniowana")
        else:
            self.actions[name](self)
