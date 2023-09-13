from flask import Flask, render_template, request, redirect, url_for
from Data_store import FileHandler, FileWriter
from functions import menu, balance, account_balance_note, sell, buy, list_overview, inventory_overview, history_overview, inventory_correction
from Manager import Manager
from flask_sqlalchemy import SQLAlchemy

data_handler = FileHandler("history.txt", "balance.txt", "inventory.json")
save_data = FileWriter(
    "history.txt", "balance.txt", "inventory.json")
manager = Manager(data_handler.history,
                  data_handler.account_balance, data_handler.inventory)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class HistoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500))


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    list_price = db.Column(db.Float)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    account_balance = round(manager.account_balance, 2)
    inventory = manager.inventory

    return render_template('index.html', account_balance=account_balance, inventory=inventory)


@app.route('/buy', methods=['POST'])
def process_buy():
    purchase_product = request.form.get('purchase_product')
    purchase_price = float(request.form.get('purchase_price'))
    selling_price = float(request.form.get('selling_price'))
    purchase_quantity = int(request.form.get('purchase_quantity'))
    manager.account_balance -= round(buy(manager.account_balance,
                                         manager.history, manager.inventory, purchase_product, purchase_price, purchase_quantity, selling_price, db), 2)
    save_data.save_history(manager.history)
    save_data.save_balance(manager.account_balance)
    save_data.save_inventory(manager.inventory)

    return render_template('index.html', account_balance=manager.account_balance, inventory=manager.inventory)


@app.route('/sell', methods=['POST'])
def process_sell():
    sell_product = request.form.get('sell_product')
    sell_quantity = int(request.form.get('sell_quantity'))
    manager.account_balance += sell(manager.history,
                                    manager.inventory, sell_product, sell_quantity, db)
    save_data.save_history(manager.history)
    save_data.save_balance(manager.account_balance)
    save_data.save_inventory(manager.inventory)

    return render_template('index.html', account_balance=manager.account_balance, inventory=manager.inventory)


@app.route('/balance', methods=['POST'])
def process_balance():
    balance_change = float(request.form.get('balance_change'))
    manager.account_balance += balance(manager.history,
                                       balance_change, manager.account_balance, db)
    save_data.save_history(manager.history)
    save_data.save_balance(manager.account_balance)

    return render_template('index.html', account_balance=manager.account_balance, inventory=manager.inventory)


@app.route('/historia/')
@app.route('/historia/<int:start>/<int:end>')
def history(start=None, end=None):
    if start is None or end is None:
        history_data = manager.history
    else:
        if start < 1:
            start = 1
        if end > len(manager.history):
            end = len(manager.history)
        history_data = manager.history[start - 1:end]

    return render_template('history.html', history_data=history_data)


if __name__ == '__main__':
    app.run()
