# Flask API(main backend)
from flask import Flask, jsonify, request
import inventory 
app = Flask(__name__)

@app.route('/inventory')
def get_all_items():
    return jsonify({"inventory": inventory.items}), 200