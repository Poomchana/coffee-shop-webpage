# Additional helper functions for cart management, sales history, etc. can be added here.
import sqlite3

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
    if user:
        return {'id': user[0], 'username': user[1], 'password': user[2], 'role': user[3], 'is_active': user[4]}
    return None

# Get all available menu items
def get_all_menu_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE is_available=1")
    items = cursor.fetchall()
    conn.close()
    return items

# Add an item to the cart (simple cart example, storing in a cart table)
def add_to_cart(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (item_id) VALUES (?)", (item_id,))
    conn.commit()
    conn.close()

# Get items currently in the cart
def get_cart():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT menu_items.name, menu_items.price 
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

# Remove item from the cart (for simplicity, only based on item_id)
def remove_from_cart(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()

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
