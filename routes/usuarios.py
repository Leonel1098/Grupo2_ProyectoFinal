from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from models import db, Usuario, Empleado, Rol, UsuarioRoles
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from app import app

########################################## Listar y agregar Usuarios ##############################################
@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombreUsuario = request.form['nombre']
        empleadoID = request.form['empleado']
        rolID = request.form['rol']
        contraseña = request.form['contraseña']
        hashed_password = generate_password_hash(contraseña)

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            nombreUsuario=nombreUsuario,
            empleadoID=empleadoID,
            contraseña=hashed_password
        )

        # Agregar el nuevo usuario a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Asignar el rol al usuario en la tabla UsuariosRoles
        usuario_rol = UsuarioRoles(usuarioID=nuevo_usuario.usuarioID, rolID=rolID)
        db.session.add(usuario_rol)
        db.session.commit()

        # Redirigir a la misma página para que se recargue la lista de usuarios
        return redirect(url_for('usuarios'))

    # Si el método es GET, obtenemos los empleados y los roles
    empleados = Empleado.query.all()
    roles = Rol.query.all()
    search_query = request.args.get('search', '')
    if search_query:
        results = Usuario.query.outerjoin(Empleado).filter(
            db.or_(
                Usuario.nombreEmpleado.ilike(f'%{search_query}%'),
                Empleado.nombreDepartamento.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        results = Usuario.query.outerjoin(Empleado).all()

    usuarios_data = [
        {
            'usuarioID': usuario.usuarioID,
            'nombreUsuario': usuario.nombreUsuario,
            'nombreEmpleado': usuario.empleado.nombreEmpleado if usuario.empleado else 'No asignado',
            'correo': usuario.empleado.correo if usuario.empleado else 'No asignado',
            'rol': ', '.join([rol.nombreRol for rol in usuario.roles])  # Accediendo a los roles asociados a través de la relación
        }
        for usuario in results
    ]
    return render_template('/usuarios/usuarios.html', 
                           active_page='usuarios',
                           usuarios=usuarios_data, 
                           empleados=empleados, 
                           roles=roles)

@app.route('/usuario/<int:usuarioID>', methods=['GET'])
def get_usuario(usuarioID):
    usuario = Usuario.query.get_or_404(usuarioID)
    # Suponiendo que un usuario puede tener múltiples roles
    roles = [rol.rolID for rol in usuario.roles]  # Puedes devolver los roles en la respuesta
    return jsonify({
        'nombreUsuario': usuario.nombreUsuario,
        'rolID': roles[0] if roles else None  # Asume que un usuario puede tener solo un rol en el formulario
    })


@app.route('/editar_usuario/<int:usuarioID>', methods=['GET', 'POST'])
def editar_usuario(usuarioID):
    # Buscar el usuario por su ID
    usuario = Usuario.query.get_or_404(usuarioID)
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombreUsuario = request.form['nombreUsuario']
        rolID = request.form['rol']
        
        # Actualizar el usuario
        usuario.nombreUsuario = nombreUsuario
        
        # Actualizar los roles del usuario
        # Primero eliminamos los roles antiguos
        UsuarioRoles.query.filter_by(usuarioID=usuarioID).delete()
        
        # Asignamos el nuevo rol
        usuario_rol = UsuarioRoles(usuarioID=usuarioID, rolID=rolID)
        db.session.add(usuario_rol)
        
        # Guardamos los cambios
        db.session.commit()

        # Redirigir a la página de usuarios
        return redirect(url_for('usuarios'))

    # Si el método es GET, mostramos el formulario con los datos actuales del usuario
    roles = Rol.query.all()
    return render_template('/usuarios/usuarios.html', usuario=usuario, roles=roles)

@app.route('/eliminarUsuario/<int:usuarioID>', methods=['GET'])
def eliminarUsuario(usuarioID):
    usuario = Usuario.query.get(usuarioID)
    if usuario:
        # Eliminar los registros asociados en la tabla UsuariosRoles
        UsuarioRoles.query.filter_by(usuarioID=usuarioID).delete()
        # Eliminar el usuario
        db.session.delete(usuario)
        db.session.commit()
    return redirect(url_for('usuarios'))