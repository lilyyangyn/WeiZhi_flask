from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange 
from wtforms import ValidationError
from ..models import Dish, Restaurant, Spiciness, Spot

class CreateDishForm(FlaskForm):
	def restaurant_query():
		return Restaurant.query.filter_by(in_cooperation=True)

	restaurant = QuerySelectField('Restaurant', query_factory=restaurant_query, get_label='name')
	name = StringField('Chinese Name', validators=[DataRequired(), Length(1, 64)])
	english_name = StringField('English Name', validators=[Length(0, 64)])
	spiciness = SelectField('Spiciness', 
		choices={(Spiciness.NotSpicy, 'Not Spicy'), 
						(Spiciness.LittleSpicy, 'Little Spicy'), 
						(Spiciness.MediumSpicy, 'Medium Spicy'), 
						(Spiciness.Spicy, 'Spicy'), 
						(Spiciness.VerySpicy, 'Very Spicy'), 
						(Spiciness.ExtraSpicy, 'Extra Spicy')}, coerce=int)
	price = IntegerField ('Price', validators=[Optional()])
	original_price = IntegerField ('Original Price', validators=[DataRequired()])
	large_img_url = StringField('Image URL', validators=[Length(0, 80)])
	in_supply = BooleanField('Supply Now', default=False)
	monday = BooleanField('Monday', default=False)
	tuesday = BooleanField('Tuesday', default=False)
	wednesday = BooleanField('Wednesday', default=False)
	thursday = BooleanField('Thursday', default=False)
	friday = BooleanField('Friday', default=False)
	saturday = BooleanField('Saturday', default=False)
	sunday = BooleanField('Sunday', default=False)
	submit = SubmitField('Create Dish')

	def validate_name(self, field):
		if Dish.query.filter_by(name=field.data).first():
			raise ValidationError('Dish already exists.')

	def validate_english_name(self, field):
		if Dish.query.filter_by(english_name=field.data).first():
			raise ValidationError('Dish already exists.')

class ChangeStockForm(FlaskForm):
	amount = IntegerField('Amount', validators=[NumberRange(1, 4)])
	submit = SubmitField('Submit')
	
class EditDishForm(FlaskForm):
	def restaurant_query():
		return Restaurant.query.filter_by(in_cooperation=True)

	restaurant = QuerySelectField('Restaurant', query_factory=restaurant_query, get_label='name')
	name = StringField('Chinese Name', validators=[DataRequired(), Length(1, 64)])
	english_name = StringField('English Name', validators=[Length(1, 64)])
	spiciness = SelectField('Spiciness', 
		choices={(Spiciness.NotSpicy, 'Not Spicy'), 
						(Spiciness.LittleSpicy, 'Little Spicy'), 
						(Spiciness.MediumSpicy, 'Medium Spicy'), 
						(Spiciness.Spicy, 'Spicy'), 
						(Spiciness.VerySpicy, 'Very Spicy'), 
						(Spiciness.ExtraSpicy, 'Extra Spicy')}, coerce=int)
	price = IntegerField ('Price', validators=[Optional()])
	original_price = IntegerField ('Original Price', validators=[DataRequired()])
	large_img_url = StringField('Image URL', validators=[Length(0, 80)])
	submit = SubmitField('Edit Dish')

	def __init__(self, dish, *args, **kwargs):
		super(EditDishForm, self).__init__(*args, **kwargs)
		self.dish = dish

	def validate_name(self, field):
		if field.data != self.dish.name and Dish.query.filter_by(name=field.data).first():
			raise ValidationError('Dish already exists.')

	def validate_english_name(self, field):
		if self.dish.english_name is None or field.data != self.dish.english_name:
			if Dish.query.filter_by(english_name=field.data).first():
				raise ValidationError('Dish already exists.')


class CreateRestaurantForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
	img_url = StringField('Image URL', validators=[Length(0, 80)])
	info = TextAreaField('Information')
	submit = SubmitField('Create Restaurant')

	def validate_name(self, field):
		if Restaurant.query.filter_by(name=field.data).first():
			raise ValidationError('Restaurant already exists.')

class EditRestaurantForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
	img_url = StringField('Image URL', validators=[Length(0, 80)])
	info = TextAreaField('Information')
	submit = SubmitField('Edit Dish')

	def __init__(self, restaurant, *args, **kwargs):
		super(EditRestaurantForm, self).__init__(*args, **kwargs)
		self.restaurant = restaurant

	def validate_name(self, field):
		if field.data != self.restaurant.name and Restaurant.query.filter_by(name=field.data).first():
			raise ValidationError('Restaurant already exists.')

class CreateSpotForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
	img_url = StringField('Image URL', validators=[Length(0, 80)])
	description = TextAreaField('Description')
	submit = SubmitField('Create Spot')

	def validate_name(self, field):
		if Spot.query.filter_by(name=field.data).first():
			raise ValidationError('Spot already exists.')

class EditSpotForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
	img_url = StringField('Image URL', validators=[Length(0, 80)])
	description = TextAreaField('Description')
	submit = SubmitField('Edit Spot')

	def __init__(self, spot, *args, **kwargs):
		super(EditSpotForm, self).__init__(*args, **kwargs)
		self.spot = spot

	def validate_name(self, field):
		if field.data != self.spot.name and Spot.query.filter_by(name=field.data).first():
			raise ValidationError('Spot already exists.')