from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Departamento(db.Model):
    __tablename__ = 'Departamentos'
    departamentoID = db.Column(db.Integer, primary_key=True)
    nombreDepartamento = db.Column(db.String(100), nullable=False)

class Empleado(db.Model):
    __tablename__ = 'Empleados'
    empleadoID = db.Column(db.Integer, primary_key=True)
    nombreEmpleado = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(255), nullable=False)
    esAdministrador = db.Column(db.Boolean, default=False)
    departamentoID = db.Column(db.Integer, db.ForeignKey('Departamentos.departamentoID'), nullable=False)

    # Relación con la tabla Departamento (en el modelo Empleado, es solo una clave foránea)
    departamento = db.relationship('Departamento', backref=db.backref('empleados', lazy=True))

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    usuarioID = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(50), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    empleadoID = db.Column(db.Integer, db.ForeignKey('Empleados.empleadoID'), nullable=False)
    
    empleado = db.relationship('Empleado', backref=db.backref('usuarios', lazy=True))
    roles = db.relationship('Rol', secondary='UsuariosRoles', backref=db.backref('usuarios', lazy='dynamic'))

class Rol(db.Model):
    __tablename__ = 'Roles'
    rolID = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String(50), nullable=False)

class UsuarioRoles(db.Model):
    __tablename__ = 'UsuariosRoles'
    rolID = db.Column(db.Integer, db.ForeignKey('Roles.rolID'), primary_key=True, nullable=False)
    usuarioID = db.Column(db.Integer, db.ForeignKey('Usuarios.usuarioID'), primary_key=True, nullable=False)
    
    rol = db.relationship('Rol', backref=db.backref('usuariosroles', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('usuarioroles', lazy=True))

class Permiso(db.Model):
    __tablename__ = 'Permisos'
    permisoID = db.Column(db.Integer, primary_key=True)
    nombrePermiso = db.Column(db.String(50), nullable=False)

class RolesPermiso(db.Model):
    __tablename__ = 'RolesPermisos'
    rolID = db.Column(db.Integer, db.ForeignKey('Roles.rolID'), primary_key=True, nullable=False)
    permisoID = db.Column(db.Integer, db.ForeignKey('Permisos.permisoID'), primary_key=True, nullable=False)
    
    rol = db.relationship('Rol', backref=db.backref('rolespermisos', lazy=True))
    permiso = db.relationship('Permiso', backref=db.backref('rolespermisos', lazy=True))

class Tarea(db.Model):
    __tablename__ = 'Tareas'

    tareaID = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(50), default='Pendiente', nullable=False)
    asignadaA = db.Column(db.Integer, db.ForeignKey('Empleados.empleadoID'), nullable=False)

    # Relación con la tabla Empleados (un empleado puede estar asignado a múltiples tareas)
    asignado_a = db.relationship('Empleado', backref=db.backref('tareas', lazy=True))