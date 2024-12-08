from flask import jsonify
from models import db
from sqlalchemy import text
from datetime import datetime

def verUsuarios():
    usuarios=db.session.execute(text(f"SELECT idUsuario, nombre, correo, direccion, fechaCreacion, estatus, foto FROM usuario"))
    if usuarios!=[]:
        data=usuarios.fetchall()
        usuarioLista=[]
        for fila in data:
            estatus=''
            if fila[5] == 0:
                estatus='Administrador'
            elif fila[5] == 1:
                estatus='Cliente'
            elif fila[5] == 2:
                estatus='Papelera'
            usuario={'idUsuario': fila[0], 'nombre': fila[1], 'correo': fila[2], 'direccion': fila[3], 'fechaCreacion': fila[4], 'estatus': estatus, 'foto': fila[6]}
            usuarioLista.append(usuario)
        return jsonify({'Usuarios': usuarioLista, 'exito':True})
    else:
        return jsonify({'message': "No existen usuarios en la base de datos", 'exito':False})
    
def verUsuario(id):
    usuarios=db.session.execute(text(f"SELECT idUsuario, nombre, correo, direccion, fechaCreacion, estatus, foto FROM usuario WHERE idUsuario='{id}'"))
    usuario={}
    if usuarios!=[]:
        data=usuarios.fetchall()
        for fila in data:
            usuario={'idUsuario': fila[0], 'nombre': fila[1], 'correo': fila[2], 'direccion': fila[3], 'fechaCreacion': fila[4], 'estatus': fila[5], 'foto': fila[6]}
        return jsonify({'Usuarios': usuario, 'exito':True})
    else:
        return jsonify({'message': "No existen usuarios en la base de datos", 'exito':False})
    
def crearUsuario(nom, cor, passw, dir, foto, stat):
    hoy=datetime.now()
    exist=verUsuarios().get_json()['Usuarios']
    correoExist=0
    if exist != []:
        for objeto in exist:
            if objeto['correo'] == cor:
                correoExist=1
    if correoExist ==0:
        db.session.execute(text(f"INSERT INTO usuario (nombre, correo, password, direccion, foto, fechaCreacion, estatus, count_try, codigoRecuperacion) values ('{nom}', '{cor}', '{passw}', '{dir}', '{foto}', '{hoy}', '{stat}', '0', '')"))
        db.session.commit()
        return jsonify({'message': "Usuario registrado", 'exito':True})
    else:
        return jsonify({'message': "Ya existe un usuario usando ese correo", 'exito':False})

def editarUsuario(id, nom, dir, foto, stat):
    exist=verUsuario(id)
    if exist != []:
        db.session.execute(text(f"UPDATE usuario SET nombre='{nom}', direccion='{dir}', foto='{foto}', estatus='{stat}' WHERE idUsuario='{id}'"))
        db.session.commit()
        return jsonify({'message': "Usuario editado", 'exito':True})
    else:
        return jsonify({'message': "El usuario que intentas modificar no existe", 'exito':False})

def eliminarUsuario(id):
    exist=verUsuario(id)
    if exist != []:
        db.session.execute(text(f"DELETE FROM usuario WHERE idUsuario='{id}'"))
        db.session.commit()
        return jsonify({'message': "Usuario eliminado", 'exito':True})
    else:
        return jsonify({'message': "El usuario que intentas eliminar no existe", 'exito':False})
    
def login(correo, passw):
    exist=db.session.execute(text(f"SELECT correo, estatus, idUsuario from usuario WHERE correo='{correo}' and password='{passw}' and estatus='1'"))
    if exist != []:
        data=exist.fetchall()
        return [data[0][0], data[0][1], data[0][2]]
    else:
        return jsonify({'message': "El correo o contraseña son erroneos", 'exito':False})
    
def loginAdmin(correo, passw):
    exist=db.session.execute(text(f"SELECT correo, estatus, idUsuario from usuario WHERE correo='{correo}' and password='{passw}' and estatus='0'"))
    if exist != []:
        data=exist.fetchall()
        return [data[0][0], data[0][1], data[0][2]]
    else:
        return jsonify({'message': "El correo o contraseña son erroneos", 'exito':False})
    
def encontrarId(cor):
    sql=db.session.execute(text(f"SELECT idUsuario FROM usuario WHERE correo='{cor}'"))
    idUsuario=sql.fetchall()[0][0]
    return idUsuario