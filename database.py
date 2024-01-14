import sqlite3
import os

def create_db():
    if not os.path.exists('users.db'):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE users (
                               id INTEGER PRIMARY KEY,
                               first_name TEXT,
                               last_name TEXT,
                               email TEXT UNIQUE,
                               password TEXT)''')
        connection.commit()
        connection.close()