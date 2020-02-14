from . import db
from .models import Dish, Order, Route

def update_to_next_working_day():
	# update the menu to next day
	with db.app.app_context():
		Route.clear_today_load()
		Dish.update_to_next_day()
