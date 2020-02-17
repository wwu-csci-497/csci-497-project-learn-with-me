from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<string:ID>/')
def account(ID):
	accountPosts=get_db().execute(
		'SELECT * FROM pages JOIN post ON pages.prog_id=post.id JOIN user ON user.id=post.author_id WHERE author_id = ?', 	(g.user['id'],)
	).fetchall()	
	
	return render_template('Profile/profile.html', posts=accountPosts)


