import mysql.connector
from database import get_db_connection
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
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


# Create Users Table
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Create Products Table
def create_products_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            quantity INT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize tables
create_users_table()
create_products_table()

# Function to register user
def register_user(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                   (username, email, hashed_password))
    conn.commit()
    conn.close()

# Function to verify user login
def verify_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.check_password_hash(user['password'], password):
        return user
    return None

