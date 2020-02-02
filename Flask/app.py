# imports
from flask import Flask, request, g, redirect, url_for, \
                  render_template, flash, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# configuration
app = Flask(__name__)
app.config.from_pyfile('config.py')

# connect to database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# create the database
def init_db():
    app.config.from_pyfile('config.py')
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def home():
    return render_template('review.home.html')

@app.route('/about')
def about():
    return render_template('review.about.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already \
                   registered.'.format(username)        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES \
               (?, ?)', (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('login'))        
        flash(error)   
    return render_template('auth.register.html')

@app.route('/login')
def login():
    return render_template('auth.login.html')


@app.route('/<page_name>')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' \
                             % page_name, 404)
    return response

if __name__ == '__main__':
    app.run(debug=True)
