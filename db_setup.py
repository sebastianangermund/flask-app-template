import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect('users.db')

with connection:
    connection.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            gamestate TEXT,
            points JSON
        )
    ''')

    connection.execute('''
        INSERT INTO users (username, password) VALUES
        ('agge', '123Hejsan')
    ''')

connection.close()
