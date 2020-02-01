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
	dishes = Dish.query.order_by(Dish.stock.desc()).order_by(Dish.in_supply).all()
	return render_template('supply/dishes/dishes.html', dishes=dishes)

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
		dish.in_supply = True
		db.session.add(dish)
		flash("{} is available to be supplied ~".format(dish.name))
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
		form = ChangeStockForm()
		if form.validate_on_submit():
			dish.stock += form.amount.data
			db.session.add(dish)
			flash("Successfully increase stock of {} by {} ~".format(dish.name, form.amount.data))
			return redirect(url_for('supply.dishes'))
		return render_template('supply/dishes/change_stock.html', form=form)
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))

@supply.route('/decrease-stock/<int:id>', methods=['GET', 'POST'])
@login_required
@moderator_required
def decrease_stock(id):
	dish = Dish.query.get(id)
	if dish is not None:
		form = ChangeStockForm()
		if form.validate_on_submit():
			if dish.stock < form.amount.data:
				amount = dish.stock
				dish.stock = 0
			else:
				amount = form.amount.data
				dish.stock -= amount
			db.session.add(dish)
			flash("Successfully decrease stock of {} by {} ~".format(dish.name, amount))
			return redirect(url_for('supply.dishes'))
		return render_template('supply/dishes/change_stock.html', form=form)
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
									Monday=form.monday.data, 
									Tuesday=form.tuesday.data, 
									Wednesday=form.wednesday.data, 
									Thursday=form.thursday.data, 
									Friday=form.friday.data, 
									Saturday=form.saturday.data, 
									Sunday=form.sunday.data)
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

# TODO: update dish info
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

@supply.route('/update-to-next-working-day')
@login_required
@moderator_required
def next_day_dishes():
	# update menu to next (working) day
	update_to_next_working_day()
	flash("Successfully update to tomorrow's dishes!")
	return redirect(url_for('supply.dishes'))










