-- Creación de la base de datos
CREATE DATABASE GestionTareas;
USE GestionTareas;

-- Tabla de Empresas
CREATE TABLE Departamentos (
    departamentoID INT PRIMARY KEY IDENTITY(1,1),
    nombreDepartamento NVARCHAR(100)
);

-- Tabla de Empleados
CREATE TABLE Empleados (
    empleadoID INT PRIMARY KEY IDENTITY(1,1),
    departamentoID INT,
    nombreEmpleado NVARCHAR(100),
	correo NVARCHAR(255),
    esAdministrador BIT DEFAULT 0,
    FOREIGN KEY (departamentoID) REFERENCES Departamentos(departamentoID)
);

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    usuarioID INT PRIMARY KEY IDENTITY(1,1),
    empleadoID INT,
    nombreUsuario NVARCHAR(50),
    contraseña NVARCHAR(255), -- Encriptada
    FOREIGN KEY (empleadoID) REFERENCES Empleados(empleadoID)
);

-- Tabla de Roles
CREATE TABLE Roles (
    rolID INT PRIMARY KEY IDENTITY(1,1),
    nombreRol NVARCHAR(50)
);

-- Tabla de Permisos
CREATE TABLE Permisos (
    permisoID INT PRIMARY KEY IDENTITY(1,1),
    nombrePermiso NVARCHAR(50)
);

-- Tabla de Roles y Permisos (Relación)
CREATE TABLE RolesPermisos (
    rolID INT,
    permisoID INT,
    PRIMARY KEY (rolID, permisoID),
    FOREIGN KEY (rolID) REFERENCES Roles(rolID),
    FOREIGN KEY (permisoID) REFERENCES Permisos(permisoID)
);

-- Tabla de Usuarios y Roles (Relación)
CREATE TABLE UsuariosRoles (
    usuarioID INT,
    rolID INT,
    PRIMARY KEY (usuarioID, rolID),
    FOREIGN KEY (usuarioID) REFERENCES Usuarios(usuarioID),
    FOREIGN KEY (rolID) REFERENCES Roles(rolID)
);

-- Tabla de Tareas
CREATE TABLE Tareas (
    tareaID INT PRIMARY KEY IDENTITY(1,1),
    titulo NVARCHAR(200),
    descripcion NVARCHAR(MAX),
    estado NVARCHAR(50) CHECK (Estado IN ('Pendiente', 'En Progreso', 'Completada')) DEFAULT 'Pendiente',
    asignadaA INT,
    FOREIGN KEY (asignadaA) REFERENCES Empleados(empleadoID)
);

drop table Tareas;
drop table UsuariosRoles;
drop table RolesPermisos;
drop table Permisos;
drop table Roles;
drop table Usuarios;
drop table Empleados;
drop table Departamentos;

-- Insertar el usuario administrador del sistema
INSERT INTO Departamentos(nombreDepartamento) 
VALUES ('SistemaGlobal');

INSERT INTO Empleados (DepartamentoID, NombreEmpleado, Correo, EsAdministrador) 
VALUES (1, 'Administrador del Sistema', 'halonzoa12@gmail.com',1);

INSERT INTO Usuarios (EmpleadoID, NombreUsuario, Contraseña) 
VALUES (1, 'admin', HASHBYTES('SHA2_256', 'admin123'));

-- Insertar rol de administrador del sistema
INSERT INTO Roles (NombreRol) 
VALUES ('AdministradorSistema');

-- Asociar permisos globales al rol de administrador
INSERT INTO Permisos (NombrePermiso) 
VALUES ('GestionarUsuarios'), ('GestionarEmpresas'), ('GestionarTareas');

SELECT * FROM Departamentos;
SELECT * FROM Empleados;
SELECT * FROM Permisos;
SELECT * FROM Roles;
SELECT * FROM RolesPermisos;
SELECT * FROM Tareas;
SELECT * FROM Usuarios;
SELECT * FROM UsuariosRoles;

INSERT INTO RolesPermisos (RolID, PermisoID)
SELECT RolID, PermisoID 
FROM Roles, Permisos
WHERE Roles.NombreRol = 'AdministradorSistema';

-- Asignar rol de administrador del sistema al usuario admin
INSERT INTO UsuariosRoles (UsuarioID, RolID)
SELECT UsuarioID, RolID 
FROM Usuarios, Roles
WHERE Usuarios.NombreUsuario = 'admin' AND Roles.NombreRol = 'AdministradorSistema';
