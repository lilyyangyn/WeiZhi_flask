# -*- coding: UTF-8 -*-
from datetime import datetime
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from .forms import LoginForm, SignupFrom, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from ..models import User
from ..email import send_email

import sys
reload(sys)
sys.setdefaultencoding('utf8')

@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		# is user is not activated, he is only allow to visit sited under 'auth' and 'main', and also static sites
		if not current_user.confirmed \
						and request.endpoint \
						and request.blueprint != 'auth' \
						and request.blueprint != 'main' \
						and request.endpoint != 'static':
				return redirect(url_for('auth.unconfirmed'))

@auth.route('/please-activate-your-account')
def unconfirmed():
	# if user has registered but yet to activate the account
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.menu'))
	return render_template('auth/to_be_activated.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# if all info meets the validation requirement, check if user exists
		usr_email = form.email.data.lower() + '@connect.hku.hk'
		user = User.query.filter_by(email=usr_email).first()
		if user is None:
			usr_email = form.email.data.lower() + '@hku.hk'
			user = User.query.filter_by(email=usr_email).first()
		if user is not None and user.varify_password(form.password.data):
			# if user exists and the password is correct, log him in
			login_user(user, form.remember_me.data)
			# redirect him to his original target url, if have one. 
			# Otherwise, homepage
			next = request.args.get('next')
			if next is None or not next.encode('utf8').startswith('/'):
				next = url_for('main.menu')
			flash('You have been logged in! ↖(^ω^)↗')
			return redirect(next)
		# Fail to log in, add flash info to notify user
		flash('Invalid email or password.')
	# when the first user reach the login page, the form is empty. Then will be directly render to login page
	return render_template('auth/login.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupFrom()
	if form.validate_on_submit():
			# if user not exists (validate by the form), create a new user
			user = User(name=form.name.data.encode("utf8"), 
									email=form.email.data.encode("utf8"), 
									phone=form.phone.data.encode("utf8"), 
									password=form.password.data.encode("utf8"), 
									gender=form.gender.data.encode("utf8"), 
									faculty=form.faculty.data.encode("utf8"),
									identity=form.identity.data.encode("utf8"))
			db.session.add(user)
			# must commit here to get user_id
			db.session.commit()
			token = user.generate_confirmation_token()
			send_email(user.email, 'Activate Account', 'auth/email/activate', user=user, token=token)
			flash('A activation email has been sent to your email address. (≧▽≦)')
			return redirect(url_for('auth.login'))		
	return render_template('auth/register.html', form=form)

@auth.route('/activate/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.menu'))
	if current_user.confirm(token):
		# if confirmed successully, update db
		db.session.commit()
		flash('You have activated your account. Thanks!')
	else:
		flash('Sorry. The activation link is invalid or has expired.')
	return redirect(url_for('main.menu'))

@auth.route('/activate')
@login_required
def resend_confirmation():
	# resend an activate email with a new token
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Activate Account', 'auth/email/activate', 
		user=current_user, token=token)
	flash('A new confirmation email has been sent to your email address.')
	return redirect(url_for('main.menu'))

@auth.route('/logout')
@login_required
def logout():
	# this route only for logged-in user
	logout_user()
	flash('You have been logged out. (*¯ ︶ ¯*)')
	return redirect(url_for('main.menu'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		# should first validate current password
		if current_user.varify_password(form.old_psw.data):
			current_user.password = form.new_psw.data.encode('utf8')
			current_user.updated_at = datetime.now()
			db.session.add(current_user)
			db.session.commit()
			flash('Your password has been updated.')
			return redirect(url_for('main.menu'))
		else:
			flash('Invalid old password.')
	return render_template('auth/change_password.html', form=form)

@auth.route('/reset-password', methods=['GET', 'POST'])
def password_reset_request():
	# if user already logged in, redirect to user-info
	if not current_user.is_anonymous:
		return redirect(url_for('client.profile'))

	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, 'Password Reset', 'auth/email/reset_password', user=user, token=token)
			flash('An email to reset your password has been sent to you.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def password_reset(token):
	# if user already logged in, redirect to user-info
	if not current_user.is_anonymous:
		return redirect(url_for(auth.profile))

	form = PasswordResetForm()
	if form.validate_on_submit():
		if User.reset_password(token, form.password.data.encode('utf8')):
			db.session.commit()
			flash('Your password has been updated.')
			return redirect(url_for('auth.login'))
		else:
			flash('Sorry. The activation link is invalid or has expired, or the user is not exists.')
			return redirect(url_for('main.menu'))
	return render_template('auth/reset_password.html', form=form)








