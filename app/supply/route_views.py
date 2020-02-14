# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from . import supply
from .. import db
from ..decorators import moderator_required
from ..models import Route
from .forms import CreateRouteForm, EditRouteForm

@supply.route('/routes')
@login_required
@moderator_required
def routes():
	# show all routes
	routes_in_use = Route.query.filter_by(in_use=True).order_by(Route.name.desc()).all()
	routes_not_in_use = Route.query.filter_by(in_use=False).order_by(Route.name.desc()).all()
	return render_template('supply/routes/routes.html', routes_in_use=routes_in_use, routes_not_in_use=routes_not_in_use)

@supply.route('/routes/new', methods=['GET', 'POST'])
@login_required
@moderator_required
def new_route():
	# create new routes
	form = CreateRouteForm()
	if form.validate_on_submit():
		# by defaut set the route in used
		route = Route(name=form.name.data.encode('utf8'), 
								maxload=form.maxload.data)
		db.session.add(route)
		flash("Successfully create new route {} ^_^".format(route.name))
		return redirect(url_for('.routes'))
	return render_template('supply/routes/create_route.html', form=form)

@supply.route('/stop-route/<int:id>')
@login_required
@moderator_required
def stop_route(id):
	# stop using this route
	route = Route.query.get(id)
	if route is not None:
		# stop cooperate all restaurants in this route 
		# and stop serving dishes from those restaurants
		for restaurant in route.restaurants.all():
			restaurant.in_cooperation = False
			db.session.add(restaurant)
			for dish in restaurant.dishes.all():
				dish.stop_serving()
				db.session.add(dish)
		# stop this route
		route.in_use = False
		db.session.add(route)
		flash("Stop using route {} and stop cooperating with all related restaurants ┬＿┬".format(route.name))
	else:
		flash("No such route, please add it first")
	return redirect(url_for('.routes'))

@supply.route('/start-route/<int:id>')
@login_required
@moderator_required
def start_route(id):
	# stop using this route
	route = Route.query.get(id)
	if route is not None:
		route.in_use = True
		db.session.add(route)
		flash("Start using route {} !".format(route.name))
	else:
		flash("No such route, please add it first")
	return redirect(url_for('.routes'))

@supply.route('/increase-maxload/<int:id>')
@login_required
@moderator_required
def increase_maxload(id):
	route = Route.query.get(id)
	if route is not None:
		route.maxload += 1
		db.session.add(route)
	else:
		flash('We do not have such route, please add it to database first.')
	return redirect(url_for('.routes'))

@supply.route('/decrease-maxload/<int:id>')
@login_required
@moderator_required
def decrease_maxload(id):
	route = Route.query.get(id)
	if route is not None:
			if route.maxload > 0:
				route.maxload -= 1
				db.session.add(route)
	else:
		flash('We do not have such route, please add it to database first.')
	return redirect(url_for('.routes'))

@supply.route('/edit-route/<int:id>')
@login_required
@moderator_required
def edit_route(id):
	route = Route.query.get_or_404(id)
	form = EditRouteForm(route=route)
	if form.validate_on_submit():
		route.name = form.name.data.encode('utf8')
		route.maxload = form.maxload.data
		db.session.add(route)
		db.session.commit()
		flash('route info has been updated ^_^')
		return redirect(url_for('.routes'))
	form.name.data = route.name
	form.maxload.data = route.maxload
	return render_template('supply/routes/edit_route.html', form=form)
