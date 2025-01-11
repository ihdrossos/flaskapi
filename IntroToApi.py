#libraries
import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

# initiate app
app = Flask(__name__)

@app.route("/")
def home_app():
    return f"Hello {app.name}"

@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return {"item": items["item_id"]}
    except KeyError:
        return {"message":"Item not found"}, 404

@app.post("/store")
def create_store():
    """
    :return:
    Διαβάζουμε απο το json με το request.get_json().
    To διαβάζει ώς εξής:
    {"name": "My Store 2"}
    και το αποθηκεύει ως dictionary
    Δημιουργούμε ένα json που έχει το name και καθόλου items.
    Αποθηκεύουμε την πληροφορία σε ένα ενδιάμεσο dict με ονομασία new_store
    Το ενδιάμεσο dict το κάνουμε append στο τελικό μας dictionary Που είναι
    το stores
    """
    # request_data = request.get_json()
    # new_store = {"name": request_data["name"], "items": []}
    # stores.append(new_store)
    # return new_store, 201

    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


    # request_data = request.get_json()
    # for store in stores:
    #     if store["name"] == name:
    #         new_item = {"name": request_data["name"], "price": request_data["price"]}
    #         store["items"].append(new_item)
    #         return new_item, 201
    #
    #         # Αν το store υπάρχει, τότε δε θα τρέξει ποτέ το τελευταίο return
    #         # Ο κώδικας θα έχει τερματίσει στο προηγούμενο return.
    #         # Σε περίπτωση που δεν υπάρχει το store που θέλουμε, τότε θα τρέξει το τελευταίο
    #
    # return {"message": "Store not found"}, 404







if __name__=="__main__":
    app.run(debug=True)