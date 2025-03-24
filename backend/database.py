import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('cafe.db')
        return conn
    except Error as e:
        print(e)
    return conn

def initialize_database():
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            
            # Users table
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT UNIQUE NOT NULL,
                         password TEXT NOT NULL,
                         role TEXT NOT NULL)''')
            
            # Inventory table
            c.execute('''CREATE TABLE IF NOT EXISTS inventory
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         quantity INTEGER NOT NULL,
                         unit TEXT NOT NULL,
                         threshold INTEGER)''')
            
            # Menu items table
            c.execute('''CREATE TABLE IF NOT EXISTS menu_items
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         description TEXT,
                         price REAL NOT NULL,
                         category TEXT,
                         is_available BOOLEAN DEFAULT 1)''')
            
            # Discounts table
            c.execute('''CREATE TABLE IF NOT EXISTS discounts
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         description TEXT,
                         discount_percent REAL NOT NULL,
                         start_date TEXT NOT NULL,
                         end_date TEXT NOT NULL,
                         is_active BOOLEAN DEFAULT 1)''')
            
            # Promotions table
            c.execute('''CREATE TABLE IF NOT EXISTS promotions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         description TEXT,
                         promo_code TEXT UNIQUE,
                         start_date TEXT NOT NULL,
                         end_date TEXT NOT NULL,
                         is_active BOOLEAN DEFAULT 1)''')
            
            # Sales table
            c.execute('''CREATE TABLE IF NOT EXISTS sales
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         transaction_date TEXT NOT NULL,
                         total_amount REAL NOT NULL,
                         discount_applied REAL DEFAULT 0,
                         payment_method TEXT NOT NULL)''')
            
            # Members table
            c.execute('''CREATE TABLE IF NOT EXISTS members
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         phone TEXT UNIQUE NOT NULL,
                         email TEXT UNIQUE,
                         points INTEGER DEFAULT 0,
                         join_date TEXT NOT NULL,
                         is_active BOOLEAN DEFAULT 1)''')
            
            # Insert admin user if not exists
            c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                     ('admin', 'admin123', 'admin'))
            
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

initialize_database()