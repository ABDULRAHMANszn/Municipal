import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            month TEXT,
            consumption REAL,
            amount REAL,
            Frate REAL,
            Arate REAL,
            type TEXT,
            status TEXT DEFAULT 'unpaid',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            firstname TEXT,
            lastname TEXT,
            email TEXT,
            phone TEXT,
            tc TEXT,
            city TEXT,
            sex TEXT,
            birthday TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            description TEXT,
            address TEXT,
            image_path TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            contact TEXT,
            description TEXT,
            complaint_type TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            suggestion TEXT,
            category TEXT,
            proposed_solution TEXT,
            placeholder TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visa_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            card_number TEXT,
            current_balance TEXT,
            topup_amount TEXT,
            owner_name TEXT,
            credit_card_number TEXT,
            month TEXT,
            year TEXT,
            cvv TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gas_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            address TEXT,
            property_type TEXT,
            stove_type TEXT,
            cylinder_size TEXT,
            usage TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cleaning_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            address TEXT,
            property_type TEXT,
            frequency TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS electricity_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            address TEXT,
            property_type TEXT,
            phase TEXT,
            usage TEXT,
            generator TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            address TEXT,
            property_type TEXT,
            residents INTEGER,
            usage TEXT,
            has_tank TEXT,
            tank_capacity TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")


def get_user_id(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_all_userW():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM water_subscriptions")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


def get_all_userC():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM cleaning_subscriptions")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


def get_all_userE():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM electricity_subscriptions")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


def get_all_userG():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM gas_subscriptions")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


def add_water_bill(user_id, username, month, consumption, amount, v1, v2):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bills (user_id, username, month, consumption, amount, Frate, Arate, type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'water', 'unpaid')
    """, (user_id, username, month, consumption, amount, v1, v2))
    conn.commit()
    conn.close()


def add_electricity_bill(user_id, username, month, consumption, amount, v1, v2):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bills (user_id, username, month, consumption, amount, Frate, Arate, type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'electricity', 'unpaid')
    """, (user_id, username, month, consumption, amount, v1, v2))
    conn.commit()
    conn.close()


def add_gas_bill(user_id, username, month, consumption, amount, v1, v2):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bills (user_id, username, month, consumption, amount, Frate, Arate, type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'gas', 'unpaid')
    """, (user_id, username, month, consumption, amount, v1, v2))
    conn.commit()
    conn.close()


def add_cleaning_bill(user_id, username, month, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bills (user_id, username, month, consumption, amount, Frate, Arate, type, status)
        VALUES (?, ?, ?, NULL, ?, NULL, NULL, 'cleaning', 'unpaid')
    """, (user_id, username, month, amount))
    conn.commit()
    conn.close()


def save_profile(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_profiles (user_id, firstname, lastname, email, phone, tc, city, sex, birthday)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            firstname=excluded.firstname,
            lastname=excluded.lastname,
            email=excluded.email,
            phone=excluded.phone,
            tc=excluded.tc,
            city=excluded.city,
            sex=excluded.sex,
            birthday=excluded.birthday
    """, data)
    conn.commit()
    conn.close()


def insert_service_request(user_id, service_type, description, address, image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO requests (user_id, type, description, address, image_path)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, service_type, description, address, image_path))
    conn.commit()
    conn.close()


def insert_complaint(user_id, title, contact, description, complaint_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (user_id, title, contact, description, complaint_type)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, title, contact, description, complaint_type))
    conn.commit()
    conn.close()


def insert_suggestion(user_id, suggestion, category, proposed_solution, placeholder):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO suggestions (user_id, suggestion, category, proposed_solution, placeholder)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, suggestion, category, proposed_solution, placeholder))
    conn.commit()
    conn.close()


def save_water_subscription(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO water_subscriptions 
        (username, address, property_type, residents, usage, has_tank, tank_capacity, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['username'],
        data['address'],
        data['type'],
        int(data['residents']),
        data['usage'],
        data['has_tank'],
        data['tank_capacity'] if data['has_tank'] == "Yes" else "N/A",
        data['notes']
    ))
    conn.commit()
    conn.close()


def save_electricity_subscription(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO electricity_subscriptions 
        (username, address, property_type, phase, usage, generator, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data['username'],
        data['address'],
        data['type'],
        data['phase'],
        data['usage'],
        data['generator'],
        data['notes']
    ))
    conn.commit()
    conn.close()


def save_cleaning_subscription(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cleaning_subscriptions 
        (username, address, property_type, frequency, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data['username'],
        data['address'],
        data['property_type'],
        data['frequency'],
        data['notes']
    ))
    conn.commit()
    conn.close()


def save_gas_subscription(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO gas_subscriptions 
        (username, address, property_type, stove_type, cylinder_size, usage, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data['username'],
        data['address'],
        data['property_type'],
        data['stove_type'],
        data['cylinder_size'],
        data['usage'],
        data['notes']
    ))
    conn.commit()
    conn.close()


def save_visa_subscription(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO visa_subscriptions (
            username, card_number, current_balance, topup_amount,
            owner_name, credit_card_number, month, year, cvv
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['username'],
        data['card_number'],
        data['balance'],
        data['topup'],
        data['owner'],
        data['credit_card'],
        data['month'],
        data['year'],
        data['cvv']
    ))
    conn.commit()
    conn.close()


def fetch_user_subscriptions(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    subscriptions = {
        "gas_subscriptions": ["address", "property_type", "usage"],
        "cleaning_subscriptions": ["address", "property_type", "frequency"],
        "electricity_subscriptions": ["address", "property_type", "usage"],
        "water_subscriptions": ["address", "property_type", "residents", "usage"],
    }

    all_rows = []
    for table, fields in subscriptions.items():
        try:
            fields_str = ", ".join(fields)
            query = f"SELECT '{table}', {fields_str} FROM {table} WHERE username = ?"
            cursor.execute(query, (username,))
            rows = cursor.fetchall()
            all_rows.extend(rows)
        except Exception as e:
            print(f"Error loading from {table}: {e}")

    conn.close()
    return all_rows


def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, name, surname, password FROM users")
    users = c.fetchall()
    conn.close()
    return users


def update_user(user_id, name, surname, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE users
        SET name = ?, surname = ?, password = ?
        WHERE id = ?
    """, (name, surname, password, user_id))
    conn.commit()
    conn.close()


