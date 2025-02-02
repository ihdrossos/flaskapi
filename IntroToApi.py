#libraries
# import uuid
# from flask_smorest import abort, Api
# from db import items, stores
# from flask import Flask, request
import os
from flask import Flask
from flask_smorest import Api
from Resources.item import blp as ItemBlueprint
from Resources.store import blp as StoreBlueprint
from db import db
import models

def create_app(db_url = None):
# initiate app
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] ="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)
    with app.app_context():
        db.create_all() # αν οι πίνακες υπάρχουν, δεν θα τους δημιουργήσει ξανά

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app

if __name__ == "__main__":
    create_app()


#
# @app.route("/")
# def home_app():
#     return f"Hello {app.name}"
#
# @app.get("/stores")
# def get_stores():
#     return {"stores": list(stores.values())}
#
#
# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         abort(404, message="Store not found")
#
#
# @app.get("/item")
# def get_all_items():
#     print(items)
#     return {"items": list(items.values())}
#
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     print(items[item_id])
#     try:
#         return {"item": items[item_id]}
#     except KeyError:
#         abort(404, message="Item not found")
#
# @app.post("/store")
# def create_store():
#     """
#     :return:
#     Διαβάζουμε απο το json με το request.get_json().
#     To διαβάζει ώς εξής:
#     {"name": "My Store 2"}
#     και το αποθηκεύει ως dictionary
#     Δημιουργούμε ένα json που έχει το name και καθόλου items.
#     Αποθηκεύουμε την πληροφορία σε ένα ενδιάμεσο dict με ονομασία new_store
#     Το ενδιάμεσο dict το κάνουμε append στο τελικό μας dictionary Που είναι
#     το stores
#     """
#     # request_data = request.get_json()
#     # new_store = {"name": request_data["name"], "items": []}
#     # stores.append(new_store)
#     # return new_store, 201
#
#     store_data = request.get_json()
#
#     """
#     print(store_data)
#         {
#         "name":"Kotsovolos"
#         }
#     """
#
#     if "name" not in store_data:
#         abort(400, message="Bad Request. Store's name is missing")
#     for store in stores.values():
#         if store_data["name"]==store["name"]:
#             abort(404, message=f"Store already exists")
#     store_id = uuid.uuid4().hex
#     new_store = {**store_data, "id": store_id}
#     stores[store_id] = new_store
#     return new_store, 201
#
# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#     print(type(item_data))
#     if (
#         "name" not in item_data or
#         "price" not in item_data or
#         "store_id" not in item_data
#     ):
#         abort(404, message="Bad Request. Name, or price, or store_id missing")
#     # items={'2351eea12ba744c8994af1bad4005d4a': {'name': 'Table', 'price': 1500, 'store_id': '36e7d738125647b3b31687b69d5d9030', 'id': '2351eea12ba744c8994af1bad4005d4a'}}
#     """
#     το item θα είναι ένα dictionary της μορφής:
#     {'name': 'Table', 'price': 1500, 'store_id': '36e7d738125647b3b31687b69d5d9030', 'id': '2351eea12ba744c8994af1bad4005d4a'}
#     Άρα κοιτάω να δω αν αυτό που διάβασα απο το request (item_data["name"] υπάρχει μέσα στο item (item["name"])
#     υπάρχει μέσα στο κατάστημα που έχω, το οποίο και αυτό το διάβασα απο το request
#     """
#     for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, message=f"Item already exists")
#
#     if item_data["store_id"] not in stores:
#         abort(404, message="Store not found")
#     item_id = uuid.uuid4().hex
#     new_item = {**item_data, "id": item_id}
#     items[item_id] = new_item
#     return new_item, 201
#
#
#     # request_data = request.get_json()
#     # for store in stores:
#     #     if store["name"] == name:
#     #         new_item = {"name": request_data["name"], "price": request_data["price"]}
#     #         store["items"].append(new_item)
#     #         return new_item, 201
#     #
#     #         # Αν το store υπάρχει, τότε δε θα τρέξει ποτέ το τελευταίο return
#     #         # Ο κώδικας θα έχει τερματίσει στο προηγούμενο return.
#     #         # Σε περίπτωση που δεν υπάρχει το store που θέλουμε, τότε θα τρέξει το τελευταίο
#     #
#     # return {"message": "Store not found"}, 404
#
#
#
# @app.delete("/item/<item_id>")
# def delete_specific_item(item_id):
#     try:
#         del items["item_id"]
#         return {"message": "Item deleted"}
#     except KeyError:
#         abort(404, message = "Item not found")
#
# @app.delete("/store/<string:store_id>")
# def delete_specific_store(store_id):
#     try:
#         del stores["store_id"]
#         return {"message": "Item deleted"}
#     except KeyError:
#         abort(404, message = "Store not found")
#
# @app.put("/item/<string:item_id>")
# def update_specific_item(item_id):
#     item_data = request.get_json()
#     if ("name" not in item_data or
#             "price" not in item_data):
#         abort(404, message="Bad request. Ensure price and name are included")
#     try:
#         item = items[item_id]
#         item |= item_data
#         return item
#     except KeyError:
#         abort(404, message="Item not found")
#
#
#
# if __name__=="__main__":
#     app.run(debug=True)