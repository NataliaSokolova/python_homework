import sqlite3
# Task 1: Complex JOINs with Aggregation
def task1():
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    query = """
    SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("Task 1: Order ID and Total Price for first 5 orders")
    for row in results:
        print(f"Order ID: {row[0]}, Total Price: {row[1]:.2f}")
    conn.close()
# Task 2: Understanding Subqueries
def task2():
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    query = """
    SELECT c.customer_name, AVG(sub.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b, SUM(p.price * li.quantity) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id, o.customer_id
    ) AS sub
    ON c.customer_id = sub.customer_id_b
    GROUP BY c.customer_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("\nTask 2: Understanding Subqueries")
    for row in results:
        name = row[0]
        avg_price = row[1]
        print(f"Customer: {name}, Average Total Price: {avg_price:.2f}" if avg_price is not None else f"Customer: {name}, No Orders")
# Task 3: An Insert Transaction Based on Data
def task3():
    print("\nTask 3: Inserting new order for Perez and Sons...")
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons';")
        customer_id = cursor.fetchone()[0]
        cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris';")
        employee_id = cursor.fetchone()[0]
        cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5;")
        product_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id)
            VALUES (?, ?)
            RETURNING order_id;
        """, (customer_id, employee_id))
        order_id = cursor.fetchone()[0]
        for pid in product_ids:
            cursor.execute("""
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, 10);
            """, (order_id, pid))
        conn.commit()
        cursor.execute("""
            SELECT li.line_item_id, li.quantity, p.product_name
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            WHERE li.order_id = ?;
        """, (order_id,))
        results = cursor.fetchall()
        print(f"Order ID: {order_id} created successfully.")
        for line_item_id, quantity, product_name in results:
            print(f"Line Item ID: {line_item_id}, Quantity: {quantity}, Product: {product_name}")
    except Exception as e:
        conn.rollback()
        print("Transaction failed:", e)
    finally:
        conn.close()
    conn.close()
# Task 4: Aggregation with HAVING
def task4():
    print("\nTask 4: Employees with more than 5 orders")
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    query = """
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id
    HAVING COUNT(o.order_id) > 5;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for emp_id, first, last, count in results:
        print(f"Employee ID: {emp_id}, Name: {first} {last}, Orders: {count}")
    conn.close()
if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()