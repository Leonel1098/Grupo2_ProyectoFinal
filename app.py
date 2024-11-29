import os
from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import emit
from models import db
from config import Config
from datetime import date, datetime
from sqlalchemy import text
from config import socketio
import pyodbc

app = Flask(__name__)
# Inicializa socketio con la app
socketio.init_app(app)
#Se carga la configuración desde un objeto config
app.config.from_object(Config)
#Se inicializa la base de datos con la aplicacióin flask usando db.init_app().
db.init_app(app)

from routes.login import *                  # Rutas de login
from routes.dashboard import *              # Rutas de Dashboard
from routes.departamentos import *          # Rutas de Empresas
from routes.usuarios import *               # Rutas de Usuarios
from routes.empleados import *              # Ruta de empleados
from routes.tareas import *                 # Ruta de tareas
from routes.permisos import *               # Ruta de permisos
from routes.roles import *                  # Ruta de roles
  

if __name__ == "__main__":
    # Obtener el puerto desde la variable de entorno de Render
    port = int(os.environ.get('PORT', 5000))  # Puerto por defecto 5000 si no se encuentra el 'PORT'
    
    # Ejecutar la aplicación Flask con SocketIO
    socketio.run(app, host='0.0.0.0', port=port, debug=True)