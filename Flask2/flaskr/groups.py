from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('groups', __name__, url_prefix='/groups')

@bp.route('/<string:ID>/')
def groups(ID):
	return render_template('groups/groups.html', groups=groups)

@bp.route('/create', methods=('GET', 'POST'))
def create():
	if request.method=='POST':
		title=request.form['title']
		body=request.form['body']
		error=None
		if not title:
			error="The Plan Must have a title"
		elif not body:
			error="The Plan Must have a body"
		if error is None:
			db=get_db()
			db.execute(
			'INSERT INTO posts(title, body, author_id) VALUES (?,?,?)',
			(title, body, g.user['id']))
			db.commit()
			postID=getID(g.user['id'])
			return redirect(url_for('plans.page', ID=postID, Pos=0))
		flash(error)
	return render_template('plans/create.html')



