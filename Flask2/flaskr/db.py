import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db(): #connects to db
	if 'db' not in g:   #g is a global var
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory =sqlite3.Row #returns data in form of dictionaries
	return g.db
	
	
def close_db(e=None):    # if connection exists, close it
	db=g.pop('db', None)
	
	if db is not None:
		db.close()
		
def init_db():
	db=get_db()
	
	with current_app.open_resource('schema.sql') as f: #opens file relative to folder, so not harcoded address
		db.executescript(f.read().decode('utf8')) #reads commands from file
		
@click.command('init-db') #used for init-db command line 
@with_appcontext
def init_db_command():
	init_db()
	click.echo('initialized database')
