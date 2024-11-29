from flask import Flask, render_template, redirect, url_for, request
from models import db, Permiso
from sqlalchemy import text
from app import app

########################################## Listar Permisos ##############################################
@app.route('/permisos', methods=['GET'])
def permisos():
    results = Permiso.query.all()
    return render_template ('/roles_permisos/permisos.html', active_page='permisos', permisos=results)

########################################## Agregar Permisos ##############################################
@app.route('/nuevoPermiso', methods=['GET','POST'])
def nuevoPermiso():
    if request.method == 'POST':
        nombrePermiso = request.form['nombre']
        permiso = Permiso(nombrePermiso=nombrePermiso)
        db.session.add(permiso)
        db.session.commit()
        return redirect(url_for('permisos'))
    return render_template('/roles_permisos/permisos.html')

########################################## Eliminar Permisos ##############################################
@app.route('/eliminarPermiso/<int:permisoID>', methods=['GET'])
def eliminarPermiso(permisoID):
    # Buscar la empresa en la base de datos
    permiso = Permiso.query.get(permisoID)
    
    if permiso:
        db.session.delete(permiso)
        db.session.commit()
    return redirect(url_for('permisos'))