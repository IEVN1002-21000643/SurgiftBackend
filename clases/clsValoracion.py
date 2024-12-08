from flask import jsonify
from models import db
from sqlalchemy import text
from datetime import datetime
from clases import clsUsuario, clsProducto

def verValoraciones(idP):
    valoraciones=db.session.execute(text(f"SELECT * FROM valoracion WHERE idProducto='{idP}'"))
    if valoraciones!=[]:
        data=valoraciones.fetchall()
        valoracionLista=[]
        for fila in data:
            valoracion={"idValoracion":fila[0], "puntuacion":fila[1], "comentario":fila[2], "fechaCreacion":fila[3], "idUsuario":fila[4], "idProducto": fila[5]}
            valoracionLista.append(valoracion)
        return jsonify({'Valoraciones': valoracionLista, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ninguna valoración para este producto", 'exito':False})

def verValoracion(idV):
    valoracion=db.session.execute(text(f"SELECT * FROM valoracion WHERE idValoracion='{idV}'"))
    return valoracion

def crearValoracion(pun, com, idU, idP):
    hoy=datetime.now()
    usuario=clsUsuario.verUsuario(idU)
    producto= clsProducto.verProducto(idP)
    if usuario != []:
        if producto != []:
            db.session.execute(text(f"INSERT INTO valoracion (puntuacion, comentario, fechaCreacion, idUsuario, id Producto) values ('{pun}', '{com}', '{hoy}', '{idU}', '{idP}')"))
            db.session.commit()
            return jsonify({'message': "Tu comentario ha sido registrado", 'exito':True})
        else:
            return jsonify({'message': "El producto no existe", 'exito':False})
    else:
        return jsonify({'message': "El usuario no existe", 'exito':False})
    
def editarValoracion(idV,pun, com, idU, idP):
    existeValoracion=verValoracion(idV)
    existeUsuario=clsUsuario.verUsuario(idU)
    existeProducto=clsProducto.verProducto(idP)
    if existeProducto != []:
        if existeUsuario != []:
            if existeValoracion != []:
                db.session.execute(text(f"UPDATE valoracion puntuacion='{pun}', comentario='{com}' WHERE idValoracion='{idV}' and idProducto='{idP}' and idUsuario='{idU}'"))
                db.session.commit()
                return jsonify({'message': "Tu comentario ha sido modificado", 'exito':True})
            else:
                return jsonify({'message': "La valoracion no existe", 'exito':False})
        else:
            return jsonify({'message': "El Usuario no existe", 'exito':False})
    else:
        return jsonify({'message': "El producto no existe", 'exito':False})
    
def eliminarValoracion(idV, idU, idP):
    existeValoracion=verValoracion(idV)
    existeUsuario=clsUsuario.verUsuario(idU)
    existeProducto=clsProducto.verProducto(idP)
    if existeProducto != []:
        if existeUsuario != []:
            if existeValoracion != []:
                db.session.execute(text(f"DELETE FROM valoracion WHERE idValoracion='{idV}' and idProducto='{idP}' and idUsuario='{idU}'"))
                db.session.commit()
                return jsonify({'message': "Tu comentario ha sido eliminado", 'exito':True})
            else:
                return jsonify({'message': "La valoracion no existe", 'exito':False})
        else:
            return jsonify({'message': "El Usuario no existe", 'exito':False})
    else:
        return jsonify({'message': "El producto no existe", 'exito':False})