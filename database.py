import json

DB_FILE = "products.json"

def load_products():
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open(DB_FILE, 'w') as file:
        json.dump(products, file, indent=4)

def get_all_products():
    return load_products()

def add_product(name, price, quantity):
    products = load_products()
    products.append({"name": name, "price": price, "quantity": quantity})
    save_products(products)

def update_product(name, price, quantity):
    products = load_products()
    for product in products:
        if product["name"] == name:
            product["price"] = price
            product["quantity"] = quantity
            break
    save_products(products)

def delete_product(name):
    products = load_products()
    products = [product for product in products if product["name"] != name]
    save_products(products)
