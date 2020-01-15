from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Role

def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not current_user.can_admin:
			abort(403)
		return f(*args, **kwargs)
	return decorated_function

def moderator_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not current_user.can_moderate:
			abort(403)
		return f(*args, **kwargs)
	return decorated_function