def delete_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_all_user_requests_info():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()

    result = []

    for user_id, username in users:
        # complaint
        cursor.execute("SELECT description FROM complaints WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
        complaint = cursor.fetchone()
        complaint_text = complaint[0] if complaint else ""

        # request
        cursor.execute("SELECT description, status, id FROM requests WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                       (user_id,))
        request = cursor.fetchone()
        request_text = request[0] if request else ""
        request_status = request[1] if request else "Pending"
        request_id = request[2] if request else None

        # suggestion
        cursor.execute("SELECT suggestion FROM suggestions WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
        suggestion = cursor.fetchone()
        suggestion_text = suggestion[0] if suggestion else ""

        result.append((username, complaint_text, request_text, suggestion_text, request_id, request_status))

    conn.close()
    return result


def update_request_status(request_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = ? WHERE id = ?", (new_status, request_id))
    conn.commit()
    conn.close()


def fetch_unpaid_bills(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
            SELECT type, month, consumption, amount, status
            FROM bills
            WHERE username = ? AND status = 'unpaid'
        """, (username,))
    results = cursor.fetchall()
    conn.close()
    return results


def register_user(username, name, surname, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match."

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone():
            return "Username already exists."

        c.execute("""
            INSERT INTO users (username, name, surname, password)
            VALUES (?, ?, ?, ?)
        """, (username, name, surname, password))
        conn.commit()

        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        if result is None:
            return "Error: Could not retrieve user ID."
        user_id = result[0]

        return "Registered successfully!"

    except sqlite3.Error as e:
        return f"Database error: {e}"

    finally:
        if conn:
            conn.close()


def check_credentials(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()

        return bool(result)

    except sqlite3.Error as e:
        print("Database error:", e)
        return False

    finally:
        conn.close()


def create_employee_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    c.execute("SELECT * FROM employee WHERE username = ?", ("admin",))
    if not c.fetchone():
        c.execute("INSERT INTO employee (username, password) VALUES (?, ?)", ("admin", "admin"))
        print("Default admin user created.")
    conn.commit()
    conn.close()


def check_employee_credentials(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM employee WHERE username = ? AND password = ?", (username, password))
        return bool(c.fetchone())
    except sqlite3.Error as e:
        print("Database error:", e)
        return False
    finally:
        conn.close()


def user_has_visa(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM visa_subscriptions WHERE username = ?
    """, (username,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0  # يرجع True إذا عنده بطاقة


def mark_bill_as_paid(username, service, month):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE bills 
        SET status = 'paid' 
        WHERE username = ? AND type = ? AND month = ? AND status = 'unpaid'
    """, (username, service, month))
    conn.commit()
    conn.close()


def get_user_visa(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT card_number, owner_name FROM visa_subscriptions WHERE username = ?
        ORDER BY id DESC LIMIT 1
    """, (username,))
    result = cursor.fetchone()
    conn.close()
    return result  # إما (card_number, owner_name) أو None
