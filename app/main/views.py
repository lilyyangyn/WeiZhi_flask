from datetime import datetime
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from . import main 
from ..models import Dish

@main.before_app_request
def before_request():
	if current_user.is_authenticated:
		# is user is not activated, he is only allow to visit sited under 'auth' and 'main', and also static sites
		if current_user.balance < 0 \
						and request.endpoint \
						and (request.blueprint == 'supply' \
						or request.endpoint == 'ordering.create_order'):
				return redirect(url_for('client.in_debt'))

@main.route('/')
def menu():
	if (datetime.now().isoweekday() == 6) or\
		 (datetime.now().isoweekday() == 5 and datetime.now().hour > 11) or\
		 (datetime.now().isoweekday() == 7 and datetime.now().hour < 21):
		 return render_template('weekend.html')
	# if not weekend, show today's menu
	dishes = []
	dishes.append(Dish.today().filter(Dish.spiciness > 1).all())
	dishes.append(Dish.today().filter(Dish.spiciness < 2).all())
	dishNum = [len(dishes[0]), len(dishes[1])]
	return render_template('menu_today.html', dishes=dishes, dishNum=dishNum)

@main.route('/weekly_menu/<day>')
def weekly_menu(day):
	if day == 'Monday':
		dishes = Dish.query.filter_by(monday=True).all()
	elif day == 'Tuesday':
		dishes = Dish.query.filter_by(tuesday=True).all()
	elif day == 'Wednesday':
		dishes = Dish.query.filter_by(wednesday=True).all()
	elif day == 'Thursday':
		dishes = Dish.query.filter_by(thursday=True).all()
	elif day == 'Friday':
		dishes = Dish.query.filter_by(friday=True).all()
	else:
		return redirect(url_for('.weekly_menu', day='Monday'))
	return render_template('weekly_menu.html', dishes=dishes, day=day)

@main.route('/about')
def about():
	return render_template('about.html')