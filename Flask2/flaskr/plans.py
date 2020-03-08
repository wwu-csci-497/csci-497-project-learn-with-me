from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
#for analytics
import datetime

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
			'INSERT INTO posts(title, body, author_id) VALUES (?,?,?)',
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
	return render_template('plans/page.html', post=post, ID=ID, position=Pos)


########plans.view
##Design: views a post of choice without ability to edit, but gives users ability to comment and rate 
##Input: Program (ID), used to assign ownership of page to post and POSITION(POS), used to determine the position at which the post lies
##Outputs: returns a "post" that is displayed. Need to update names
########
@bp.route('/<int:ID>/<int:Pos>/view', methods=( 'GET', 'POST'))  #used to allow users to see all of their posts, and can make an override that will share all sharable posts
def view(ID, Pos):
	db=get_db()
	#getting post from DB	
	posts=db.execute(
		'SELECT * FROM pages JOIN posts ON pages.prog_id=posts.id JOIN users ON users.id=posts.author_id WHERE prog_id = ? AND position = ?', (ID, Pos)
	).fetchone()
	#getting rating from DB
	rating=db.execute(
		'SELECT SUM(rate) as score FROM (SELECT DISTINCT author_id, rate from comments WHERE prog_id= ?)', (ID,)
	).fetchone()
	
	#used to determine if there should be a next button
	next=True
	nextPost=db.execute(
		'SELECT ptitle FROM pages JOIN posts ON pages.prog_id=posts.id JOIN users ON users.id=posts.author_id WHERE prog_id = ? AND position = ?', (ID, (Pos+1))
	).fetchone()
	if nextPost is None:
		next=False
	#getting comments from DB
	comms=db.execute(
		'SELECT U.username, C.comments FROM comments C JOIN users U ON U.id=C.author_id WHERE prog_id = ? AND position = ?', (ID, Pos)
	).fetchall()

	#time tracking Creates analytics entry with timeIn, later updated with timeOut. Helper function to purge lost(no timeOut) analytics IDs
	time=datetime.datetime.now()
	db.execute(
		'INSERT INTO analytics(P_id, U_id, pos, timeIn, viewed, timeOut) VALUES (?,?,?,?,?,?)',
		(ID,g.user['id'], Pos, time , 1, 0))
	db.commit()
	#grabs analytics ID to then pass to DCAR
	analyticID= db.execute(
			'SELECT A_id as aid from analytics where P_id=? and U_id=? and timeOut=? ORDER BY aid DESC',(ID, g.user['id'], 0)
	).fetchone()

	if request.method=='POST':
		comment=request.form['body']
		try:
			rate=request.form['rate']
		except: 
			rate=0
		error=None
		if not comment:
			error="Comments Must have a body"
		elif error is None:
			db.execute(
			'INSERT INTO comments(prog_id, author_id, position, comments, rate) VALUES(?,?,?,?,?)',
			(ID, g.user['id'], Pos, comment, rate ))
			db.commit()
			return redirect(url_for('plans.view', ID=ID, Pos=Pos))
		flash(error)
	#of all these, there is not a single one with a good name 
	return render_template('plans/view.html', post = posts,  postID = ID, position = Pos, next = next, comms = comms,rating = rating, AID = analyticID['aid'])

#########plans.summary
##Design: shows stats of a certain page, rating views and length of stay
##Input: Post ID, page#
##Outputs: updates an existing entry in the analytics db with the timeOUT
########
@bp.route('/<int:ID>/<int:Pos>/summary', methods=( 'GET', 'POST'))
def summary(ID, Pos):
	db=get_db()
	rating=db.execute(
		'SELECT SUM(rate) as score FROM (SELECT DISTINCT author_id, rate from comments WHERE prog_id= ?)', (ID,)
	).fetchone()
	views=db.execute(
		'SELECT SUM(viewed) as viewCount FROM (SELECT DISTINCT U_id, viewed from analytics WHERE P_id= ? and pos= ?)', (ID,Pos,)
	).fetchone()
	time=db.execute(
		'SELECT ((JulianDay(timeOut) - JulianDay(timeIn))) as timeLength FROM (SELECT timeOut, timeIn from analytics WHERE P_id= ? and pos= ?)', (ID,Pos,)
	).fetchone()

	return render_template('plans/summary.html', postID=ID, position=Pos, views =views,rating =rating, time=time)

#########plans.assess
##Design: allows users to create a multiple choice assessment in lieu of a page in a post
##Input: Post ID, page#
##Outputs: 
########
@bp.route('/<int:ID>/<int:Pos>/edit', methods=( 'GET', 'POST'))
def assess(ID, Pos):
	return render_template('plans/assess.html', postID=ID, position=Pos)



#########plans.DCAR
##Design: data collect and redirect, just used to monitor if a user has viewed a page and how long they were there
##Input: Post ID, page#, the analytics ID and if the user is going to the next page or previous (updates on those buttons)
##Outputs: updates an existing entry in the analytics db with the timeOUT
########
@bp.route('/DCAR/<int:ID>/<int:Pos>/<int:AID>/<int:direction>', methods=( 'GET', 'POST'))
def DCAR(ID, Pos, AID, direction):
	#time
	time=datetime.datetime.now()	

	##db stuff
	db=get_db()
	db.execute(
		'UPDATE analytics set timeOut=? WHERE A_id=?', (time, AID ))
	db.commit()
	
	#Which way the user is going
	Pos=Pos+direction
	
	#redirects to original destination after
	return redirect(url_for('plans.view', ID=ID, Pos=Pos))



########plans.getID
##Design: snags the most recently created ID
##Input: Author g.user
##Outputs: 
########
def getID(author): # used to find the id of the post, which is then used as the identifier, the linker between the post head and the pages after it
	#picks up most recent post by that author and returns the ID, should work
	PostID=get_db().execute(
		'SELECT * FROM posts WHERE author_id = ? ORDER BY created DESC' , (author,) ).fetchone()
	return PostID['id']


