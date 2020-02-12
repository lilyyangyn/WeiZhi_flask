from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import supply
from .. import db
from ..models import Dish
from ..email import send_email
from ..decorators import moderator_required, admin_required
from .forms import CreateDishForm, ChangeStockForm, EditDishForm
from ..schedulerjobs import update_to_next_working_day

import sys
reload(sys)
sys.setdefaultencoding('utf8')


@supply.route('/dishes')
@login_required
@moderator_required
def dishes():
	# show all the dishes CDS has, ordered by their stock
	dishes_in_supply = Dish.query.filter_by(in_supply=True).order_by(Dish.restaurant_id).order_by(Dish.stock.desc()).all()
	dishes_not_in_supply = Dish.query.filter_by(in_supply=False).order_by(Dish.restaurant_id).order_by(Dish.stock.desc()).all()
	return render_template('supply/dishes/dishes.html', dishes_in_supply=dishes_in_supply, dishes_not_in_supply=dishes_not_in_supply)

@supply.route('/dishes/clear-all-stocks')
@login_required
@moderator_required
def clear_all_stocks():
	# clear all stocks of dishes
	Dish.clear_all_stocks()
	db.session.commit()
	flash("Successfully clear all stocks!")
	return redirect(url_for('supply.dishes'))

@supply.route('/dishes/reset-available-days')
@login_required
@moderator_required
def reset_available_days():
	# set availibility of all 7 days of all the dishes to false
	# simultaneously clear all stock
	dishes = Dish.query.order_by(Dish.stock.desc()).all()
	for dish in dishes:
		for i in range(1, 8):
			dish.cancel_available_day(i)
		db.session.add(dish)
	Dish.clear_all_stocks()
	db.session.commit()
	flash('Successfully reset the weekly menu!')
	return redirect(url_for('supply.dishes'))

@supply.route('/supply-dish/<int:id>')
@login_required
@moderator_required
def supply_dish(id):
	dish = Dish.query.get(id)
	if dish is not None:
		if dish.restaurant.in_cooperation:
			dish.in_supply = True
			db.session.add(dish)
			flash("{} is available to be supplied ~".format(dish.name))
		else:
			flash("Please cooperate with the dish restaurant {} first.".format(dish.restaurant.name))
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))

@supply.route('/stop_supply-dish/<int:id>')
@login_required
@moderator_required
def stop_supply_dish(id):
	dish = Dish.query.get(id)
	if dish is not None:
		dish.in_supply = False
		dish.stock = 0
		db.session.add(dish)
		flash("Stop supplying {} ~".format(dish.name))
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))

@supply.route('/increase-stock/<int:id>', methods=['GET', 'POST'])
@login_required
@moderator_required
def increase_stock(id):
	dish = Dish.query.get(id)
	if dish is not None:
		dish.stock += 1
		db.session.add(dish)
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))

@supply.route('/decrease-stock/<int:id>', methods=['GET', 'POST'])
@login_required
@moderator_required
def decrease_stock(id):
	dish = Dish.query.get(id)
	if dish is not None:
			if dish.stock > 0:
				dish.stock -= 1
				db.session.add(dish)
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))

@supply.route('/add-available/<int:id>/<int:day>', methods=['GET', 'POST'])
@login_required
@moderator_required
def add_available(id, day):
	dish = Dish.query.get(id)
	if dish is not None and day > 0 and day < 8:
		weekday = dish.add_available_day(day)
		db.session.add(dish)
		flash("Successfully add the supply of {} in {}".format(dish.name, weekday))
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))

@supply.route('/cancel-available/<int:id>/<int:day>', methods=['GET', 'POST'])
@login_required
@moderator_required
def cancel_available(id, day):
	dish = Dish.query.get(id)
	if dish is not None and day > 0 and day < 8:
		weekday = dish.cancel_available_day(day)
		db.session.add(dish)
		flash("Successfully cancel the supply of {} in {}".format(dish.name, weekday))
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))


@supply.route('/dishes/new', methods=['GET', 'POST'])
@login_required
@moderator_required
def new_dish():
	# create new dish
	form = CreateDishForm()
	if form.validate_on_submit():
		if form.in_supply.data:
			# if dish is to be supplied immediately, should choose the days it is in supply
			dish = Dish(restaurant_id=form.restaurant.data.id, 
									name=form.name.data.encode('utf8'), 
									spiciness=form.spiciness.data, 
									price=form.price.data, 
									original_price=form.original_price.data, 
									large_img_url=form.large_img_url.data.encode('utf8'),
									in_supply=True, 
									monday=form.monday.data, 
									tuesday=form.tuesday.data, 
									wednesday=form.wednesday.data, 
									thursday=form.thursday.data, 
									friday=form.friday.data, 
									saturday=form.saturday.data, 
									sunday=form.sunday.data)
		else:
			# if dishi is not to be in supply, set all days to False by default
			dish = Dish(restaurant_id=form.restaurant.data.id, 
									name=form.name.data.encode('utf8'), 
									spiciness=form.spiciness.data, 
									price=form.price.data, 
									original_price=form.original_price.data, 
									large_img_url=form.large_img_url.data.encode('utf8'))
		if form.english_name.data != '':
			dish.english_name=form.english_name.data.encode('utf8')
		db.session.add(dish)
		flash("Successfully create new dish {} ^_^".format(dish.name))
		return redirect(url_for('supply.dishes'))
	return render_template('supply/dishes/create_dish.html', form=form)

@supply.route('/edit-dish/<int:id>', methods=['GET', 'POST'])
@login_required
@moderator_required
def edit_dish(id):
	dish = Dish.query.get_or_404(id)
	form = EditDishForm(dish=dish)
	if form.validate_on_submit():
		dish.restaurant_id = form.restaurant.data.id
		dish.name = form.name.data.encode('utf8')
		dish.english_name = form.english_name.data.encode('utf8')
		dish.spiciness = form.spiciness.data
		dish.price = form.price.data
		dish.original_price = form.original_price.data
		dish.large_img_url = form.large_img_url.data.encode('utf8')
		db.session.add(dish)
		db.session.commit()
		flash('Dish info has been updated ^_^')
		return redirect(url_for('.dishes'))
	form.restaurant.data = dish.restaurant
	form.name.data = dish.name
	form.english_name.data = dish.english_name
	form.spiciness.data = dish.spiciness
	form.price.data = dish.price
	form.original_price.data = dish.original_price
	form.large_img_url.data = dish.large_img_url
	return render_template('supply/dishes/edit_dish.html', form=form)

@supply.route('/dish-details/<int:id>')
@login_required
def dish_details(id):
	dish = Dish.query.filter_by(id=id).first()
	if dish is None:
		return redirect(url_for('main.menu'))
	return render_template('supply/dishes/dish_details.html', dish=dish)

@supply.route('/update-to-next-working-day')
@login_required
@moderator_required
def next_day_dishes():
	# update menu to next (working) day
	update_to_next_working_day()
	flash("Successfully update to tomorrow's dishes!")
	return redirect(url_for('supply.dishes'))










