from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('greeting'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and (user['password'] == password):
            session['user_id'] = user['id']
            return redirect(url_for('greeting'))

        return 'Invalid username or password'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if existing_user:
            return 'Username already exists'

        conn.execute(f'INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/greeting')
def greeting():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('greeting.html', username=session['user_id'])

@app.route('/interactive', methods=['GET', 'POST'])
def interactive():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        search_text = request.form['search_text']
        
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users WHERE username LIKE ?', ('%' + search_text + '%',)).fetchall()
        conn.close()
        
        return render_template('interactive.html', users=users)
    
    return render_template('interactive.html', users=[])

if __name__ == '__main__':
    app.run(debug=True)
