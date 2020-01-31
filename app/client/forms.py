# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import ValidationError
from ..models import User

def faculties():
	return [('文學院', 'Faculty of Arts 文學院'),\
  ('法律學院', 'Faculty of Law 法律學院'),\
  # ('研究學院', '研究學院 Graduate School'),\
  ('理學院', 'Faculty of Science 理學院'),\
  ('牙醫學院', 'Faculty of Dentistry 牙醫學院'),\
  ('教育學院', 'Faculty of Education 教育學院'),\
  ('工程學院', 'Faculty of Engineering 工程學院'),\
  ('建築學院', 'Faculty of Architecture 建築學院'),\
  ('香港大學專業進修學院', 'HKU SPACE 香港大學專業進修學院'),\
  ('社會科學學院', 'Faculty of Social Sciences 社會科學學院'),\
  ('李嘉誠醫學院', 'Li Ka Shing Faculty of Medicine 李嘉誠醫學院'),\
  ('經濟及工商管理學院', 'Faculty of Business and Economics 經濟及工商管理學院')]

class EditProfileForm(FlaskForm):
	phone = StringField('Phone', validators=[DataRequired()], render_kw={'placeholder': 'HK telephone number (8 digits)'})
	gender = SelectField('Gender', validators=[DataRequired()], choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], render_kw={'placeholder': 'Please select your gender'})
	identity = SelectField('Identity', validators=[DataRequired()], choices=[('student', 'Student'), ('staff', 'Staff')], render_kw={'placeholder': 'Please select your identity'})
	faculty = SelectField('Faculty', validators=[DataRequired()], choices=faculties(), render_kw={'placeholder': 'Please select your faculty'})
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.user = user

	def validate_phone(self, field):
		if len(field.data.encode('utf8') ) != 8:
			raise ValidationError('Phone should have exactly 8 digits.')
		if field.data != self.user.phone and User.query.filter_by(phone=field.data).first():
			raise ValidationError('Phone already registered.')


class CreateDepositForm(FlaskForm):
	phone = StringField('Phone', validators=[DataRequired()], render_kw={'placeholder': 'Phone number'})
	amount = IntegerField('Amount', validators=[DataRequired()], render_kw={'placeholder': 'Top up amount'})
	explanation = TextAreaField('Explanation', render_kw={'placeholder': 'Explanation for the top up'})
	submit = SubmitField('Create Deposit')

	def validate_phone(self, field):
		if not User.query.filter_by(phone=field.data):
			raise ValidationError("No such user.")

	def validate_explanation(self, field):
		if self.amount.data < 0 and not field.data:
			raise ValidationError("Please explain the negative top up.")