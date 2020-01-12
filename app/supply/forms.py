from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Optional 
from wtforms import ValidationError
from ..models import Dish, Restaurant, Spiciness

class CreateDishForm(FlaskForm):
	def restaurant_query():
		return Restaurant.query.filter_by(in_cooperation=True)

	restaurant_id = QuerySelectField('Restaurant', query_factory=restaurant_query, get_label='name')
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

class CreateRestaurantForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
	img_url = StringField('Image URL', validators=[Length(0, 80)])
	info = TextAreaField('Information')
	submit = SubmitField('Create Restaurant')

	def validate_name(self, field):
		if Restaurant.query.filter_by(name=field.data).first():
			raise ValidationError('Restaurant already exists.')

	