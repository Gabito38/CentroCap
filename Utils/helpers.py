from functools import wraps
from flask import session, redirect, url_for, flash
import datetime
import re

# ---------------------------------------------------------
# Decorador para requerir login
# ---------------------------------------------------------
def login_required(f):
    """
    Decorador que exige que el usuario esté autenticado
    antes de acceder a una vista protegida.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.')
            return redirect(url_for('auth_controller.login'))
        return f(*args, **kwargs)
    return decorated_function