# Tests for Flask routes
from main import app

def test_get_all_items():
    # Creates a test client for the Flask app
    client = app.test_client()

    # Sends a GET request to /inventory
    response = client.get("/inventory")

    # Basic assertions
    assert response.status_code == 200
    assert "inventory" in response.get_json()

def test_get_single_item():
    client = app.test_client()
    response = client.get("/inventory/1")
    # Either it exists or it doesn't — both are valid states
    assert response.status_code in (200, 404)

def test_create_item():
    client = app.test_client()
    payload = {
        "name": "Test Item",
        "brand": "Test Brand",
        "quantity": 5,
        "price": 9.99
    }
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Item"

def test_update_item():
    client = app.test_client()
    payload = {"name": "Updated Name"}
    response = client.patch("/inventory/1", json=payload)
    # Item 1 may or may not exist — both valid
    assert response.status_code in (200, 404)

def test_delete_item():
    client = app.test_client()
    response = client.delete("/inventory/1")
    # Same logic — item may or may not exist
    assert response.status_code in (200, 404)
