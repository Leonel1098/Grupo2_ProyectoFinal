CREATE DATABASE gestor_tareas;
USE gestor_tareas;

CREATE TABLE Empleados(
	id_empleado INT PRIMARY KEY IDENTITY(1,1),
	nombres NVARCHAR(100),
	apellidos NVARCHAR(100),
	email NVARCHAR(50),
	telefono INT,
	direccion NVARCHAR(150)
);

CREATE TABLE Permisos(
	id_permiso INT PRIMARY KEY IDENTITY(1,1),
	nombre_permiso NVARCHAR(50)
);

CREATE TABLE Roles (
    id_rol INT PRIMARY KEY IDENTITY(1,1),
    nombre_rol NVARCHAR(50) NOT NULL
);

CREATE TABLE Usuarios(
    id_usuario INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50) NOT NULL,
    password_hash NVARCHAR(255) NOT NULL,
    estatus BIT DEFAULT 1,
	id_empleado INT,
	id_rol INT,
	CONSTRAINT FK_Usuario_Empleado FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado),
	CONSTRAINT FK_Usuario_Rol FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
);

CREATE TABLE Usuarios_permisos(
	id_usuario INT,
	id_permiso INT,
	PRIMARY KEY(id_usuario, id_permiso),
	CONSTRAINT FK_UsuarioPermisos_Usuarios FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    CONSTRAINT FK_UsuarioPermisos_Permisos FOREIGN KEY (id_permiso) REFERENCES Permisos(id_permiso)
);