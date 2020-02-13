from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from config import config


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

scheduler = APScheduler()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	db.init_app(app)
	db.app = app
	login_manager.init_app(app)

	if config_name == 'development' or 'default':
		# logger 
		import logging
		log = logging.getLogger('apscheduler.executors.default')
		log.setLevel(logging.INFO)  # DEBUG
		fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
		h = logging.StreamHandler()
		h.setFormatter(fmt)
		log.addHandler(h)

	scheduler.init_app(app)
	# job run at 11am every CDS working day (Monday - Friday)
	from .schedulerjobs import update_to_next_working_day
	scheduler.add_job(func=update_to_next_working_day, 
										id='to_next_working_day', 
										trigger='cron', day_of_week="1-5", hour=11, minute=0, second=0)
	scheduler.start()

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .supply import supply as supply_blueprint
	app.register_blueprint(supply_blueprint)

	from .ordering import ordering as ordering_blueprint
	app.register_blueprint(ordering_blueprint)

	from .client import client as client_blueprint
	app.register_blueprint(client_blueprint)

	return app