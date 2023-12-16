import uuid
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema
blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store did not found")

@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self, store_data):
        try:
            # store_data = request.get_json()
            print(store_data)
            # if 'name' not in store_data:
            #     abort(400, message="Bad Request. Make sure 'name' is included")
            for store in stores.values():
                abort(400, message = "Store already exists")
            # if store does not exists
            store_id = uuid.uuid4().hex
            store = {**store_data, "id": store_id}
            stores[store_id] = store
            print(store)
            return store
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500