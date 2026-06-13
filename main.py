# Flask API(main backend)
from flask import Flask, jsonify, request

from inventory import items 
from external_api import fetch_product_by_barcode

app = Flask(__name__)

# GET ROUTES
@app.route('/inventory')
def get_all_items():
    return jsonify({"inventory": items}), 200

@app.route("/inventory/<int:id>")
def get_single_items(id):
    for i in items:
        if i['id'] == id:
            return jsonify(i)
    return jsonify({"error": "Item not found"}), 404

# Used string type to avoid routing conflicts with the integer ID endpoint
@app.route('/inventory/<string:barcode>')
def get_product_by_barcode(barcode):
      product = fetch_product_by_barcode(barcode)
      if not product:
          return jsonify({"error": "Product not found"}), 404
      else:
          return jsonify(product), 200


# POST ROUTES
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

# Route to fetch an external item and append it directly to storage
@app.route("/inventory/import/<string:barcode>", methods=["POST"])
def import_product(barcode):
    product = fetch_product_by_barcode(barcode)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    new_id = max([i["id"] for i in items]) + 1 if items else 1
    # Keeping the code DRY by injecting the ID into the existing dict
    product["id"] = new_id
    items.append(product)
    return jsonify(product), 201
    

# PATCH ROUTES
@app.route('/inventory/<int:id>', methods=["PATCH"])
def update_items(id):
    item = next((i for i in items if i["id"] == id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404
    # Merged the incoming data directly into the item dictionary
    item.update(request.get_json())
    item["id"] = id
    return jsonify(item), 200



# DELETE ROUTES
@app.route('/inventory/<int:id>', methods=["DELETE"])
def delete_items(id):
    item = next((i for i in items if i["id"] == id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    items.remove(item)
    return jsonify({"message": "Item successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
