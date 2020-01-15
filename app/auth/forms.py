# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 48)], render_kw={'placeholder': 'e.g. u3502870'})
	password = PasswordField('Password', validators=[DataRequired(), Length(8, 20)], render_kw={'placeholder': 'Password'})
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Login')

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

class SignupFrom(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(1, 16)], render_kw={'placeholder': 'Username'})
	phone = StringField('Phone', validators=[DataRequired()], render_kw={'placeholder': 'HK telephone number (8 digits)'})
	email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)], render_kw={'placeholder': 'e.g. u3502870'})
	password = PasswordField('Password', validators=[DataRequired(), Length(8, 20)], render_kw={'placeholder': 'Password (8-20 digits/characters)'})
	password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={'placeholder': 'Confirm password'})
	gender = SelectField('Gender', validators=[DataRequired()], choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], render_kw={'placeholder': 'Please select your gender'})
	identity = SelectField('Identity', validators=[DataRequired()], choices=[('student', 'Student'), ('staff', 'Staff')], render_kw={'placeholder': 'Please select your identity'})
	faculty = SelectField('Faculty', validators=[DataRequired()], choices=faculties(), render_kw={'placeholder': 'Please select your faculty'})
	submit = SubmitField('Register')

	def validate_name(self, field):
		if User.query.filter_by(name=field.data).first():
			raise ValidationError('Name already registered.')

	def validate_phone(self, field):
		if len(field.data.encode('utf8') ) != 8:
			raise ValidationError('Phone should have exactly 8 digits.')
		if User.query.filter_by(phone=field.data).first():
			raise ValidationError('Phone already registered.')

	def validate_email(self, field):
		strs = field.data.lower().split("@")
		if len(strs) == 2:
			if strs[1] != "connect.hku.hk" and strs[1] != "hku.hk":
				raise ValidationError('You must be a HKUer ! Please register with a HKU email ^_^')
			email1 = strs[0] + "@connect.hku.hk"
			email2 = strs[0] + "@hku.hk"
			if User.query.filter_by(email=email1).first():
				raise ValidationError('Email already registered.')
			if User.query.filter_by(email=email2).first():
				raise ValidationError('Email already registered.')

class ChangePasswordForm(FlaskForm):
	old_psw = PasswordField('Old password', validators=[DataRequired()], render_kw={'placeholder': 'Old password'})
	new_psw = PasswordField('New password', validators=[DataRequired(), Length(8, 20)], render_kw={'placeholder': 'New password (8-20 digits/characters)'})
	new_psw2 = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_psw', message='Passwords must match')], render_kw={'placeholder': 'Confirm new password'})
	submit = SubmitField('Update Password')

class PasswordResetRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()], render_kw={'placeholder': 'Registered Email e.g. u3502870@(connect.)hku.hk'})
	submit = SubmitField('Submit')

class PasswordResetForm(FlaskForm):
	password = PasswordField('New Password', validators=[DataRequired(), Length(8, 20)], render_kw={'placeholder': 'New password (8-20 digits/characters)'})
	password2 = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={'placeholder': 'Confirm new password'})
	submit = SubmitField('Reset Password')

class ChangeEmailForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
	submit = SubmitField('Update Email Address')

	def validate_email(self, field):
		strs = field.data.lower().split("@")
		email1 = strs[0] + "@connect.hku.hk"
		email2 = strs[0] + "@hku.hk"
		if User.query.filter_by(email=email1).first():
			raise ValidationError('Email already registered.')
		if User.query.filter_by(email=email2).first():
			raise ValidationError('Email already registered.')