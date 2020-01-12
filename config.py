# -*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'cds very hard-to-guess string'

	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
	MAIL_PORT = os.environ.get('MAIL_PORT', '587')
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	CDS_MAIL_SUBJECT_PREFIX = '[CDS味致]'
	CDS_MAIL_SENDER = 'CDS <lilyyangyn@gmail.com>'

	CDS_ADMIN = os.environ.get('FLASK_ADMIN')

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

config = {
	'development': DevelopmentConfig,

	'default': DevelopmentConfig
}
