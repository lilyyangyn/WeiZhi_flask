from flask import render_template, redirect, url_for, flash, request, make_response
from flask_login import current_user, login_required
from . import shopping_cart

@shopping_cart.route('/')
@login_required
def my_cart():
	return render_template('shopping_cart/my_cart.html')

@shopping_cart.route('/add-item/<int:id>')
@login_required
def add_item(id):
	return redirect('.my_cart')

@shopping_cart.route('/remove-item/<int:id>')
@login_required
def remove_item(id):
	return redirect('.my_cart')

@shopping_cart.route('/inc-stock/<int:id>')
@login_required
def inc_stock(id):
	return redirect('.my_cart')

@shopping_cart.route('/dec-stock/<int:id>')
def dec_stock(id):
	return redirect('.my_cart')

@shopping_cart.route('/clear-all')
@login_required
def clear_all():
	return redirect('.my_cart')

@shopping_cart.route('/check-out')
@login_required
def check_out():
	return render_template('shopping_cart/cart_checkout.html')