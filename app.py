from flask import Flask, render_template, g, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


Db = 'shortly.db'
app = Flask(__name__)
app.secret_key = "sUpErSeCrEtKeYtHiSiSsOsAfEhAhAhAiNeEdSlUsHiEs"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(Db)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

def init():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0
        );                 
    ''')
    db.commit()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("history.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template("login.html", success=request.args.get('success'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        existing = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            return render_template('signup.html', error='Username already taken')
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
        db.commit()
        return redirect(url_for('login', success='Account created successfully! Log In'))
    return render_template("signup.html")

@app.route('/shorten', methods=['POST'])
def shorten():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return '', 204

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/<code>')
def redirect_short(code):
    return '', 204

if __name__ == "__main__":
    with app.app_context():
        init()
    app.run(debug=True)