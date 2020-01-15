from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
	with app.app_context():
		# mutually create program context when sending mail in diff threads
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()
	# create message
	msg = Message(app.config['CDS_MAIL_SUBJECT_PREFIX'] + '-' + subject, sender=app.config['CDS_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)
	# generate thread to send email
	#thr = Thread(target=send_async_email, args=[app, msg])
	#thr.start()
	#return thr