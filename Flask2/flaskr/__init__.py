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
	
	@app.route('/hello')
	def hello():
		return 'Hello world'
	
	@app.route('/')
	def home():
		return 'Welcome to my website!'
		
	return app
