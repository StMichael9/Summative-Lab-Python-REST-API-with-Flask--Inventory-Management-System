import requests

BASE_URL = "http://127.0.0.1:5000"

def show_menu():
    print("\n=== INVENTORY MANAGEMENT SYSTEM ===")
    print("1. View all items")
    print("2. View item by ID")
    print("3. Add item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Fetch product by barcode")
    print("7. Import product by barcode")
    print("8. Exit")

def request_json(method, endpoint, payload=None):
    try:
        url = f"{BASE_URL}{endpoint}"
        res = requests.request(method, url, json=payload)
        return res.status_code, res.json()
    except requests.exceptions.ConnectionError:
        print("\n❌ Server not reachable. Make sure Flask is running.")
        return None, None

def view_all_items():
    status, data = request_json("GET", "/inventory")
    if status == 200:
        items = data.get("inventory", [])
        if not items:
            print("No items in inventory.")
            return
        for item in items:
            print(f"ID: {item['id']} | {item['name']} ({item['brand']}) "
                  f"- Qty: {item['quantity']} - ${item['price']}")
    else:
        print("Failed to fetch inventory.")

def view_item_by_id():
    item_id = input("Enter Item ID: ")
    if not item_id.isdigit():
        print("ID must be a number.")
        return
    status, data = request_json("GET", f"/inventory/{item_id}")
    if status == 200:
        for k, v in data.items():
            print(f"{k.capitalize()}: {v}")
    else:
        print("Item not found.")

def add_item():
    name = input("Name: ")
    brand = input("Brand: ")
    quantity = input("Quantity: ")
    price = input("Price: ")

    try:
        payload = {
            "name": name,
            "brand": brand,
            "quantity": int(quantity),
            "price": float(price)
        }
    except ValueError:
        print("Invalid quantity or price.")
        return

    status, data = request_json("POST", "/inventory", payload)
    print("Success!" if status == 201 else "Failed to add item.")
    print(data)

def update_item():
    item_id = input("Enter Item ID: ")
    if not item_id.isdigit():
        print("Invalid ID.")
        return

    payload = {}
    for field in ["name", "brand", "quantity", "price"]:
        value = input(f"New {field} (blank to skip): ")
        if value:
            if field == "quantity" and not value.isdigit():
                print("Invalid quantity. Skipping.")
                continue
            if field == "price":
                try:
                    value = float(value)
                except ValueError:
                    print("Invalid price. Skipping.")
                    continue
            payload[field] = value

    if not payload:
        print("No updates provided.")
        return

    status, data = request_json("PATCH", f"/inventory/{item_id}", payload)
    print("Updated!" if status == 200 else "Update failed.")
    print(data)

def delete_item():
    item_id = input("Enter Item ID: ")
    if not item_id.isdigit():
        print("Invalid ID.")
        return
    status, data = request_json("DELETE", f"/inventory/{item_id}")
    print(data.get("message", "Delete failed."))

def fetch_product():
    barcode = input("Enter barcode: ").strip()
    if not barcode:
        print("Barcode cannot be blank.")
        return
    status, data = request_json("GET", f"/inventory/{barcode}")
    print(data if status == 200 else "Product not found.")

def import_product():
    barcode = input("Enter barcode to import: ").strip()
    if not barcode:
        print("Barcode cannot be blank.")
        return
    status, data = request_json("POST", f"/inventory/import/{barcode}")
    print(data if status == 201 else "Import failed.")

def main():
    actions = {
        "1": view_all_items,
        "2": view_item_by_id,
        "3": add_item,
        "4": update_item,
        "5": delete_item,
        "6": fetch_product,
        "7": import_product
    }

    while True:
        show_menu()
        choice = input("\nChoose an option (1-8): ")

        if choice == "8":
            print("Goodbye!")
            return

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")
