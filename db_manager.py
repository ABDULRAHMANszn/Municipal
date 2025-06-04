import sqlite3
import os

# المسار الديناميكي للقاعدة
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bills_admin", "data.db")


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # جدول المستخدمين
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # جدول الفواتير (نوع + username)
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
            type TEXT,  -- water / electricity / gas / cleaning
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
);

           """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            contact TEXT,
            description TEXT,
            complaint_type TEXT,
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    print("Tables created successfully.")
    conn.commit()
    conn.close()


def get_user_id(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_all_usernames():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
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
