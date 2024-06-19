import sqlite3

connection = sqlite3.connect('users.db')

with connection:
    connection.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    connection.execute('''
        INSERT INTO users (username, password) VALUES
        ('john', 'pigeons')
    ''')

connection.close()
