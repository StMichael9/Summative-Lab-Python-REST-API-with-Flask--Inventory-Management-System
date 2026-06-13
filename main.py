# Flask API(main backend)
from flask import Flask, jsonify, request
from inventory import items 
app = Flask(__name__)

@app.route('/inventory')
def get_all_items():
    return jsonify({"inventory": items}), 200

@app.route("/inventory/<int:id>")
def get_single_items(id):
    for i in items:
        if i['id'] == id:
            return jsonify(i)
    return jsonify({"error": "Item not found"}), 404
    
@app.route('/inventory', methods=["POST"])
def create_items():
    data = request.get_json()
    new_id = max([i["id"] for i in items]) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": data.get("name"),
        "brand": data.get("brand"),
        "quantity": data.get("quantity"),
        "price": data.get("price")
    }
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:id>', methods=["PATCH"])
def update_items(id):
    item = next((i for i in items if i["id"] == id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404
    # Merged the incoming data directly into the item dictionary
    item.update(request.get_json())
    item["id"] = id
    return jsonify(item), 200


@app.route('/inventory/<int:id>', methods=["DELETE"])
def delete_items(id):
    item = next((i for i in items if i["id"] == id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    items.remove(item)
    return jsonify({"message": "Item successfully deleted"}), 200