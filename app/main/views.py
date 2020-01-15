from datetime import datetime
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from . import main 

@main.before_app_request
def before_request():
	if current_user.is_authenticated:
		# is user is not activated, he is only allow to visit sited under 'auth' and 'main', and also static sites
		if current_user.balance < 0 \
						and request.endpoint \
						and request.blueprint != 'auth' \
						and request.blueprint != 'main' \
						and request.endpoint != 'static':
				return redirect(url_for('.in_debt'))

@main.route('/')
def menu():
	if (datetime.now().isoweekday() == 6) or\
		 (datetime.now().isoweekday() == 5 and datetime.now().hour > 11) or\
		 (datetime.now().isoweekday() == 7 and datetime.now().hour < 21):
		 return render_template('weekend.html')
	# if not weekend, show today's menu
	return render_template('menu_today.html')

@main.route('/weekly_menu')
def weekly_menu():
	return render_template('weekly_menu.html')

@main.route('/about')
def about():
	return render_template('about.html')

@main.route('/in-debt')
def in_debt():
	return render_template('in_debt.html')