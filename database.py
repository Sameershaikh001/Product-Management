import mysql.connector
from flask_bcrypt import Bcrypt
import config  # Import database credentials from config.py

bcrypt = Bcrypt()

# ✅ Establish database connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
    except mysql.connector.Error as err:
        print(f"❌ Database Connection Error: {err}")
        return None

# ✅ Fetch all products from the database
def get_all_products():
    conn = get_db_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

# ✅ Add a new product
def add_product(name, price, quantity):
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error adding product: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# ✅ Update product details
def update_product(name, price, quantity):
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE products SET price=%s, quantity=%s WHERE name=%s", (price, quantity, name))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error updating product: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# ✅ Delete a product
def delete_product(name):
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE name=%s", (name,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error deleting product: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# ✅ Register a new user with hashed password
def register_user(username, password):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    
    # Hash the password before storing
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print(f"✅ User '{username}' registered successfully!")  # Debugging
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error registering user: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# ✅ Verify user login
def verify_user(username, password):
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user["password"]

            print(f"🔹 Retrieved User: {user}")  # Debugging
            print(f"🔹 Stored Password (Hashed in DB): {repr(stored_password)}")  # Debugging

            # Verify hashed password using bcrypt
            if bcrypt.check_password_hash(stored_password, password):
                print("✅ Password Matched!")
                return user
            else:
                print("❌ Password Incorrect!")

        return None
    finally:
        cursor.close()
        conn.close()