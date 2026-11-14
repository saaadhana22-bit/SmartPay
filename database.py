
import sqlite3

DB_NAME = "smartpay.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            monthly_salary REAL NOT NULL,
            net_salary REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_employee(name, emp_id, salary, net_salary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO employees
            (employee_name, employee_id, monthly_salary, net_salary)
            VALUES (?, ?, ?, ?)
        """, (name, emp_id, salary, net_salary))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_employees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    records = cursor.fetchall()

    conn.close()
    return records
