from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp=Blueprint('groups', __name__, url_prefix='/groups')

@bp.route('/<string:ID>/')
def groups(ID):
	return render_template('groups/groups.html', groups=groups)

@bp.route('/quickstart/')
def quickstart():
	return render_template('groups/quickstart.html')
