from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import add_product, get_db_connection, update_product, delete_product

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    if 'user_id' not in session:
        flash('You must log in to view products.', 'warning')
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {str(e)}", 'danger')
        products = []
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', products=products)

@routes.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        flash('You must log in to add products.', 'warning')
        return redirect(url_for('auth.login'))

    name = request.form['name'].strip()
    price = request.form['price']
    quantity = request.form['quantity']

    # Validate data
    if not name or not price or not quantity:
        flash('All fields are required!', 'danger')
        return redirect(url_for('routes.index'))

    try:
        price = float(price)
        quantity = int(quantity)
        add_product(name, price, quantity)
        flash('Product added successfully!', 'success')
    except ValueError:
        flash('Invalid input: Price must be a number, Quantity must be an integer.', 'danger')

    return redirect(url_for('routes.index'))

@routes.route('/update/<int:product_id>', methods=['POST'])
def update(product_id):
    if 'user_id' not in session:
        flash('You must log in to update products.', 'warning')
        return redirect(url_for('auth.login'))

    price = request.form['price']
    quantity = request.form['quantity']

    if not price or not quantity:
        flash('All fields are required!', 'danger')
        return redirect(url_for('routes.index'))

    try:
        price = float(price)
        quantity = int(quantity)
        update_product(product_id, price, quantity)
        flash('Product updated successfully!', 'success')
    except ValueError:
        flash('Invalid input format.', 'danger')

    return redirect(url_for('routes.index'))

@routes.route('/delete/<int:product_id>')
def delete(product_id):
    if 'user_id' not in session:
        flash('You must log in to delete products.', 'warning')
        return redirect(url_for('auth.login'))

    delete_product(product_id)
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('routes.index'))
