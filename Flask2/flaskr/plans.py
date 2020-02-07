from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('plans', __name__, url_prefix='/plans')

@bp.route('/create', methods=('GET', 'POST')) 
def create():
	if request.method=='post':
		title=request.form['title']
		body=request.form['body']
		goal=request.form['goal']
		error=None
		if not title:
			error="The Plan Must have a title"
		elif not body:
			error="The Plan Must have a body"
		elif not goal:
			error="The plan must have goal"
		if error is None:
			db.execute(
			'INSERT INTO plan(title, body, goal, author_id) VALUES (?,?)',
			(title, body, goal, g.user['id']))
			db.commit()
			return redirect(url_for('auth.create'))
		flash(error)
	return render_template('plans/create.html')

@bp.route('/view')
def view():
	return render_template('plans/view.html')
