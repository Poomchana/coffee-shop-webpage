import sqlite3

def create_connection():
    conn = sqlite3.connect('cafe.db')
    return conn


def get_user_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()  # Fetch the user (returns a tuple)
    conn.close()

    # If user exists, return a dictionary with column names as keys
    if user:
        user_dict = {
            'id': user[0],         # Assuming 'id' is the first column
            'username': user[1],   # Assuming 'username' is the second column
            'password': user[2],   # Assuming 'password' is the third column
            'role': user[3],       # Assuming 'role' is the fourth column
            'is_active': user[4]   # Assuming 'is_active' is the fifth column
        }
        return user_dict
    return None


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
