# -*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'cds very hard-to-guess string'

	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
	#MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.office365.com')
	MAIL_PORT = os.environ.get('MAIL_PORT', '587')
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	CDS_MAIL_SUBJECT_PREFIX = 'CDS味致'
	CDS_MAIL_SENDER = 'noreply <cds.hku@gmail.com>'

	CDS_ADMIN = os.environ.get('CDS_ADMIN')

	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	CDS_ADMIN = "lilyyang@connect.hku.hk"
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                'postgresql://yuening:@localhost:5432/cds_development' 
	SQLALCHEMY_ECHO = True

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                'postgresql://yuening:@localhost:5432/cds_testing' 

class ProductionConfig(Config):
	PRODUCE = True
	#SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or '' 

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
