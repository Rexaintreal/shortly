from flask import Flask, render_template, g
import sqlite3


Db = 'shortly.db'
app = Flask(__name__)

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
    return render_template("index.html")

@app.route('/shorten', methods=['POST'])
def shorten():
    pass

@app.route('/login')
def auth():
    return render_template("auth.html")

@app.route('/history')
def history():
    return render_template("history.html")

@app.route('/logout')
def logout():
    pass

@app.route('/<code>')
def redirect_short(code):
    pass

if __name__ == "__main__":
    with app.app_context():
        init()
    app.run(debug=True)