from . import db
from .models import Dish, Order

def update_to_next_working_day():
	# update the menu to next day
	with db.app.app_context():
		Dish.update_to_next_day()
	
