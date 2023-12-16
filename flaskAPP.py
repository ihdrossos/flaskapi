import uuid
from flask import Flask, request, jsonify
from datetime import datetime
from db import items, stores
from flask_smorest import abort, Api
from Resources.item import blp as ItemBlueprint
from Resources.store import blp as StoreBlueprint


app = Flask(__name__)

"""
    ΠΛέον θα χρησιμοποιούμε τα Bluprints
    και για αυτό θα πρέπει να τα κάνουμε register
    Θα χρειστούν configuration options
"""

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Store REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] ="/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# connects flask_smorest extension to flask app
api = Api(app)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)


# @app.route("/")
# def home():
#     return "Hello, Flask!"
#
#
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message":"Item deleted"}
#     except KeyError:
#         abort(404, message="Iten did not found")
#
# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message":"Store deleted"}
#     except KeyError:
#         abort(404, message="Store did not found")
#
#
# # Retrive Item and Store
#
# @app.get('/stores')
# def get_stores():
#     return {"stores": list(stores.values())}
#
# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}
#
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="Item not found")
#
# @app.get("/store/<string:store_id>/")
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except:
#         abort(404, message="Store not found")
#
# # Create Item and Store
# @app.post("/store")
# def create_store():
#     try:
#         store_data = request.get_json()
#         print(store_data)
#         if 'name' not in store_data:
#             abort(400, message="Bad Request. Make sure 'name' is included")
#         store_id = uuid.uuid4().hex
#         store = {**store_data, "id":store_id}
#         stores[store_id] = store
#         print(store)
#         return store
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return jsonify({"error": "Internal Server Error"}), 500
#
# @app.post("/item")
# def create_item():
#     # γράφουμε το νεο item ως json
#     item_data = request.get_json()
#     print(item_data)
#     # be sure all info is here
#     if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
#         abort(400, message="Bad Request. Ensure 'price', 'name' and 'store_id' are included in the JSON payload")
#
#     # check if item already exists
#     for item in items.values():
#         if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
#             abort(400, message=f"Item already exists")
#
#     if item_data["store_id"] not in stores:
#         abort(404, message="Store not found")
#
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#     return item, 201
#
# # Update Items and Store
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data["price"] or "name" not in item_data["name"]:
#         abort(400, message = "Bad Request. Ensure 'price' or 'name' are included in the JSON payload")
#     try:
#         """
#         Ο operator: "|=", είναι σα να κάνεις
#         item["name"] = item_data["name"]
#         item["price"] = item_data["price"]
#         """
#         item = items[item_id]
#         item |= item_data
#         return item
#     except KeyError:
#         abort(404, message= "Item not found")






