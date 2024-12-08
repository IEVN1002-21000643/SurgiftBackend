from flask import jsonify
from models import db
from sqlalchemy import text
from datetime import datetime
from zoneinfo import ZoneInfo
from clases import clsProducto, clsUsuario

def verOrdenes():
    ordenes=db.session.execute(text(f"SELECT * FROM orden"))
    if ordenes != []:
        data=ordenes.fetchall()
        ordenesLista=[]
        for fila in data:
            estatus=''
            if fila[7]== "0":
                estatus='Cancelado'
            if fila[7]== "1":
                estatus='Proceso'
            if fila[7]== "2":
                estatus='En envio'
            if fila[7]== "3":
                estatus='Entregado'
            orden={"idOrden": fila[0], "nombre": fila[1], "direccion": fila[2], "telefono": fila[3], "correo": fila[4], "fechaPedido": fila[5], "total": fila[6], "estatus": estatus, "idUsuario":fila[9]}
            ordenesLista.append(orden)
        return jsonify({'Ordenes': ordenesLista, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})
    
def verMisOrdenes(idU):
    ordenes=db.session.execute(text(f"SELECT * FROM orden WHERE idUsuario='{idU}'"))
    if ordenes != []:
        data=ordenes.fetchall()
        ordenesLista=[]
        for row in data:
            estatus=''
            if row[7]== "0":
                estatus='Cancelado'
            if row[7]== "1":
                estatus='Proceso'
            if row[7]== "2":
                estatus='En envio'
            if row[7]== "3":
                estatus='Entregado'
            orden={"idOrden": row[0], "nombre": row[1], "direccion": row[2], "telefono": row[3], "correo": row[4], "fechaPedido": row[5], "total": row[6], "estatus": estatus}
            ordenesLista.append(orden)
        return jsonify({'Ordenes': ordenesLista, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})

def verOrden(idO):
    ordenes=db.session.execute(text(f"SELECT * FROM orden WHERE idOrden='{idO}'"))
    productos=db.session.execute(text(f"SELECT * FROM orden_producto WHERE idOrden='{idO}'"))
    if ordenes != []:
        data=ordenes.fetchall()
        datos=productos.fetchall()
        ordenesLista=[]
        productosLista=[]
        for fila in datos:
            producto={'producto': clsProducto.verProducto(fila[2]).get_json()['Producto'], 'cantidad': fila[3], 'precio':fila[4], 'decoracion':fila[5], 'destinatario':fila[6], 'fechaLlegada':fila[7]}
            productosLista.append(producto)
        for row in data:
            estatus=''
            if row[7]== "0":
                estatus='Cancelado'
            if row[7]== "1":
                estatus='Proceso'
            if row[7]== "2":
                estatus='En envio'
            if row[7]== "3":
                estatus='Entregado'
            orden={"idOrden": row[0], "nombre": row[1], "direccion": row[2], "telefono": row[3], "correo": row[4], "fechaPedido": row[5], "total": row[6], "estatus": estatus, "productos": productosLista}
            ordenesLista.append(orden)
        return jsonify({'Ordenes': ordenesLista, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})
    
def verMiOrden(idO, idU):
    ordenes=db.session.execute(text(f"SELECT * FROM orden WHERE idOrden='{idO}' and idUsuario='{idU}'"))
    productos=db.session.execute(text(f"SELECT * FROM orden_producto WHERE idOrden='{idO}'"))
    if ordenes != []:
        data=ordenes.fetchall()
        datos=productos.fetchall()
        ordenesLista=[]
        productosLista=[]
        for fila in datos:
            producto={'producto': clsProducto.verProducto(fila[2]).get_json()['Producto'], 'cantidad': fila[3], 'precio':fila[4], 'decoracion':fila[5], 'destinatario':fila[6], 'fechaLlegada':fila[7]}
            productosLista.append(producto)
        for row in data:
            estatus=''
            if row[7]== "0":
                estatus='Cancelado'
            if row[7]== "1":
                estatus='Proceso'
            if row[7]== "2":
                estatus='En envio'
            if row[7]== "3":
                estatus='Entregado'
            orden={"idOrden": row[0], "nombre": row[1], "direccion": row[2], "telefono": row[3], "correo": row[4], "fechaPedido": row[5], "total": row[6], "estatus": estatus, "productos": productosLista}
            ordenesLista.append(orden)
        return jsonify({'Ordenes': ordenesLista, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})
    
