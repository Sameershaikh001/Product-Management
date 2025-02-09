from flask import Flask, render_template, request, redirect, url_for
from database import add_product, get_all_products, update_product, delete_product

app = Flask(__name__)

@app.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        add_product(name, price, quantity)
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/update/<string:product_name>', methods=['GET', 'POST'])
def update(product_name):
    if request.method == 'POST':
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        update_product(product_name, price, quantity)
        return redirect(url_for('index'))
    return render_template('update_product.html', product_name=product_name)

@app.route('/delete/<string:product_name>')
def delete(product_name):
    delete_product(product_name)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
