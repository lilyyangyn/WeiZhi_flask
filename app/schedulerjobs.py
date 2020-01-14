from .models import Dish, Order

def update_to_next_working_day():
	# update the menu to next day
	Dish.update_to_next_day()
	
