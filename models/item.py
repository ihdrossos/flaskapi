from db import db


class ItemModel(db.Model):
    __tablename__ = "Items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    price = db.Column(db.Float)