import sqlite3

def create_users_table():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("users table created (if it wasn't already).")


def create_employees_table():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Employees table created (if it wasn't already).")


def register_user(username, name, surname, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match."

    try:
        create_users_table()
        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone():
            return "Username already exists."

        c.execute("""
            INSERT INTO users (username, name, surname, password)
            VALUES (?, ?, ?, ?)
        """, (username, name, surname, password))

        conn.commit()
        return "Registered successfully!"

    except sqlite3.Error as e:
        return f"Database error: {e}"

    finally:
        conn.close()


def check_credentials(username, password):
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()

        return bool(result)

    except sqlite3.Error as e:
        print("Database error:", e)
        return False

    finally:
        conn.close()


def get_all_users():
    """
    جلب كل المستخدمين من قاعدة البيانات.
    """
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT id, username, name, surname, password FROM users")
    users = c.fetchall()
    conn.close()
    return users


def update_user(user_id, name, surname, password):
    """
    تحديث بيانات مستخدم بناءً على الـ ID.
    """
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
              UPDATE users
              SET name     = ?,
                  surname  = ?,
                  password = ?
              WHERE id = ?
              """, (name, surname, password, user_id))
    conn.commit()
    conn.close()


def delete_user_by_id(user_id):
    """
    حذف مستخدم بناءً على الـ ID.
    """
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


