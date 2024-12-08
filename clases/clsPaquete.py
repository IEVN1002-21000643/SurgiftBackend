from flask import jsonify
from models import db
from sqlalchemy import text
from datetime import datetime
from clases import clsProducto

def crearPaquete(nom, pre, descC, descL, foto, cat, stat, idProducto):
    productoExiste=clsProducto.verProducto(idProducto)
    if productoExiste != []:
        clsProducto.crearProducto(nom, pre, descC, descL, foto, cat, stat)
        result=db.session.execute(text(f"SELECT idProducto FROM producto  WHERE idProducto=(SELECT max(idProducto) FROM producto)"))
        idPaquete=result.fetchall()
        db.session.execute(text(f"INSERT INTO paquete_producto (idProducto, idPaquete) VALUES ('{idProducto}', '{idPaquete[0][0]}')"))
        db.session.commit()
        return jsonify({'message': "Paquete agregado", 'exito':True})
    else:
        return jsonify({'message': "El producto que intentas añadir al paquete no existe", 'exito':False})


def editarPaquete(id, nom, pre, descC, descL, foto, cat, stat, idP, idProducto):
    paqueteExiste=clsProducto.verProducto(id)
    productoExiste=clsProducto.verProducto(idP)
    newProducto=clsProducto.verProducto(idProducto)
    if productoExiste != [] and paqueteExiste !=[] and newProducto != []:
        db.session.execute(text(f"UPDATE producto set nombre='{nom}', precio='{pre}', descripcionCorta='{descC}', descripcionLarga='{descL}', foto='{foto}', categoria='{cat}', estatus='{stat}' WHERE idProducto='{id}'"))
        db.session.execute(text(f"UPDATE paquete_producto set idProducto='{idProducto}' where idPaquete='{id}' and idProducto='{idP}'"))
        db.session.commit()
        return jsonify({'message': "Paquete editado", 'exito':True})
    else:
        return jsonify({'message': "El Paquete o producto en el paqeute que intentas editar no existe", 'exito':False})


def eliminarPaquete(id, idP):
    paqueteExiste=clsProducto.verProducto(id)
    productoExiste=clsProducto.verProductos(idP)
    if productoExiste != [] and paqueteExiste !=[]:
        db.session.execute(text(f"DELETE FROM paquete_producto WHERE idPaquete='{id}' and idProducto='{idP}'"))
        db.session.commit()
        db.session.execute(text(f"DELETE FROM producto WHERE idProducto='{id}'"))
        db.session.commit()
        return jsonify({'message': "Paquete eliminado", 'exito':True})
    else:
        return jsonify({'message': "El Paquete que intentas eliminar no existe", 'exito':False})