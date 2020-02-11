from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('plans', __name__, url_prefix='/plans')

#creates an entry in the post table, needs to lead into creating pages of the post
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
			'INSERT INTO post(title, body, author_id) VALUES (?,?,?)',
			(title, body, g.user['id']))
			db.commit()
			return redirect(url_for('plans.page', ID=24, Pos=0))
		flash(error)
	return render_template('plans/create.html')

#method for creating the actual pages of the posts, passing arguments may need to be done by info in url, will test
@bp.route('/<int:ID>/<int:Pos>/edit', methods=( 'GET', 'POST')) 
def page(ID,Pos):
	#initialize variables
	if ID is None:
		return redirect(url_for('plans.create'))
	post=None	
	db=get_db()
	#check if there is a page that already exists, to incorporate an editor
		#pre load as place holder?
	#post=get_db().execute(
	#	'SELECT prog_id, position, title, body, goal'
	#	'FROM pages'
	#	'WHERE prog_id = (?) AND position = (?) ',
	#	(ID, Pos)
	#).fetchone()
		
	#if post is not None:
	#	request.form['title']=post['title']
	#	request.form['body']=post['body']  
	#	request.form['goal']=post['goal']
	#allow user to edit, and then commit the changes to the database (SQL part)
	if request.method=='POST': 
		title=request.form['title']
		body=request.form['body']
		goal=request.form['Goals']		
		error=None
		if not title:
			error="The Plan Must have a title"
		elif not body:
			error="The Plan Must have a body"
		elif not goal:
			error="The Plan Must have a goal"
		if error is None:  #if the post already exists, and the user is editing then should update not create another entry
			if post is None:
				db.execute(
				'INSERT INTO pages(prog_id, position, title, body, goal) VALUES (?,?,?,?,?)',
				(ID,Pos,title, body, goal))
				db.commit()
				return redirect(url_for('home.home'))
			
			else:
				db.execute(
					'UPDATE post' 
					'SET title=?, body=?, goal=?',
					(title, body, goal)
				)
				db.commit()
				return redirect(url_for('home.home'))
		
		flash(error)
	return render_template('plans/page.html')

		 

@bp.route('/view') #used to allow users to see all of their posts, and can make an override that will share all sharable posts
def view():
	
	posts=get_db().execute(
		'SELECT author_id, created, title, body '
		'FROM post '	
		'ORDER BY created DESC'
	).fetchall()
	return render_template('plans/view.html', posts=posts)
		

def getID(author): # used to find the id of the post, which is then used as the identifier, the linker between the post head and the pages after it
	#picks up most recent post by that author and returns the ID, should work
	PostID=get_db().execute(
		'SELECT id'
		'FROM post'
		'WHERE author_id = (?)',
		(author,)).fetchone()
	return PostID['id']



