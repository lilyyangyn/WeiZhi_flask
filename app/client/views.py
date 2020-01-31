from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy.sql import func
from . import client
from .. import db
from ..decorators import admin_required
from ..models import User, Deposit
from .forms import CreateDepositForm, EditProfileForm
from ..email import send_email

@client.route('/profile')
@login_required
def profile():
	return render_template('client/profile.html', user=current_user)

@client.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(user=current_user)
	if form.validate_on_submit():
		current_user.phone = form.phone.data.encode('utf8')
		current_user.gender = form.gender.data.encode('utf8')
		current_user.identity = form.identity.data.encode('utf8')
		current_user.faculty = form.faculty.data.encode('utf8')
		db.session.add(current_user._get_current_object())
		db.session.commit()
		flash('Your profile has been updated ^_^')
		return redirect(url_for('.profile'))
	form.phone.data = current_user.phone
	form.gender.data = current_user.gender
	form.identity.data = current_user.identity
	form.faculty.data = current_user.faculty
	return render_template('client/edit_profile.html', form=form)

@client.route('/users')
@login_required
@admin_required
def users():
	# display users data, ordered by account balance
	users_in_debt = User.query.filter(User.balance<0).order_by(User.balance.asc()).all()
	other_users = User.query.filter(User.balance>=0).order_by(User.balance.desc()).all()
	total_students = db.session.query(func.count(User.id)).filter(User.identity == 'student').scalar()
	total_staffs = db.session.query(func.count(User.id)).filter(User.identity == 'staff').scalar()
	total_balance = db.session.query(func.sum(User.balance)).scalar()
	return render_template('client/users.html', users_in_debt=users_in_debt, other_users=other_users, total_students=total_students, total_staffs=total_staffs, total_balance=total_balance)

@client.route('/deposits')
@login_required
@admin_required
def deposits():
	# display all deposits, ordered by id (created time)
	# notice here deposists are query
	deposits = Deposit.query.order_by(Deposit.created_at.desc()).all()
	return render_template('client/deposits.html', deposits=deposits)

@client.route('/deposits/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_deposit():
	# create new deposit
	form = CreateDepositForm()
	if form.validate_on_submit():
		phone = form.phone.data
		user = User.query.filter_by(phone=phone).first()
		amount = form.amount.data
		# increase user balance
		user.balance += amount
		db.session.add(user)
		# create new deposit
		deposit = Deposit(user_id=user.id, amount=amount, explanation=form.explanation.data)
		db.session.add(deposit)
		# must commit here to get created time
		db.session.commit()
		# send top up confirmation email
		send_email(user.email, 'Top Up Confirmation', 'client/email/top_up', user=user, deposit=deposit)
		flash("Successful create the deposit.")
		return redirect(url_for('.deposits'))
	return render_template('client/create_deposit.html', form=form)

@client.route('/in-debt')
@login_required
def in_debt():
	return render_template('client/in_debt.html')

