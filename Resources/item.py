import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema
blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Iten did not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # item_data, goes in front of everything else
    def put(self, item_data, item_id):
        item_data = request.get_json()
        # if "price" not in item_data["price"] or "name" not in item_data["name"]:
        #     abort(400, message="Bad Request. Ensure 'price' or 'name' are included in the JSON payload")
        try:
            """
            Ο operator: "|=", είναι σα να κάνεις
            item["name"] = item_data["name"]
            item["price"] = item_data["price"]
            """
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemLits(MethodView):

    @blp.response(200, ItemSchema(many=True))
    # Instance of item schema and the result returned to list
    # so all we need is items.value()
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # γράφουμε το νεο item ως json
        # item_data = request.get_json()
        print(item_data)
        # be sure all info is here
        # check if item already exists
        for item in items.values():
            if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
                abort(400, message=f"Item already exists")

        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201