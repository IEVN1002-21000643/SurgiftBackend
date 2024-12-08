from flask import jsonify
from models import db
from sqlalchemy import text

def ventasMes():
    VentasMes=db.session.execute(text(f"SELECT sum(total) as totalGrafica, DATE_FORMAT(fechaPedido, '%m-%Y') AS fechaGrafica FROM orden WHERE estatus>0 GROUP by fechaGrafica"))
    if VentasMes != []:
        datos=VentasMes.fetchall()
        x=[]
        y=[]
        for data in datos:
            y.append(data[0])
            x.append(data[1])
        grafica={'graficaX':x, 'graficaY':y}
        return jsonify({'grafica': grafica, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})
    
def usuariosMes():
    UsuarioMes=db.session.execute(text(f"SELECT count(*) as totalGrafica, DATE_FORMAT(fechaCreacion, '%m-%Y') AS fechaGrafica FROM usuario GROUP BY fechaGrafica"))
    if UsuarioMes != []:
        datos=UsuarioMes.fetchall()
        print(datos)
        x=[]
        y=[]
        for data in datos:
            y.append(data[0])
            x.append(data[1])
        grafica={'graficaX':x, 'graficaY':y}
        print(grafica)
        return jsonify({'grafica': grafica, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})

def productosMes():
    productosMes=db.session.execute(text(f"SELECT COUNT(OP.idOrden) as totalGrafica, DATE_FORMAT(O.fechaPedido, '%m-%Y') AS fechaGrafica FROM orden_producto as OP INNER JOIN orden as O ON (OP.idOrden = O.idOrden) GROUP BY fechaGrafica"))
    if productosMes != []:
        datos=productosMes.fetchall()
        x=[]
        y=[]
        for data in datos:
            y.append(data[0])
            x.append(data[1])
        grafica={'graficaX':x, 'graficaY':y}
        return jsonify({'grafica': grafica, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})
    
def estatusOrden():
    productosMes=db.session.execute(text(f"SELECT estatus, COUNT(estatus) FROM orden GROUP BY estatus"))
    if productosMes != []:
        datos=productosMes.fetchall()
        x=[]
        y=[]
        for data in datos:
            y.append(data[1])
            estatus=''
            if data[0]== "0":
                estatus='Cancelado'
            if data[0]== "1":
                estatus='Proceso'
            if data[0]== "2":
                estatus='En envio'
            if data[0]== "3":
                estatus='Entregado'
            x.append(estatus)
        grafica={'graficaX':x, 'graficaY':y}
        return jsonify({'grafica': grafica, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})



#-------Card Datos------#
def totalVenta():
    totalVenta=db.session.execute(text(f"SELECT sum(total) as total FROM orden WHERE estatus>0"))
    if totalVenta != []:
        data=totalVenta.fetchone()[0]
        return jsonify({'grafica': data, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})

def numUsuarios():
    numUsuario=db.session.execute(text(f"SELECT count(*) FROM usuario"))
    if numUsuario != []:
        data=numUsuario.fetchone()[0]
        return jsonify({'grafica': data, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})
    
def numOrdenes():
    numOrdenes=db.session.execute(text(f"SELECT count(*) FROM orden"))
    if numOrdenes != []:
        data=numOrdenes.fetchone()[0]
        return jsonify({'grafica': data, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})

def promedioCompraProducto():
    promProducto=db.session.execute(text(f"SELECT AVG(idProducto) FROM orden_producto"))
    if promProducto != []:
        data=promProducto.fetchone()[0]
        return jsonify({'grafica': data, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})
    
def promedioVenta():
    promVenta=db.session.execute(text(f"SELECT AVG(total) as total FROM orden"))
    if promVenta != []:
        data=promVenta.fetchone()[0]
        return jsonify({'grafica': data, 'exito':True})
    else:
        return jsonify({'message': "Por el momento no hay ordenes", 'exito':False})