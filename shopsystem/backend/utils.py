import sqlite3
from datetime import datetime

# Create a connection to the database
def create_connection():
    conn = sqlite3.connect('cafe.db')
    return conn


# Get user by username (for login purposes)
def get_user_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


# Get all available menu items
def get_all_menu_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE is_available=1")
    items = cursor.fetchall()
    conn.close()
    return items


# Add an item to the cart
def add_to_cart(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (item_id) VALUES (?)", (item_id,))
    conn.commit()
    conn.close()


# Remove an item from the cart
def remove_from_cart(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()


# Get the items currently in the cart
def get_cart():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT menu_items.id, menu_items.name, menu_items.price 
        FROM cart
        JOIN menu_items ON cart.item_id = menu_items.id
    """)
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items


# Get sales history (all past sales transactions)
def get_sales_history():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY transaction_date DESC")
    sales = cursor.fetchall()
    conn.close()
    return sales


# Calculate the total amount of the items in the cart
def calculate_cart_total():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(menu_items.price) 
        FROM cart
        JOIN menu_items ON cart.item_id = menu_items.id
    """)
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0


# Checkout the cart and record the sale in the sales table, then clear the cart
def checkout(payment_method):
    # Calculate the total amount for the transaction
    total_amount = calculate_cart_total()
    
    # Insert the sale transaction into the sales table
    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = create_connection()
    cursor = conn.cursor()
    
    # Insert sale into sales table
    cursor.execute("""
        INSERT INTO sales (transaction_date, total_amount, payment_method) 
        VALUES (?, ?, ?)
    """, (transaction_date, total_amount, payment_method))
    
    # Get the sale ID of the inserted transaction (to later update with discount, if any)
    sale_id = cursor.lastrowid
    conn.commit()
    
    # Clear the cart
    cursor.execute("DELETE FROM cart")
    conn.commit()
    conn.close()
    
    return sale_id  # Return the sale ID to use for further processing (like discount, etc.)
