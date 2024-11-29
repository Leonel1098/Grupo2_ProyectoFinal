import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://publico:123456789@34.170.26.184/GestionTareas?driver=ODBC+Driver+17+for+SQL+Server'
    # SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://hector:Alonzo123@DESKTOP-OV27GS9/GestionTareas?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)


from flask_socketio import SocketIO

# Inicializar SocketIO
socketio = SocketIO()
