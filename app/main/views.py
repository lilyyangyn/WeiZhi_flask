from datetime import datetime
from flask import render_template
from flask_login import login_required, current_user
from . import main 

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