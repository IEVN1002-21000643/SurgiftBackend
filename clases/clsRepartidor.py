from flask import jsonify
from models import db
from sqlalchemy import text
from datetime import datetime

def verRepartidores():
    repartidores=db.session.execute(text(f"SELECT * FROM repartidor"))
    if repartidores != []:
        data=repartidores.fetchall()
        repartidorLista=[]
        for fila in data:
            estatus=''
            if fila[6] == 0:
                estatus='Borrador'
            elif fila[6] == 1:
                estatus='Publicado'
            else:
                estatus='Papelera'
            repartidor={'idRepartidor': fila[0], 'nombre': fila[1], 'sueldo': fila[2], 'telefono': fila[3], 'compania': fila[4], 'foto': fila[5], 'estatus': estatus}
            repartidorLista.append(repartidor)
        return jsonify({'Repartidores': repartidorLista, 'exito':True})
    else:
        return jsonify({'message': "No existen repartidores en la base de datos", 'exito':False})

def verRepartidor(id):
    repartidor=db.session.execute(text(f"SELECT * FROM repartidor WHERE idRepartidor='{id}'"))
    data=repartidor.fetchall()
    repartidor={}
    if repartidor!=[]:
        for fila in data:
            estatus=''
            if fila[6] == 0:
                estatus='Borrador'
            elif fila[6] == 1:
                estatus='Publicado'
            else:
                estatus='Papelera'
            repartidor={'idRepartidor': fila[0], 'nombre': fila[1], 'sueldo': fila[2], 'telefono': fila[3], 'compania': fila[4], 'foto': fila[5], 'estatus': estatus}
        return jsonify({'Repartidor':repartidor, 'exito':True})
    else:
        return jsonify({'message': "El Repartidor que buscas no existe", 'exito':False})
    
def crearRepartidor(nom, sue, tel, com, foto, stat):
    db.session.execute(text(f"INSERT INTO repartidor (nombre, sueldo, telefono, compañia, foto, estatus) values ('{nom}', '{sue}', '{tel}', '{com}', '{foto}', '{stat}')"))
    db.session.commit()
    return jsonify({'message': 'Repartidor agregado', 'exito':True})

def modificarRepartidor(id, nom, sue, tel, com, foto, stat):
    exist=verRepartidor(id).get_json()['Repartidor']
    if exist != []:
        db.session.execute(text(f"UPDATE repartidor SET nombre='{nom}', sueldo='{sue}', telefono='{tel}', compañia='{com}', foto='{foto}', estatus='{stat}' WHERE idRepartidor='{id}'"))
        db.session.commit()
        return jsonify({'message': "Repartidor actualizado", 'exito':True})
    else:
        return jsonify({'message': "El Repartidor que quieres editar no existe", 'exito':False})
    
def eliminarRepartidor(id):
    exist=verRepartidor(id)
    if exist != []:
        db.session.execute(text(f"DELETE FROM repartidor WHERE idRepartidor='{id}'"))
        db.session.commit()
        return jsonify({'message': "Repartidor eliminado", 'exito':False})
    else:
        return jsonify({'message': "El Repartidor que quieres eliminar no existe", 'exito':False})