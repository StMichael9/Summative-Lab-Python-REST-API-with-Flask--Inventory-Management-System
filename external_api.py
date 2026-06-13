# OpenFoodFacts API

import requests

def fetch_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    if data.get("status") == 0:
        return None
    product = data.get("product", {})

    return {
        "name": product.get("product_name"),
        "brand": product.get("brands"),
        "ingredients": product.get("ingredients_text"),
        "nutriscore": product.get("nutriscore_grade")
    }