# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from . import supply
from .. import db
from ..decorators import moderator_required
from ..models import Restaurant
from .forms import CreateRestaurantForm, EditRestaurantForm

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


@supply.route('/stop-cooperation/<int:id>')
@login_required
@moderator_required
def stop_cooperation(id):
	# stop cooperating with this restaurant
	restaurant = Restaurant.query.get(id)
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

@supply.route('/edit-restaurant/<int:id>', methods=['GET', 'POST'])
@login_required
@moderator_required
def edit_restaurant(id):
	restaurant = Restaurant.query.get_or_404(id)
	form = EditRestaurantForm(restaurant=restaurant)
	if form.validate_on_submit():
		restaurant.name = form.name.data.encode('utf8')
		restaurant.img_url = form.img_url.data.encode('utf8')
		restaurant.info = form.info.data.encode('utf8')
		db.session.add(restaurant)
		db.session.commit()
		flash('Restaurant info has been updated ^_^')
		return redirect(url_for('.restaurants'))
	form.name.data = restaurant.name
	form.img_url.data = restaurant.img_url
	form.info.data = restaurant.info
	return render_template('supply/restaurants/edit_restaurant.html', form=form)




