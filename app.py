from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import add_product, get_all_products, update_product, delete_product, register_user, verify_user, get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this for security

# Home route
@app.route('/')
def index():
    if 'user_id' not in session:
        flash('Please log in to manage products.', 'warning')
        return redirect(url_for('login'))
    products = get_all_products()
    return render_template('index.html', products=products)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if register_user(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Try a different username.', 'danger')
    
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_user(username, password)

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Add product
@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        flash('You must log in to add products.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        add_product(name, price, quantity)
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

# Update product
@app.route('/update/<string:product_name>', methods=['GET', 'POST'])
def update(product_name):
    if 'user_id' not in session:
        flash('You must log in to update products.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        update_product(product_name, price, quantity)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('update_product.html', product_name=product_name)

# Delete product
@app.route('/delete/<string:product_name>')
def delete(product_name):
    if 'user_id' not in session:
        flash('You must log in to delete products.', 'warning')
        return redirect(url_for('login'))
    
    delete_product(product_name)
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)