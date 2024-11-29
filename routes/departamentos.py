from flask import Flask, render_template, redirect, url_for, request
from models import db, Departamento
# from config import Config
# from datetime import date, datetime
from sqlalchemy import text
from app import app

########################################## Listar Departamentos ##############################################
@app.route('/departamentos', methods=['GET'])
def departamentos():
    results = Departamento.query.all()
    return render_template ('/departamentos/departamentos.html', active_page='departamentos', departamentos=results)

########################################## Agregar Departamentos ##############################################
@app.route('/nuevoDepartamento', methods=['GET','POST'])
def nuevoDepartamento():
    if request.method == 'POST':
        nombreDepartamento = request.form['nombre']
        departamento = Departamento(nombreDepartamento=nombreDepartamento)        
        db.session.add(departamento)
        db.session.commit()
        return redirect(url_for('departamentos'))
    return render_template('/departamentos/departamentos.html')

########################################## Editar Departamentos ##############################################
@app.route('/editarDepartamento', methods=['POST'])
def editarDepartamento():
    if request.method == 'POST':
        departamentoID = request.form['departamentoID']
        nombreDepartamento = request.form['nombre']

        # Buscar el departamento en la base de datos por ID
        departamento = Departamento.query.get(departamentoID)
        if departamento:
            departamento.nombreDepartamento = nombreDepartamento
            db.session.commit()
        return redirect(url_for('departamentos'))

########################################## Eliminar Departamentos ##############################################
@app.route('/eliminarDepartamento/<int:departamentoID>', methods=['GET'])
def eliminarDepartamento(departamentoID):
    # Buscar la empresa en la base de datos
    departamento = Departamento.query.get(departamentoID)
    
    if departamento:
        db.session.delete(departamento)
        db.session.commit()
    return redirect(url_for('departamentos'))

