from flask import Flask, request, jsonify
from config import DevelopmentConfig
from models import db
from clases import clsProducto, clsPaquete, clsRepartidor, clsUsuario, clsValoracion, clspseudoperfil, clsOrden, clsGraficas
from flask_cors import CORS, cross_origin
import os
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)


jwt=JWTManager(app)

#--------------------------PRODUCTO---------------------#
@app.route("/productos", methods=['GET'])
def verProductos():
    try:
        data=clsProducto.verProductos()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/producto/<id>", methods=['GET'])
def verProducto(id):
    try:
        data=clsProducto.verProducto(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
        
@app.route("/producto", methods=['POST'])
def registrarProducto():
    try:
        hoy=datetime.now()
        fecha_formateada = hoy.strftime("%Y-%m-%d-%H-%M-%S")
        foto=request.files['foto']
        os.makedirs('./static/img/productos', exist_ok=True)
        foto.filename=fecha_formateada+foto.filename
        foto_filename=os.path.join('static/img/productos/', foto.filename)
        data=clsProducto.crearProducto(request.form['nombre'], request.form['precio'], request.form['descripcionCorta'], request.form['descripcionLarga'], foto_filename, request.form['categoria'], request.form['estatus'])
        foto.save(foto_filename)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/producto/<id>", methods=['PUT'])
def editarProducto(id):
    try:
        foto_filename=''
        if 'foto' not in request.files:
            foto_filename=request.form['foto']
        else:
            hoy=datetime.now()
            fecha_formateada = hoy.strftime("%Y-%m-%d-%H-%M-%S")
            foto=request.files['foto']
            os.makedirs('./static/img/productos', exist_ok=True)
            foto.filename=fecha_formateada+foto.filename
            foto_filename=os.path.join('static/img/productos/', foto.filename)
        data=clsProducto.modificarProducto(id, request.form['nombre'], request.form['precio'], request.form['descripcionCorta'], request.form['descripcionLarga'], foto_filename, request.form['categoria'], request.form['estatus'])
        if 'foto' not in request.files:
            pass
        else:
            foto.save(foto_filename)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/producto/<id>", methods=['DELETE'])
def eliminarProducto(id):
    try:
        data=clsProducto.borrarProducto(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

#--------------------------PAQUETE---------------------#
@app.route("/paquete", methods=['POST'])
def registrarPaquete():
    try:
        data=clsPaquete.crearPaquete(request.json['nombre'], request.json['precio'], request.json['descripcionCorta'], request.json['descripcionLarga'], request.json['foto'], request.json['categoria'], request.json['estatus'], request.json['idProducto'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/paquete", methods=['PUT'])
def editarPaquete():
    try:
        data=clsPaquete.editarPaquete(request.json['idPaquete'], request.json['nombre'], request.json['precio'], request.json['descripcionCorta'], request.json['descripcionLarga'], request.json['foto'], request.json['categoria'], request.json['estatus'], request.json['idProducto'], request.json['idNewProducto'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/paquete", methods=['DELETE'])
def eliminarPaquete():
    try:
        data=clsPaquete.eliminarPaquete(request.json['idPaquete'], request.json['idProducto'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

#--------------------------REPARTIDOR---------------------#
@app.route("/repartidores", methods=['GET'])
def verRepartidores():
    try:
        data=clsRepartidor.verRepartidores()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/repartidor/<id>", methods=['GET'])
def verRepartidor(id):
    try:
        data=clsRepartidor.verRepartidor(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/repartidor", methods=['POST'])
def registrarRepartidor():
    try:
        hoy=datetime.now()
        fecha_formateada = hoy.strftime("%Y-%m-%d-%H-%M-%S")
        foto=request.files['foto']
        os.makedirs('./static/img/repartidores', exist_ok=True)
        foto.filename=fecha_formateada+foto.filename
        foto_filename=os.path.join('static/img/repartidores/', foto.filename)
        data=clsRepartidor.crearRepartidor(request.form['nombre'], request.form['sueldo'], request.form['telefono'], request.form['compañia'], foto_filename, request.form['estatus'])
        foto.save(foto_filename)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/repartidor/<id>", methods=['PUT'])
def editarRepartidor(id):
    try:
        if 'foto' not in request.files:
            foto_filename=request.form['foto']
        else:
            hoy=datetime.now()
            fecha_formateada = hoy.strftime("%Y-%m-%d-%H-%M-%S")
            foto=request.files['foto']
            os.makedirs('./static/img/repartidores', exist_ok=True)
            foto.filename=fecha_formateada+foto.filename
            foto_filename=os.path.join('static/img/repartidores/', foto.filename)
        data=clsRepartidor.modificarRepartidor(id, request.form['nombre'], request.form['sueldo'], request.form['telefono'], request.form['compañia'], foto_filename, request.form['estatus'])
        if 'foto' not in request.files:
            pass
        else:
            foto.save(foto_filename)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/repartidor/<id>", methods=['DELETE'])
def eliminarRepartidor(id):
    try:
        data=clsRepartidor.eliminarRepartidor(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
#--------------------------USUARIO------------------------#
@app.route("/usuarios", methods=['GET'])
def verUsuarios():
    try:
        data=clsUsuario.verUsuarios()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/usuario/<id>", methods=['GET'])
def verUsuario(id):
    try:
        data=clsUsuario.verUsuario(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/usuario", methods=['POST'])
def registrarUsuario():
    try:
        hoy=datetime.now()
        fecha_formateada = hoy.strftime("%Y-%m-%d-%H-%M-%S")
        foto=request.files['foto']
        os.makedirs('./static/img/usuarios', exist_ok=True)
        foto.filename=fecha_formateada+foto.filename
        foto_filename=os.path.join('static/img/usuarios/', foto.filename)
        data=clsUsuario.crearUsuario(request.form['nombre'], request.form['correo'], request.form['password'], request.form['direccion'], foto_filename, request.form['estatus'])
        foto.save(foto_filename)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/usuario/<id>", methods=['PUT'])
def editarUsuario(id):
    try:
        if 'foto' not in request.files:
            foto_filename=request.form['foto']
        else:
            hoy=datetime.now()
            fecha_formateada = hoy.strftime("%Y-%m-%d-%H-%M-%S")
            foto=request.files['foto']
            os.makedirs('./static/img/usuarios', exist_ok=True)
            foto.filename=fecha_formateada+foto.filename
            foto_filename=os.path.join('static/img/usuarios/', foto.filename)
        data=clsUsuario.editarUsuario(id, request.form['nombre'], request.form['direccion'], foto_filename, request.form['estatus'])
        if 'foto' not in request.files:
            pass
        else:
            foto.save(foto_filename)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/usuario/<id>", methods=['DELETE'])
def eliminarUsuario(id):
    try:
        data=clsUsuario.eliminarUsuario(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/login", methods=['POST'])
def login():
    try:
        data=clsUsuario.login(request.json['correo'], request.json['password'])
        access_token= create_access_token(identity={'correo': data[0], 'estatus': data[1], 'idUsuario': data[2]})
        return jsonify({'token': access_token})
    except Exception as ex:
        return jsonify({'message': "El Correo o la Contraseña estan incorrectos", 'exito':False})
    
@app.route("/loginAdmin", methods=['POST'])
def loginAdmin():
    try:
        data=clsUsuario.loginAdmin(request.json['correo'], request.json['password'])
        access_token= create_access_token(identity={'correo': data[0], 'estatus': data[1], 'idUsuario': data[2]})
        return jsonify({'token': access_token})
    except Exception as ex:
        return jsonify({'message': "El Correo o la Contraseña estan incorrectos", 'exito':False})
    
@app.route("/registro", methods=['POST'])
def registro():
    try:
        hoy=datetime.now()
        fecha_formateada = hoy.strftime("%Y-%m-%d-%H-%M-%S")
        foto=request.files['foto']
        os.makedirs('./static/img/usuarios', exist_ok=True)
        foto.filename=fecha_formateada+foto.filename
        foto_filename=os.path.join('static/img/usuarios/', foto.filename)
        data=clsUsuario.crearUsuario(request.form['nombre'], request.form['correo'], request.form['password'], request.form['direccion'], foto_filename, 1)
        foto.save(foto_filename)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

#--------------------------VALORACION------------------------#
@app.route("/valoracion", methods=['GET'])
def verValoraciones():
    try:
        data=clsValoracion.verValoraciones(request.json['idProducto'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/valoracion", methods=['POST'])
def registrarValoracion():
    try:
        data=clsValoracion.crearValoracion(request.json['puntuacion'], request.json['comentario'], request.json['idUsuario'], request.json['idProducto'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/valoracion", methods=['PUT'])
def editarValoracion():
    try:
        data=clsValoracion.editarValoracion(request.json['idValoracion'], request.json['puntuacion'], request.json['comentario'], request.json['idUsuario'], request.json['idProducto'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/valoracion", methods=['DELETE'])
def eliminarValoracion():
    try:
        data=clsValoracion.eliminarValoracion(request.json['idValoracion'], request.json['idUsuario'], request.json['idProducto'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

#--------------------------PSEUDOPERFIL------------------------#
@app.route("/pseudoperfiles/<id>", methods=['GET'])
def verPseudoperfiles(id):
    try:
        data=clspseudoperfil.verPseudoperfiles(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/pseudoperfil/<idP>/<idU>", methods=['GET'])
def verPseudoperfil(idP, idU):
    try:
        data=clspseudoperfil.verPseudoperfil(idP, idU)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/pseudoperfil", methods=['POST'])
def registrarPseudoperfil():
    try:
        idUsuarioR=''
        if request.json['usuarioReal']!='':
            idUsuarioR=clsUsuario.encontrarId(request.json['usuarioReal'])
        data=clspseudoperfil.crearPseudoperfil(request.json['idUsuario'], request.json['nombre'], request.json['caracteristicas'], idUsuarioR)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/pseudoperfil", methods=['PUT'])
def editarPseudoperfil():
    try:
        idUsuarioR=''
        if request.json['usuarioReal']!='':
            idUsuarioR=clsUsuario.encontrarId(request.json['usuarioReal'])
        data=clspseudoperfil.editarPseudoperfil(request.json['idUsuario'], request.json['nombre'], request.json['caracteristicas'], request.json['idPseudoperfil'], idUsuarioR)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/pseudoperfil/<idP>/<idU>", methods=['DELETE'])
def eliminarPseudoperfil(idP, idU):
    try:
        data=clspseudoperfil.eliminarPseudoperfil( idP, idU)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

#--------------------------ORDENES---------------------#
@app.route("/ordenes", methods=['GET'])
def verOrdenes():
    try:
        data=clsOrden.verOrdenes()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/misOrdenes/<id>", methods=['GET'])
def verMisOrdenes(id):
    try:
        data=clsOrden.verMisOrdenes(id)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/orden/<idO>", methods=['GET'])    
def verOrden(idO):
    try:
        data=clsOrden.verOrden(idO)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/miOrden/<idO>/<idU>", methods=['GET'])    
def verMiOrden(idO, idU):
    try:
        data=clsOrden.verMiOrden(idO, idU)
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/orden", methods=['POST'])    
def registrarOrden():
    try:
        hoy=datetime.now()
        usuario=None
        estatus=1
        if 'idUsuario' in request.json:
            usuario=request.json['idUsuario']
        if 'estatus' in request.json:
            estatus=request.json['estatus']
        data=clsOrden.crearOrden(request.json['nombre'], request.json['direccion'], request.json['telefono'], request.json['correo'], hoy, 
                                 request.json['total'], estatus, usuario, request.json['productos'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/orden/<idO>", methods=['PUT'])
def editarOrden(idO):
    try:
        usuario=None
        if 'idUsuario' in request.json:
            usuario=request.json['idUsuario']
        data=clsOrden.editarOrden(idO, request.json['nombre'], request.json['direccion'], request.json['telefono'], request.json['correo'],
                                  request.json['fechaPedido'], request.json['total'], request.json['estatus'], usuario, request.json['productos'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/orden", methods=['DELETE'])    
def eliminarOrden():
    try:
        data=clsOrden.eliminarOrden(request.json['idOrden'], request.json['idUsuario'])
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/chatbot", methods=['POST'])
def chatbotResponse():
    try:
        return jsonify({'mensaje': 'respuesta generica xd', 'tipo': 'bot'})
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

#--------------------------GRÁFICAS---------------------#
@app.route("/ventas_mes", methods=['GET'])
def getVentasMes():
    try:
        data=clsGraficas.ventasMes()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/usuarios_mes", methods=['GET'])
def getUsuariosMes():
    try:
        data=clsGraficas.usuariosMes()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/productos_mes", methods=['GET'])
def getProductosMes():
    try:
        data=clsGraficas.productosMes()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

@app.route("/estatus_venta", methods=['GET'])
def getEstatusOrden():
    try:
        data=clsGraficas.estatusOrden()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
#--------------------------CARDS---------------------#
@app.route("/total_venta", methods=['GET'])
def getTotalVenta():
    try:
        data=clsGraficas.totalVenta()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/num_usuario", methods=['GET'])
def getNumUsuarios():
    try:
        data=clsGraficas.numUsuarios()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/num_ordenes", methods=['GET'])
def getNumOrdenes():
    try:
        data=clsGraficas.numOrdenes()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})
    
@app.route("/promedio_producto", methods=['GET'])
def getPromProducto():
    try:
        data=clsGraficas.promedioCompraProducto()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False}) 

@app.route("/promedio_venta", methods=['GET'])
def getPromVenta():
    try:
        data=clsGraficas.promedioVenta()
        return data
    except Exception as ex:
        return jsonify({'message': "Error al conectar a la base de datos {}".format(ex), 'exito':False})

#--------------------------DEFAULT---------------------#
def pagina_no_encontrada(error):
    return '<h1> La página que estas buscando no existe </h1>', 400

if __name__=="__main__":
    db.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)

    with app.app_context():
        db.create_all()

    app.run(debug=True)