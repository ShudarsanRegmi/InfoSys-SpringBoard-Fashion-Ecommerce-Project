from flask import redirect, url_for
from flask_login import  current_user

def is_admin(f):
    def wrapper(*args, **kwargs):
        if not current_user.isAdmin():
            return redirect(url_for('views.auth_error'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def is_delivery_person(f):
    def wrapper(*args, **kwargs):
        if not current_user.isDeliveryPerson():
            return redirect(url_for('views.auth_error'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper