from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Rol, Permiso, RolesPermiso
from sqlalchemy import text
from app import app

########################################## Listar Roles ##############################################
@app.route('/roles', methods=['GET'])
def roles():
    results = Rol.query.all()
    return render_template ('/roles_permisos/roles.html', active_page='roles', roles=results)

########################################## Agregar Roles ##############################################
@app.route('/nuevoRol', methods=['GET','POST'])
def nuevoRol():
    if request.method == 'POST':
        nombreRol = request.form['nombre']
        rol = Rol(nombreRol=nombreRol)
        db.session.add(rol)
        db.session.commit()
        return redirect(url_for('roles'))
    return render_template('/roles_permisos/roles.html')

########################################## ROLES Y PERMISOS ##############################################
# @app.route('/asignarPermisos/<int:role_id>', methods=['GET', 'POST'])
# def asignarPermisos(role_id):
#     role = Rol.query.get(role_id)
#     permisos = Permiso.query.all()

#     if request.method == 'POST':
#         rolID = role.rolID
#         permisos = request.form.getlist('permisos')      

#         permisos = Permiso.query.filter(Permiso.permisoID.in_(permisos)).all()
        
#         # Remover permisos existentes
#         RolesPermiso.query.filter_by(rolID=rolID).delete()

#         # Asignar nuevos permisos
#         for permiso in permisos:
#             roles_permiso = RolesPermiso(rolID=rolID, permisoID=permiso.permisoID)
#             db.session.add(roles_permiso)
#         db.session.commit()
#         return redirect(url_for('roles'))

#     return render_template('/roles_permisos/asignarPermisos.html', role=role, permisos=permisos)

########################################## CONTROL PERMISOS ##############################################
@app.route('/controlPermisos/<int:rol_id>', methods=['GET', 'POST'])
def controlPermisos(rol_id):
    # Obtener el rol seleccionado
    rol = Rol.query.get_or_404(rol_id)
    # Obtener todos los permisos
    permisos = Permiso.query.all()
    # Obtener los permisos actuales del rol
    permisos_rol = db.session.query(Permiso).join(RolesPermiso).filter(RolesPermiso.rolID == rol_id).all()
    permisos_rol_ids = {permiso.permisoID for permiso in permisos_rol}

    if request.method == 'POST':
        # Obtener los permisos seleccionados en el formulario
        permisos_seleccionados = request.form.getlist('permisos')
        # Eliminar los permisos actuales del rol
        RolesPermiso.query.filter_by(rolID=rol_id).delete()
        # Asignar los permisos seleccionados
        for permiso_id in permisos_seleccionados:
            roles_permiso = RolesPermiso(rolID=rol_id, permisoID=int(permiso_id))
            db.session.add(roles_permiso)
        db.session.commit()
        # Redirigir a la lista de roles o a otra página
        return redirect(url_for('roles'))
    return render_template('/roles_permisos/controlPermisos.html', rol=rol, permisos=permisos, permisos_rol_ids=permisos_rol_ids)

########################################## ELIMINAR ROL ##############################################
@app.route('/eliminarRol/<int:rolID>', methods=['GET'])
def eliminarRol(rolID):
    roles_permisos = RolesPermiso.query.filter_by(rolID=rolID).all()

    if roles_permisos:
        # Si existen registros, no se puede eliminar el rol
        return redirect(url_for('roles', error_message="No se puede eliminar este rol porque tiene permisos asociados."))
    else:
        # Si no existen registros, proceder con la eliminación del rol
        rol = Rol.query.get(rolID)
        if rol:
            db.session.delete(rol)
            db.session.commit()
            return redirect(url_for('roles', success_message="Rol eliminado exitosamente."))

########################################## Editar ROL ##############################################
@app.route('/editarRol', methods=['POST'])
def editarRol():
    if request.method == 'POST':
        rolID = request.form['rolID']
        nombreRol = request.form['nombre']

        # Buscar el departamento en la base de datos por ID
        rol = Rol.query.get(rolID)
        if rol:
            rol.nombreRol = nombreRol
            db.session.commit()
        return redirect(url_for('roles'))