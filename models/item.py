from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precission=2), unique=False, nullable=False),
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),unique=False, nullable=False)
    # populate store model based on stores.id
    # and also the items the store has
    store = db.relationship("StoreModel", back_populates="items")
