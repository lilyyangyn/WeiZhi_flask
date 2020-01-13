from flask import Blueprint

ordering = Blueprint('ordering', __name__)

from . import views