import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel



blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item_id)
        db.session.commit()
        return {"message": "Item deleted"}


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # item_data, goes in front of everything else
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        # if item exists
        if item:
            item.price = item_data["price"]
            item.name  = item_data["name"]
        # if item does not exists, then create it
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    # Instance of item schema and the result returned to list
    # so all we need is items.value()
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        # Δεν χρειάζεται να ορίζω πλέον το item_data γιατί το json που ορίζει ο χρήστης περνάει μέσα απο το check schema
        # και δίνει αυτό στην μέθοδο το συγκεκριμένο argument
        #item_data = request.get_json()
        # Δεν το χρειάζομαι ποια αυτό τον έλεγχο καθώς θα τον κάνει το Marshmallow
        # if (
        #         "name" not in item_data or
        #         "price" not in item_data or
        #         "store_id" not in item_data
        # ):
        #     abort(404, message="Bad Request. Name, or price, or store_id missing")
        # items={'2351eea12ba744c8994af1bad4005d4a': {'name': 'Table', 'price': 1500, 'store_id': '36e7d738125647b3b31687b69d5d9030', 'id': '2351eea12ba744c8994af1bad4005d4a'}}
        """
        το item θα είναι ένα dictionary της μορφής:
        {'name': 'Table', 'price': 1500, 'store_id': '36e7d738125647b3b31687b69d5d9030', 'id': '2351eea12ba744c8994af1bad4005d4a'}
        Άρα κοιτάω να δω αν αυτό που διάβασα απο το request (item_data["name"] υπάρχει μέσα στο item (item["name"])
        υπάρχει μέσα στο κατάστημα που έχω, το οποίο και αυτό το διάβασα απο το request
        """
        # for item in items.values():
        #     if (
        #             item_data["name"] == item["name"]
        #             and item_data["store_id"] == item["store_id"]
        #     ):
        #         abort(400, message=f"Item already exists")
        #
        # # if item_data["store_id"] not in stores:
        # #     abort(404, message="Store not found")
        # item_id = uuid.uuid4().hex
        # new_item = {**item_data, "id": item_id}
        # items[item_id] = new_item

        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")
        return item, 201