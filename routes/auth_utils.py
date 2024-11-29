from flask import session, redirect, url_for, flash
from functools import wraps

# Autenticador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            # Verificar si el usuario tiene sesión activa y un rol válido
            if 'rol' not in session or session['rol'] not in allowed_roles:
                # flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('dashboard'))  # Redirigir al dashboard o a una página permitida
            return f(*args, **kwargs)
        return wrapped_function
    return decorator
