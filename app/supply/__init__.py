from flask import Blueprint

supply = Blueprint('supply', __name__)

from . import dish_views, restaurant_views, spot_views, route_views