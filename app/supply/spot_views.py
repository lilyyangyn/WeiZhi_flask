# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from . import supply
from .. import db
from ..decorators import moderator_required
from ..models import Spot
from .forms import CreateSpotForm, EditSpotForm

@supply.route('/spots')
@login_required
@moderator_required
def spots():
	# show all spots
	spots = Spot.query.order_by(Spot.name.desc()).all()
	return render_template('supply/spots/spots.html', spots=spots)

@supply.route('/spots/new', methods=['GET', 'POST'])
@login_required
@moderator_required
def new_spot():
	# create new spots
	form = CreateSpotForm()
	if form.validate_on_submit():
		# by defaut set the spot in used
		spot = Spot(name=form.name.data.encode('utf8'), 
								img_url=form.img_url.data.encode('utf8'), 
								description=form.description.data.encode('utf8'))
		db.session.add(spot)
		flash("Successfully create new spot {} ^_^".format(spot.name))
		return redirect(url_for('.spots'))
	return render_template('supply/spots/create_spot.html', form=form)

@supply.route('/stop-use/<int:id>')
@login_required
@moderator_required
def stop_use(id):
	# stop using this spot
	spot = Spot.query.get(id)
	if spot is not None:
		spot.in_use = False
		db.session.add(spot)
		flash("Stop using spot spot {} ┬＿┬".format(spot.name))
	else:
		flash("No such spot, please add it first")
	return redirect(url_for('.spots'))

@supply.route('/start-use/<int:id>')
@login_required
@moderator_required
def start_use(id):
	# stop using this spot
	spot = Spot.query.get(id)
	if spot is not None:
		spot.in_use = True
		db.session.add(spot)
		flash("Start using spot spot {} !".format(spot.name))
	else:
		flash("No such spot, please add it first")
	return redirect(url_for('.spots'))

@supply.route('/edit-spot/<int:id>', methods=['GET', 'POST'])
@login_required
@moderator_required
def edit_spot(id):
	spot = Spot.query.get_or_404(id)
	form = EditSpotForm(spot=spot)
	if form.validate_on_submit():
		spot.name = form.name.data.encode('utf8')
		spot.img_url = form.img_url.data.encode('utf8')
		spot.description = form.description.data.encode('utf8')
		db.session.add(spot)
		db.session.commit()
		flash('Spot info has been updated ^_^')
		return redirect(url_for('.spots'))
	form.name.data = spot.name
	form.img_url.data = spot.img_url
	form.description.data = spot.description
	return render_template('supply/spots/edit_spot.html', form=form)
