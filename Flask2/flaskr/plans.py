from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('plans', __name__, url_prefix='/plans')

########plans.create
##Design: creates a post, which has mutable attributes title and body. Upon completion redirects to pages
##Input: None
##Outputs: will create or (update need to implement) a post, basically a title page and will redirect to create a page
########
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
			postID=getID(g.user['id'])
			return redirect(url_for('plans.page', ID=postID, Pos=0))
		flash(error)
	return render_template('plans/create.html')

########plans.page
##Design: used to create a page which is a subunit of a post, has mutable attributes ptitle, pbody and goal. Do not confuse with title and body which are attributes of post
##Input: Program (ID), used to assign ownership of page to post and POSITION(POS), used to determine the position at which the post lies
##Outputs: will either create a new db entry for a page or will update a previously existing
########
@bp.route('/<int:ID>/<int:Pos>/edit', methods=( 'GET', 'POST'))
def page(ID,Pos):
	#initialize variables
	if ID is None:
		return redirect(url_for('plans.create'))
	post=None
	db=get_db()
	#check if there is a page that already exists, to incorporate an editor
		#pre load as place holder?
	post=get_db().execute(
		'SELECT prog_id, position, ptitle, pbody, goal FROM pages WHERE prog_id = ? AND position = ?', (ID, Pos,)
	).fetchone()

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
				'INSERT INTO pages(prog_id, position, ptitle, pbody, goal) VALUES (?,?,?,?,?)',
				(ID,Pos,title, body, goal))
				db.commit()
				return redirect(url_for('plans.page', ID=ID, Pos=Pos))

			else:
				db.execute(
					'UPDATE pages SET ptitle=?, pbody=?, goal=? WHERE prog_id= ? AND position=?', (title, body, goal, ID, Pos,)
				)
				db.commit()
				return redirect(url_for('plans.page', ID=ID, Pos=Pos))

		flash(error)
	return render_template('plans/page.html', post=post, postID=ID, position=Pos)


########plans.view
##Design: views a post of choice without ability to edit
##Input: Program (ID), used to assign ownership of page to post and POSITION(POS), used to determine the position at which the post lies
##Outputs: returns a "post" that is displayed. Need to update names
########
@bp.route('/<int:ID>/<int:Pos>/view', methods=( 'GET', 'POST'))  #used to allow users to see all of their posts, and can make an override that will share all sharable posts
def view(ID, Pos):

	posts=get_db().execute(
		'SELECT * FROM pages JOIN post ON pages.prog_id=post.id JOIN user ON user.id=post.author_id WHERE prog_id = ? AND position = ?', (ID, Pos)
	).fetchone()
	return render_template('plans/view.html', post=posts)

########plans.create
##Design: creates a post, which has mutable attributes title and body. Upon completion redirects to pages
##Input: None
##Outputs: will create or (update need to implement) a post, basically a title page and will redirect to create a page
########
def getID(author): # used to find the id of the post, which is then used as the identifier, the linker between the post head and the pages after it
	#picks up most recent post by that author and returns the ID, should work
	PostID=get_db().execute(
		'SELECT * FROM post WHERE author_id = ? ORDER BY created DESC' , (author,) ).fetchone()
	return PostID['id']
