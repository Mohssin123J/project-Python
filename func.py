import sqlite3
from datetime import datetime

DB_NAME = "hotel.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            phone TEXT,
            national_id TEXT,
            room_type TEXT,
            rooms INTEGER,
            start_date TEXT,
            end_date TEXT,
            days INTEGER,
            total_price REAL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_admins_once():
    conn = get_connection()
    cur = conn.cursor()

    admins = [
        ("yassine", "yassine@gmail.com", "1234"),
        ("mohssin", "mohssin@gmail.com", "1234"),
        ("majid", "majid@gmail.com", "1234"),
        ("ayman", "ayman@gmail.com", "1234"),
        ("zakariya", "zakariya@gmail.com", "1234"),
    ]

    cur.executemany("""
        INSERT OR IGNORE INTO admins (username, email, password)
        VALUES (?, ?, ?)
    """, admins)

    conn.commit()
    conn.close()


def check_admin_login(username, email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM admins
        WHERE username = ? AND email = ? AND password = ?
    """, (username, email, password))
    admin = c.fetchone()
    conn.close()
    return admin


def calculate_days(start_date, end_date):
    d1 = datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    days = (d2 - d1).days
    if days <= 0:
        raise ValueError("Veuillez saisir l'heure correctement")
    return days


def insert_reservation(full_name, phone, national_id, room_type,
                       rooms, start_date, end_date, price_per_night):
    days = calculate_days(start_date, end_date)
    total_price = days * price_per_night * rooms

    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO reservations
        (full_name, phone, national_id, room_type, rooms,
         start_date, end_date, days, total_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        full_name, phone, national_id, room_type, rooms,
        start_date, end_date, days, total_price
    ))

    reservation_id = c.lastrowid
    conn.commit()
    conn.close()
    return reservation_id, total_price


def get_reservation_by_id(res_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM reservations WHERE id = ?", (res_id,))
    data = c.fetchone()
    conn.close()
    return data


def get_reservation_by_nid(nid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM reservations WHERE national_id = ?", (nid,))
    data = c.fetchone()
    conn.close()
    return data


def get_all_reservations():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM reservations")
    data = c.fetchall()
    conn.close()
    return data


def delete_reservation(res_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM reservations WHERE id = ?", (res_id,))
    conn.commit()
    conn.close()
