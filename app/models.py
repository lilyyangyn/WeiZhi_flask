# -*- coding: UTF-8 -*-     
from datetime import datetime, time, timedelta
from bcrypt import hashpw, gensalt, checkpw
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from sqlalchemy import and_
from . import db, login_manager

class Role:
	Customer = "customer"
	Moderator = "moderator"
	Admin = "admin"

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)	
	name = db.Column(db.String(16), unique=True, index=True, nullable=False)			# 姓名
	email = db.Column(db.String(64), unique=True, index=True, nullable=False)			# 邮箱地址
	phone = db.Column(db.String(16), unique=True, index=True, nullable=False)			# 联系电话
	password_hash = db.Column(db.String(128))												# 密码哈希
	created_at = db.Column(db.DateTime(), default=datetime.now())	# 创建时间
	updated_at = db.Column(db.DateTime(), default=datetime.now())	# 更新时间
	confirmed = db.Column(db.Boolean, default=False)								# 确认创建
	role = db.Column(db.Enum(Role.Customer, Role.Moderator, Role.Admin, name='role_enum'))							# 角色
	balance = db.Column(db.Integer, default=0)	# 余额
	gender = db.Column(db.String(8))						# 性别
	faculty = db.Column(db.String(20))					# 学院
	identity = db.Column(db.String(8))					# 在校身份
	deposits = db.relationship('Deposit', backref='user', lazy='dynamic')
	orders = db.relationship('Order', backref='user', lazy='dynamic')

	@staticmethod
	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		# role of user should not be explicitly set when created. 
		# If the user is determed admin (by checking the config), then set the role as 'admin', otherwise, 'customer'
		if self.role is None:
			if self.email == current_app.config['CDS_ADMIN']:
				self.role = Role.Admin
			else:
				self.role = Role.Customer

	@property
	def password(self):
		# not allow password to be read
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		# set the password
		self.password_hash = hashpw(password, gensalt(12))

	def varify_password(self, password):
		return checkpw(password.encode('utf'), self.password_hash.encode('utf'))

	@property
	def can_admin(self):
		# has admin privilege
		return self.role == Role.Admin

	@property
	def can_moderate(self):
		# has moderator/admin privilege
		return self.role == Role.Admin or self.role == Role.Moderator

	def generate_confirmation_token(self, expiration=3600):
		# generate token, which includes user_id as identifier
		# the token will be expired in {{expiration}} seconds
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		# Generates an encrypted signature, and serializes data and signature
		return s.dumps({'confirm': self.id}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			# will first check the signature and expiration time
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.id:
			# logged-in user can only confirm the account of himself
			return False
		self.confirmed = True
		self.updated_at = datetime.now()
		db.session.add(self)
		return True

	def generate_reset_token(self, expiration=3600):
		# generate token, which includes user_id as identifier
		# the token will be expired in {{expiration}} seconds
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		# Generates an encrypted signature, and serializes data and signature
		return s.dumps({'reset': self.id}).decode('utf-8')

	@staticmethod
	def reset_password(token, new_password):
		# get user id
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf8'))
		except:
			return False
		user = User.query.filter_by(id=data.get('reset')).first()
		# update password
		if user is None:
			return False
		user.password = new_password
		user.updated_at = datetime.now()
		db.session.add(user)
		return True

	@property
	def is_VIP(self):
		return self.balance > 0

	@property
	def can_order_now(self):
		if self.balance < 0:
			return False

		today = datetime.now().isoweekday()
		hour = datetime.now().hour
		if hour < 11:
			# before 11am
			if today == 6 or today == 7:
				# day time on Sat & Sun
				return False
			else:
				return True
		elif hour > 20:
			# after 9pm
			if self.is_VIP:
				# only vip can order at night
				if today == 5 or today == 6:
					# night on Fri & Sat
					return False
				else:
					return True
		return False			

class AnonymousUser(AnonymousUserMixin):
	@property
	def can_admin(self):
		return False

	@property
	def can_moderate(self):
		return False

	@property
	def is_VIP(self):
		return False

	@property
	def can_order_now(self):
		return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Spiciness:
	NotSpicy = 0
	LittleSpicy = 1
	MediumSpicy = 2
	Spicy = 3
	VerySpicy = 4
	ExtraSpicy = 5

class Dish(db.Model):
	__tablename__ = 'dishes'
	id = db.Column(db.Integer, primary_key=True)
	restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
	name = db.Column(db.String(64), unique=True)
	english_name = db.Column(db.String(64), unique=True)
	price = db.Column(db.Integer)
	original_price=db.Column(db.Integer)
	spiciness = db.Column(db.Integer)
	large_img_url = db.Column(db.Text())
	created_at = db.Column(db.DateTime(), default=datetime.now())
	in_supply = db.Column(db.Boolean, default=False)
	stock = db.Column(db.Integer, default=0, index=True)
	sunday = db.Column(db.Boolean, default=False)
	monday = db.Column(db.Boolean, default=False)
	tuesday = db.Column(db.Boolean, default=False)
	wednesday = db.Column(db.Boolean, default=False)
	thursday = db.Column(db.Boolean, default=False)
	friday = db.Column(db.Boolean, default=False)
	saturday = db.Column(db.Boolean, default=False)
	orders = db.relationship('Order', backref='dish', lazy='dynamic')

	@property
	def sold_out(self):
		return self.stock < 1

	def clear_stock(self):
		self.stock = 0

	def set_stock(self, amount):
		self.stock += amount

	def is_available(self, is_vip=False):
		if not self.in_supply:
			return False;
		today = datetime.now().isoweekday()
		hour = datetime.now().hour
		if hour < 11:
			# before 11 am
			if today == 1:
				return self.monday
			elif today == 2:
				return self.tuesday
			elif today == 3:
				return self.wednesday
			elif today == 4:
				return self.thursday
			elif today == 5:
				return self.friday
			elif today == 6:
				return self.saturday
			elif today == 7:
				return self.sunday
		elif hour > 20:
			# after 9 pm
			if is_vip:
				# available only to vip
				if today == 7:
					return self.monday
				elif today == 1:
					return self.tuesday
				elif today == 2:
					return self.wednesday
				elif today == 3:
					return self.thursday
				elif today == 4:
					return self.friday
				elif today == 5:
					return self.saturday
				elif today == 6:
					return self.sunday
			else:
				return False
		else:
			return False

	def add_available_day(self, day):
		if day == 1:
			self.monday = True
			return 'Monday'
		elif day == 2:
			self.tuesday = True
			return 'Tuesday'
		elif day == 3:
			self.wednesday = True
			return 'Wednesday'
		elif day == 4:
			self.thursday = True
			return 'Thursday'
		elif day == 5:
			self.friday = True
			return 'Friday'
		elif day == 6:
			self.saturday = True
			return 'Saturday'
		elif day == 7:
			self.sunday = True
			return 'Sunday'
		return 'Not Know'

	def cancel_available_day(self, day):
		if day == 1:
			self.monday = False
			return 'Monday'
		elif day == 2:
			self.tuesday = False
			return 'Tuesday'
		elif day == 3:
			self.wednesday = False
			return 'Wednesday'
		elif day == 4:
			self.thursday = False
			return 'Thursday'
		elif day == 5:
			self.friday = False
			return 'Friday'
		elif day == 6:
			self.saturday = False
			return 'Saturday'
		elif day == 7:
			self.sunday = False
			return 'Sunday'
		return 'Not Know'

	def stop_serving(self):
		self.stock = 0
		self.in_supply = False

	@staticmethod
	def clear_all_stocks():
		# set all stock to zero
		available = Dish.query.filter(Dish.stock>0)
		if available is not None:
			for dish in available:
				dish.clear_stock()
				db.session.add(dish)

	@staticmethod
	def set_all_stock(dishes, amount):
		# set all stock to amount
		for dish in dishes:
			dish.set_stock(amount)
			db.session.add(dish)

	@staticmethod
	def today():
		today = datetime.now().isoweekday()
		hour = datetime.now().hour
		if today == 6 or today == 7:
			# weekend
			return Dish.query.filter_by(monday=True)
		if hour < 11:
			# before 11 am
			if today == 1:
				return Dish.query.filter_by(monday=True)
			elif today == 2:
				return Dish.query.filter_by(tuesday=True)
			elif today == 3:
				return Dish.query.filter_by(wednesday=True)
			elif today == 4:
				return Dish.query.filter_by(thursday=True)
			elif today == 5:
				return Dish.query.filter_by(friday=True)
		else:
			# after 11 am
			if today == 1:
				return Dish.query.filter_by(tuesday=True)
			elif today == 2:
				return Dish.query.filter_by(wednesday=True)
			elif today == 3:
				return Dish.query.filter_by(thursday=True)
			elif today == 4:
				return Dish.query.filter_by(friday=True)
			elif today == 5:
				return Dish.query.filter_by(monday=True)

	@staticmethod
	def update_to_next_day():
		# update the menu to next day
		# only call this method at 11am by the scheduler
		Dish.clear_all_stocks()
		today = datetime.now().isoweekday()
		if today == 1:
			dishes_next_day = Dish.query.filter_by(tuesday=True)
		elif today == 2:
			dishes_next_day = Dish.query.filter_by(wednesday=True)
		elif today == 3:
			dishes_next_day = Dish.query.filter_by(thursday=True)
		elif today == 4:
			dishes_next_day = Dish.query.filter_by(friday=True)
		else:
			# for friday to sunday, the next menu is monday's menu
			dishes_next_day = Dish.query.filter_by(monday=True)
		Dish.set_all_stock(dishes_next_day, 8)



class Restaurant(db.Model):
	__tablename__ = 'restaurants'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	img_url = db.Column(db.Text())
	info = db.Column(db.Text())
	restaurant_url = db.Column(db.Text())
	in_cooperation = db.Column(db.Boolean, default=True)
	dishes = db.relationship('Dish', backref='restaurant', lazy='dynamic')



class Spot(db.Model):
	__tablename__ = 'spots'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	img_url = db.Column(db.Text())
	description = db.Column(db.Text())
	in_use = db.Column(db.Boolean, default=True)
	orders = db.relationship('Order', backref='spot', lazy='dynamic')



class Deposit(db.Model):
	__tablename__ = 'deposits'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	created_at = db.Column(db.DateTime(), default=datetime.now())
	explanation = db.Column(db.Text())



class Order_Status:
	PaidOff = 0
	ToPay = 1
	Cancelled = 2

class Order(db.Model):
	__tablename__ = 'orders'
	id = db.Column(db.Integer, primary_key=True)
	dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
	spot_id = db.Column(db.Integer, db.ForeignKey('spots.id'))
	to_be_paid = db.Column(db.Integer, nullable=False)
	today_id = db.Column(db.String(16))
	status = db.Column(db.Integer, default=Order_Status.ToPay)
	price_sold = db.Column(db.Integer, nullable=False)
	original_price = db.Column(db.Integer, nullable=False)
	created_at = db.Column(db.DateTime(), default=datetime.now(), index=True)

	@staticmethod
	def __init__(self, **kwargs):
		super(Order, self).__init__(**kwargs)
		# set order status
		if self.to_be_paid == 0:
			self.status = Order_Status.PaidOff
		else:
			self.status = Order_Status.ToPay

	@staticmethod
	def today():
		today = datetime.now().date()
		hour_now = datetime.now().hour
		hour_boundary = time(21)
		if hour_now < 21:
			datetime_start = datetime.combine(today, hour_boundary) + timedelta(-1)
			datetime_end = datetime.combine(today, hour_boundary)
		else:
			datetime_start = datetime.combine(today, hour_boundary) 
			datetime_end = datetime.combine(today, hour_boundary) + timedelta(1)
		return Order.query.filter(and_(Order.created_at >= datetime_start, Order.created_at < datetime_end))

	@staticmethod
	def yesterday():
		today = datetime.now().date()
		hour_now = datetime.now().hour
		hour_boundary = time(21)
		if hour_now < 21:
			datetime_start = datetime.combine(today, hour_boundary) + timedelta(-2)
			datetime_end = datetime.combine(today, hour_boundary) + timedelta(-1)
		else:
			datetime_start = datetime.combine(today, hour_boundary) + + timedelta(-1)
			datetime_end = datetime.combine(today, hour_boundary)
		return Order.query.filter(and_(Order.created_at >= datetime_start, Order.created_at < datetime_end))

	@staticmethod 
	def YesterdayMaxID():
		last_order = Order.yesterday().order_by(Order.created_at.desc()).first()
		if last_order is not None:
			return last_order.id
		else:
			return 0

	def set_today_id(self, dish_name):
		# set today id
		self.today_id = "{num}{name}".format(num=self.id - Order.YesterdayMaxID(), name=dish_name[:2])

	@property
	def is_valid(self):
		if self.status == Order_Status.Cancelled:
			return False
		today = datetime.now().date()
		hour_now = datetime.now().hour
		hour_available = time(21)
		if hour_now < 11:
			# invoice available to be modified before 11 pm
			datetime_available = datetime.combine(today, hour_available) + timedelta(-1)
			return self.created_at >= datetime_available
		elif hour_now > 20:
			# invoice available after 9pm
			datetime_available = datetime.combine(today, hour_available) 
			return self.created_at >= datetime_available
		else:
			return False


