import os 
from flask import Flask

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True) # application factory
	
	# default config
	app.config.from_mapping(
		SECRET_KEY='yolo',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)
	#loads config
	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)
		
	#tests for instance folder	
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
		
	#app blueprints
	
	from . import db # imports the db file from the current directory
	db.init_app(app)

	from . import auth #authentication for login and register
	app.register_blueprint(auth.bp)

	from . import about #File that controls, the about section
	app.register_blueprint(about.bp)
	
	from . import home #home screen
	app.register_blueprint(home.bp)
	
	from . import plans #plans
	app.register_blueprint(plans.bp)
	
	#app views
	@app.route('/hello')
	def hello():
		return 'Hello world'
		
	return app
