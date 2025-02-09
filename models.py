import mysql.connector

# MySQL Connection Configuration
db_config = {
    "host": "localhost",
    "user": "root",  # Change to your MySQL username
    "password": "Sameer@123",  # Change to your MySQL password
    "database": "product_management"
}

# Function to create a MySQL connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to add a product
def add_product(name, price, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
    conn.commit()
    conn.close()

# Function to fetch all products
def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

# Function to update a product
def update_product(product_id, name, price, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s", (name, price, quantity, product_id))
    conn.commit()
    conn.close()

# Function to delete a product
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    conn.commit()
    conn.close()
