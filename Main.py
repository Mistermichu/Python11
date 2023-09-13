from Data_store import FileWriter, FileHandler
from functions import menu, balance, account_balance_note, sell, buy, list_overview, inventory_overview, history_overview, inventory_correction
from Manager import Manager


load_data = FileHandler("history.txt", "balance.txt", "inventory.json")
manager = Manager(load_data.history,
                  load_data.account_balance, load_data.inventory)


# Change balance
@manager.assign(1)
def manage_balance(manager):
    manager.account_balance += balance(manager.history)
    account_balance_note(manager.account_balance)


# Sell
@manager.assign(2)
def manage_sell(manager):
    manager.account_balance += sell(manager.history, manager.inventory)
    account_balance_note(manager.account_balance)


# Buy
@manager.assign(3)
def manage_buy(manager):
    manager.account_balance -= buy(manager.account_balance,
                                   manager.history, manager.inventory)
    account_balance_note(manager.account_balance)


# Account balance
@manager.assign(4)
def manage_account_balance(manager):
    account_balance_note(manager.account_balance)


# List
@manager.assign(5)
def manage_list_overview(manager):
    list_overview(manager.inventory)


# Inventory
@manager.assign(6)
def manage_inventory_overview(manager):
    inventory_overview(manager.inventory)


# History
@manager.assign(7)
def manage_history_overview(manager):
    history_overview(manager.history)


# Inventory corrections
@manager.assign(8)
def manage_inventory_correction(manager):
    inventory_correction(manager.history, manager.inventory)


# Exit
@manager.assign(9)
def manage_exit(manager):
    global run
    run = False
    save_data = FileWriter(
        "history.txt", "balance.txt", "inventory.json")
    save_data.save_history(manager.history)
    save_data.save_balance(manager.account_balance)
    save_data.save_inventory(manager.inventory)


# Run app
run = True
while run:
    menu()
    try:
        command = int(input(": "))
        manager.execute(command)
    except ValueError:
        print("Akcja niezdefiniowana")
