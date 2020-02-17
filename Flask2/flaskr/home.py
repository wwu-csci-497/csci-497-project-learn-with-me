from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
bp=Blueprint('home', __name__, url_prefix='')

########home.home
##Design: Title page, code just populates front end with items from back end
##Input: None
##Outputs: Most recent posts, will eventually have different categories for highest rated, most popular things like that.
########
@bp.route('/')
def home():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('home.html', posts=posts)
