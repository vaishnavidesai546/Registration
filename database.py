import sqlite3
from datetime import datetime

DB_NAME = 'registration.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Registration (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                DateOfBirth DATE NOT NULL,
                PhoneNumber TEXT,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def create_registration(name, email, dob, phone=None):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Registration (Name, Email, DateOfBirth, PhoneNumber)
                VALUES (?, ?, ?, ?)
            ''', (name, email, dob, phone))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        return f"Error: {e}"

def get_registration_by_id(reg_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Registration WHERE ID = ?', (reg_id,))
        return cursor.fetchone()

def get_all_registrations():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Registration')
        return cursor.fetchall()

def update_registration(reg_id, name=None, email=None, dob=None, phone=None):
    fields = []
    values = []

    if name:
        fields.append("Name = ?")
        values.append(name)
    if email:
        fields.append("Email = ?")
        values.append(email)
    if dob:
        fields.append("DateOfBirth = ?")
        values.append(dob)
    if phone:
        fields.append("PhoneNumber = ?")
        values.append(phone)

    if not fields:
        return "No fields to update."

    values.append(reg_id)
    query = f"UPDATE Registration SET {', '.join(fields)} WHERE ID = ?"

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount

def delete_registration(reg_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Registration WHERE ID = ?', (reg_id,))
        conn.commit()
        return cursor.rowcount
