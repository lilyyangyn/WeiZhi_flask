from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import supply
from .. import db
from ..models import Dish
from ..email import send_email
from ..decorators import moderator_required
from .forms import CreateDishForm

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

@supply.route('/dishes/next-day-dishes')
@login_required
@moderator_required
def next_day_dishes():
	# update menu to next (working) day
	Dish.update_to_next_day()
	db.session.commit()
	flash("Successfully update to tomorrow's dishes!")
	return redirect(url_for('supply.dishes'))

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

@supply.route('/supply-dish/<dish_id>')
@login_required
@moderator_required
def supply_dish(dish_id):
	dish = Dish.query.filter_by(id=dish_id).first()
	if dish is not None:
		dish.to_supply = True
		db.session.add(dish)
		flash("{} is available to be supplied ~".format(dish.name))
	else:
		flash('We do not have such dish, please add it to database first.')
	return redirect(url_for('supply.dishes'))


# TODO: increase-stock, decrease-stock


@supply.route('/dishes/new', methods=['GET', 'POST'])
@login_required
@moderator_required
def new_dish():
	# create new dish
	form = CreateDishForm()
	if form.validate_on_submit():
		if form.in_supply.data:
			# if dish is to be supplied immediately, should choose the days it is in supply
			dish = Dish(restaurant_id=form.restaurant_id.data.id, 
									name=form.name.data.encode('utf8'), 
									english_name=form.english_name.data.encode('utf8'), 
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
			dish = Dish(restaurant_id=form.restaurant_id.data.id, 
									name=form.name.data.encode('utf8'), 
									english_name=form.english_name.data.encode('utf8'), 
									spiciness=form.spiciness.data, 
									price=form.price.data, 
									original_price=form.original_price.data, 
									large_img_url=form.large_image_url.data.encode('utf8'))
		db.session.add(dish)
		flash("Successfully create new dish {} ^_^".format(dish.name))
		return redirect(url_for('supply.dishes'))
	return render_template('supply/dishes/create_dish.html', form=form)

# TODO: update dish info














