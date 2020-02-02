#auth

from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
	return render_template('auth/login.html')

@bp.route('/register', methods=('GET', 'POST'))
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
    return render_template('auth/register.html')
