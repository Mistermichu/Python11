from app import db
from flask_sqlalchemy import SQLAlchemy


class HistoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(500))


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)


db.create_all()
