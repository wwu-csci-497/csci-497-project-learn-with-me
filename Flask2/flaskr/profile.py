from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/profile')
def account():
	return render_template('Profile/profile.html')


