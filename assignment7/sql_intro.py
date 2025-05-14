import sqlite3
import os

def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    try:
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to {db_file}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def close_connection(conn):
    if conn:
        conn.close()

def create_tables(conn):
    """Create tables"""
    try:
        cursor = conn.cursor()

        # publishers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        # magazines
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(id)
            )
        """)

        # subscribers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE(name, address)
            )
        """)

        # subscriptions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id),
                UNIQUE(subscriber_id, magazine_id)
            )
        """)

        conn.commit()
        print("Tables created successfully")
    except sqlite3.Error as e:
        print("Error creating tables:", e)

def add_publisher(conn, name):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.Error as e:
        print("Error adding publisher:", e)

def add_magazine(conn, name, publisher_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (publisher_name,))
        publisher_id = cursor.fetchone()
        if publisher_id:
            cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", 
                          (name, publisher_id[0]))
            conn.commit()
            print(f"Magazine '{name}' added under publisher '{publisher_name}'")
        else:
            print(f"Publisher '{publisher_name}' not found")
    except sqlite3.Error as e:
        print("Error adding magazine:", e)

def add_subscriber(conn, name, address):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO subscribers (name, address) VALUES (?, ?)", 
                      (name, address))
        conn.commit()
        print(f"Subscriber added: '{name}', '{address}'")
    except sqlite3.Error as e:
        print("Error adding subscriber:", e)

def add_subscription(conn, subscriber_name, subscriber_address, magazine_name, expiration_date):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", 
                       (subscriber_name, subscriber_address))
        subscriber_id = cursor.fetchone()
        cursor.execute("SELECT id FROM magazines WHERE name = ?", (magazine_name,))
        magazine_id = cursor.fetchone()
        if subscriber_id and magazine_id:
            cursor.execute("""
                INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
                VALUES (?, ?, ?)
            """, (subscriber_id[0], magazine_id[0], expiration_date))
            conn.commit()
        else:
            if not subscriber_id:
                print(f"Subscriber '{subscriber_name}' at '{subscriber_address}' not found")
            if not magazine_id:
                print(f"Magazine '{magazine_name}' not found")
    except sqlite3.Error as e:
        print("Error adding subscription:", e)

def run_queries(conn):
    try:
        cursor = conn.cursor()

        print("\nAll Subscribers:")
        for row in cursor.execute("SELECT * FROM subscribers"):
            print(row)

        print("\nAll Magazines Sorted by Name:")
        for row in cursor.execute("SELECT * FROM magazines ORDER BY name"):
            print(row)

        print("\nMagazines Published by 'Penguin':")
        cursor.execute("""
            SELECT m.id, m.name 
            FROM magazines m
            JOIN publishers p ON m.publisher_id = p.id
            WHERE p.name = 'Penguin'
        """)
        for row in cursor.fetchall():
            print(row)

    except sqlite3.Error as e:
        print("Error running queries:", e)

if __name__ == "__main__":
    db_file = "../db/magazines.db"
    conn = create_connection(db_file)

    if conn:
        conn.execute("PRAGMA foreign_keys = 1")
        create_tables(conn)


        add_publisher(conn, "Penguin")
        add_publisher(conn, "Conde Nast")
        add_publisher(conn, "Time Inc")


        add_magazine(conn, "National Geographic", "Penguin")
        add_magazine(conn, "Vogue", "Conde Nast")
        add_magazine(conn, "TIME", "Time Inc")


        add_subscriber(conn, "Alice Smith", "123 Main St")
        add_subscriber(conn, "Bob Johnson", "456 Elm St")
        add_subscriber(conn, "Alice Smith", "123 Main St")  # Will be ignored

 
        add_subscription(conn, "Alice Smith", "123 Main St", "TIME", "2025-12-31")
        add_subscription(conn, "Bob Johnson", "456 Elm St", "Vogue", "2025-08-31")


        run_queries(conn)


        close_connection(conn)
