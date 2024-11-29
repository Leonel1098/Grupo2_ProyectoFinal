from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, Usuario, Rol, UsuarioRoles
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from functools import wraps
from app import app

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombreUsuario = request.form['username']
        contraseña = request.form['password']
        user = Usuario.query.filter_by(nombreUsuario=nombreUsuario).first()

        if user and check_password_hash(user.contraseña, contraseña):
            # Obtener los roles del usuario
            roles = [rol.nombreRol for rol in user.roles]

            # Establecer los datos en la sesión
            session['user_id'] = user.usuarioID
            session['rol'] = 'Administrador' if 'Administrador' in roles else 'Empleado'

            # Redirigir al dashboard
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'danger')

    return render_template("/login/login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

