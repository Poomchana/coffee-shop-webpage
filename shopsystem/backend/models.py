import sqlite3

def create_connection():
    conn = sqlite3.connect('cafe.db')
    return conn


def get_user_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_all_menu_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE is_available=1")
    items = cursor.fetchall()
    conn.close()
    return items


def add_to_cart(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (item_id) VALUES (?)", (item_id,))
    conn.commit()
    conn.close()


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


def get_sales_history():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY transaction_date DESC")
    sales = cursor.fetchall()
    conn.close()
    return sales
