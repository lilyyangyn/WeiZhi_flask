# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from . import supply
from .. import db
from ..decorators import moderator_required
from ..models import Restaurant
from .forms import CreateRestaurantForm

@supply.route('/restaurants')
@login_required
@moderator_required
def restaurants():
	# show all restaurants CDS coorperate with
	restaurant = Restaurant.query.order_by(Restaurant.name.desc()).all()
	return render_template('supply/restaurants/restaurants.html', restaurant=restaurant)

@supply.route('/restaurants/new', methods=['GET', 'POST'])
@login_required
@moderator_required
def new_restaurant():
	# create new restaurant
	form = CreateRestaurantForm()
	if form.validate_on_submit():
		# set restaurant.in_cooperation True by default
		restaurant = Restaurant(name=form.name.data.encode('utf8'), 
														img_url=form.img_url.data.encode('utf8'), 
														info=form.info.data.encode('utf8'))
		db.session.add(restaurant)
		flash("Successfully create new restaurant {} ^_^".format(restaurant.name))
		return redirect(url_for('supply.restaurants'))
	return render_template('supply/restaurants/create_restaurant.html', form=form)


@supply.route('/stop-cooperation/<restaurant_id>')
@login_required
@moderator_required
def stop_cooperation(restaurant_id):
	# stop to cooperate with this restaurant
	restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
	if restaurant is not None:
		# stop serving all dishes from this restaurant
		for dish in restaurant.dishes.all():
			dish.stop_serving()
			db.session.add(dish)
		# stop coorperate with the restaurant
		restaurant.in_cooperation = False
		db.session.add(restaurant)
		flash("Stop coorperating with {} ┬＿┬".format(restaurant.name))
	else:
		flash("No such restaurant, hope to coorperate with it one day.")
	return redirect(url_for('supply.restaurants'))
