from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Spot

class CreateOrderForm(FlaskForm):
	def spot_query():
		return Spot.query.filter_by(in_use=True)

	spot = QuerySelectField('Pickup Spot', query_factory=spot_query, get_label='name')
	balance_pay = RadioField('Payment', default=0, coerce=int)
	submit = SubmitField('Confirm Order')

	def __init__(self, userBalance, *args, **kwargs):
		super(CreateOrderForm, self).__init__(*args, **kwargs)
		if userBalance > 0:
			self.balance_pay.choices = [(1, 'balance'), (0, 'cash')]
		else:
			self.balance_pay.choices = [(0, 'cash')]