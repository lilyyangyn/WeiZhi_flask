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
	name = StringField('Chinese Name', validators=[DataRequired(), Length(1, 64)], render_kw={'placeholder': 'Chinese name'})
	english_name = StringField('English Name', validators=[Length(0, 64), Optional()], default=None, render_kw={'placeholder': 'English name'})
	spiciness = SelectField('Spiciness', 
		choices={(Spiciness.NotSpicy, 'Not Spicy'), 
						(Spiciness.LittleSpicy, 'Little Spicy'), 
						(Spiciness.MediumSpicy, 'Medium Spicy'), 
						(Spiciness.Spicy, 'Spicy'), 
						(Spiciness.VerySpicy, 'Very Spicy'), 
						(Spiciness.ExtraSpicy, 'Extra Spicy')}, coerce=int, default=Spiciness.NotSpicy)
	price = IntegerField ('Price', validators=[Optional()], render_kw={'placeholder': 'Price sold'})
	original_price = IntegerField ('Original Price', validators=[DataRequired()], render_kw={'placeholder': 'Original price'})
	large_img_url = TextAreaField('Image URL', render_kw={'placeholder': 'Image URL'})
	in_supply = BooleanField('Supply Now', default=False)
	monday = BooleanField('Mon', default=False)
	tuesday = BooleanField('Tue', default=False)
	wednesday = BooleanField('Wed', default=False)
	thursday = BooleanField('Thu', default=False)
	friday = BooleanField('Fri', default=False)
	saturday = BooleanField('Sat', default=False)
	sunday = BooleanField('Sun', default=False)
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
	name = StringField('Chinese Name', validators=[DataRequired(), Length(1, 64)], render_kw={'placeholder': 'Chinese name'})
	english_name = StringField('English Name', validators=[Length(0, 64), Optional()], default=None, render_kw={'placeholder': 'English name'})
	spiciness = SelectField('Spiciness', 
		choices={(Spiciness.NotSpicy, 'Not Spicy'), 
						(Spiciness.LittleSpicy, 'Little Spicy'), 
						(Spiciness.MediumSpicy, 'Medium Spicy'), 
						(Spiciness.Spicy, 'Spicy'), 
						(Spiciness.VerySpicy, 'Very Spicy'), 
						(Spiciness.ExtraSpicy, 'Extra Spicy')}, coerce=int)
	price = IntegerField ('Price', validators=[Optional()], render_kw={'placeholder': 'Price sold'})
	original_price = IntegerField ('Original Price', validators=[DataRequired()], render_kw={'placeholder': 'Original price'})
	large_img_url = TextAreaField('Image URL', render_kw={'placeholder': 'Image URL'})
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
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)], render_kw={'placeholder': 'Name'})
	img_url = TextAreaField('Image URL', render_kw={'placeholder': 'Image URL'})
	info = TextAreaField('Information', render_kw={'placeholder': 'Information'})
	restaurant_url = TextAreaField('Restaurant URL', render_kw={'placeholder': 'Restaurant URL'})
	submit = SubmitField('Create Restaurant')

	def validate_name(self, field):
		if Restaurant.query.filter_by(name=field.data).first():
			raise ValidationError('Restaurant already exists.')

class EditRestaurantForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)], render_kw={'placeholder': 'Name'})
	img_url = TextAreaField('Image URL', render_kw={'placeholder': 'Image URL'})
	info = TextAreaField('Information', render_kw={'placeholder': 'Information'})
	restaurant_url = TextAreaField('Restaurant URL', render_kw={'placeholder': 'Restaurant URL'})
	submit = SubmitField('Edit Restaurant')

	def __init__(self, restaurant, *args, **kwargs):
		super(EditRestaurantForm, self).__init__(*args, **kwargs)
		self.restaurant = restaurant

	def validate_name(self, field):
		if field.data != self.restaurant.name and Restaurant.query.filter_by(name=field.data).first():
			raise ValidationError('Restaurant already exists.')

class CreateSpotForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)], render_kw={'placeholder': 'Name'})
	img_url = TextAreaField('Image URL', render_kw={'placeholder': 'Image URL'})
	description = TextAreaField('Description', render_kw={'placeholder': 'Description'})
	submit = SubmitField('Create Spot')

	def validate_name(self, field):
		if Spot.query.filter_by(name=field.data).first():
			raise ValidationError('Spot already exists.')

class EditSpotForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)], render_kw={'placeholder': 'Name'})
	img_url = TextAreaField('Image URL', render_kw={'placeholder': 'Image URL'})
	description = TextAreaField('Description', render_kw={'placeholder': 'Description'})
	submit = SubmitField('Edit Spot')

	def __init__(self, spot, *args, **kwargs):
		super(EditSpotForm, self).__init__(*args, **kwargs)
		self.spot = spot

	def validate_name(self, field):
		if field.data != self.spot.name and Spot.query.filter_by(name=field.data).first():
			raise ValidationError('Spot already exists.')