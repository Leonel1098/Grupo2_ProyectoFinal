from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from models import db, Empleado, Departamento
from config import Config
from datetime import date, datetime
from sqlalchemy import text
from app import app

########################################## Listar y agregar Empleados ##############################################
@app.route('/empleados', methods=['GET', 'POST'])
def empleados():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombreEmpleado = request.form['nombre']
        correo = request.form['email']
        esAdministrador = True if request.form.get('admin') else False
        departamentoID = request.form['departamento']

        # Crear un nuevo empleado con los datos del formulario
        nuevo_empleado = Empleado(
            nombreEmpleado=nombreEmpleado,
            correo=correo,
            esAdministrador=esAdministrador,
            departamentoID=departamentoID
        )

        # Agregar el nuevo empleado a la base de datos
        db.session.add(nuevo_empleado)
        db.session.commit()

        # Redirigir a la misma página para que se recargue la lista de empleados
        return redirect(url_for('empleados'))

    # Si el método es GET, obtenemos los departamentos y los empleados
    departamentos = Departamento.query.all()
    search_query = request.args.get('search', '')
    if search_query:
        results = Empleado.query.outerjoin(Departamento).filter(
            db.or_(
                Empleado.nombreEmpleado.ilike(f'%{search_query}%'),
                Departamento.nombreDepartamento.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        results = Empleado.query.outerjoin(Departamento).all()

    empleados_data = [
        {
            'empleadoID': empleado.empleadoID,
            'nombreEmpleado': empleado.nombreEmpleado,
            'correo': empleado.correo,
            'nombreDepartamento': empleado.departamento.nombreDepartamento if empleado.departamento else 'No asignado',
            'esAdministrador': "SI" if empleado.esAdministrador else "NO"
        }
        for empleado in results
    ]
    # Renderizar la plantilla pasando los datos de empleados y departamentos
    return render_template('/empleados/empleados.html', 
                           active_page='empleados', 
                           empleados=empleados_data, 
                           departamentos=departamentos)

########################################## Cargar datos y editar empleado ##############################################
@app.route('/empleado/<int:empleadoID>/editar', methods=['GET'])
def cargarEmpleadoEditar(empleadoID):
    empleado = Empleado.query.get_or_404(empleadoID)
    return jsonify({
        'empleadoID': empleado.empleadoID,
        'nombreEmpleado': empleado.nombreEmpleado,
        'correo': empleado.correo,
        'esAdministrador': "SI" if empleado.esAdministrador else "NO",
        'departamentoID': empleado.departamentoID
    })

@app.route('/editarEmpleado', methods=['POST'])
def editarEmpleado():
    empleadoID = request.form['empleadoID']
    nombre = request.form['nombre']
    correo = request.form['email']
    esAdministrador = request.form.get('admin') == 'on'
    departamentoID = request.form['departamento']
    
    empleado = Empleado.query.get_or_404(empleadoID)
    empleado.nombreEmpleado = nombre
    empleado.correo = correo
    empleado.esAdministrador = esAdministrador
    empleado.departamentoID = departamentoID

    db.session.commit()
    return redirect(url_for('empleados'))

########################################## Eliminar Empleado ##############################################
@app.route('/eliminarEmpleado/<int:empleadoID>', methods=['GET'])
def eliminarEmpleado(empleadoID):
    # Buscar la empresa en la base de datos
    empleado = Empleado.query.get(empleadoID)
    
    if empleado:
        db.session.delete(empleado)
        db.session.commit()
    return redirect(url_for('empleados'))
