from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from utils import get_user_by_username, get_all_menu_items, add_to_cart, get_cart, get_sales_history

app = Flask(__name__, template_folder='../frontend/templates')
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            return "Invalid login credentials", 401
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/menu')
def menu():
    items = get_all_menu_items()
    return render_template('menu.html', items=items)


@app.route('/add_to_cart/<item_id>', methods=['POST'])
def add_to_cart_route(item_id):
    add_to_cart(item_id)
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    items = get_cart()
    return render_template('cart.html', items=items)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Handle payment processing here
        return redirect(url_for('sales_history'))
    return render_template('checkout.html')


@app.route('/sales_history')
def sales_history():
    sales = get_sales_history()
    return render_template('sales_history.html', sales=sales)


@app.route('/inventory')
def inventory():
    return render_template('inventory.html')


if __name__ == '__main__':
    app.run(debug=True)
