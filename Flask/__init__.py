#__init__

import os 
from flask import Flask

def create_app(config_file=None):
	app= Flask(__name__)

	if(config_name is not None):
		app.config.from_pyfile(config_file, silent=True)
	else: 
		app.config.from_mapping(
			SECRET_KEY='sdfigtertairasgkd8dty60546j4563l43563'
			DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
		)
	
	#routes and blueprints	
	from . import db
	db.init_app(app)
	
	from . import auth
	app.register_blueprint(auth.bp)

	return app


