from flask_sqlalchemy import SQLAlchemy
import datetime

db=SQLAlchemy()

class AdminLogs(db.Model):
    __tablename__ = 'admin_logs'
    folio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idAdministrador = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    hora = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

#class Carrito(db.Model):
#    __tablename__ = 'carrito'
#    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), primary_key=True)
#    idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), primary_key=True)
#    cantidad = db.Column(db.Integer, nullable=False)

class Orden(db.Model):
    __tablename__ = 'orden'
    idOrden = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(70), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(16), nullable=False)
    correo = db.Column(db.String(70), nullable=False)
    fechaPedido = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.String(20), nullable=False)
    idRepartidor = db.Column(db.Integer, db.ForeignKey('repartidor.idRepartidor'), nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=True)

class OrdenProducto(db.Model):
    __tablename__ = 'orden_producto'
    idOP = db.Column(db.Integer, autoincrement=True, primary_key=True)
    idOrden = db.Column(db.Integer, db.ForeignKey('orden.idOrden'), primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    decoracion = db.Column(db.Text, nullable=True)
    destinatario = db.Column(db.String(70), nullable=True)
    fechaLlegada = db.Column(db.DateTime, nullable=True)

class PaqueteProducto(db.Model):
    __tablename__ = 'paquete_producto'
    idPaquete = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), primary_key=True)

class Producto(db.Model):
    __tablename__ = 'producto'
    idProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcionCorta = db.Column(db.String(200), nullable=False)
    descripcionLarga = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(256), nullable=False)
    categoria = db.Column(db.Text, nullable=False)
    fechaCreacion = db.Column(db.DateTime, nullable=False)
    estatus = db.Column(db.Integer, nullable=False)

class Pseudoperfil(db.Model):
    __tablename__ = 'pseudoperfil'
    idPseudoperfil = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(70), nullable=False)
    caracteristicas = db.Column(db.Text, nullable=False)
    idPseudoperfilReal = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)

class Repartidor(db.Model):
    __tablename__ = 'repartidor'
    idRepartidor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(70), nullable=False)
    sueldo = db.Column(db.Float, nullable=False)
    telefono = db.Column(db.String(16), nullable=False)
    compañia = db.Column(db.String(50), nullable=False)
    foto = db.Column(db.String(256), nullable=False)
    estatus = db.Column(db.Integer, nullable=False)

class SessionLogs(db.Model):
    __tablename__ = 'session_logs'
    folio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_session = db.Column(db.DateTime, nullable=False)
    end_session = db.Column(db.DateTime, nullable=True)
    ip = db.Column(db.String(20), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(70), nullable=False)
    correo = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    foto = db.Column(db.String(256), nullable=False)
    fechaCreacion = db.Column(db.DateTime, nullable=False)
    estatus = db.Column(db.Integer, nullable=False)
    count_try = db.Column(db.Integer, nullable=False)
    codigoRecuperacion = db.Column(db.String(6), nullable=False)

class Valoracion(db.Model):
    __tablename__ = 'valoracion'
    idValoracion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    puntuacion = db.Column(db.Float, nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fechaCreacion = db.Column(db.DateTime, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'), nullable=False)