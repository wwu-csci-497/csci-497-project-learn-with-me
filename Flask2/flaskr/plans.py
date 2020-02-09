from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('plans', __name__, url_prefix='/plans')

@bp.route('/create', methods=('GET', 'POST')) #creates an entry in the post table, needs to lead into creating pages of the post
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
			db.execute(
			'INSERT INTO plan(title, body, author_id) VALUES (?,?,?)',
			(title, body, g.user['id']))
			db.commit()
			return redirect(url_for('plans.page'))
		flash(error)
	return render_template('plans/create.html')


@bp.route('/edit', methods= 'GET', 'POST')) #method for creating the actual pages of the posts
def page(Pos, ID):
	#initialize variables
		
	#check if there is a page that already exists, to incorporate an editor
		#pre load as place holder?
	post=get_db().execute(
		'SELECT prog_id, position, title, body, goal'
		'FROM pages'
		'WHERE prog_id=? and position= ?',
		(Pos, ID)).fetchone()
		
	if post is not None:
		request.form['title']=post['title']
		request.form['body']=post['body']  
		request.form['goal']=post['goal']
	#allow user to edit, and then commit the changes to the database (SQL part)
		
	if request.method=='POST': 
		title=request.form['title']
		body=request.form['body']
		goal=request.form['goal']		
		error=None
		if not title:
			error="The Plan Must have a title"
		elif not body:
			error="The Plan Must have a body"
		if error is None and post is None:
			db.execute(
			'INSERT INTO pages(title, body, goal, author_id) VALUES (?,?,?)',
			(title, body, goal))
			db.commit()
			return redirect(url_for('plans.page'))
			
		else:
			db.execute(
				'UPDATE post' 
				'SET title=?, body=?, goal=?',
				(title, body, goal)
			)
			db.commit()
			return redirect(url_for('plans.page'))
		flash(error)
	return render_template('plans/edit.html')

		 

@bp.route('/view') #used to allow users to see all of their posts, and can make an override that will share all sharable posts
def view():
	db=get_db()
	posts=db.execute(
		'SELECT title, body, created, author_id, username'
		'FROM post JOIN user on post.author_id = user.id'
		'ORDER BY created DESC'
	).fetchall()
	return render_template('plan/view.html')
		



