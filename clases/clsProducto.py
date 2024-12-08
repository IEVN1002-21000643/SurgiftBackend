from flask import jsonify
from models import db
from sqlalchemy import text
from datetime import datetime

def verProductos():
    productos = db.session.execute(text(f"SELECT * FROM producto"))
    if productos != []:
        data=productos.fetchall()
        productoLista=[]
        for fila in data:
            estatus=''
            if fila[8] == 0:
                estatus='Borrador'
            elif fila[8] == 1:
                estatus='Publicado'
            else:
                estatus='Papelera'
            paqueteExist=db.session.execute(text(f"SELECT * FROM paquete_producto WHERE idPaquete='{fila[0]}'"))
            isPaquete=paqueteExist.fetchall()
            if isPaquete!=[]:
                paquetes=db.session.execute(text(f"SELECT * from producto where idProducto={isPaquete[0][1]}"))
                paqueteData=paquetes.fetchall()
                paqueteLista=[]
                for filaPaquete in paqueteData:
                    estatus=''
                    if filaPaquete[8] == 0:
                        estatus='Borrador'
                    elif filaPaquete[8] == 1:
                        estatus='Publicado'
                    else:
                        estatus='Papelera'
                    paquete={'idProducto':filaPaquete[0], 'nombre':filaPaquete[1], 'precio':filaPaquete[2], 'descripcionCorta':filaPaquete[3], 'descripcionLarga':filaPaquete[4], 'foto':filaPaquete[5], 'categoria':filaPaquete[6].split(', '), 'estatus':estatus, 'contenido':''}
                    paqueteLista.append(paquete)
                producto={'idProducto':fila[0], 'nombre':fila[1], 'precio':fila[2], 'descripcionCorta':fila[3], 'descripcionLarga':fila[4], 'foto':fila[5], 'categoria':fila[6].split(', '), 'estatus':estatus, 'contenido':paqueteLista}
                productoLista.append(producto)
            else:
                producto={'idProducto':fila[0], 'nombre':fila[1], 'precio':fila[2], 'descripcionCorta':fila[3], 'descripcionLarga':fila[4], 'foto':fila[5], 'categoria':fila[6].split(', '), 'estatus':estatus, 'contenido':''}
                productoLista.append(producto)
        return jsonify({'Productos': productoLista, 'exito': True})
    else:
        return jsonify({'message': "No existen productos en la base de datos", 'exito': False})

def verProducto(id):
    productos = db.session.execute(text(f"SELECT * from producto where idProducto={id}"))
    data=productos.fetchall()
    productoLista=[]
    if productos != []:
        for fila in data:
            estatus=''
            if fila[8] == 0:
                estatus='Borrador'
            elif fila[8] == 1:
                estatus='Publicado'
            else:
                estatus='Papelera'
            paqueteExist=db.session.execute(text(f"SELECT * FROM paquete_producto WHERE idPaquete='{fila[0]}'"))
            isPaquete=paqueteExist.fetchall()
            if isPaquete!=[]:
                paquetes=db.session.execute(text(f"SELECT * from producto where idProducto={isPaquete[0][1]}"))
                paqueteData=paquetes.fetchall()
                paqueteLista=[]
                for filaPaquete in paqueteData:
                    estatus=''
                    if filaPaquete[8] == 0:
                        estatus='Borrador'
                    elif filaPaquete[8] == 1:
                        estatus='Publicado'
                    else:
                        estatus='Papelera'
                    paquete={'idProducto':filaPaquete[0], 'nombre':filaPaquete[1], 'precio':filaPaquete[2], 'descripcionCorta':filaPaquete[3], 'descripcionLarga':filaPaquete[4], 'foto':filaPaquete[5], 'categoria':filaPaquete[6].split(', '), 'fechaCreacion': filaPaquete[7], 'estatus':estatus, 'contenido':''}
                    paqueteLista.append(paquete)
                producto={'idProducto':fila[0], 'nombre':fila[1], 'precio':fila[2], 'descripcionCorta':fila[3], 'descripcionLarga':fila[4], 'foto':fila[5], 'categoria':fila[6].split(', '), 'fechaCreacion': fila[7], 'estatus':estatus, 'contenido':paqueteLista}
                productoLista.append(producto)
            else:
                producto={'idProducto':fila[0], 'nombre':fila[1], 'precio':fila[2], 'descripcionCorta':fila[3], 'descripcionLarga':fila[4], 'foto':fila[5], 'categoria':fila[6].split(', '), 'fechaCreacion': fila[7], 'estatus':estatus, 'contenido':''}
                productoLista.append(producto)
        return jsonify({'Producto': productoLista, 'exito': True})
    else:
        return jsonify({'message': "El producto no existe", 'exito': False})

def crearProducto(nom, pre, descC, descL, foto, cat, stat):
    hoy=datetime.now()
    db.session.execute(text(f"INSERT INTO producto (nombre, precio, descripcionCorta, descripcionLarga, foto, categoria, fechaCreacion, estatus) VALUES ('{nom}', '{pre}', '{descC}', '{descL}', '{foto}', '{cat}', '{hoy}', '{stat}')"))
    db.session.commit()
    return jsonify({'message': 'Producto agregado', 'exito':True})

def modificarProducto(id, nom, pre, descC, descL, foto, cat, stat):
    exist=verProducto(id).get_json()['Producto']
    if exist != []:
        db.session.execute(text(f"UPDATE producto SET nombre='{nom}', precio='{pre}', descripcionCorta='{descC}', descripcionLarga='{descL}', foto='{foto}', categoria='{cat}', estatus='{stat}' WHERE idProducto='{id}'"))
        db.session.commit()
        return jsonify({'message': 'Producto editado', 'exito':True})
    else:
        return jsonify({'message': 'Producto no encontrado', 'exito':False})

def borrarProducto(id):
    exist=verProducto(id)
    if exist != []:
        db.session.execute(text(f"DELETE FROM producto WHERE idProducto='{id}'"))
        db.session.commit()
        return jsonify({'message': 'Producto eliminado', 'exito':True})
    else:
        return jsonify({'message': 'Producto no encontrado', 'exito':False})
