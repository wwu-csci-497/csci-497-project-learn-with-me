from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp=Blueprint('about', __name__, url_prefix='/about')


########about.about
##Design: N0thing here yet but will probably end up a static html with information on company
##Input: nothing
##Outputs: nothing
########
@bp.route('/')
def about():
	return render_template('about.html')

