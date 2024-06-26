from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from random import randint


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
        username = request.form['username'].lower()
        password = request.form['password'].lower()
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and (user['password'] == password):
            session['user_id'] = user['username']
            if user['username'] == 'john':
                return redirect(url_for('interactive'))
            else:
                return redirect(url_for('greeting'))
        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password'].lower()
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
    if session['user_id'] == 'John':
        return redirect(url_for('interactive'))
    return render_template('greeting.html', username=session['user_id'])

@app.route('/interactive', methods=['GET', 'POST'])
def interactive():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        search_text = request.form['search_text']
        responses = ['yippee ki yay, that\'s wrong', 'yippee ki try again, motherfucker', 'the bomb would have blown by now']
        response = '784' if search_text == '52054' else responses[randint(0, len(responses)-1)]
        # conn = get_db_connection()
        # users = conn.execute('SELECT * FROM users WHERE username LIKE ?', ('%' + search_text + '%',)).fetchall()
        # conn.close()
        return render_template('interactive.html', users=[response])
    return render_template('interactive.html', users=[])


if __name__ == "__main__":
    app.run(debug=False)