def crearOrden(nom, dir, tel, cor, fPed, tot, stat, idU, prod):
    if idU==None:
        db.session.execute(text(f"INSERT INTO orden (nombre, direccion, telefono, correo, fechaPedido, total, estatus) values ('{nom}', '{dir}', '{tel}', '{cor}', '{fPed}', '{tot}', '{stat}')"))
    else:
        db.session.execute(text(f"INSERT INTO orden (nombre, direccion, telefono, correo, fechaPedido, total, estatus, idUsuario) values ('{nom}', '{dir}', '{tel}', '{cor}', '{fPed}', '{tot}', '{stat}', '{idU}')"))
    db.session.commit()
    for item in prod:
        crearOrdenPaquete(item['idProducto'], item['cantidad'], item['precio'], item['decoracion'], item['destinatario'], item['fechaLlegada'])
    return jsonify({'message': "Tu orden se ha agregado", 'exito':True})
    
def crearOrdenPaquete(idP, cant, pre, dec, des, fLlegada):
    orden=db.session.execute(text(f"SELECT idOrden from orden ORDER BY idOrden DESC LIMIT 1"))
    idO=orden.fetchall()[0][0]
    if dec=='' and des=='' and fLlegada=='':
        db.session.execute(text(f"INSERT INTO orden_producto (idOrden, idProducto, cantidad, precio) values ('{idO}', '{idP}', '{cant}', '{pre}')"))
    if dec!='' and des=='' and fLlegada=='':
        db.session.execute(text(f"INSERT INTO orden_producto (idOrden, idProducto, cantidad, precio, decoracion) values ('{idO}', '{idP}', '{cant}', '{pre}', '{dec}')"))
    if dec!='' and des!='' and fLlegada!='':
        db.session.execute(text(f"INSERT INTO orden_producto (idOrden, idProducto, cantidad, precio, decoracion, destinatario, fechaLlegada) values ('{idO}', '{idP}', '{cant}', '{pre}', '{dec}', '{des}', '{fLlegada}')"))
    db.session.commit()
    
def editarOrden(idO, nom, dir, tel, cor, fPed, tot, stat, idU, product):
    orden=verOrden(idO).get_json()
    if orden!=[]:
        formato = "%a, %d %b %Y %H:%M:%S %Z"
        fecha=datetime.strptime(fPed, formato)
        if idU!=None:
            db.session.execute(text(f"UPDATE orden SET nombre='{nom}', direccion='{dir}', telefono='{tel}', correo='{cor}', fechaPedido='{fecha}', total='{tot}', estatus='{stat}', idUsuario='{idU}' WHERE idOrden='{idO}'"))
        else:
            db.session.execute(text(f"UPDATE orden SET nombre='{nom}', direccion='{dir}', telefono='{tel}', correo='{cor}', fechaPedido='{fecha}', total='{tot}', estatus='{stat}' WHERE idOrden='{idO}'"))
        db.session.commit()
        return jsonify({'message': "La orden ha sido editada", 'exito':True})
    else:
        return jsonify({'message': "La orden no existe", 'exito':False})
    
def editarOrdenProducto(idO, idP, cant, pre, dec, des, fLL):
    if dec=='' and des=='' and fLL=='':
        db.session.execute(text(f"UPDATE orden_producto SET idProducto='{idP}', cantidad='{cant}', precio='{pre}' WHERE idOrden='{idO}'"))
    if dec!='' and des=='' and fLL=='':
        db.session.execute(text(f"UPDATE orden_producto SET idProducto='{idP}', cantidad='{cant}', precio='{pre}' WHERE idOrden='{idO}' and decoracion='{dec}'"))
    if dec!='' and des!='' and fLL!='':
        db.session.execute(text(f"UPDATE orden_producto SET idProducto='{idP}', cantidad='{cant}', precio='{pre}', destinatario='{des}', fechaLLegada='{fLL}' WHERE idOrden='{idO}' and decoracion='{dec}'"))
    
def eliminarOrden(idO, idU):
    orden=verOrden(idO, idU)
    if orden!=[]:
        db.session.execute(text(f"DELETE from orden_producto WHERE idOrden='{idO}'"))
        db.session.commit()
        db.session.execute(text(f"DELETE from orden WHERE idUsuario='{idU}' and idOrden='{idO}'"))
        db.session.commit()
        return jsonify({'message': "La orden ha sido eliminada", 'exito':True})
    else:
        return jsonify({'message': "La orden no existe", 'exito':False})