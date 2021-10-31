import os
from os import environ
import sqlite3
from flask import Flask, g, render_template, request, session, flash, redirect, url_for, abort, jsonify
from config import Config, DevConfig

# Using a production configuration
# app.config.from_object('config.ProdConfig')

# Using a development configuration
# app.config.from_object('config.DevConfig')

DATABASE = "flaskr.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = os.environ.get('SECRET_KEY')


# create and initialize a new Flask app

app = Flask(__name__)

# Using a production configuration
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# generate secret keys
#   >>> import uuid
#   >>> uuid.uuid4().hex
#   '3d6f45a5fc12445dbac2f59c3b6c7cb1'

# >>> import secrets
# >>> secrets.token_urlsafe(16)
# 'Drmhze6EPcv0fN_81Bj-nA'
# >>> secrets.token_hex(16)
# '8f42a73054b1749f8f58848be5e6502c'

# >>> import os
# >>> os.urandom(12).hex()
# 'f3cfe9ed8fae309f02079dbf'

# connect to database
def connect_db():
    """Connects to the database."""
    rv = sqlite3.connect(Config.DATABASE)
    rv.row_factory = sqlite3.Row
    return rv


# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


# open database connection
def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


@app.route("/")
def index():
    '''Searches the db for entries, then displays them'''
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database."""
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute(
        'insert into entries (title, text) values (?, ?)',
        [request.form['title'], request.form['text']]
    )
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/delete/<post_id>', methods=['GET'])
def delete_entry(post_id):
    """Delete post from database"""
    result = {'status': 0, 'message': 'Error'}
    try:
        db = get_db()
        db.execute('delete from entries where id=' + post_id)
        db.commit()
        result = {'status': 1, 'message': "Post Deleted"}
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run()
