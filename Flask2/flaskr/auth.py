import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp=Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method =='POST':
		username=request.form['username']
		password=request.form['password']
		confPassword=request.form['CheckPassword']
		db=get_db()
		error=None
	
		if not username:
			error='Username is required'
		elif not password:
			error='Password is required'
		elif password != confPassword:
			error='Passwords must match'
		elif db.execute(
			'SELECT id FROM users WHERE username = ?', (username,)
			).fetchone() is not None:
				error= 'user {} is already registered.'.format(username)
		if error is None:
			db.execute(
			'INSERT INTO users(username, password) VALUES (?,?)', 
			(username, generate_password_hash(password))
			) ## ? are filled with tuple after 
			db.commit()
			return redirect(url_for('auth.login'))
		flash(error)
	return render_template('auth/register.html')


@bp.route('/login', methods=('GET','POST'))
def login():
	if request.method =='POST':
		username=request.form['username']
		password=request.form['password']
		db=get_db()
		error=None
		user=db.execute(
		'SELECT * FROM users WHERE username=?', (username,)
		).fetchone()
		
		if user is None:
			error='incorrect username'
		elif not check_password_hash(user['password'], password):
			error='incorrect password'
		
		if error is None:
			session.clear() #saves session
			session['user_id']=user['id']
			return redirect(url_for('home.home'))
		flash(error)
	return render_template('auth/login.html')


@bp.before_app_request #loads a previously logged in user
def load_logged_in_user():
	user_id=session.get('user_id')

	if user_id is None: 
		g.user=None
	else:
		g.user=get_db().execute(
		'SELECT * FROM users WHERE id =?', (user_id,)
		).fetchone()


@bp.route('/logout') #self explanatory
def logout():
	session.clear()
	return redirect(url_for('auth.login'))

def login_required(view): # if user is not logged in it will redirect
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
		return view(**kwargs)
	return wrapped_view









